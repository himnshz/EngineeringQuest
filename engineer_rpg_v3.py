import tkinter as tk
from tkinter import messagebox, simpledialog
import json, os

SAVE_FILE = "save_game.json"

# =====================
# PLAYER
# =====================
player = {
    "intelligence": {"arrays": 0, "recursion": 0},
    "coding_xp": 0,
    "rank": "Trainee",
    "solved": [],
    "unlocked": ["arrays"],
    "accuracy": 1.0
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
# MCQs
# =====================
MCQS = {
    "arrays": [
        ("Which uses contiguous memory?", "Array"),
        ("Index access time of array?", "O(1)")
    ],
    "recursion": [
        ("Recursion stops using?", "Base case"),
        ("Recursion uses which stack?", "Call stack")
    ]
}

# =====================
# PRACTICE PROBLEMS
# =====================
PROBLEMS = {
    "arrays": [
        {
            "id": "A1",
            "title": "Sum of Array",
            "difficulty": "easy",
            "desc": "Return sum of elements",
            "code": "def solve(arr):\n    pass",
            "tests": [([1,2,3],6), ([5,5],10)],
            "base_xp": 50
        },
        {
            "id": "A2",
            "title": "Max Element",
            "difficulty": "medium",
            "desc": "Return max element",
            "code": "def solve(arr):\n    pass",
            "tests": [([1,9,3],9), ([5,2],5)],
            "base_xp": 70
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
            "base_xp": 80
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
            return 0.0
        passed = 0
        for i, o in tests:
            if env["solve"](i) == o:
                passed += 1
        return passed / len(tests)
    except:
        return 0.0

# =====================
# UI ACTIONS
# =====================
current_zone = "arrays"
current_problem = None

def do_mcq():
    q, a = MCQS[current_zone][player["intelligence"][current_zone] % len(MCQS[current_zone])]
    ans = simpledialog.askstring("MCQ", q)
    if ans and ans.lower() == a.lower():
        player["intelligence"][current_zone] += 10
        if current_zone == "arrays" and player["intelligence"]["arrays"] >= 20:
            if "recursion" not in player["unlocked"]:
                player["unlocked"].append("recursion")
        messagebox.showinfo("Correct", "🧠 Intelligence +10")
        save()
    else:
        messagebox.showerror("Wrong", "Incorrect")
    update_ui()

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
    problem_label.config(text="All battles cleared here 🎉")

def submit():
    if not current_problem:
        return

    code = code_box.get("1.0", tk.END)
    accuracy = run_code(code, current_problem["tests"])

    if accuracy < 0.5:
        messagebox.showerror("Failed", "❌ Too many test cases failed")
        return

    xp = int(
        current_problem["base_xp"]
        * DIFF_MULTI[current_problem["difficulty"]]
        * accuracy
    )

    player["coding_xp"] += xp
    player["accuracy"] = (player["accuracy"] + accuracy) / 2
    player["solved"].append(current_problem["id"])
    update_rank()
    save()

    messagebox.showinfo(
        "Battle Result",
        f"Accuracy: {int(accuracy*100)}%\n⚔️ XP +{xp}"
    )

    load_problem()
    update_ui()

def switch_zone():
    global current_zone
    z = simpledialog.askstring("Zone", f"Choose zone: {', '.join(player['unlocked'])}")
    if z in player["unlocked"]:
        current_zone = z
        load_problem()
        update_ui()

def update_ui():
    stats.config(
        text=f"Zone: {current_zone.upper()} | "
             f"🧠 Int: {player['intelligence'][current_zone]} | "
             f"⚔️ XP: {player['coding_xp']} | "
             f"🎯 Acc: {int(player['accuracy']*100)}% | "
             f"🏆 {player['rank']}"
    )

# =====================
# UI
# =====================
load()

root = tk.Tk()
root.title("Engineer RPG v3")
root.geometry("760x560")

stats = tk.Label(root, font=("Arial", 12))
stats.pack(pady=5)

tk.Button(root, text="🧠 MCQ", command=do_mcq).pack()
tk.Button(root, text="🗺️ Switch Zone", command=switch_zone).pack(pady=3)
tk.Button(root, text="⚔️ Load Battle", command=load_problem).pack()

problem_label = tk.Label(root, text="Load a battle", font=("Arial", 11))
problem_label.pack(pady=8)

code_box = tk.Text(root, width=90, height=14)
code_box.pack()

tk.Button(root, text="Submit Code", command=submit).pack(pady=10)

update_ui()
root.mainloop()
