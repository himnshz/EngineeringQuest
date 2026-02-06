import tkinter as tk
from tkinter import messagebox, simpledialog

# =====================
# PLAYER DATA
# =====================
player = {
    "intelligence": 0,
    "coding_power": 0,
    "rank": "Trainee",
    "solved": set()
}

# =====================
# MCQs (INTELLIGENCE)
# =====================
MCQS = [
    {
        "q": "Which data structure uses contiguous memory?",
        "options": ["Linked List", "Array", "Tree", "Graph"],
        "ans": "Array"
    },
    {
        "q": "Time complexity of binary search?",
        "options": ["O(n)", "O(log n)", "O(n log n)", "O(1)"],
        "ans": "O(log n)"
    }
]

# =====================
# CODING PROBLEMS (PRACTICE)
# =====================
PROBLEMS = [
    {
        "id": "p1",
        "title": "Sum of Array",
        "desc": "Return sum of array elements",
        "starter": "def solve(arr):\n    pass",
        "tests": [
            ([1,2,3], 6),
            ([5,5], 10)
        ],
        "xp": 50
    },
    {
        "id": "p2",
        "title": "Factorial",
        "desc": "Return factorial of n",
        "starter": "def solve(n):\n    pass",
        "tests": [
            (5, 120),
            (3, 6)
        ],
        "xp": 80
    }
]

current_problem = None

# =====================
# CORE LOGIC
# =====================
def update_rank():
    xp = player["coding_power"]
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
            return False, "Function solve() missing"

        solve = env["solve"]
        passed = 0

        for inp, out in tests:
            if solve(inp) == out:
                passed += 1

        acc = passed / len(tests)
        return True, acc
    except Exception as e:
        return False, str(e)

# =====================
# UI ACTIONS
# =====================
def show_mcq():
    q = MCQS[player["intelligence"] % len(MCQS)]
    ans = simpledialog.askstring(
        "MCQ",
        f"{q['q']}\nOptions: {', '.join(q['options'])}"
    )
    if ans and ans.strip() == q["ans"]:
        player["intelligence"] += 10
        messagebox.showinfo("Correct", "🧠 Intelligence +10")
    else:
        messagebox.showerror("Wrong", "Incorrect answer")
    update_ui()

def load_problem():
    global current_problem
    idx = player["coding_power"] // 100
    idx = min(idx, len(PROBLEMS)-1)
    current_problem = PROBLEMS[idx]
    code_box.delete("1.0", tk.END)
    code_box.insert(tk.END, current_problem["starter"])
    problem_label.config(
        text=f"⚔️ {current_problem['title']}\n{current_problem['desc']}"
    )

def submit_code():
    if not current_problem:
        return

    if current_problem["id"] in player["solved"]:
        messagebox.showinfo("Done", "Already solved")
        return

    code = code_box.get("1.0", tk.END)
    ok, res = run_code(code, current_problem["tests"])

    if ok is not True:
        messagebox.showerror("Error", res)
        return

    if res < 1.0:
        messagebox.showwarning("Partial", "Not all test cases passed")
        return

    player["coding_power"] += current_problem["xp"]
    player["solved"].add(current_problem["id"])
    update_rank()
    messagebox.showinfo("Victory", f"⚔️ XP +{current_problem['xp']}")
    update_ui()
    load_problem()

def update_ui():
    stats.config(
        text=f"🧠 Intelligence: {player['intelligence']}   "
             f"⚔️ XP: {player['coding_power']}   "
             f"🏆 Rank: {player['rank']}"
    )

# =====================
# UI SETUP
# =====================
root = tk.Tk()
root.title("Engineer RPG")
root.geometry("700x500")

stats = tk.Label(root, font=("Arial", 12))
stats.pack(pady=5)

btn_frame = tk.Frame(root)
btn_frame.pack()

tk.Button(btn_frame, text="🧠 MCQ (Intelligence)", command=show_mcq).pack(side="left", padx=5)
tk.Button(btn_frame, text="⚔️ Load Battle", command=load_problem).pack(side="left", padx=5)

problem_label = tk.Label(root, text="⚔️ Load a problem", font=("Arial", 11))
problem_label.pack(pady=10)

code_box = tk.Text(root, height=12, width=80)
code_box.pack()

tk.Button(root, text="Submit Code", command=submit_code).pack(pady=10)

update_ui()
root.mainloop()
