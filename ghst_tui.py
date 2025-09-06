#!/usr/bin/env python3
"""
GHST TUI

Interactive terminal UI to consult the GHST think-tank and launch common actions.
Uses `prompt_toolkit` for clickable buttons when available, and falls back to a
simple numbered menu when not.

Usage: python ghst_tui.py
"""
from __future__ import annotations

import subprocess
import sys
from typing import List, Dict


def load_personas() -> List[Dict[str, str]]:
    # reuse local loader from consult_local to avoid import side-effects
    import json
    import random
    from hashlib import sha256
    from pathlib import Path

    def load_local():
        possible = (Path('ghosts/ghost_list.json'), Path('ghosts/ghost_list.txt'), Path('.ghost_list.json'), Path('.github/ghost_list.txt'))
        for p in possible:
            if p.exists():
                try:
                    if p.suffix == '.json':
                        with open(p, 'r', encoding='utf-8', errors='replace') as f:
                            data = json.load(f)
                        out = []
                        for item in data:
                            if isinstance(item, dict) and 'name' in item:
                                out.append({'name': item['name'], 'role': item.get('role', 'GHST Doctor')})
                            elif isinstance(item, str):
                                out.append({'name': item, 'role': 'GHST Doctor'})
                        if out:
                            return out
                    else:
                        out = []
                        with open(p, 'r', encoding='utf-8', errors='replace') as f:
                            for line in f:
                                line = line.strip()
                                if not line:
                                    continue
                                out.append({'name': line, 'role': 'GHST Doctor'})
                        if out:
                            return out
                except Exception:
                    continue
        # fallback
        fields = ['Automated Code Cleaner', 'Syntax Specialist', 'Dependency Wrangler', 'Style & Lint', 'Repository Steward', 'Test Strategist', 'Refactorer', 'Merge Whisperer', 'Type System Guru']
        base = ['Dr. TidyCode', 'Dr. Syntax', 'Dr. ImportOrder', 'Dr. Formatter', 'Dr. Archivist']
        out = []
        for n in base:
            out.append({'name': n, 'role': random.choice(fields)})
        return out

    personas = load_local()
    # deterministic emoji mapping
    pool = ['👻', '🕯️', '🔮', '🪄', '🪦', '🧿', '🦴', '👁️', '👾', '👽', '🛠️', '🧹', '🧠', '🔬', '🧪', '🕵️', '🧩', '⚙️', '🔧', '🧭']
    mapping = {}
    used = set()
    from hashlib import sha256
    for p in personas:
        name = p['name']
        h = int(sha256(name.encode('utf-8')).hexdigest(), 16)
        idx = h % len(pool)
        for shift in range(len(pool)):
            cand = pool[(idx + shift) % len(pool)]
            if cand not in used:
                mapping[name] = cand
                used.add(cand)
                break
        else:
            mapping[name] = '👻'
    for p in personas:
        p['emoji'] = mapping.get(p['name'], '👻')
    return personas


def show_debate(personas):
    # a short collaborative debate for display
    opinions = {
        'Style & Lint': 'Enforce style, add pre-commit hooks, and run formatters in CI.',
        'Automated Code Cleaner': 'Dry-run the fixer, inspect diffs, apply in small batches.',
        'Syntax Specialist': 'Fix parse errors first (unterminated strings).',
        'Repository Steward': 'Archive large non-code files to speed tools.',
        'Test Strategist': 'Run targeted tests for changed modules.',
    }
    lines = []
    lines.append('GHST Think-Tank Debate:')
    for p in personas:
        role = p.get('role', 'GHST Doctor')
        advice = opinions.get(role, 'Document changes and run tests.')
        lines.append(f"{p['emoji']} {p['name']} — {role}\n  {advice}\n")
    return '\n'.join(lines)


def run_action(action: str):
    # Map actions to ghst_agent or direct scripts
    mapping = {
        'syntax-scan': [sys.executable, '-c', "import ast, pathlib; files=list(pathlib.Path('core').rglob('*.py'))+list(pathlib.Path('scripts').rglob('*.py'));\n\nfor f in files:\n    try:\n        ast.parse(f.read_text(encoding='utf-8', errors='replace'))\n    except Exception as e:\n        print(f'{f}: {e}')"],
        'fix-dry': [sys.executable, 'ghst_agent.py', 'fix-once', '--dry-run'],
        'fix-apply': [sys.executable, 'ghst_agent.py', 'fix-once'],
        'cleanup-dry': [sys.executable, 'ghst_agent.py', 'cleanup-once'],
        'list-personas': [sys.executable, 'ghst_agent.py', 'list-personas'],
    }
    cmd = mapping.get(action)
    if not cmd:
        print('Unknown action', action)
        return 1
    print('Running:', ' '.join(cmd))
    proc = subprocess.run(cmd, capture_output=False)
    return proc.returncode


def run_tui():
    personas = load_personas()
    debate = show_debate(personas)
    try:
        from prompt_toolkit.shortcuts import button_dialog

        result = button_dialog(
            title='GHST Think-Tank',
            text=debate + '\nChoose an action:',
            buttons=[
                ('Run syntax scan', 'syntax-scan'),
                ('Fix (dry-run)', 'fix-dry'),
                ('Fix (apply)', 'fix-apply'),
                ('Cleanup (dry-run)', 'cleanup-dry'),
                ('List personas', 'list-personas'),
                ('Exit', 'exit'),
            ],
        ).run()
        if result == 'exit' or result is None:
            print('Goodbye')
            return 0
        return run_action(result)
    except Exception:
        # Fallback menu
        print(debate)
        opts = [
            ('1', 'Run syntax scan', 'syntax-scan'),
            ('2', 'Fix (dry-run)', 'fix-dry'),
            ('3', 'Fix (apply)', 'fix-apply'),
            ('4', 'Cleanup (dry-run)', 'cleanup-dry'),
            ('5', 'List personas', 'list-personas'),
            ('0', 'Exit', 'exit'),
        ]
        for k, label, _ in opts:
            print(f'[{k}] {label}')
        choice = input('Choose: ').strip()
        for k, label, act in opts:
            if choice == k:
                if act == 'exit':
                    print('Goodbye')
                    return 0
                return run_action(act)
        print('Invalid choice')
        return 1


def main():
    if '--demo' in sys.argv:
        personas = load_personas()
        print(show_debate(personas))
        return 0
    return run_tui()


if __name__ == '__main__':
    sys.exit(main())
