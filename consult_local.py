#!/usr/bin/env python3
"""Temporary consult script to query GHST personas and print advice."""
from __future__ import annotations

import sys

def main(topic: str = "general", count: int = 5) -> int:
    # Local persona loader (avoids importing modules that configure logging)
    import json
    import random
    from hashlib import sha256
    from pathlib import Path

    def load_ghost_list_local() -> list:
        mod_paths = (
            'src.ai_collaboration.ghost_generator',
            'ai_collaboration.ghost_generator',
            'ghost_generator',
        )
        accessors = (
            'generate_ghosts', 'get_ghosts', 'get_ghost_list',
            'load_ghosts', 'ghost_list', 'ghosts'
        )
        for mod_path in mod_paths:
            try:
                mod = __import__(mod_path, fromlist=['*'])
            except Exception:
                continue
            for acc in accessors:
                val = getattr(mod, acc, None)
                if val is None:
                    continue
                try:
                    data = val() if callable(val) else val
                except Exception:
                    data = val
                if not isinstance(data, list) or not data:
                    continue
                out = []
                for item in data:
                    if isinstance(item, dict) and 'name' in item:
                        out.append({'name': item['name'], 'role': item.get('role', 'GHST Doctor')})
                    elif isinstance(item, str):
                        out.append({'name': item, 'role': 'GHST Doctor'})
                if out:
                    return out

        possible = (Path('ghosts/ghost_list.json'), Path('ghosts/ghost_list.txt'), Path('.ghost_list.json'), Path('.github/ghost_list.txt'))
        for p in possible:
            if not p.exists():
                continue
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

    def assign_unique_emojis_local(personas: list) -> dict:
        pool = ['👻','🕯️','🔮','🪄','🪦','🧿','🦴','👁️','👾','👽','🛠️','🧹','🧠','🔬','🧪','🕵️','🧩','⚙️','🔧','🧭','📚','📈','🧰','💡','🎯','🪙','🧬']
        mapping = {}
        used = set()
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
        return mapping

    personas = load_ghost_list_local()
    emoji_map = assign_unique_emojis_local(personas)
    chosen = personas[:max(1, min(len(personas), count))]

    role_templates = {
        'Automated Code Cleaner': 'Run formatters, then run tests. Prefer small commits.',
        'Syntax Specialist': 'Search for unterminated strings and mismatched quotes; run linters.',
        'Dependency Wrangler': 'Pin dependency versions and run an audit.',
        'Style & Lint': 'Enforce max-line-length and add pre-commit hooks.',
        'Repository Steward': 'Archive unused files and document layout.',
        'Test Strategist': 'Add focused unit tests and CI coverage for critical paths.',
        'Refactorer': 'Refactor one module at a time with tests.' ,
        'Merge Whisperer': 'Keep PRs small and reviewable; prefer rebasing.',
        'Type System Guru': 'Add type hints incrementally and run mypy in CI.'
    }

    print(f"Consulting {len(chosen)} GHST(s) on: {topic}\n")
    for p in chosen:
        name = p.get('name')
        role = p.get('role', 'GHST Doctor')
        emoji = emoji_map.get(name, '👻')
        advice = role_templates.get(role, None)
        if advice is None:
            advice = f"(As a {role}) Consider documenting and running targeted tests. Topic: {topic}."
        print(f"{emoji} {name} — {role}\n  ➜ {advice}\n")
    return 0


if __name__ == '__main__':
    topic = sys.argv[1] if len(sys.argv) > 1 else 'general'
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    sys.exit(main(topic, count))
