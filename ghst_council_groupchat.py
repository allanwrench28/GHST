# GHST Council Group Chat - iOS Style Terminal Bubbles
# Requires: pip install colorama

from colorama import init, Fore, Back, Style
init(autoreset=True)

council = [
    ("Dr. Ethos", "👻", "Consider the ethical implications of your next move."),
    ("Prof. Pluginator", "👻", "Try integrating a new plugin for flexibility."),
    ("Ghostly UI", "👻", "Refine the user interface for clarity."),
    ("Data Wisp", "👻", "Audit your data management routines."),
    ("ThinkTank Specter", "👻", "Brainstorm with the council for new ideas."),
    ("Phantom Debugger", "👻", "Run automated tests and fix errors."),
    ("Orchestrator Shade", "👻", "Automate repetitive tasks for efficiency."),
    ("Slicer Sage", "👻", "Optimize gcode workflows for hardware compatibility."),
    ("Feedback Phantom", "👻", "Solicit user feedback for improvements."),
    ("Pi Whisperer", "👻", "Test deployment on a Raspberry Pi."),
    ("Home Assistant Haunt", "👻", "Prototype a Home Assistant plugin."),
    ("Recency Revenant", "👻", "Review recent changes and update docs."),
    ("Complexity Spirit", "👻", "Refactor for maintainability."),
    ("Emoji Oracle", "👻", "Assign new emojis to emerging personas."),
    ("Council Keeper", "👻", "Update the council roster.")
]

bubble_colors = [Back.LIGHTBLUE_EX, Back.LIGHTGREEN_EX]

print("\nGHST Council Group Chat (iOS Style):\n")
for i, (name, emoji, msg) in enumerate(council):
    color = bubble_colors[i % 2]
    left_pad = " " * (0 if i % 2 == 0 else 10)
    bubble = f"{color}{Fore.BLACK}  {emoji} {name}: {msg}  {Style.RESET_ALL}"
    print(f"{left_pad}{bubble}\n")
