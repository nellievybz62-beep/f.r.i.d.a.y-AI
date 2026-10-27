#!/usr/bin/env python3
"""Minimal authenticated, fixed-query F.R.I.D.A.Y. ↔ Zetaris bridge."""
import hmac
import json
import os
import re
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
ENV_FILE = ROOT / ".env"
HOST = "127.0.0.1"
PORT = 8765
MAX_BODY = 1024

def env_value(name):
    value = os.environ.get(name)
    if value:
        return value
    if ENV_FILE.is_file():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            if line.startswith(name + "="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""

def post_json(url, payload, headers=None):
    request_headers = {"Content-Type": "application/json"}
    if headers:
        request_headers.update(headers)
    req = Request(
        url, data=json.dumps(payload).encode("utf-8"),
        headers=request_headers, method="POST"
    )
    with urlopen(req, timeout=20) as response:
        return response.read().decode("utf-8")

def run_test_query():
    email = env_value("ZETARIS_ADMIN_EMAIL")
    password = env_value("ZETARIS_ADMIN_PASSWORD")
    base_url = env_value("ZETARIS_UI_URL") or "http://127.0.0.1:3000"
    if not email or not password:
        raise RuntimeError("Zetaris credentials are not configured")

    login = post_json(
        base_url + "/api/auth/login",
        {"username": email, "password": password}
    )
    token_match = re.search(
        r"[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}",
        login,
    )
    org_match = re.search(r'"orgId"\s*:\s*(\d+)', login)
    if not token_match or not org_match:
        raise RuntimeError("Unexpected Zetaris login response")
    token = token_match.group(0)
    org_id = org_match.group(1)

    result = json.loads(post_json(
        base_url + "/api/proxy/query/sql/start",
        {"select": "select 7 as seven", "pageLimit": 5},
        {
            "Authorization": "Bearer " + token,
            "X-Org-ID": str(org_id),
            "X-Request-ID": str(uuid.uuid4()),
        }
    ))
    # Never return authentication/session tokens to the caller.
    records = result.get("records", [])
    if not records or str(records[0].get("seven")) != "7":
        raise RuntimeError("SQL test did not return the expected result")
    return {"ok": True, "records": [{"seven": "7"}]}

class Handler(BaseHTTPRequestHandler):
    def respond(self, status, data):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path != "/health":
            self.respond(404, {"ok": False, "error": "Not found"})
            return
        self.respond(200, {"ok": True, "service": "friday-zetaris-bridge"})

    def do_POST(self):
        if self.path != "/query-test":
            self.respond(404, {"ok": False, "error": "Not found"})
            return
        expected = env_value("FRIDAY_ZETARIS_BRIDGE_KEY")
        supplied = self.headers.get("X-FRIDAY-KEY", "")
        if not expected or not hmac.compare_digest(supplied, expected):
            self.respond(401, {"ok": False, "error": "Unauthorized"})
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if size < 0 or size > MAX_BODY:
                self.respond(413, {"ok": False, "error": "Request too large"})
                return
            if size:
                self.rfile.read(size)  # No SQL or other commands accepted.
            self.respond(200, run_test_query())
        except (HTTPError, URLError, TimeoutError, OSError, ValueError, RuntimeError) as exc:
            print("Bridge request failed:", type(exc).__name__)
            self.respond(502, {"ok": False, "error": "Zetaris query failed"})

    def log_message(self, fmt, *args):
        # Avoid logging request headers or credentials.
        print("Bridge:", args[1] if len(args) > 1 else "request")

if __name__ == "__main__":
    if not env_value("FRIDAY_ZETARIS_BRIDGE_KEY"):
        raise SystemExit("Missing FRIDAY_ZETARIS_BRIDGE_KEY in environment or .env")
    print(f"F.R.I.D.A.Y.–Zetaris bridge listening on {HOST}:{PORT}")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
