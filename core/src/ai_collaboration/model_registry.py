"""Simple registry of model callables for MoE and adapters.

Provides small helper to choose between 'local', 'remote_foss', and 'mock'
models. Remote FOSS endpoints are simple HTTP wrappers expecting a JSON
POST {"prompt":...} returning text in `text` or `output`.
"""
from __future__ import annotations

from typing import Callable, Optional, Dict
import os
import json
import urllib.request
import urllib.error
import logging

logger = logging.getLogger(__name__)


def _make_remote_http_callable(url: str, api_key: Optional[str] = None) -> Callable[[str], str]:
    def fn(prompt: str) -> str:
        payload = json.dumps({"prompt": prompt}).encode("utf-8")
        req = urllib.request.Request(url, data=payload, method="POST")
        req.add_header("Content-Type", "application/json")
        if api_key:
            req.add_header("Authorization", f"Bearer {api_key}")
            req.add_header("X-API-Key", api_key)
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                body = resp.read()
                try:
                    j = json.loads(body.decode("utf-8"))
                    for k in ("text", "output", "result"):
                        if k in j:
                            return j[k]
                    vals = [v for v in j.values() if isinstance(v, str)]
                    if vals:
                        return vals[0]
                except Exception:
                    return body.decode("utf-8")
        except Exception as e:
            logger.debug(f"Remote model call failed: {e}")
            return f"[remote error] {e}"

    return fn


# Simple registry
_REGISTRY: Dict[str, Dict] = {}


def register_model(name: str, fn: Callable[[str], str], *, meta: Optional[dict] = None) -> None:
    """Register a callable under `name`. Overwrites existing registration."""
    _REGISTRY[name] = {"fn": fn, "meta": meta or {}}


def list_models() -> Dict[str, Dict]:
    """Return a shallow copy of the registry metadata."""
    return {k: v.get("meta", {}) for k, v in _REGISTRY.items()}


def get_registered_model(name: str) -> Callable[[str], str]:
    entry = _REGISTRY.get(name)
    if not entry:
        raise KeyError(f"No registered model named {name}")
    return entry["fn"]


def _make_ollama_callable(model: str, host: str = "http://localhost:11434") -> Callable[[str], str]:
    """Return a callable that queries an Ollama local server (simple HTTP wrapper).

    This expects Ollama running locally with model name available. It posts
    {"prompt":...} to /api/models/{model}/generate and returns the text.
    """
    url = f"{host.rstrip('/')}/api/models/{model}/generate"

    def fn(prompt: str) -> str:
        payload = json.dumps({"prompt": prompt}).encode("utf-8")
        req = urllib.request.Request(url, data=payload, method="POST")
        req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                body = resp.read()
                try:
                    j = json.loads(body.decode("utf-8"))
                    # Ollama's JSON shape may vary; try common keys
                    for k in ("text", "output", "result"):
                        if k in j:
                            return j[k]
                    vals = [v for v in j.values() if isinstance(v, str)]
                    if vals:
                        return vals[0]
                except Exception:
                    return body.decode("utf-8")
        except Exception as e:
            logger.debug(f"Ollama call failed: {e}")
            return f"[ollama error] {e}"

    return fn


# Pre-register simple models
try:
    register_model("mock", lambda p: f"m({p})", meta={"type": "mock"})
except Exception:
    pass


    # Auto-register a Grok-like remote if env vars are present
    def _register_grok_from_env():
        url = os.environ.get("GHST_GROK_API_URL") or os.environ.get("GROK_API_URL")
        key = os.environ.get("GHST_GROK_API_KEY") or os.environ.get("GROK_API_KEY") or os.environ.get("X_API_KEY")
        if url:
            try:
                register_model("grok_remote", _make_remote_http_callable(url, key), meta={"type": "remote", "url": url})
                logger.info("Registered grok_remote from env")
            except Exception as e:
                logger.debug(f"Failed to register grok_remote: {e}")


    try:
        _register_grok_from_env()
    except Exception:
        pass


    def get_summarizer(name: str | None = None) -> Callable[[str, Dict], str] | None:
        """Return a summarizer callable if available in the registry.

        If `name` is provided, try to return that registered model. Otherwise
        prefer `grok_remote` then `summarizer` registered entry. Returns None
        if no summarizer is available.
        """
        try:
            if name:
                return get_registered_model(name)
        except Exception:
            pass
        for prefer in ("grok_remote", "summarizer"):
            try:
                return get_registered_model(prefer)
            except Exception:
                continue
        return None



def get_model(name: str, **kwargs) -> Callable[[str], str]:
    """Return a callable by name.

    Supported names:
      - 'mock' : returns a simple deterministic mock
      - 'remote_foss' : expects url and optional api_key in kwargs
      - 'local' : expects model_path and prefix in kwargs and uses
          local_model.make_local_model_callable
    """
    if name == "mock":
        prefix = kwargs.get("prefix", "m")

        def fn(p: str) -> str:
            return f"{prefix}({p})"

        return fn

    if name == "remote_foss":
        url = kwargs.get("url") or os.environ.get("REMOTE_FOSS_URL")
        api_key = kwargs.get("api_key") or os.environ.get("REMOTE_FOSS_KEY")
        if not url:
            raise RuntimeError("remote_foss requires a url")
        return _make_remote_http_callable(url, api_key)

    if name == "local":
        from core.src.ai_collaboration.local_model import make_local_model_callable

        model_path = kwargs.get("model_path")
        prefix = kwargs.get("prefix", "lm")
        # Note: local model returns a fn(token, ctx). Adapter users expect fn(prompt)->str
        local_fn = make_local_model_callable(model_path=model_path, prefix=prefix)

        def wrapper(p: str) -> str:
            return local_fn(p, {})

        return wrapper

    raise KeyError(f"Unknown model name: {name}")
