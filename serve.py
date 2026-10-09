"""Local preview server for the site, plus a save endpoint for the edit panel.

Run:  python3 serve.py   then open http://localhost:4321
Edits made in the page's ✎ panel are written to content.json
(the previous version is kept as content.backup.json).
"""
import json
import os
import shutil
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = 4321
CONTENT = os.path.join(ROOT, "content.json")
ALLOWED_ORIGINS = {f"http://localhost:{PORT}", f"http://127.0.0.1:{PORT}"}


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_POST(self):
        if self.path != "/api/save":
            return self.send_error(404)
        origin = self.headers.get("Origin")
        if origin and origin not in ALLOWED_ORIGINS:
            return self.send_error(403, "bad origin")
        length = int(self.headers.get("Content-Length", 0))
        if not 0 < length <= 2_000_000:
            return self.send_error(413)
        try:
            data = json.loads(self.rfile.read(length))
        except ValueError:
            return self.send_error(400, "invalid JSON")
        if not isinstance(data, dict) or "projects" not in data:
            return self.send_error(400, "unexpected content shape")

        if os.path.exists(CONTENT):
            shutil.copyfile(CONTENT, os.path.join(ROOT, "content.backup.json"))
        tmp = CONTENT + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        os.replace(tmp, CONTENT)
        self.send_response(204)
        self.end_headers()


if __name__ == "__main__":
    print(f"serving {ROOT} on http://localhost:{PORT}")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
