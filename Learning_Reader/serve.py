"""Optional live reader: python serve.py, then open http://127.0.0.1:8765."""
from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import urllib.parse

from build_reader import APP, DEFAULT_SOURCE, build, collect_library


class ReaderHandler(SimpleHTTPRequestHandler):
    source = DEFAULT_SOURCE.resolve()

    def end_headers(self):
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_GET(self):
        request = urllib.parse.urlsplit(self.path)
        if request.path == "/api/library":
            body = json.dumps(collect_library(self.source), ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if request.path.startswith("/materials/"):
            rel = urllib.parse.unquote(request.path[len("/materials/"):])
            target = (self.source / rel).resolve()
            if not target.is_relative_to(self.source) or not target.is_file() or any(part in {".git", "build", "__pycache__"} for part in target.relative_to(self.source).parts) or target.name.startswith("~$"):
                self.send_error(404)
                return
            data = target.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", self.guess_type(str(target)))
            self.send_header("Content-Disposition", f"attachment; filename*=UTF-8''{urllib.parse.quote(target.name)}")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        super().do_GET()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    args = parser.parse_args()
    build(args.source)
    ReaderHandler.source = args.source.resolve()
    handler = partial(ReaderHandler, directory=str(APP))
    with ThreadingHTTPServer(("127.0.0.1", args.port), handler) as server:
        print(f"Reader: http://127.0.0.1:{args.port}", flush=True)
        print("Local read-only server. Ctrl+C to stop.", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
