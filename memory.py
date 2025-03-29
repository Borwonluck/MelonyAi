import json
import os

MEMORY_FILE = "memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {}

def summarize_memory():
    memory = load_memory()
    summary_lines = []

    if "name" in memory:
        summary_lines.append(f"The user's name is {memory['name']}.")

    if "preferences" in memory:
        for key, value in memory["preferences"].items():
            summary_lines.append(f"The user {value}")

    if "personality" in memory:
        if "tone" in memory["personality"]:
            summary_lines.append(f"You should respond in a {memory['personality']['tone']} tone.")
        if "style" in memory["personality"]:
            summary_lines.append(f"You should speak in a style where you {memory['personality']['style']}")

    if "goals" in memory:
        for goal in memory["goals"]:
            summary_lines.append(f"A key goal is: {goal}")

    return " ".join(summary_lines)
