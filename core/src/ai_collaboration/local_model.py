"""Light wrapper for a local quantized model runtime (llama.cpp via llama-cpp-python).

This module provides a factory that returns a callable compatible with the
`Expert.fn(token, ctx)` signature used by the MoE orchestrator. It falls back
to a small mock responder if `llama_cpp` is unavailable.
"""

from typing import Callable, Dict, Any
import os
import logging

logger = logging.getLogger(__name__)


def make_local_model_callable(
    model_path: str | None = None, prefix: str = "lm"
) -> Callable[[str, Dict[str, Any]], str]:
    """Return a callable fn(token, ctx) -> str.

    If `llama_cpp` is installed and `model_path` points to a model file, this
    will return a wrapper that uses the model. Otherwise returns a deterministic
    mock that imitates responses.
    """
    try:
        import llama_cpp  # type: ignore
    except Exception:
        llama_cpp = None

    if llama_cpp and model_path and os.path.exists(model_path):
        try:
            llm = llama_cpp.Llama(model_path=str(model_path))
            logger.info(f"Loaded local model from {model_path}")

            def fn(token: str, ctx: Dict[str, Any]) -> str:
                # We keep calls short: generate a short completion for the token
                try:
                    resp = llm.create(
                        prompt=token, max_tokens=16, stop=["\n"]
                    )  # simple
                    return resp["choices"][0]["text"].strip()
                except Exception as e:
                    return f"[model error] {e}"

            return fn
        except Exception as e:
            logger.warning(f"Failed to load llama_cpp model: {e}")

    # Fallback mock
    def mock_fn(token: str, ctx: Dict[str, Any]) -> str:
        return f"{prefix}({token})"

    return mock_fn
