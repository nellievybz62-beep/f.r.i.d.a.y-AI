# Verified Zetaris + Meterless H-MEM Workflow

## Verified test
The combined integration script was run successfully on the development PC.

1. The script sent an authenticated request to the local Zetaris bridge.
2. The bridge executed its fixed SQL smoke test and returned `seven = 7`.
3. The script stored the result in Meterless H-MEM under a generated memory ID.
4. A follow-up retrieval recalled the saved result and displayed memory provenance.

## Components
- Zetaris: local Python bridge with authenticated fixed-query endpoint.
- Meterless: H-MEM memory-mining and retrieval engine.
- Integration driver: `integrations/zetaris_hmem_demo.py`.

## Reproduction
Requirements: Python 3, Node.js 20+, npm, the Zetaris platform, and a locally configured bridge.

1. Start Zetaris and the local bridge following `docs/LOCAL_BRIDGE_SETUP.md`.
2. Install the Meterless starter dependencies:
   `cd meterless-hmem && npm install && npm run setup`
3. From the repository root, set local environment variables without committing secrets:
   - `FRIDAY_ZETARIS_ENV_FILE` to the local Zetaris `.env` file path.
   - `FRIDAY_METERLESS_DIR` to the absolute path of `meterless-hmem`.
4. Run `python3 integrations/zetaris_hmem_demo.py`.

## Scope and limitations
This verifies a combined integration demo, not integration into the missing
main F.R.I.D.A.Y. `app.py`. The query is fixed and does not accept arbitrary
SQL from the client. NVIDIA Nemotron has not been verified in this workflow.
Keep credentials local and do not expose the bridge publicly.
