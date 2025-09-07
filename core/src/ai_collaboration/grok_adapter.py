"""
Lightweight adapter to use a local Grok-1 clone as a mediator between two LLM backends.
This adapter is intentionally small: it tries to import a local grok implementation and
exposes a simple `mediate(prompt, left_model_fn, right_model_fn)` function which feeds
prompt through local Grok (if available) and then queries the two provided model
callables. If Grok is unavailable, it falls back to directly calling the two models.

The adapter does not bundle or load model weights; that must be handled by the
local `grok-1` code you cloned (this file only provides a minimal integration layer).

Usage:
    from core.src.ai_collaboration.grok_adapter import mediate

    def model_a(prompt):
        return "..."
    def model_b(prompt):
        return "..."

    result = mediate("fix this function", model_a, model_b)

"""

from typing import Callable, Optional, Dict, Any
import importlib
import logging
import json
import os
import urllib.request
import urllib.error
from pathlib import Path

logger = logging.getLogger(__name__)

# Try to import a local grok module if present under repo path 'grok-1'.
_grok = None
try:
    # The user cloned grok-1 at repo root. We attempt to import a common entrypoint.
    import sys

    repo_root = Path(__file__).resolve().parents[4]
    grok_path = repo_root / "grok-1"
    if grok_path.exists():
        sys.path.insert(0, str(grok_path))
        try:
            _grok = importlib.import_module("grok")
            logger.info("Local grok module imported for mediation.")
        except Exception:
            # try other names
            try:
                _grok = importlib.import_module("grok_1")
                logger.info("Local grok_1 module imported for mediation.")
            except Exception:
                _grok = None
    else:
        logger.info("No local grok-1 folder found; continuing without local Grok.")
except Exception:
    logger.warning("Failed to import local grok module.")


def mediate(
    prompt: str,
    left_model_fn: Callable[[str], str],
    right_model_fn: Callable[[str], str],
    grok_options: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Mediate a prompt between two model callables, optionally using local Grok-1 as a transformer.
    Returns a dict with keys: 'grok' (if used), 'left', 'right'.
    """
    result = {}
    grok_options = grok_options or {}

    # If local Grok is available, use it to transform the prompt
    if _grok:
        try:
            # Assume grok has a callable like 'analyze' or 'run'; adjust based on actual API
            grok_fn = getattr(_grok, "analyze", getattr(_grok, "run", None))
            if grok_fn and callable(grok_fn):
                transformed_prompt = grok_fn(prompt, **grok_options)
                result["grok"] = transformed_prompt
                prompt = transformed_prompt  # Use transformed prompt for the two models
            else:
                logger.warning(
                    "Local grok module found but no suitable callable (e.g., analyze or run)."
                )
        except Exception as e:
            logger.error(f"Error using local grok: {e}")

    # If no local grok transformed the prompt, attempt remote Grok API if configured
    if "grok" not in result:
        try:
            remote_transformed = _call_remote_grok(prompt, grok_options)
            if remote_transformed:
                result["grok"] = remote_transformed
                prompt = remote_transformed
        except Exception as e:
            logger.debug(f"Remote Grok call skipped/failed: {e}")

    # Query the two model callables
    try:
        result["left"] = left_model_fn(prompt)
    except Exception as e:
        result["left"] = f"Error: {e}"

    try:
        result["right"] = right_model_fn(prompt)
    except Exception as e:
        result["right"] = f"Error: {e}"

    return result


def _call_remote_grok(
    prompt: str, options: Optional[Dict[str, Any]] = None
) -> Optional[str]:
    """
    Call a remote Grok-like HTTP API if environment variables are set.

    Environment variables checked (in order):
      - GHST_GROK_API_URL or GROK_API_URL
      - GHST_GROK_API_KEY or GROK_API_KEY or X_API_KEY

    The adapter sends a JSON payload {"prompt": ..., "options": {...}} via POST
    and expects a JSON response with a top-level "transformed_prompt" or a
    string body.
    """
    options = options or {}
    api_url = os.environ.get("GHST_GROK_API_URL") or os.environ.get("GROK_API_URL")
    api_key = (
        os.environ.get("GHST_GROK_API_KEY")
        or os.environ.get("GROK_API_KEY")
        or os.environ.get("X_API_KEY")
    )
    if not api_url or not api_key:
        raise RuntimeError("Grok API URL/key not configured in environment")

    payload = json.dumps({"prompt": prompt, "options": options}).encode("utf-8")
    req = urllib.request.Request(api_url, data=payload, method="POST")
    # Prefer Authorization Bearer but also set an X-API-Key header as some endpoints use that
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {api_key}")
    req.add_header("X-API-Key", api_key)

    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = resp.read()
            # Try to parse JSON
            try:
                j = json.loads(body.decode("utf-8"))
                # Common key names
                for key in ("transformed_prompt", "result", "output", "text"):
                    if key in j:
                        return j[key]
                # If response is dict with single string value, return that
                vals = [v for v in j.values() if isinstance(v, str)]
                if vals:
                    return vals[0]
            except Exception:
                # Not JSON; return raw text
                return body.decode("utf-8")
    except urllib.error.HTTPError as he:
        logger.debug(f"Grok API HTTPError: {he.code} {he.reason}")
        raise
    except Exception as e:
        logger.debug(f"Grok API call failed: {e}")
        raise


# New: Multi-model orchestration for heavy/light setup
class MultiModelOrchestrator:
    """
    Orchestrates multiple models: two heavy models for training/predictions, and a light model that pulls from their datasets.
    """

    def __init__(
        self,
        heavy_model_1: Callable[[str], str],
        heavy_model_2: Callable[[str], str],
        light_model: Callable[[str], str],
    ):
        self.heavy_1 = heavy_model_1
        self.heavy_2 = heavy_model_2
        self.light = light_model
        self.dataset = []  # Shared dataset from heavy models

    def run_heavy_training(self, prompt: str) -> Dict[str, Any]:
        """Run heavy prediction algorithm training and dry runs on both heavy models."""
        results = {}
        # Simulate heavy tasks (e.g., training loops)
        for i, model in enumerate([self.heavy_1, self.heavy_2], 1):
            try:
                # Mock heavy computation: e.g., multiple inferences for training
                training_output = [
                    model(f"{prompt} - iteration {j}") for j in range(5)
                ]  # Dry run iterations
                results[f"heavy_{i}"] = training_output
                self.dataset.extend(training_output)  # Add to shared dataset
            except Exception as e:
                results[f"heavy_{i}"] = f"Error: {e}"
        return results

    def run_light_pull(self, query: str) -> str:
        """Light model pulls from the dataset generated by heavy models."""
        if not self.dataset:
            return "No dataset available from heavy models."
        # Mock: Use dataset to inform light model's response
        context = " ".join(self.dataset[-10:])  # Last 10 outputs as context
        try:
            return self.light(f"{query} based on: {context}")
        except Exception as e:
            return f"Light model error: {e}"


# Example usage
def example_usage():
    def mock_heavy_model(prompt):
        return f"Heavy prediction: {prompt}"

    def mock_light_model(prompt):
        return f"Light response: {prompt}"

    orchestrator = MultiModelOrchestrator(
        mock_heavy_model, mock_heavy_model, mock_light_model
    )

    # Heavy training
    heavy_results = orchestrator.run_heavy_training("Train on algorithm X")
    print("Heavy results:", json.dumps(heavy_results, indent=2))

    # Light pull
    light_result = orchestrator.run_light_pull("Summarize the training")
    print("Light result:", light_result)


if __name__ == "__main__":
    example_usage()
