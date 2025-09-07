import argparse
import sys
import json
from pathlib import Path

sys.path.insert(0, r'c:/Users/allan/OneDrive/Desktop/GHST LOCAL/GHST')
from scripts.run_moe_demo import build_orchestrator


def consult_moe(prompt: str, model_name: str | None = None, experts_per_token: int = 2):
    settings_path = Path(r'c:/Users/allan/OneDrive/Desktop/GHST LOCAL/GHST') / 'core' / '.model_settings.json'
    chosen = model_name
    if not chosen and settings_path.exists():
        try:
            d = json.loads(settings_path.read_text(encoding='utf8'))
            chosen = d.get('selected_model') or d.get('model_name')
        except Exception:
            chosen = None

    orch = build_orchestrator(chosen)
    try:
        orch.experts_per_token = max(1, int(experts_per_token))
    except Exception:
        pass

    # attempt to resolve a summarizer from the model registry
    try:
        from core.src.ai_collaboration.model_registry import get_summarizer

        summarizer = get_summarizer(None)
    except Exception:
        summarizer = None

    res = orch.run(prompt, summarizer_fn=summarizer)

    print('--- SCRUBBED PROMPT ---')
    print(res.get('scrubbed', ''))
    print('\n--- COMBINED OUTPUT ---')
    print(res.get('combined', ''))
    print('\n--- DECISION / SUMMARY ---')
    print(res.get('decision', ''))
    print('\n--- PER-EXPERT CONTRIBUTIONS (counts) ---')
    print({k: len(v) for k, v in res.get('per_expert', {}).items()})
    print('\n--- SAMPLE FROM EACH EXPERT (last item) ---')
    for k, v in res.get('per_expert', {}).items():
        print(f"{k}: {v[-1] if v else ''}")


def main():
    parser = argparse.ArgumentParser(description='Consult the local MoE')
    parser.add_argument('--prompt', '-p', help='Prompt to ask the MoE', default=None)
    parser.add_argument('--model-name', help='Registered model name to use for experts', default=None)
    parser.add_argument('--expert-models', help='Comma-separated model names for each expert slot', default=None)
    parser.add_argument('--experts-per-token', type=int, default=2, help='How many experts per token')
    args = parser.parse_args()

    prompt = args.prompt
    if not prompt:
        prompt = (
            "Analyze this repository and propose the top three high-impact engineering improvements to get GHST to a stable developer-friendly release."
        )

    expert_models = None
    if args.expert_models:
        expert_models = [s.strip() for s in args.expert_models.split(',') if s.strip()]
    # If expert_models supplied, we will build heterogeneous experts by name
    if expert_models:
        # temporarily import build_orchestrator to create and run a bespoke orchestrator
        from scripts.run_moe_demo import build_orchestrator
        orch = build_orchestrator(model_name=None, model_path=None, expert_model_names=expert_models)
        try:
            orch.experts_per_token = max(1, int(args.experts_per_token))
        except Exception:
            pass
        res = orch.run(prompt)
        print('--- SCRUBBED PROMPT ---')
        print(res.get('scrubbed', ''))
        print('\n--- DECISION / SUMMARY ---')
        print(res.get('decision', ''))
        print('\n--- PER-EXPERT CONTRIBUTIONS (counts) ---')
        print({k: len(v) for k, v in res.get('per_expert', {}).items()})
        print('\n--- SAMPLE FROM EACH EXPERT (last item) ---')
        for k, v in res.get('per_expert', {}).items():
            print(f"{k}: {v[-1] if v else ''}")
        return

    consult_moe(prompt, model_name=args.model_name, experts_per_token=args.experts_per_token)


if __name__ == '__main__':
    main()
