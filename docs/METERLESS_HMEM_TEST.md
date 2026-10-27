# Meterless H-MEM Test Evidence

## Verified standalone test
- Runtime: Node.js 22.23.4 in Ubuntu/WSL.
- Engine loaded: `vendor/hmem`.
- Seed command mined five example memories.
- Retrieval query: `what did we decide about storage`.
- Retrieval returned relevant memories with provenance IDs.
- A separate `remember` command stored F.R.I.D.A.Y.'s
  "protected intelligence" principle as `mem-6`.
- A separate `ask` command retrieved that principle and cited `mem-6`.

## Reproduction
From this directory:
1. Run `npm install`.
2. Run `npm run setup`.
3. Run `npx tsx notebook.ts seed`.
4. Run `npx tsx notebook.ts ask "what did we decide about storage"`.
5. Run `npx tsx notebook.ts remember "F.R.I.D.A.Y. follows protected intelligence: automatic actions only in isolated, authorized labs."`.
6. Run `npx tsx notebook.ts ask "What is F.R.I.D.A.Y.'s security philosophy?"`.

Generated dependencies, vendored engine files, and local memory state are excluded from Git.

## Integration limitation
This verifies the standalone Meterless H-MEM starter, not integration with the main F.R.I.D.A.Y. backend. The main `app.py` was absent from the repository copy inspected; full application integration remains incomplete.
