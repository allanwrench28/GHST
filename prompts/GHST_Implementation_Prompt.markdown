# GHST Implementation Prompt (Version 14)

**Prompt**:  
Design a standalone, lightweight AI coding engine named GHST (pronounced “ghost”) for Raspberry Pi and desktop, using permissive open-source components (Apache 2.0, MIT, BSD) to avoid copyright infringement. GHST is a self-building LLM that generates near-flawless code for any programming task (e.g., fish feeder on GPIO 18, 3D printing spaghetti detection), with a Grok-inspired GUI, Pi-exclusive super light mode, mini-scripts for randomized training, resource awareness, and slicer-like settings. It provides dynamic 2-5 multi-angle suggestions (how-to, UI menus, perspectives like cost/scalability), auto-popping when triggered. Language handling: Ask user preference (e.g., “Python for ease, C++ for speed, mixed?”) with explanations; auto-optimize if none (100% Python for Pi, mixed via ctypes/pybind11, auto-generating bindings). Bug prediction: Simulate each line in a QEMU/bubblewrap environment. *Instant File Mode*: Generate files in the background (no animations, buffer wheel, EST via \( \text{ETA} = 0.1L + 0.5C \)). Pause/resume editing on the fly, inspired by Copilot but open-source (Tkinter/asyncio). Thumbs-up/down feedback refines suggestions, adjusting weights (+1/-1) via interactive sliders, retraining mini-scripts on downvotes, prioritizing APIs (xAI Grok for complex tasks). Feedback weights persist across projects in the project tab, stored in SQLite (`ghst_feedback.db`). Prompt users for context to resolve feedback conflicts (e.g., prioritize project, average, or new weight). The “Ghost Pool” is a GitHub folder (`ghosts/`) with .json files (name, expertise, templates). Local GHST uses `ghost_list.txt` to fetch ghosts via `requests.get(URL)`. Poll GitHub raw `ghost_list.txt` hourly/daily (optional) using background thread (`threading`, built-in). Compare hash (`hashlib`, built-in), no reinstall needed. Compile into a Windows `.exe` with wizard installer (PyInstaller/NSIS). GHST learns from prompts and feedback, storing in local Ghost Pool for keyword recalls. Internet scrubbing: Ghosts fetch permissive data (GitHub, Stack Overflow CC BY-SA, The Pile) in online mode, prioritized via “Scrub Priority” (0=GitHub, 100=mixed). Free AI APIs (xAI Grok, Hugging Face, DeepInfra) enhance suggestions, weighted by “API Blend” (0=local, 100=multi-API). The ghost council viewport (debates, suggestions) is in the GUI—panels/tabs for standard mode, text window for super light mode. Main viewport button labeled “GHST” triggers generation/*Ghost Theory*. Desktop tiers (2/3) include ghost animation (floating, 0.2-0.8 opacity). Drag-and-drop files (PDFs, CSVs) via tkinterdnd2 enhance suggestions. Project tab organizes tasks, feedback, and code. Feedback sliders in viewport adjust suggestion weights dynamically.

**Core Requirements**:
1. **LLM Tiers**:
   - Tier 1 (SD card, ~32GB): Mistral 7B, 4-bit (~4GB, Apache 2.0).
   - Tier 2 (USB SSD, ~256GB): Gemma 7B (~10GB, Apache 2.0).
   - Tier 3 (NAS, ~1TB): Falcon 40B (~50GB, Apache 2.0).
   - Use **Llama.cpp** (MIT, v0.2.82) for inference. Detect storage with `shutil.disk_usage()`. Heavier models grow via LoRA, capped by settings.
2. **Self-Training**:
   - **LoRA** for fine-tuning on user tasks/data (e.g., PDFs via **pdfplumber**, MIT, v0.7.6).
   - Mini-scripts in `training_scripts/` (e.g., `few_shot.py`) randomize methods. `train_manager.py` selects based on “Randomization Intensity” (0-100%).
   - **Psutil** (BSD, v5.9.5) pauses if CPU > 80%, RAM > max (1.5GB on Pi 4), storage > max (40GB).
3. **Code Generation**:
   - Generate validated code (Python default, C++ for performance, mixed via ctypes/pybind11) from natural language prompts. Use **pylint** (GPL, bundled) for Python, clang for C++ (optional). Simulate lines in **QEMU**/**bubblewrap** (BSD, v0.6.2) for bug prediction.
   - Ask preference with explanations; auto-optimize if none. *Instant File Mode*: Async generation (asyncio) with buffer wheel, EST via \( \text{ETA} = 0.1L + 0.5C \).
   - Output 2-5 suggestions (how-to, UI, angles) based on data size (2 for small, 5 for large), task complexity (+1 for complex), resources (cap at 2 if RAM low). Store in **SQLite** (public domain).
   - Thumbs-up/down feedback adjusts suggestion weights (+1/-1) via interactive sliders, retrains mini-scripts on downvotes, prioritizes APIs (xAI Grok for complex tasks). Feedback persists across projects in project tab; prompt users for context to resolve conflicts. Integrate free AI APIs (xAI Grok, Hugging Face, DeepInfra) for suggestions, weighted by “API Blend” (0-100).
4. **GUI**:
   - **Standard GUI** (Tkinter, built-in): Grok-inspired, with prompt, hardware, code, data panels, auto-shift Markdown/LaTeX tabs (**markdown** v3.4.1, **pylatex** v1.4.1). Ghost council viewport in panel/tab for debates/suggestions, “API Insights” tab for multi-API outputs, “Project Tab” for task management, “Feedback Sliders” tab for weight adjustment, “Feedback History” sub-tab for persisted weights. “GHST” button triggers generation/*Ghost Theory*. Buffer wheel for *Instant File Mode*; pause/resume buttons. Ghost animation (floating, 0.2-0.8 opacity) on desktop tiers. Drag-and-drop files via **tkinterdnd2** (MIT, bundled).
   - **Super Light Mode** (Pi-only): KIAUH-style text window, numbered tabs. Viewport in text format; text-based pause/resume (Y/N), no animation, text-based conflict prompts (e.g., “Cost conflict: 1=Keep 75%, 2=Average, 3=New”).
   - Preferences menu with global (CPU, RAM, storage, Poll Frequency=off/hourly/daily, Language Preference=Python/C++/Mixed/Auto, Mix Level=0-100, API Blend=0-100, Scrub Priority=0-100, Animation Enable=on/off, Drag-Drop Size Limit=1-10MB, Feedback Processing Budget=1-50MB, Feedback Storage Budget=1-100MB) and engine-specific sliders (Randomization, Topic Focus, Angle Variety=2-5, Validation Rigor=0-100, Simulation Depth=0-100, Feedback Weight=0-100, API Priority=0-100, Feedback Persistence=0-100, Conflict Resolution Preference=0-100). Klipper-like save/refresh via `config.json`.
5. **Ghost Pool**:
   - GitHub folder `ghosts/` with .json files (e.g., `code_alchemist.json`). Local `ghost_list.txt` for fetches via `requests.get(URL)`. Poll raw `ghost_list.txt` hourly/daily (optional). Cache in `local_pool/`.
   - Engine-specific “Auto-Fetch Threshold” (0-100), “Learning Rate” (0-100).
6. **Internet Scrubbing**:
   - Ghosts scrub permissive data (GitHub, Stack Overflow CC BY-SA, The Pile) in online mode. Prioritize GitHub for code, Stack Overflow for Q&A, recent data (<1 year). Controlled by “Scrub Priority” (0=GitHub, 100=mixed).
7. **Windows Installer**:
   - Compile with **PyInstaller** (GPL, v5.13.0) into `.exe`. **NSIS** (MIT, v3.09) wizard places files in `C:\Program Files\GHST`, configs in `AppData`. Toggle “Portable Mode,” “API Bundle,” “Animation Enable,” “Feedback Bundle,” “Conflict Bundle.”
8. **Copyright Compliance**:
   - Use Apache 2.0/MIT/BSD components. **ATTRIBUTIONS.md** credits all (xAI, Hugging Face, DeepInfra, The Pile, tkinterdnd2). Bundle deps in `vendor/`. Startup license checker warns: “Use non-copyrighted data/files.”

**Fish Feeder Example**:
- **Prompt**: “Make a fish feeder program for GPIO 18, 8 AM/6 PM.”
- **Language**: Ask preference; auto-mixed (Python main, C++ for timing via ctypes).
- **Output** (3 angles, medium data, *Instant File Mode*):
  - **How-To**: Async-generated Python/C++ script, validated in QEMU.
    ```python
    # feeder.py
    import ctypes, schedule, time
    lib = ctypes.CDLL("./feeder.so")
    def feed_fish(): lib.dispense_food(18); print("Fish fed!")
    schedule.every().day.at("08:00").do(feed_fish)
    while True: schedule.run_pending(); time.sleep(60)
    ```
    ```cpp
    // feeder.cpp
    #include <wiringPi.h>
    extern "C" void dispense_food(int pin) {
        wiringPiSetup(); pinMode(pin, OUTPUT); digitalWrite(pin, HIGH); delay(1000); digitalWrite(pin, LOW);
    }
    ```
  - **UI Menus**: Tkinter GUI with sliders, generated in background.
  - **Angles**: Cost (cheap servo, weight +2 from upvotes), scalability (multi-tank), safety (sensor). API angle: “xAI Grok: Smart servo control.”
- **Viewport**: Standard GUI shows Markdown tab with API insights, project tab for task management, feedback sliders tab for weight adjustment, feedback history sub-tab for persisted weights, conflict prompt pop-up. Super light mode prints text.