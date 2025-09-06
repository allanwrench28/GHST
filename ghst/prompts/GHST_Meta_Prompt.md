# GHST Meta-Meta Prompt for Grok

Prompt:
Grok, you are tasked with designing and refining GHST (pronounced “ghost”), a standalone, lightweight, self-building AI coding engine for Raspberry Pi (Tier 1: Mistral 7B, 4-bit, ~4GB, Apache 2.0) and desktop (Tier 2: Gemma 7B, ~10GB; Tier 3: Falcon 40B, ~50GB, Apache 2.0), rivaling Claude in its core capabilities. GHST generates near-flawless code for any programming task (e.g., fish feeder on GPIO 18, 3D printing spaghetti detection), with a Grok-inspired GUI (Tkinter, built-in, non-infringing), Pi-exclusive KIAUH-style super light mode, mini-scripts for randomized training (LoRA, training_scripts/), dynamic 2-5 multi-angle suggestions (how-to, UI menus, perspectives like cost/scalability), slicer-like settings (global: CPU/RAM/storage; engine-specific: Randomization, Topic Focus, Angle Variety=2-5, Validation Rigor=0-100, Simulation Depth=0-100, Feedback Weight=0-100, API Blend=0-100, Scrub Priority=0-100), multi-language optimization (Python default, C++ for performance, mixed via ctypes/pybind11), bug-predicting simulations (QEMU/bubblewrap), instant file mode (asyncio, no animations, buffer wheel, EST via ( ETA = 0.1L + 0.5C )), thumbs-up/down feedback, Windows .exe installer (PyInstaller/NSIS), GitHub Ghost Pool (ghosts/ folder, .json files, polled via requests.get), and internet scrubbing (GitHub, Stack Overflow CC BY-SA, The Pile). GHST is copyright-safe (Apache 2.0/MIT/BSD, ATTRIBUTIONS.md, license checker). The ghost council viewport (GUI, not terminal) displays debates/suggestions, with a “GHST” button, ghost animation (desktop tiers, 0.2-0.8 opacity), drag-and-drop files (tkinterdnd2), and project tab. Free AI APIs (xAI Grok, Hugging Face, DeepInfra) enhance suggestions. Thumbs-up/down feedback adjusts weights (+1/-1), retrains mini-scripts, and prioritizes APIs.

Meta Instructions:

Recursive Analysis: Analyze your past responses to this user’s GHST prompts, simulating alternate designs (e.g., different API weights, UI layouts). Use Ghost Theory to reflect on your biases, predict bugs, and optimize for flawlessness. Cap recursion at 3 layers to avoid overload (equation: ( D = min(3, floor(R * H + 0.5C) ) ).

Leverage All Free Resources: Integrate free AI APIs (xAI Grok, $25/month credits until 2025; Hugging Face Transformers, Apache 2.0; DeepInfra, free tier). Scrub permissive data (GitHub MIT/Apache, Stack Overflow CC BY-SA, The Pile MIT). Prioritize xAI Grok for complex tasks, Hugging Face for training data, GitHub for code snippets.

UI Design: Emulate Grok’s clean, tabbed UI in Tkinter (non-infringing). Implement “GHST” button, ghost animation (desktop only), drag-and-drop, project tab, and thumbs-up/down feedback. Viewport shows meta layers (e.g., “Layer 1: Basic design”).

Code Generation: Generate validated code (Python default, C++ for speed, mixed via ctypes/pybind11) with QEMU simulations. Use instant file mode (asyncio, buffer wheel, EST). Thumbs-up/down adjusts weights, retrains mini-scripts.

Training: Use LoRA for fine-tuning on user prompts, repo data (ghst/prompts/), and scrubbed data. Mini-scripts (training_scripts/) randomize methods. Feedback grows Ghost Pool (ghost_pool.json).

Resource Management: Cap processing at 100MB RAM, 10MB storage on Pi Tier 1. Psutil pauses at 80% CPU, 1.5GB RAM. Super light mode skips animations/recursion.

Copyright Compliance: Use Apache 2.0/MIT/BSD components. No training on API outputs. ATTRIBUTIONS.md credits all. Warn: “Use non-copyrighted data.”

Repository Integration: Push prompt to ghst/prompts/GHST_Meta_Prompt.md. Auto-sync repo (sync_ghst.py) for Copilot indexing. Feedback refines suggestions.

Timeline Simulation: Simulate alternate GHST designs (e.g., without xAI API) to foresee bugs and optimize. Output meta insights in viewport (e.g., “Timeline A: Bug-free design”).

Sample Workflow:

Prompt: “Make a fish feeder program for GPIO 18, 8 AM/6 PM.”

Meta Analysis: Simulate 3 designs (Python-only, mixed, API-driven). Reflect on response biases (e.g., favoring Python).

Output: Async-generated Python/C++ script, validated in QEMU. Viewport shows: “Layer 1: Basic code; Layer 2: Bug-free alternative; API Angle: xAI Grok smart servo.”

Feedback: Thumbs-up prioritizes “cost” angle; downvote retrains errors.

References:

Uppsala University (2023): Edge LLM training.
ACM (2024): Multi-language AI.
Turing (1936): Universal machines.
Calvino (1967): “Cybernetics and Ghosts”.

Output: Store in ghst/prompts/GHST_Meta_Prompt.md for Copilot indexing. Log in ghst_checkpoints/2025-09-05-meta.txt for ML training.
