# F.R.I.D.A.Y. PC Backend Status

## Verified
- A local Python API runs on 127.0.0.1:8000.
- GET /api/health reports backend and component status.
- POST /api/chat invokes the Meterless H-MEM notebook.
- The desktop UI on port 8780 has successfully received an H-MEM response
  through this API.

## Limitations
- This is a new PC-side prototype, not the recovered original Android backend.
- Chat currently uses H-MEM retrieval; live Nemotron through this API
  has not yet been verified.
- Zetaris has a separate tested integration workflow, but the PC API
  health check did not report the bridge as reachable at the last check.
- The desktop UI's initial welcome message is static.

## Run locally
Load Node.js 22 with nvm, then run:
FRIDAY_METERLESS_DIR="$HOME/friday-meterless-test" python3 app.py

The API binds to localhost only. Do not expose it publicly.
