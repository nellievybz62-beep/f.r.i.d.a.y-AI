#!/usr/bin/env python3
"""F.R.I.D.A.Y. local PC backend prototype.

Connects HTTP clients to the tested Meterless H-MEM CLI.
Binds to localhost only. It does not replace the original Android app.
"""

import json
import os
import shutil
import subprocess
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parent
METERLESS_DIR = Path(
    os.environ.get("FRIDAY_METERLESS_DIR", str(ROOT / "meterless-hmem"))
).expanduser()
HOST = "127.0.0.1"
PORT = 8000
MAX_BODY = 8192


def meterless_command(*args):
    npx = shutil.which("npx")
    if not npx:
        raise RuntimeError(
            "npx not found. Load Node.js 22 with nvm before starting app.py."
        )
    if not (METERLESS_DIR / "notebook.ts").is_file():
        raise RuntimeError(
            "Meterless notebook.ts not found. Set FRIDAY_METERLESS_DIR "
            "to your prepared Meterless project directory."
        )
    return subprocess.run(
        [npx, "tsx", "notebook.ts", *args],
        cwd=METERLESS_DIR,
        capture_output=True,
        text=True,
        timeout=90,
        check=False,
    )


def bridge_health():
    try:
        with urlopen("http://127.0.0.1:8765/health", timeout=2) as r:
            data = json.loads(r.read().decode("utf-8"))
            return bool(data.get("ok"))
    except (OSError, URLError, ValueError, TimeoutError):
        return False


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print("[F.R.I.D.A.Y. API]", fmt % args)

    def send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "http://127.0.0.1:8780")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_json(204, {})

    def do_GET(self):
        if self.path != "/api/health":
            self.send_json(404, {"ok": False, "error": "Not found"})
            return

        self.send_json(200, {
            "ok": True,
            "service": "friday-pc-api",
            "meterless_notebook_present": (METERLESS_DIR / "notebook.ts").is_file(),
            "hmem_engine_prepared": (METERLESS_DIR / "vendor" / "hmem").is_dir(),
            "nvidia_key_configured": bool(os.environ.get("NVIDIA_API_KEY")),
            "zetaris_bridge_reachable": bridge_health(),
            "mode": "local-prototype",
        })

    def do_POST(self):
        if self.path not in ("/api/chat", "/api/memory/remember"):
            self.send_json(404, {"ok": False, "error": "Not found"})
            return

        try:
            size = int(self.headers.get("Content-Length", "0"))
            if size <= 0 or size > MAX_BODY:
                self.send_json(400, {"ok": False, "error": "Invalid body size"})
                return
            data = json.loads(self.rfile.read(size).decode("utf-8"))
            if not isinstance(data, dict):
                raise ValueError("JSON body must be an object")

            if self.path == "/api/chat":
                message = data.get("message", "")
                if not isinstance(message, str) or not message.strip():
                    self.send_json(400, {"ok": False, "error": "Message is required"})
                    return
                if len(message) > 2000:
                    self.send_json(400, {"ok": False, "error": "Message too long"})
                    return
                result = meterless_command("ask", message.strip())
            else:
                note = data.get("text", "")
                if not isinstance(note, str) or not note.strip() or len(note) > 2000:
                    self.send_json(400, {"ok": False, "error": "Valid text is required"})
                    return
                result = meterless_command("remember", note.strip())

            output = (result.stdout or "").strip()
            if result.stderr:
                # stderr is diagnostic output, but never echo the environment
                # or credentials in an API response.
                print("[Meterless stderr]", result.stderr[-1500:])

            if result.returncode != 0:
                self.send_json(502, {
                    "ok": False,
                    "error": "Meterless command failed",
                    "detail": output[-3000:],
                    "exit_code": result.returncode,
                })
                return

            self.send_json(200, {
                "ok": True,
                "action": "chat" if self.path == "/api/chat" else "remember",
                "output": output,
                "engine": "Meterless H-MEM",
            })

        except subprocess.TimeoutExpired:
            self.send_json(504, {"ok": False, "error": "Meterless command timed out"})
        except (ValueError, UnicodeDecodeError):
            self.send_json(400, {"ok": False, "error": "Invalid JSON request"})
        except Exception as exc:
            print("[F.R.I.D.A.Y. API] Error:", type(exc).__name__)
            self.send_json(500, {
                "ok": False,
                "error": "Backend error",
                "detail": str(exc)[:300],
            })


if __name__ == "__main__":
    print("F.R.I.D.A.Y. local API: http://127.0.0.1:8000")
    print("Health: http://127.0.0.1:8000/api/health")
    print("Meterless directory:", METERLESS_DIR)
    print("Local prototype only; press Ctrl+C to stop.")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
