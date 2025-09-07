"""Example thin wrapper to demonstrate using the Grok adapter.

This module provides a small example function `grok_mediated_chat` which is
safe to import and does not execute any network or model calls by default.
"""

from typing import Callable


def grok_mediated_chat(
    prompt: str,
    left_fn: Callable[[str], str],
    right_fn: Callable[[str], str],
):
    """Return mediation result from grok_adapter if available.

    This function imports the adapter lazily so the dependency is optional.
    """
    try:
        from core.src.ai_collaboration.grok_adapter import mediate
    except Exception:
        # Adapter missing or failed; call the models directly
        return {
            "grok": None,
            "left": left_fn(prompt),
            "right": right_fn(prompt),
        }

    return mediate(prompt, left_fn, right_fn)
