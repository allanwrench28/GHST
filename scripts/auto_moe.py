"""Auto-run MoE helper.

Usage:
  - One-shot: python scripts/auto_moe.py --once "Your question"
  - REPL: python scripts/auto_moe.py --repl
  - HTTP server: python scripts/auto_moe.py --http-port 8080

HTTP API: POST /ask with JSON {"prompt": "...", "model_name": "...", "experts_per_token": 2}
Responds with JSON containing scrubbed, combined, decision, per_expert, dataset_size.
"""
from __future__ import annotations
import argparse
import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any, Dict

# ensure repo top is importable
sys.path.insert(0, r'c:/Users/allan/OneDrive/Desktop/GHST LOCAL/GHST')
from scripts.run_moe_demo import build_orchestrator


def run_once(prompt: str, model_name: str | None = None, experts_per_token: int = 2) -> Dict[str, Any]:
    orch = build_orchestrator(model_name)
    try:
        orch.experts_per_token = max(1, int(experts_per_token))
    except Exception:
        pass
    res = orch.run(prompt)
    return res


def repl_loop(model_name: str | None = None, experts_per_token: int = 2) -> None:
    print("MoE REPL — enter prompts, empty line to quit.")
    while True:
        try:
            prompt = input('> ').strip()
        except EOFError:
            break
        if not prompt:
            break
        res = run_once(prompt, model_name=model_name, experts_per_token=experts_per_token)
        print(json.dumps({
            'scrubbed': res.get('scrubbed'),
            'decision': res.get('decision'),
            'combined': res.get('combined'),
            'per_expert_counts': {k: len(v) for k, v in res.get('per_expert', {}).items()},
        }, indent=2))


class SimpleHandler(BaseHTTPRequestHandler):
    def _set_json_headers(self, code=200):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def do_POST(self):
        if self.path != '/ask':
            self._set_json_headers(404)
            self.wfile.write(json.dumps({'error': 'not found'}).encode('utf8'))
            return
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf8') if length else ''
        try:
            payload = json.loads(body) if body else {}
        except Exception:
            self._set_json_headers(400)
            self.wfile.write(json.dumps({'error': 'invalid json'}).encode('utf8'))
            return
        prompt = payload.get('prompt')
        if not prompt:
            self._set_json_headers(400)
            self.wfile.write(json.dumps({'error': 'missing prompt'}).encode('utf8'))
            return
        model_name = payload.get('model_name')
        experts_per_token = int(payload.get('experts_per_token', 2))
        try:
            res = run_once(prompt, model_name=model_name, experts_per_token=experts_per_token)
            out = {
                'scrubbed': res.get('scrubbed'),
                'combined': res.get('combined'),
                'decision': res.get('decision'),
                'per_expert_counts': {k: len(v) for k, v in res.get('per_expert', {}).items()},
                'dataset_size': res.get('dataset_size'),
            }
            self._set_json_headers(200)
            self.wfile.write(json.dumps(out).encode('utf8'))
        except Exception as e:
            self._set_json_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode('utf8'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--once', help='Run one prompt and exit')
    parser.add_argument('--repl', action='store_true', help='Interactive REPL mode')
    parser.add_argument('--http-port', type=int, default=0, help='Start HTTP server on port (0 = disabled)')
    parser.add_argument('--model-name', help='Registered model name to use', default=None)
    parser.add_argument('--experts-per-token', type=int, default=2)
    parser.add_argument('--autopilot', help='Run autopilot for a high-level goal and persist tasks', default=None)
    args = parser.parse_args()

    if args.once:
        res = run_once(args.once, model_name=args.model_name, experts_per_token=args.experts_per_token)
        print(json.dumps({
            'scrubbed': res.get('scrubbed'),
            'decision': res.get('decision'),
            'combined': res.get('combined'),
            'per_expert_counts': {k: len(v) for k, v in res.get('per_expert', {}).items()},
            'dataset_size': res.get('dataset_size'),
        }, indent=2))
        return

    if args.autopilot:
        # Run the MoE to produce a decision and try to extract actionable steps
        res = run_once(args.autopilot, model_name=args.model_name, experts_per_token=args.experts_per_token)
        decision = res.get('decision') or res.get('combined') or ''

        # If a summarizer is registered, ask it to produce actionable next steps.
        summarizer_callable = None
        try:
            from core.src.ai_collaboration.model_registry import get_summarizer

            summ = get_summarizer(None)
            if summ:
                # wrap single-arg summarizers into a prompt that requests numbered steps
                def _summarizer(combined_text: str, payload: dict) -> str:
                    instr = (
                        "You are an expert project manager. Given the expert outputs below,"
                        " produce a numbered list (1..5) of concise, actionable next steps"
                        " to get the project moving toward a developer-friendly release."
                        " Output each step on its own numbered line.\n\n"
                    )
                    # include combined text and a short excerpt of expert outputs
                    body = combined_text
                    try:
                        # attach a small sample of per-expert outputs
                        per = payload.get('per_expert', {})
                        samp = []
                        for k, v in list(per.items())[:6]:
                            if v:
                                samp.append(f"{k}: {v[-1]}")
                        if samp:
                            samples = "\n".join(samp)
                            body = body + "\n\nExpert samples:\n" + samples
                    except Exception:
                        pass
                    return summ(instr + "\n" + body)
                summarizer_callable = _summarizer
        except Exception:
            summarizer_callable = None

        steps = []
        # if we have a summarizer_fn, call it and parse numbered lines
        if summarizer_callable:
            try:
                payload = {
                    "per_expert": res.get('per_expert', {}),
                    "combined": res.get('combined', ''),
                }
                raw = summarizer_callable(decision, payload)
                # parse numbered lines
                for line in raw.splitlines():
                    line = line.strip()
                    if not line:
                        continue
                    if line[0].isdigit():
                        parts = line.split('.', 1)
                        if len(parts) > 1:
                            steps.append(parts[1].strip())
                        else:
                            steps.append(line)
                    elif line.startswith('-') or line.startswith('*'):
                        steps.append(line.lstrip('-* ').strip())
                    else:
                        # accept short sentence as a step
                        if len(line.split()) <= 20:
                            steps.append(line)
                # if parsing failed, fall back below
            except Exception:
                steps = []

        # Fallback heuristics if no summarizer or parsing failed
        if not steps:
            # Simple extractor: look for numbered lines or split by newlines; keep top 6
            lines = [ln.strip() for ln in decision.splitlines() if ln.strip()]
            for ln in lines:
                starts = ln.lstrip().startswith(('1.', '1)', '-', '*'))
                two_digits = len(ln) > 1 and ln[:2].isdigit()
                if starts or two_digits:
                    parts = ln.split('.', 1)
                    if len(parts) > 1 and parts[0].strip().isdigit():
                        steps.append(parts[1].strip())
                    else:
                        steps.append(ln.lstrip('-*0123456789.) ').strip())
                else:
                    if len(ln.split()) > 2:
                        steps.append(ln)

            # Fallback to splitting into sentences
            if not steps:
                import re

                sents = re.split(r'[\r\n]+|[.!?]+\s+', decision)
                steps = [s.strip() for s in sents if s.strip()][:5]

        # Persist to AUTOPILOT_TASKS.md and core/.autopilot_queue.json
        repo_root = Path.cwd()
        tasks_md = repo_root / 'AUTOPILOT_TASKS.md'
        queue_path = repo_root / 'core' / '.autopilot_queue.json'

        with tasks_md.open('w', encoding='utf8') as f:
            f.write('# AUTOPILOT TASKS\n\n')
            f.write('Goal: ' + args.autopilot + '\n\n')
            for i, s in enumerate(steps, start=1):
                f.write(f'{i}. {s}\n')

        try:
            tasks = [
                {'id': i + 1, 'task': t, 'status': 'pending'}
                for i, t in enumerate(steps)
            ]
            queue = {'goal': args.autopilot, 'tasks': tasks}
            queue_path.parent.mkdir(parents=True, exist_ok=True)
            queue_path.write_text(json.dumps(queue, indent=2), encoding='utf8')
        except Exception:
            # best-effort persistence; ignore failures
            pass

        print('Autopilot created', tasks_md)
        for i, s in enumerate(steps, start=1):
            print(f'{i}. {s}')
        return

    if args.repl:
        repl_loop(
            model_name=args.model_name,
            experts_per_token=args.experts_per_token,
        )
        return

    if args.http_port:
        server_address = ('', args.http_port)
        httpd = HTTPServer(server_address, SimpleHandler)
        print(f'Starting MoE HTTP server on port {args.http_port}, POST /ask')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('Shutting down')
            httpd.server_close()
        return

    parser.print_help()


if __name__ == '__main__':
    main()
