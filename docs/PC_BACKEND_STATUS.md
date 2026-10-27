# F.R.I.D.A.Y. PC Backend

## Verified
- Local Python API starts on 127.0.0.1:8000.
- `/api/health` reports backend status.
- `POST /api/chat` calls the Meterless H-MEM notebook.
- A live request returned H-MEM retrieval output with memory provenance.

## Limitations
- This is a PC-side prototype, not the recovered original Android backend.
- Chat was verified in retrieval-only mode.
- Nemotron was tested separately, but the running API has not yet been
  verified with Nemotron enabled.
- The Zetaris bridge is a separate component and must be running locally.

## Run
Load Node.js 22 using nvm, then set `FRIDAY_METERLESS_DIR` to the prepared
Meterless directory and run `python3 app.py`.

The API binds to localhost only.
