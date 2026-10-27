# F.R.I.D.A.Y. — Local Zetaris Bridge

The bridge is a prototype integration component.

## Run locally
1. Use a trusted development machine with Python 3 installed.
2. Configure the required Zetaris and bridge settings in a local `.env`.
3. Never commit `.env`, credentials, tokens, or bridge keys.
4. Start the bridge using the project's configured local environment.
5. Verify the health endpoint at `http://127.0.0.1:8765/health`.

The fixed test query has returned `seven: 7` with HTTP 200.
Requests without the bridge key were rejected as Unauthorized.
Authenticated Android-to-Zetaris query execution remains unverified.
Do not expose the bridge publicly.
