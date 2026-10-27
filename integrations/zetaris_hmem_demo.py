#!/usr/bin/env python3
"""Run the fixed Zetaris bridge query and store/recall it with H-MEM."""

import json
import os
import subprocess
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError

ROOT = Path(__file__).resolve().parents[1]
BRIDGE_URL = os.getenv(
    "FRIDAY_ZETARIS_QUERY_URL",
    "http://127.0.0.1:8765/query-test",
)
ENV_FILE = Path(os.getenv("FRIDAY_ZETARIS_ENV_FILE", ""))
METERLESS_DIR = Path(os.getenv(
    "FRIDAY_METERLESS_DIR",
    str(ROOT / "meterless-hmem"),
)).expanduser()

def get_bridge_key():
    key = os.getenv("FRIDAY_ZETARIS_BRIDGE_KEY", "")
    if key:
        return key

    if not ENV_FILE.is_file():
        raise RuntimeError(
            "Set FRIDAY_ZETARIS_BRIDGE_KEY or "
            "FRIDAY_ZETARIS_ENV_FILE to a local .env path."
        )

    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        name, sep, value = line.strip().partition("=")
        if sep and name.strip() == "FRIDAY_ZETARIS_BRIDGE_KEY":
            value = value.strip().strip("'\"")
            if value:
                return value

    raise RuntimeError("Bridge key is missing from the local environment.")

def main():
    notebook = METERLESS_DIR / "notebook.ts"
    if not notebook.is_file():
        raise RuntimeError("H-MEM notebook.ts not found; check METERLESS_DIR.")

    req = Request(
        BRIDGE_URL,
        data=b"{}",
        headers={
            "Content-Type": "application/json",
            "X-FRIDAY-KEY": get_bridge_key(),
        },
        method="POST",
    )

    with urlopen(req, timeout=65) as response:
        result = json.loads(response.read().decode("utf-8"))

    records = result.get("records", [])
    if not result.get("ok") or not records:
        raise RuntimeError("Zetaris bridge did not return a successful result.")

    record = records[0]
    if str(record.get("seven")) != "7":
        raise RuntimeError("Unexpected result from the fixed Zetaris test query.")

    note = (
        "Zetaris authenticated bridge test returned seven = 7. "
        "This was a fixed-query smoke test."
    )
    print("Zetaris query verified: seven = 7.")

    subprocess.run(
        ["npx", "tsx", "notebook.ts", "remember", note],
        cwd=METERLESS_DIR,
        check=True,
    )
    print("\n=== Recall the Zetaris result from H-MEM ===")
    subprocess.run(
        [
            "npx", "tsx", "notebook.ts", "ask",
            "What did the Zetaris integration smoke test return?",
        ],
        cwd=METERLESS_DIR,
        check=True,
    )

if __name__ == "__main__":
    try:
        main()
    except HTTPError as exc:
        print(f"Zetaris bridge returned HTTP {exc.code}.", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(f"Integration test failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        sys.exit(1)
