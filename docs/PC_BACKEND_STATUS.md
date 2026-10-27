# F.R.I.D.A.Y. PC Backend

## Verified
- Python API starts locally on 127.0.0.1:8000.
- `/api/health` reports backend and Meterless configuration.
- `POST /api/chat` successfully invoked the Meterless agent.
- The running API returned `mode: model` through NVIDIA Nemotron.
- H-MEM memory `mem-1` was retrieved and included in a generated answer.
- A separate Nemotron API smoke test returned `FRIDAY_BRAIN_OK`.
- A separate Zetaris smoke test returned `seven: 7`; its result was stored and recalled through H-MEM.

## Limitations
- The NVIDIA key was supplied to the running process at launch and is not stored in source control.
- The Zetaris bridge was not reachable in the latest PC backend health check.
- Browser UI-to-backend operation has not yet been independently verified.
- This is a PC prototype, not the original Android application.
- Full Android-to-Zetaris integration remains unverified.

## Run
Use Node.js 22, set `FRIDAY_METERLESS_DIR` to the prepared Meterless agent directory, configure `NVIDIA_API_KEY` securely in the process environment, and run `python3 app.py`.

The API binds to localhost only.
