"""Lightweight Mixture-of-Experts (MoE) orchestrator scaffold.

This is a simulated MoE implementation intended for local GUI integration and
development. It does not implement real MoE training or large-model inference.
Instead it provides:
- registration for 8 named experts (callables)
- token-level routing that picks 2 experts per token (round-robin/hash)
- simple dataset accumulation for learning simulation
- a defensive text scrubbing helper to remove PII/URLs before use

The orchestration API is intentionally small and synchronous so it can be
called from GUI threads (or a worker thread) easily.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List, Any, Tuple
import logging
from core.src.ai_collaboration import dataset_store
import re
import hashlib

logger = logging.getLogger(__name__)


@dataclass
class Expert:
    name: str
    fn: Callable[[str, Dict[str, Any]], str]
    metadata: Dict[str, Any]


class MultiExpertOrchestrator:
    """Manage a small MoE of 8 experts and provide routing + simple learning.

    Design notes:
    - We simulate expert routing by hashing tokens -> picking two experts per token.
    - Experts are simple callables that accept (text, context) and return a string.
    - The orchestrator keeps a lightweight dataset list for later "replay" or
      incremental improvements (simulated).
    """

    def __init__(self, experts: List[Expert] | None = None, experts_per_token: int = 2):
        # initialize 8 slot experts with placeholders if not provided
        self.slots: List[Expert] = []
        if experts:
            self.slots = experts[:8]
        # if fewer than 8 provided, fill with dummy experts
        while len(self.slots) < 8:
            idx = len(self.slots)
            self.slots.append(
                Expert(
                    name=f"expert_{idx}",
                    fn=self._default_expert_fn,
                    metadata={"idx": idx},
                )
            )

        self.dataset: List[Dict[str, Any]] = []  # list of {prompt, scrubbed, expert_outputs}
        # how many experts to call per token (default 2)
        if experts_per_token < 1:
            raise ValueError("experts_per_token must be >= 1")
        self.experts_per_token = min(experts_per_token, max(1, len(self.slots)))

    # ------------------ scrubbing ------------------
    SCRUB_EMAIL_RE = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
    SCRUB_URL_RE = re.compile(r"https?://\S+|www\.\S+")
    SCRUB_KEY_RE = re.compile(r"(?:api_key|secret|password)[:=]\s*\S+", re.IGNORECASE)

    @classmethod
    def scrub_text(cls, text: str) -> str:
        """Remove or redact obvious PII or sensitive tokens from text.

        This is intentionally conservative and heuristic-based.
        """
        t = cls.SCRUB_EMAIL_RE.sub("[REDACTED_EMAIL]", text)
        t = cls.SCRUB_URL_RE.sub("[REDACTED_URL]", t)
        t = cls.SCRUB_KEY_RE.sub("[REDACTED_KEY]", t)
        return t

    # ------------------ experts / routing ------------------
    @staticmethod
    def _default_expert_fn(text: str, ctx: Dict[str, Any]) -> str:
        return f"(noop) {text[:120]}"

    def register_expert(self, idx: int, expert: Expert) -> None:
        if not 0 <= idx < 8:
            raise ValueError("expert index must be in 0..7")
        self.slots[idx] = expert

    def _token_hash(self, token: str) -> int:
        # stable hash for routing
        h = hashlib.sha256(token.encode("utf-8")).digest()
        return h[0]  # simple byte -> 0..255

    def _route_experts(self, token: str, k: int | None = None) -> Tuple[int, ...]:
        """Return k expert slot indices for the token.

        Deterministic selection: start index based on hash byte, then take k
        consecutive slots modulo the number of available slots.
        """
        k = k or self.experts_per_token
        b = self._token_hash(token)
        start = b % len(self.slots)
        indices = tuple(((start + o) % len(self.slots)) for o in range(k))
        return indices

    def run(self, prompt: str, context: Dict[str, Any] | None = None, summarizer_fn: Callable[[str, Dict[str, Any]], str] | None = None) -> Dict[str, Any]:
        """Run the MoE on a prompt and return per-expert outputs + combined output.

        This function:
        - scrubs the prompt
        - tokenizes simply on whitespace
        - routes each token to two experts and collects their replies
        - aggregates replies into a combined message
        - appends the example to the local dataset for 'learning'
        """
        ctx = context or {}
        scrubbed = self.scrub_text(prompt)
        tokens = scrubbed.split()
        per_expert_outputs: Dict[str, List[str]] = {e.name: [] for e in self.slots}

        # For each token, call the configured number of experts
        for t in tokens:
            indices = self._route_experts(t)
            for idx in indices:
                expert = self.slots[idx]
                try:
                    out = expert.fn(t, {**ctx, "full_prompt": scrubbed})
                except Exception as e:
                    out = f"Error in expert {expert.name}: {e}"
                per_expert_outputs[expert.name].append(out)

        # Simple aggregation strategy: join the last few outputs of top experts
        # Weighting: experts with more responses get more influence
        scores = {name: len(v) for name, v in per_expert_outputs.items()}
        # pick top 3 experts by contribution
        top_experts = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)[:3]
        combined_parts = []
        for name, _ in top_experts:
            combined_parts.append(" ".join(per_expert_outputs[name][-5:]))

        combined = "\n---\n".join(combined_parts).strip()

        # Produce a readable decision/summary. If a summarizer_fn is provided,
        # call it with the combined parts and context. Otherwise use a simple
        # heuristic summarizer that picks top experts and extracts readable
        # suggestions from their recent outputs.
        decision = None
        try:
            if summarizer_fn:
                # Provide the summarizer with a payload it can consume.
                payload = {
                    "prompt": prompt,
                    "scrubbed": scrubbed,
                    "combined": combined,
                    "per_expert": per_expert_outputs,
                }
                decision = summarizer_fn(combined, payload)
            else:
                # Heuristic summarizer: build a short top-3 list from top experts
                top_names = [name for name, _ in top_experts]
                suggestions = []
                for name in top_names[:3]:
                    # take the last non-empty response fragment from the expert
                    outputs = [s for s in per_expert_outputs.get(name, []) if s]
                    sample = outputs[-1] if outputs else "(no suggestion)"
                    # make short readable phrase
                    suggestions.append(f"From {name}: {sample}")
                decision = "\n".join([f"Top suggestions:"] + [f"{i+1}. {s}" for i, s in enumerate(suggestions)])
        except Exception:
            logger.exception("Summarization failed; falling back to combined text")
            decision = combined

        # Save to dataset (simulate learning data collection)
        example = {
            "prompt": prompt,
            "scrubbed": scrubbed,
            "expert_outputs": per_expert_outputs,
        }
        self.dataset.append(example)
        try:
            dataset_store.save_example(example)
        except Exception:
            logger.exception("Failed to persist example to dataset store")

        return {
            "scrubbed": scrubbed,
            "per_expert": per_expert_outputs,
            "combined": combined,
            "decision": decision,
            "dataset_size": len(self.dataset),
        }

    # Small utility: let light model pull from dataset
    def light_pull(
        self, light_fn: Callable[[str, Dict[str, Any]], str], query: str
    ) -> str:
        if not self.dataset:
            return "No dataset available."
        # Use last 10 examples as context
        context = " ".join([e["scrubbed"] for e in self.dataset[-10:]])
        return light_fn(f"{query} based on: {context}", {})


def example_usage():
    # create mock experts
    def make_expert(prefix: str):
        def fn(token: str, ctx: Dict[str, Any]):
            # small deterministic pseudo-response
            return f"{prefix}({token})"

        return fn

    names = [
        "data_science",
        "coding_genius",
        "debugging",
        "automation",
        "ai_research",
        "ops",
        "security",
        "ux",
    ]

    experts = [Expert(name=n, fn=make_expert(n), metadata={}) for n in names]
    orch = MultiExpertOrchestrator(experts)

    prompt = "Analyze dataset download error and suggest fixes"
    res = orch.run(prompt)
    print("Scrubbed prompt:", res["scrubbed"])
    print("Top combined output:\n", res["combined"])
    print("Dataset size:", res["dataset_size"])


if __name__ == "__main__":
    example_usage()
