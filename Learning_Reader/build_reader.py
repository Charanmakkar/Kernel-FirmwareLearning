"""Build an offline HTML reader without modifying any learning-program file.

Uses Python's standard library only. Libraries used in the browser are vendored.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import re
import zipfile
import xml.etree.ElementTree as ET

APP = Path(__file__).resolve().parent
DEFAULT_SOURCE = APP.parent / "Embedded_Linux_Kernel_Firmware_Learning"
TEXT_EXTENSIONS = {".md", ".txt", ".csv", ".json", ".c", ".h", ".py", ".sh", ".ps1", ".yaml", ".yml", ".conf", ".cfg", ".ini", ".cmake", ".dts", ".dtsi", ".bb", ".bbappend", ".in"}
SKIP_DIRS = {"build", ".git", "__pycache__", ".venv", "node_modules"}
SECTIONS = [
    ("00_Start_Here", "Start here", "compass"),
    ("01_Learning_Roadmap", "Learning roadmap", "route"),
    ("02_Interview_Questions_and_Answers", "Interview preparation", "chat"),
    ("03_JD_JR_Skills_and_Learning_Content", "Lessons & skills", "book"),
    ("04_Skill_Assessments", "Skill assessments", "check"),
    ("05_Interview_Strategy", "Interview strategy", "target"),
    ("06_AI_Integration", "AI integration", "spark"),
    ("07_Projects", "Project workshop", "code"),
    ("08_Portfolio_and_Job_Readiness", "Portfolio & readiness", "case"),
    ("09_References_and_Resources", "References & resources", "link"),
    ("10_Progress_Tracking", "Progress & evidence", "chart"),
    ("Word_Edition", "Word editions", "file"),
    ("_root", "Program overview", "layers"),
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_answer(path: str) -> bool:
    lower = path.lower()
    return any(token in lower for token in ("/answer_keys/", "/solutions/", "reference_solutions", "assessment_answer_keys"))


def word_text(path: Path) -> str:
    """Extract every body paragraph/table in order from an existing Word edition."""
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    with zipfile.ZipFile(path) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
    result = []
    body = root.find("w:body", ns)
    if body is None:
        return ""
    for child in body:
        if child.tag == f"{{{ns['w']}}}p":
            text = "".join(t.text or "" for t in child.findall(".//w:t", ns))
            if not text.strip():
                continue
            style = child.find("w:pPr/w:pStyle", ns)
            style_name = style.get(f"{{{ns['w']}}}val", "") if style is not None else ""
            if style_name.startswith("Heading") and style_name[-1:].isdigit():
                text = "#" * min(int(style_name[-1]), 4) + " " + text
            result.append(text)
        elif child.tag == f"{{{ns['w']}}}tbl":
            rows = []
            for row in child.findall("w:tr", ns):
                rows.append([" ".join("".join(t.text or "" for t in p.findall(".//w:t", ns)) for p in cell.findall("w:p", ns)) for cell in row.findall("w:tc", ns)])
            if rows:
                result.append("\n".join(" | ".join(row) for row in rows))
    return "\n\n".join(result)


def title_for(path: str, text: str) -> str:
    first_heading = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    if first_heading and path.endswith(".md"):
        return first_heading.group(1).replace("**", "")
    known = {
        "roadmap_64_weeks.csv": "64-week learning roadmap",
        "project_plan.csv": "15-project plan",
        "reference_skills_matrix.csv": "Reference skills matrix",
        "skills_tracker.csv": "Your skills tracker",
        "revision_30_days.csv": "30-day interview revision",
        "question_index.csv": "Interview question index",
        "bank.json": "Interview bank · complete dataset",
        "manifest.csv": "Delivery manifest",
        "sources.csv": "Primary reference register",
        "host.json": "B01 · normal build evidence",
        "sanitize.json": "B01 · sanitizer evidence",
        "package_audit.json": "Package validation audit",
        "file_inventory.csv": "Package file inventory",
    }
    return known.get(Path(path).name, Path(path).stem.replace("_", " "))


def collect_library(source: Path = DEFAULT_SOURCE) -> dict:
    source = source.resolve()
    if not source.is_dir():
        raise FileNotFoundError(f"Learning folder not found: {source}")
    files = []
    skipped = []
    for path in sorted(source.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(source).as_posix()
        if any(part in SKIP_DIRS for part in path.relative_to(source).parts) or path.name.startswith(("~$", ".")):
            skipped.append(rel)
            continue
        suffix = path.suffix.lower()
        content = ""
        kind = "attachment"
        error = None
        if suffix == ".docx":
            kind = "word"
            try:
                content = word_text(path)
            except (zipfile.BadZipFile, KeyError, ET.ParseError) as exc:
                error = f"Could not extract document text: {exc}"
        elif suffix in TEXT_EXTENSIONS or path.name in {"Makefile", "Kbuild", "Kconfig", "LICENSE", "CMakeLists.txt"}:
            try:
                content = path.read_text(encoding="utf-8-sig")
                kind = {".md": "markdown", ".csv": "csv", ".json": "json"}.get(suffix, "code")
            except UnicodeDecodeError:
                error = "This file is not UTF-8 text; open the original attachment."
        section = rel.split("/")[0] if "/" in rel else "_root"
        item = {
            "path": rel, "title": title_for(rel, content), "kind": kind,
            "section": section, "text": content, "bytes": path.stat().st_size,
            "sha256": digest(path), "answer": is_answer(rel),
            "words": len(content.split()), "error": error,
        }
        if kind == "csv":
            rows = list(csv.reader(io.StringIO(content)))
            item["columns"] = rows[0] if rows else []
            item["rows"] = rows[1:]
        elif kind == "json":
            try:
                item["value"] = json.loads(content)
            except json.JSONDecodeError as exc:
                item["error"] = str(exc)
        files.append(item)
    bank = next((f.get("value", []) for f in files if f["path"] == "02_Interview_Questions_and_Answers/bank.json"), [])
    projects = next((f for f in files if f["path"] == "01_Learning_Roadmap/project_plan.csv"), None)
    project_records = [dict(zip(projects["columns"], row)) for row in projects["rows"]] if projects else []
    manifest = next((f for f in files if f["path"] == "manifest.csv"), None)
    deliveries = [dict(zip(manifest["columns"], row)) for row in manifest["rows"]] if manifest else []
    complete_lessons = sum(row.get("Kind") == "lesson" and row.get("Completion status") == "complete lesson" for row in deliveries)
    implemented_projects = sum(row.get("Kind") == "project" and row.get("Completion status") == "complete implementation" for row in deliveries)
    return {
        "name": "Embedded Systems · Fieldnotes", "sourceFolder": source.name,
        "generatedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sections": [{"id": id_, "label": label, "icon": icon} for id_, label, icon in SECTIONS],
        "files": files, "questions": bank, "projects": project_records,
        "skipped": skipped,
        "stats": {"files": len(files), "questions": len(bank), "projects": len(project_records),
                  "completeLessons": complete_lessons, "implementedProjects": implemented_projects,
                  "weeks": len(next((f["rows"] for f in files if f["path"].endswith("roadmap_64_weeks.csv")), []))},
    }


def embedded_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")


def build(source: Path = DEFAULT_SOURCE) -> dict:
    library = collect_library(source)
    shell = (APP / "src/shell.html").read_text(encoding="utf-8")
    replacements = {
        "/* READER_STYLES */": (APP / "src/reader.css").read_text(encoding="utf-8"),
        "/* VENDORED_MARKED */": (APP / "vendor/marked.umd.js").read_text(encoding="utf-8"),
        "/* VENDORED_PURIFY */": (APP / "vendor/purify.min.js").read_text(encoding="utf-8"),
        "/* LIBRARY_JSON */": embedded_json(library),
        "/* LICENSES_JSON */": embedded_json({
            "Marked 16.4.2": (APP / "vendor/MARKED_LICENSE.txt").read_text(encoding="utf-8"),
            "DOMPurify 3.3.0": (APP / "vendor/DOMPURIFY_LICENSE.txt").read_text(encoding="utf-8"),
        }),
        "/* READER_SCRIPT */": (APP / "src/reader.js").read_text(encoding="utf-8"),
    }
    for token, content in replacements.items():
        if token not in shell:
            raise ValueError(f"Missing template token: {token}")
        shell = shell.replace(token, content)
    target = APP / "index.html"
    target.write_text(shell, encoding="utf-8", newline="\n")
    report = {"builtAt": library["generatedAt"], "sourceFolder": library["sourceFolder"],
              "included": library["stats"], "skipped": library["skipped"],
              "sourceHashes": {f["path"]: f["sha256"] for f in library["files"]},
              "htmlBytes": target.stat().st_size, "htmlSha256": digest(target),
              "originalFilesModified": False}
    (APP / "build_report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    args = parser.parse_args()
    report = build(args.source)
    print(f"Reader ready: {APP / 'index.html'}")
    print(json.dumps(report["included"]))
    print("Original learning files were read only.")
