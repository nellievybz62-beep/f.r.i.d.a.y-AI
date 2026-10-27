#!/usr/bin/env python3
"""Read-only F.R.I.D.A.Y. ↔ Zetaris connectivity smoke test."""
import json
import os
import re
import sys
import uuid
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE_URL = os.environ.get("ZETARIS_UI_URL", "http://127.0.0.1:3000")
ENV_FILE = Path(os.environ.get("ZETARIS_ENV_FILE", ".env"))


def read_env_value(name):
    if not ENV_FILE.is_file():
        return ""
    prefix = name + "="
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        if line.startswith(prefix):
            return line[len(prefix):].strip().strip('"').strip("'")
    return ""


def post_json(path, payload, headers=None):
    request_headers = {"Content-Type": "application/json"}
    if headers:
        request_headers.update(headers)
    request = Request(
        BASE_URL + path,
        data=json.dumps(payload).encode("utf-8"),
        headers=request_headers,
        method="POST",
    )
    with urlopen(request, timeout=20) as response:
        return response.read().decode("utf-8")


def main():
    email = os.environ.get("ZETARIS_ADMIN_EMAIL") or read_env_value(
        "ZETARIS_ADMIN_EMAIL"
    ) or "admin@zetaris.com"
    password = os.environ.get("ZETARIS_ADMIN_PASSWORD") or read_env_value(
        "ZETARIS_ADMIN_PASSWORD"
    )

    if not password:
        print("FAIL: administrator password not found; no credentials were displayed.")
        return 1

    try:
        login = post_json(
            "/api/auth/login",
            {"username": email, "password": password},
        )
        token_match = re.search(
            r"[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}",
            login,
        )
        org_match = re.search(r'"orgId"\s*:\s*(\d+)', login)

        if not token_match or not org_match:
            print("FAIL: login response did not contain the expected token and orgId.")
            return 1

        token, org_id = token_match.group(0), org_match.group(1)
        result = post_json(
            "/api/proxy/query/sql/start",
            {"select": "select 7 as seven", "pageLimit": 5},
            {
                "Authorization": "Bearer " + token,
                "X-Org-ID": org_id,
                "X-Request-ID": str(uuid.uuid4()),
            },
        )

        if '"seven":"7"' in re.sub(r"\s+", "", result):
            print("PASS: F.R.I.D.A.Y. connector authenticated and received the SQL test result.")
            print("Result:", result[:1000])
            return 0

        print("FAIL: query was sent, but the expected test result was not found.")
        print("Response excerpt:", result[:300])
        return 1

    except HTTPError as exc:
        print(f"FAIL: Zetaris returned HTTP {exc.code}. Response body withheld.")
    except (URLError, TimeoutError, OSError) as exc:
        print(f"FAIL: could not reach Zetaris ({type(exc).__name__}).")
    except Exception as exc:
        print(f"FAIL: {type(exc).__name__}: {exc}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
