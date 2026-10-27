# Fieldnotes — your embedded systems reading room

Open **[index.html](index.html)** in Edge, Chrome, or Firefox. Double-clicking works: no server, installation, account, or internet connection is needed to read the built application.

The reader brings all 88 distributable learning files into one application: Markdown chapters, CSV tables, source code, JSON evidence, and extracted text from the four Word editions. The sidebar follows the learning program. **Continuous reading** combines the collection or a selected section into one page. Code, tables, datasets, and compiled Word copies expand when needed.

- Search titles, full learning text, and question IDs with **Ctrl+K** (or Cmd+K).
- Filter the 200 interview questions by topic, type, and role; reveal each answer after attempting it.
- Search CSV rows, switch between a compact view and all columns, and select a row for complete details.
- Use the table of contents, copy code blocks, change text size or theme, and enter focus mode.
- Save bookmarks and reading marks in this browser. These preferences do not change course files or claim skill mastery.
- Assessment answer keys require a deliberate reveal. This is a study aid, not a security boundary.
- Download an original file from its reading page. Keep this folder beside `Embedded_Linux_Kernel_Firmware_Learning/` for original-file downloads to work when opening from disk.

## Refresh after changing your learning material

The HTML contains a snapshot of the original folder. After adding or editing course files, double-click **refresh.cmd**, or run from the repository directory:

```powershell
python Learning_Reader/build_reader.py
```

This reads the source folder and updates only `Learning_Reader/index.html` and `Learning_Reader/build_report.json`. It does not run course-generation scripts or modify the learning package, Word editions, ZIP, checksums, source, assessments, or evidence.

For refresh directly inside the application, double-click **start_live.cmd**, or run:

```powershell
python Learning_Reader/serve.py
```

Open **http://127.0.0.1:8765**. The sidebar's **Refresh content** button rereads the source folder. Stop the server with Ctrl+C. Python 3.9+ is required for rebuilding/live mode; the ready-to-open HTML needs only a modern browser. Neither command needs administrator privileges. If the port is busy, use `python Learning_Reader/serve.py --port 8766` and open the matching URL.

The built HTML can be copied by itself for offline reading. Downloads of original documents need the adjacent course folder or the live server. Browser preferences belong to the browser/origin; file mode and live mode can have separate saved preferences. If browser storage is disabled, reading still works and saving is limited to the current visit.

## Scope and validation

The collection is still the original staged program: one complete lesson and one implemented project, with the remaining delivery status preserved. The reader adds presentation and navigation; it does not fill in pending learning content. Binary build outputs and temporary Word lock files are excluded. Word text is extracted for reading; use the original DOCX for its exact formatting.

All implementation files are separate in this directory. `src/` contains the editable HTML shell, CSS, and JavaScript; `build_reader.py` collects and embeds the files; `serve.py` provides optional read-only live access. `build_report.json` records source hashes and inclusion counts. `original_files.sha256.json` records the pre-change files for the preservation check.

Executed validation is recorded in `evidence/browser_qa.json` and `evidence/validation.json`, with desktop/mobile screenshots. The checks cover offline file opening, source coverage, Markdown/code rendering, CSV filtering/details, interview filters/reveal, answer-key gating, saved reading state, continuous reading, Word extraction, live refresh, server path boundaries, and browser errors. No old files were changed.

To rerun the standard-library checks:

```powershell
python -m unittest discover -s Learning_Reader/tests -p test_reader.py -v
```

`tests/browser_qa.py` is developer-only QA. It uses an isolated headless Edge profile and Playwright 1.58.0 from `.qa/python`; none of that is required to use or rebuild the reader. The connected in-app browser was unavailable, so a separate headless browser was used for the recorded checks.

## Third-party notices

The application bundles [Marked 16.4.2](https://github.com/markedjs/marked/releases/tag/v16.4.2) to render Markdown and [DOMPurify 3.3.0](https://github.com/cure53/DOMPurify/releases/tag/3.3.0) to sanitize the rendered HTML. They are bundled locally and make no runtime CDN requests. Their license texts are in `vendor/MARKED_LICENSE.txt` and `vendor/DOMPURIFY_LICENSE.txt`, and their download URLs/hashes are recorded in `vendor/sources.json`. License notices are also embedded in the standalone HTML. No source document is executed as application code.
