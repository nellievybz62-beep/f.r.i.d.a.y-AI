# NVIDIA Nemotron Verification

## Observed result
- Model configured: `nvidia/nemotron-3.5-super-vl-120b-a12b`.
- The Meterless H-MEM agent printed `mode: nvidia-nemotron`.
- A live response answered the question about F.R.I.D.A.Y.'s security philosophy.
- The answer cited the stored memory `mem-6`, demonstrating use of retrieved memory context.

## Remaining caveat
The terminal reported exit code 1 after printing the response. The live
response was produced, but the command's final exit status needs investigation.

## Scope
The test was run in the local H-MEM test copy using the NVIDIA adapter source
copied from the submission project. This verifies the adapter's live response
path, but does not establish that the missing main F.R.I.D.A.Y. `app.py`
uses Nemotron.

## Security
API credentials are supplied locally. Never commit `.env` files, API keys,
or access tokens.
