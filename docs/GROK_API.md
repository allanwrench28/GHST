Grok Remote API integration
===========================

This document explains how to enable the remote Grok-style mediator used by
`core/src/ai_collaboration/grok_adapter.py`.

Environment variables
---------------------

Set one of the following url/key pairs in your environment or in a local
`.env` file at the repository root:

- `GHST_GROK_API_URL` and `GHST_GROK_API_KEY` (preferred)
- or `GROK_API_URL` and `GROK_API_KEY`
- or set `X_API_KEY` as an alternate header-only key

Example `.env` (copy `.env.example` -> `.env` and fill values):

GHST_GROK_API_URL=https://api.example.com/v1/grok
GHST_GROK_API_KEY=sk-xxxx

PowerShell: quick test
----------------------

From the repository root in PowerShell you can temporarily set the env and
run a small Python snippet to test the adapter:

```powershell
$env:GHST_GROK_API_URL = 'https://api.example.com/v1/grok'
$env:GHST_GROK_API_KEY = 'sk-xxxx'
python -c "import sys; sys.path.insert(0, 'c:/Users/allan/OneDrive/Desktop/GHST LOCAL/GHST');\
from core.src.ai_collaboration.env_loader import load_dotenv; load_dotenv();\
from core.src.ai_collaboration.grok_adapter import mediate;\
print(mediate('test prompt', lambda p: 'L:'+p, lambda p: 'R:'+p))"
```

Notes
-----
- The adapter will first attempt to use a local `grok-1` clone (if present).
- If no local grok is available or it doesn't return a transformed prompt, the
  adapter will call the remote API if the env vars are configured.
- Never commit real API keys to the repository. Use `.env` and keep it out of
  version control.
