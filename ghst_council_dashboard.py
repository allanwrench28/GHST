from nicegui import ui

import random

# --- Battle Counter ---
battle_count = 0
fun_emojis = ['🎉', '😎', '🤩', '🥳', '🦄', '✨', '🍕', '🚀', '🎨', '🧠']

def increment_battle():
    global battle_count
    battle_count += 1
    chosen_emoji = random.choice(fun_emojis)
    battle_counter.text = f'Battle Counter: {battle_count} {chosen_emoji}'
    add_log(f'Dr. Fun {chosen_emoji}: "Let’s make this restructuring a party!"')

with ui.row().classes('w-full items-center'):
    battle_counter = ui.label(f'Battle Counter: {battle_count}').style('font-size: 1.1rem; color: #FF3B30; margin-top: 20px; margin-right: 20px;')
    ui.button('Syntax Supervisor Action', on_click=increment_battle).style('background: #007AFF; color: #fff; border-radius: 8px; margin-top: 20px;')
from datetime import datetime
import threading
import time

# --- GHST Council Data ---
GHSTS = [
    {'name': 'Dr. TidyCode', 'emoji': '🧭', 'field': 'Refactoring', 'color': '#007AFF'},
    {'name': 'Dr. Syntax', 'emoji': '🕯️', 'field': 'Syntax', 'color': '#34C759'},
    {'name': 'Dr. ImportOrder', 'emoji': '🦴', 'field': 'Imports', 'color': '#FF9500'},
    {'name': 'Dr. Formatter', 'emoji': '🪄', 'field': 'Formatting', 'color': '#AF52DE'},
    {'name': 'Dr. Archivist', 'emoji': '🧪', 'field': 'Archiving', 'color': '#FF2D55'},
    {'name': 'Dr. Debugger', 'emoji': '🐛', 'field': 'Debugging', 'color': '#5856D6'},
    {'name': 'Dr. Data', 'emoji': '📊', 'field': 'Data Science', 'color': '#FFCC00'},
    {'name': 'Dr. Architect', 'emoji': '🏗️', 'field': 'Architecture', 'color': '#5AC8FA'},
    {'name': 'Dr. Security', 'emoji': '🔒', 'field': 'Security', 'color': '#FF3B30'},
    {'name': 'Dr. Test', 'emoji': '🧪', 'field': 'Testing', 'color': '#30B0C7'},
]

problem_solver_logs = []
problem_solver_active = True
internet_access = True

def add_log(message):
    timestamp = datetime.now().strftime('%H:%M:%S')
    problem_solver_logs.append(f'[{timestamp}] {message}')

# --- Problem Solver Daemon ---
def problem_solver_daemon():
    topics = [
        'Refactoring core logic', 'Optimizing imports', 'Running style checks',
        'Debugging edge cases', 'Improving data pipeline', 'Securing API endpoints',
        'Testing new features', 'Building UI components', 'Automating deployment',
    ]
    while problem_solver_active:
        ghst = GHSTS[int(time.time()) % len(GHSTS)]
        topic = topics[int(time.time() * 1.3) % len(topics)]
        add_log(f'{ghst["emoji"]} {ghst["name"]} is {topic}...')
        time.sleep(3)

daemon_thread = threading.Thread(target=problem_solver_daemon, daemon=True)
daemon_thread.start()

# --- UI ---
ui.colors(primary='#007AFF', secondary='#F2F2F7', accent='#34C759', positive='#34C759', negative='#FF3B30', background='#F2F2F7', text='#1C1C1E')
ui.query('body').style('background: #F2F2F7;')

with ui.header().classes('items-center justify-between'):
    ui.label('GHST Council').style('font-size: 2rem; font-weight: 600; color: #1C1C1E;')
    ui.switch('Internet Access', value=internet_access, on_change=lambda e: set_internet_access(e.value)).style('margin-left: 2rem;')

def set_internet_access(value):
    global internet_access
    internet_access = value
    add_log(f'Internet access toggled to {"ON" if value else "OFF"}')

with ui.row().classes('w-full items-start'):
    with ui.card().style('background: #fff; border-radius: 20px; box-shadow: 0 2px 8px #0001; width: 40%; min-width: 350px; padding: 24px;'):
        ui.label('Council Chat').style('font-size: 1.3rem; font-weight: 500; color: #007AFF; margin-bottom: 12px;')
        chat_column = ui.column().classes('w-full')
        council_messages = [
            f'{g["emoji"]} <b>{g["name"]}</b>: "{g["field"]} is my specialty!"' for g in GHSTS
        ]
        def update_chat():
            chat_column.clear()
            for msg in council_messages[-10:]:
                ui.html(f'<div style="color:#1C1C1E;font-size:1.1rem;margin-bottom:8px;">{msg}</div>')
        update_chat()
    with ui.card().style('background: #fff; border-radius: 20px; box-shadow: 0 2px 8px #0001; width: 55%; min-width: 350px; padding: 24px;'):
        ui.label('Problem Solver Logs').style('font-size: 1.3rem; font-weight: 500; color: #007AFF; margin-bottom: 12px;')
        log_box = ui.textarea(label='', value='').classes('w-full').style('height: 300px; background: #F2F2F7; color: #1C1C1E; border-radius: 12px;')
        def update_logs():
            while True:
                log_box.value = '\n'.join(problem_solver_logs[-30:])
                time.sleep(2)
        threading.Thread(target=update_logs, daemon=True).start()

with ui.row().classes('w-full items-center'):
    time_estimator = ui.label('Estimated Time for Current Task: Calculating...').style('font-size: 1.1rem; color: #007AFF; margin-top: 20px;')
    progress_bar = ui.linear_progress(0).classes('w-full').style('height: 16px; margin-top: 10px;')

def update_time_estimator():
    tasks = [
        ('Refactoring', 5),
        ('Style Checks', 3),
        ('Import Optimization', 2),
        ('Testing', 4),
        ('Deployment', 6)
    ]
    while True:
        task, est_time = tasks[int(time.time()) % len(tasks)]
        time_estimator.text = f'Estimated Time for {task}: {est_time} minutes'
        progress_bar.value = (time.time() % 60) / 60 * 100
        time.sleep(5)
threading.Thread(target=update_time_estimator, daemon=True).start()

with ui.expansion('🏆 GHST Hall of Fame').classes('w-full'):
    ui.label('Celebrating Innovations and Excellence').style('font-size: 1.2rem; color: #007AFF; margin-bottom: 10px;')
    with ui.grid(columns=2):
        for g in GHSTS:
            with ui.card().style('background: #F2F2F7; border-radius: 16px; padding: 14px; margin: 5px; box-shadow: 0 1px 4px #0001;'):
                ui.label(f'{g["emoji"]} {g["name"]}').style(f'font-size: 1.1rem; color: {g["color"]}; font-weight: 500;')
                ui.label(f'Field: {g["field"]}').style('color: #1C1C1E;')
                ui.label('Innovation: Excellence in automation and collaboration.').style('color: #1C1C1E;')
                ui.label('"Inspiration for all future coders."').style('font-style: italic; color: #888;')

ui.run()
