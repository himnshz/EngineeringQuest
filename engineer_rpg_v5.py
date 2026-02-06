import tkinter as tk
from tkinter import messagebox, simpledialog
import json, os

SAVE_FILE = "save_game.json"

# =====================
# KNOWLEDGE BASE (RAG CORE)
# =====================
KB = {
    "arrays_second_largest": (
        "To find the second largest element:\n"
        "- Track largest and second largest separately\n"
        "- Handle duplicates carefully\n"
        "- Do NOT sort unless allowed\n"
        "- Edge case: array length < 2"
    ),
    "recursion_base_case": (
        "Every recursive function must:\n"
        "- Have a base case\n"
        "- Reduce the problem size\n"
        "- Return the recursive result properly"
    ),
    "general_logic": (
        "Check:\n"
        "- Function returns value\n"
        "- Correct variable updates\n"
        "- All test cases handled"
    )
}

# =====================
# PLAYER
# =====================
player = {
    "intelligence": {"arrays": 0, "recursion": 0},
    "coding_xp": 0,
    "rank": "Trainee",
    "solved": [],
    "unlocked": ["arrays"],
    "accuracy": 1.0,
    "mastery": {"arrays": 0, "recursion": 0}
}

# =====================
# DIFFICULTY MULTIPLIER
# =====================
DIFF_MULTI = {
    "easy": 1.0,
    "medium": 2.0,
    "hard": 3.5,
    "boss": 5.0
}

# =====================
# PROBLEMS
# =====================
PROBLEMS = {
    "arrays": [
        {
            "id": "A_BOSS",
            "title": "Array Boss: Second Largest",
            "difficulty": "boss",
            "desc": "Return second largest element",
            "code": "def solve(arr):\n    pass",
            "tests": [
                ([1,2,3,4],3),
                ([9,9,8],8),
                ([5,1],1)
            ],
            "base_xp": 120,
            "kb_key": "arrays_second_largest"
        },
        {
            "id": "A2",
            "title": "Reverse Array",
            "difficulty": "easy",
            "desc": "Return the reversed array",
            "code": "def solve(arr):\n    pass",
            "tests": [
                ([1,2,3], [3,2,1]),
                ([5,1], [1,5])
            ],
            "base_xp": 50,
            "kb_key": "general_logic"
        },
        {
            "id": "A3",
            "title": "Find Minimum",
            "difficulty": "easy",
            "desc": "Return minimum element",
            "code": "def solve(arr):\n    pass",
            "tests": [
                ([3,1,2], 1),
                ([9,5], 5)
            ],
            "base_xp": 50,
            "kb_key": "general_logic"
        }

    ],
    "recursion": [
        {
            "id": "R1",
            "title": "Factorial",
            "difficulty": "easy",
            "desc": "Return factorial",
            "code": "def solve(n):\n    pass",
            "tests": [(5,120), (3,6)],
            "base_xp": 80,
            "kb_key": "recursion_base_case"
        }
    ]
}

# =====================
# SAVE / LOAD
# =====================
def save():
    with open(SAVE_FILE, "w") as f:
        json.dump(player, f)

def load():
    global player
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE) as f:
            player = json.load(f)
    # FIX FOR OLD SAVE FILES
    if "mastery" not in player:
        player["mastery"] = {"arrays": 0, "recursion": 0}

    if "accuracy" not in player:
        player["accuracy"] = 1.0

    if "solved" not in player:
        player["solved"] = []

    if "unlocked" not in player:
        player["unlocked"] = ["arrays"]

# =====================
# CORE LOGIC
# =====================
def update_rank():
    xp = player["coding_xp"]
    if xp < 300:
        player["rank"] = "Trainee"
    elif xp < 800:
        player["rank"] = "Coder"
    elif xp < 1500:
        player["rank"] = "DSA Fighter"
    else:
        player["rank"] = "Algorithm Knight"

def run_code(code, tests):
    env = {}
    try:
        exec(code, {}, env)
        if "solve" not in env:
            return 0.0, "Function solve() missing"

        passed = 0
        for i, o in tests:
            try:
                if env["solve"](i) == o:
                    passed += 1
            except:
                pass

        acc = passed / len(tests)
        return acc, None
    except Exception as e:
        return 0.0, str(e)

# =====================
# RAG EXPLANATION ENGINE
# =====================
def explain_failure(problem, accuracy, error):
    if error:
        return f"Runtime Error Detected:\n{error}\n\n{KB['general_logic']}"

    if accuracy == 0:
        return KB.get(problem["kb_key"], KB["general_logic"])

    return (
        "Partial correctness detected.\n"
        "Likely missing edge cases.\n\n"
        + KB.get(problem["kb_key"], KB["general_logic"])
    )

# =====================
# UI ACTIONS
# =====================
current_zone = "arrays"
current_problem = None

def load_problem():
    global current_problem
    for p in PROBLEMS[current_zone]:
        if p["id"] not in player["solved"]:
            current_problem = p
            code_box.delete("1.0", tk.END)
            code_box.insert(tk.END, p["code"])
            problem_label.config(
                text=f"{p['title']} ({p['difficulty'].upper()})\n{p['desc']}"
            )
            return
    problem_label.config(text="Zone Cleared 🎉")

def submit():
    if not current_problem:
        return

    code = code_box.get("1.0", tk.END)
    accuracy, error = run_code(code, current_problem["tests"])

    if accuracy < 0.5:
        explanation = explain_failure(current_problem, accuracy, error)
        messagebox.showerror("Failed", explanation)
        return

    xp = int(
        current_problem["base_xp"]
        * DIFF_MULTI[current_problem["difficulty"]]
        * accuracy
    )

    player["coding_xp"] += xp
    player["accuracy"] = (player["accuracy"] + accuracy) / 2
    player["solved"].append(current_problem["id"])
    player["mastery"][current_zone] = min(
        100, player["mastery"][current_zone] + int(accuracy * 25)
    )

    update_rank()
    save()

    messagebox.showinfo(
        "Victory",
        f"Accuracy: {int(accuracy*100)}%\n⚔️ XP +{xp}"
    )

    load_problem()
    update_ui()

def update_ui():
    stats.config(
        text=f"Zone: {current_zone.upper()} | "
             f"⚔️ XP: {player['coding_xp']} | "
             f"📊 Mastery: {player['mastery'][current_zone]}% | "
             f"🏆 {player['rank']}"
    )

# =====================
# UI
# =====================
load()

root = tk.Tk()
root.title("Engineer RPG v5 – RAG Tutor")
root.geometry("880x620")

stats = tk.Label(root, font=("Arial", 12))
stats.pack(pady=5)

tk.Button(root, text="⚔️ Load Battle", command=load_problem).pack(pady=5)

problem_label = tk.Label(root, text="Load a battle", font=("Arial", 11))
problem_label.pack(pady=8)

code_box = tk.Text(root, width=100, height=16)
code_box.pack()

tk.Button(root, text="Submit Code", command=submit).pack(pady=10)

update_ui()
root.mainloop()
