"""Run a headless MoE demo or launch the terminal GUI if available.

This script constructs 8 experts using `local_model.make_local_model_callable` and
registers them with the `MultiExpertOrchestrator`. By default it runs a headless
prompt and prints the combined output. If PyQt5 is available, you can pass
--gui to open the terminal-centered GUI.
"""
import argparse
from pathlib import Path
from core.src.ai_collaboration.moe_orchestrator import MultiExpertOrchestrator, Expert
from core.src.ai_collaboration.model_registry import get_model
import json


def build_orchestrator(model_name: str | None = None, model_path: str | None = None, expert_model_names: list[str] | None = None) -> MultiExpertOrchestrator:
    """Create an orchestrator where each expert is a callable resolved from the registry.

    model_name: if provided and registered in the registry, that callable will be used
    for all experts. Otherwise a mock callable is used.
    """
    experts = []

    # Helper to resolve a model callable by name with fallbacks
    def resolve_callable(name: str | None):
        if not name:
            return get_model("mock")
        try:
            return get_model(name, model_path=model_path)
        except Exception:
            try:
                from core.src.ai_collaboration.model_registry import get_registered_model

                return get_registered_model(name)
            except Exception:
                return get_model("mock")

    # Build per-slot experts; if expert_model_names provided, use those entries (repeat or truncate to 8)
    slots = []
    if expert_model_names:
        # normalize length to 8
        names = (expert_model_names + expert_model_names)[:8]
        for i in range(8):
            names = names
            model_call = resolve_callable(names[i] if i < len(names) else None)
            slots.append(model_call)
    else:
        default_callable = resolve_callable(model_name)
        slots = [default_callable for _ in range(8)]

    def _wrap_callable(fn):
        # Return a callable that accepts (text, ctx) and falls back to single-arg functions.
        def _call(text, ctx):
            try:
                return fn(text, ctx)
            except TypeError:
                try:
                    return fn(text)
                except Exception as e:
                    return f"Error in wrapped model call: {e}"
            except Exception as e:
                return f"Error in wrapped model call: {e}"

        return _call

    for i, fn in enumerate(slots):
        safe_fn = _wrap_callable(fn)
        experts.append(Expert(name=f"expert_{i}", fn=safe_fn, metadata={}))

    return MultiExpertOrchestrator(experts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gui", action="store_true", help="Launch terminal GUI if available")
    parser.add_argument("--model", help="Path to local quantized model file (optional)")
    parser.add_argument("--model-name", help="Registered model name to use for experts (optional)")
    parser.add_argument("--experts-per-token", type=int, default=2, help="How many experts to call per token (default 2)")
    args = parser.parse_args()

    # persist chosen model name
    settings_path = Path(__file__).resolve().parents[1] / 'core' / '.model_settings.json'
    if args.model_name:
        try:
            settings_path.parent.mkdir(parents=True, exist_ok=True)
            settings_path.write_text(json.dumps({"model_name": args.model_name}, indent=2), encoding='utf8')
        except Exception:
            pass

    chosen = None
    if args.model_name:
        chosen = args.model_name
    else:
        if settings_path.exists():
            try:
                j = json.loads(settings_path.read_text(encoding='utf8'))
                chosen = j.get('model_name')
            except Exception:
                chosen = None

    orch = build_orchestrator(chosen, model_path=args.model)
    # If the CLI requested a different experts-per-token, set it on the orchestrator
    try:
        orch.experts_per_token = max(1, int(args.experts_per_token))
    except Exception:
        pass
    prompt = "Please diagnose build failure and propose fixes"
    res = orch.run(prompt)
    print("Combined:\n", res['combined'])

    if args.gui:
        try:
            from core.src.ui_components.gui_terminal import run_terminal_gui
            run_terminal_gui(orch)
        except Exception as e:
            print("GUI unavailable:", e)


if __name__ == '__main__':
    main()
