# GHST Council Roster Terminal Display
# Run this script to see the council with big emojis and styled names in your terminal

council = [
    ("Dr. Ethos", "👻"),
    ("Prof. Pluginator", "👻"),
    ("Ghostly UI", "👻"),
    ("Data Wisp", "👻"),
    ("ThinkTank Specter", "👻"),
    ("Phantom Debugger", "👻"),
    ("Orchestrator Shade", "👻"),
    ("Slicer Sage", "👻"),
    ("Feedback Phantom", "👻"),
    ("Pi Whisperer", "👻"),
    ("Home Assistant Haunt", "👻"),
    ("Recency Revenant", "👻"),
    ("Complexity Spirit", "👻"),
    ("Emoji Oracle", "👻"),
    ("Council Keeper", "👻"),
]

# Box drawing characters for style
border = "═" * 40
print(f"\n╔{border}╗")
print("║{:^40}║".format("GHST COUNCIL ROSTER"))
print(f"╠{border}╣")
for name, emoji in council:
    # Print emoji large and name centered
    print(f"║  {emoji}  {name:<30}║")
print(f"╚{border}╝\n")

# Optionally, print each emoji on its own line for extra size
print("\nBig Emojis:")
for name, emoji in council:
    print(f"{emoji}  {name}")
