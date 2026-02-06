import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

SAVE_FILE = "save_game.json"

# =====================
# PLAYER
# =====================
player = {
    "intelligence": {"arrays": 0, "recursion": 0},
    "coding_xp": 0,
    "rank": "Trainee",
    "solved": [],
    "unlocked": ["arrays"]
}

# =====================
# MCQs (INTELLIGENCE)
# =====================
MCQS = {
    "arrays": [
        ("Which uses contiguous memory?", "Array"),
        ("Index access time of array?", "O(1)")
    ],
    "recursion": [
        ("Base case is needed to?", "Stop recursion"),
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
            "desc": "Return sum of elements",
            "code": "def solve(arr):\n    pass",
            "tests": [([1,2,3],6), ([5,5],10)],
            "xp": 50
        }
    ],
    "recursion": [
        {
            "id": "R1",
            "title": "Factorial",
            "desc": "Return factorial of n",
            "code": "def solve(n):\n    pass",
            "tests": [(5,120), (3,6)],
            "xp": 80
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
    if xp < 200:
        player["rank"] = "Trainee"
    elif xp < 500:
        player["rank"] = "Coder"
    elif xp < 1000:
        player["rank"] = "DSA Fighter"
    else:
        player["rank"] = "Algorithm Knight"

def run_code(code, tests):
    env = {}
    try:
        exec(code, {}, env)
        if "solve" not in env:
            return False
        for i,o in tests:
            if env["solve"](i) != o:
                return False
        return True
    except:
        return False

# =====================
# UI ACTIONS
# =====================
current_zone = "arrays"
current_problem = None

def do_mcq():
    q,a = MCQS[current_zone][player["intelligence"][current_zone] % len(MCQS[current_zone])]
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
            problem_label.config(text=f"{p['title']}: {p['desc']}")
            return
    problem_label.config(text="All problems cleared here 🎉")

def submit():
    if not current_problem:
        return
    code = code_box.get("1.0", tk.END)
    if run_code(code, current_problem["tests"]):
        player["coding_xp"] += current_problem["xp"]
        player["solved"].append(current_problem["id"])
        update_rank()
        save()
        messagebox.showinfo("Victory", f"⚔️ XP +{current_problem['xp']}")
        load_problem()
    else:
        messagebox.showerror("Failed", "Wrong output")

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
             f"🏆 {player['rank']}"
    )

# =====================
# UI
# =====================
load()

root = tk.Tk()
root.title("Engineer RPG")
root.geometry("720x520")

stats = tk.Label(root, font=("Arial", 12))
stats.pack(pady=5)

tk.Button(root, text="🧠 MCQ", command=do_mcq).pack()
tk.Button(root, text="🗺️ Switch Zone", command=switch_zone).pack(pady=3)
tk.Button(root, text="⚔️ Load Battle", command=load_problem).pack()

problem_label = tk.Label(root, text="Load a problem", font=("Arial", 11))
problem_label.pack(pady=8)

code_box = tk.Text(root, width=85, height=12)
code_box.pack()

tk.Button(root, text="Submit Code", command=submit).pack(pady=10)

update_ui()
root.mainloop()
