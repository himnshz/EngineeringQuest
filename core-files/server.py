"""
EngineerQuest RPG - Backend API Server
Flask-based REST API for the coding RPG game
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import os
import copy

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

SAVE_FILE = "player_data.json"

# =====================
# KNOWLEDGE BASE (RAG CORE)
# =====================
KB = {
    "arrays_second_largest": (
        "To find the second largest element:\n"
        "• Track largest and second largest separately\n"
        "• Handle duplicates carefully\n"
        "• Do NOT sort unless allowed\n"
        "• Edge case: array length < 2"
    ),
    "recursion_base_case": (
        "Every recursive function must:\n"
        "• Have a base case\n"
        "• Reduce the problem size\n"
        "• Return the recursive result properly"
    ),
    "dp_overlapping": (
        "Dynamic Programming requires:\n"
        "• Overlapping subproblems\n"
        "• Optimal substructure\n"
        "• Memoization or tabulation"
    ),
    "general_logic": (
        "Check:\n"
        "• Function returns a value\n"
        "• Correct variable updates\n"
        "• All test cases handled"
    )
}

# =====================
# MCQ PROBLEMS DATABASE
# =====================
MCQS = {
    "training_camp": [
        {
            "id": "MCQ_TC_1",
            "title": "Python Basic Type",
            "category": "MCQ",
            "difficulty": "easy",
            "question": "What is the type of the result of '3 / 2' in Python 3?",
            "options": ["int", "float", "decimal", "error"],
            "answer": 1,  # Index of correct answer (0-based): "float"
            "intelligence_xp": 10
        },
        {
            "id": "MCQ_TC_2",
            "title": "List Indexing",
            "category": "MCQ",
            "difficulty": "easy",
            "question": "What does arr[-1] return for arr = [1, 2, 3]?",
            "options": ["1", "3", "Error", "None"],
            "answer": 1,  # "3"
            "intelligence_xp": 10
        },
        {
            "id": "MCQ_TC_3",
            "title": "OS Paging",
            "category": "MCQ",
            "difficulty": "easy",
            "question": "Which memory management technique divides memory into fixed-size blocks?",
            "options": ["Segmentation", "Paging", "Swapping", "Compaction"],
            "answer": 1,  # "Paging"
            "intelligence_xp": 10
        },
        {
            "id": "MCQ_TC_4",
            "title": "Thread vs Process",
            "category": "MCQ",
            "difficulty": "medium",
            "question": "Which of the following is shared between threads of the same process?",
            "options": ["Stack", "Registers", "Heap memory", "Program counter"],
            "answer": 2,  # "Heap memory"
            "intelligence_xp": 15
        },
        {
            "id": "MCQ_TC_5",
            "title": "Big O Notation",
            "category": "MCQ",
            "difficulty": "easy",
            "question": "What is the time complexity of accessing an element in an array by index?",
            "options": ["O(1)", "O(n)", "O(log n)", "O(n²)"],
            "answer": 0,  # "O(1)"
            "intelligence_xp": 10
        },
        {
            "id": "MCQ_TC_6",
            "title": "Binary Search Requirement",
            "category": "MCQ",
            "difficulty": "easy",
            "question": "What is required for binary search to work?",
            "options": ["Linked list", "Sorted array", "Hash table", "Queue"],
            "answer": 1,  # "Sorted array"
            "intelligence_xp": 10
        },
        {
            "id": "MCQ_TC_7",
            "title": "Stack Data Structure",
            "category": "MCQ",
            "difficulty": "easy",
            "question": "Which principle does a Stack follow?",
            "options": ["FIFO", "LIFO", "Random", "Priority"],
            "answer": 1,  # "LIFO"
            "intelligence_xp": 10
        }
    ],
    "array_forest": [
        {
            "id": "MCQ_AF_1",
            "title": "Array Memory",
            "category": "MCQ",
            "difficulty": "medium",
            "question": "Which data structure uses contiguous memory allocation?",
            "options": ["Linked List", "Array", "Tree", "Graph"],
            "answer": 1,  # "Array"
            "intelligence_xp": 15
        },
        {
            "id": "MCQ_AF_2",
            "title": "Array Insertion",
            "category": "MCQ",
            "difficulty": "medium",
            "question": "What is the worst-case time complexity of inserting at the beginning of an array?",
            "options": ["O(1)", "O(n)", "O(log n)", "O(n²)"],
            "answer": 1,  # "O(n)"
            "intelligence_xp": 15
        },
        {
            "id": "MCQ_AF_3",
            "title": "Two Pointer Technique",
            "category": "MCQ",
            "difficulty": "medium",
            "question": "Two pointer technique is commonly used for?",
            "options": ["Sorting", "Finding pairs in sorted array", "Tree traversal", "Graph BFS"],
            "answer": 1,
            "intelligence_xp": 15
        }
    ],
    "recursion_cave": [
        {
            "id": "MCQ_RC_1",
            "title": "Recursion Base Case",
            "category": "MCQ",
            "difficulty": "medium",
            "question": "What happens if a recursive function has no base case?",
            "options": ["Returns 0", "Stack overflow", "Returns None", "Runs once"],
            "answer": 1,  # "Stack overflow"
            "intelligence_xp": 15
        },
        {
            "id": "MCQ_RC_2",
            "title": "Tail Recursion",
            "category": "MCQ",
            "difficulty": "hard",
            "question": "What is tail recursion?",
            "options": [
                "Recursion at the start",
                "Recursive call is the last operation",
                "Two recursive calls",
                "No base case"
            ],
            "answer": 1,
            "intelligence_xp": 20
        }
    ],
    "dp_castle": [
        {
            "id": "MCQ_DP_1",
            "title": "DP Prerequisites",
            "category": "MCQ",
            "difficulty": "hard",
            "question": "Which property is NOT required for Dynamic Programming?",
            "options": [
                "Overlapping subproblems",
                "Optimal substructure",
                "Greedy choice property",
                "Memoization"
            ],
            "answer": 2,  # "Greedy choice property"
            "intelligence_xp": 20
        },
        {
            "id": "MCQ_DP_2",
            "title": "Fibonacci DP",
            "category": "MCQ",
            "difficulty": "medium",
            "question": "What is the time complexity of Fibonacci using memoization?",
            "options": ["O(2^n)", "O(n)", "O(n²)", "O(log n)"],
            "answer": 1,  # "O(n)"
            "intelligence_xp": 15
        }
    ]
}

# =====================
# CODE PROBLEMS DATABASE
# =====================
PROBLEMS = {
    "training_camp": [
        {
            "id": "TC_C1",
            "title": "Hello World",
            "difficulty": "easy",
            "type": "code",
            "desc": "Return the string 'Hello World'",
            "code": "def solve():\n    # Return 'Hello World'\n    pass",
            "tests": [
                {"input": None, "expected": "Hello World"}
            ],
            "base_xp": 20,
            "kb_key": "general_logic"
        },
        {
            "id": "TC_C2",
            "title": "Add Two Numbers",
            "difficulty": "easy",
            "type": "code",
            "desc": "Return the sum of two numbers. Input: [a, b]",
            "code": "def solve(data):\n    a, b = data\n    # Return a + b\n    pass",
            "tests": [
                {"input": [1, 2], "expected": 3},
                {"input": [10, 20], "expected": 30}
            ],
            "base_xp": 30,
            "kb_key": "general_logic"
        },
        {
            "id": "TC_C3",
            "title": "Even or Odd",
            "difficulty": "easy",
            "type": "code",
            "desc": "Return 'Even' if n is even, 'Odd' if n is odd",
            "code": "def solve(n):\n    # Return 'Even' or 'Odd'\n    pass",
            "tests": [
                {"input": 4, "expected": "Even"},
                {"input": 7, "expected": "Odd"},
                {"input": 0, "expected": "Even"}
            ],
            "base_xp": 25,
            "kb_key": "general_logic"
        },
        {
            "id": "TC_C4",
            "title": "Multiply Numbers",
            "difficulty": "easy",
            "type": "code",
            "desc": "Return the product of two numbers. Input: [a, b]",
            "code": "def solve(data):\n    a, b = data\n    # Return a * b\n    pass",
            "tests": [
                {"input": [3, 4], "expected": 12},
                {"input": [5, 0], "expected": 0},
                {"input": [7, 7], "expected": 49}
            ],
            "base_xp": 25,
            "kb_key": "general_logic"
        },
        {
            "id": "TC_C5",
            "title": "Square a Number",
            "difficulty": "easy",
            "type": "code",
            "desc": "Return the square of n (n * n)",
            "code": "def solve(n):\n    # Return n squared\n    pass",
            "tests": [
                {"input": 5, "expected": 25},
                {"input": 3, "expected": 9},
                {"input": 0, "expected": 0}
            ],
            "base_xp": 20,
            "kb_key": "general_logic"
        },
        {
            "id": "TC_C6",
            "title": "Absolute Value",
            "difficulty": "easy",
            "type": "code",
            "desc": "Return the absolute value of n (without using abs())",
            "code": "def solve(n):\n    # Return absolute value\n    pass",
            "tests": [
                {"input": -5, "expected": 5},
                {"input": 10, "expected": 10},
                {"input": 0, "expected": 0}
            ],
            "base_xp": 30,
            "kb_key": "general_logic"
        },
        {
            "id": "TC_C7",
            "title": "Max of Two",
            "difficulty": "easy",
            "type": "code",
            "desc": "Return the larger of two numbers. Input: [a, b]",
            "code": "def solve(data):\n    a, b = data\n    # Return the larger number\n    pass",
            "tests": [
                {"input": [5, 3], "expected": 5},
                {"input": [2, 8], "expected": 8},
                {"input": [4, 4], "expected": 4}
            ],
            "base_xp": 25,
            "kb_key": "general_logic"
        }
    ],
    "array_forest": [
        {
            "id": "AF_C1",
            "title": "Sum of Array",
            "difficulty": "easy",
            "type": "code",
            "desc": "Return the sum of all elements in the array",
            "code": "def solve(arr):\n    # Your code here\n    pass",
            "tests": [
                {"input": [1, 2, 3], "expected": 6},
                {"input": [10, 20], "expected": 30},
                {"input": [5], "expected": 5}
            ],
            "base_xp": 40,
            "kb_key": "general_logic"
        },
        {
            "id": "AF_C2",
            "title": "Reverse Array",
            "difficulty": "easy",
            "type": "code",
            "desc": "Return the reversed array",
            "code": "def solve(arr):\n    # Your code here\n    pass",
            "tests": [
                {"input": [1, 2, 3], "expected": [3, 2, 1]},
                {"input": [5, 1], "expected": [1, 5]}
            ],
            "base_xp": 50,
            "kb_key": "general_logic"
        },
        {
            "id": "AF_C3",
            "title": "Find Maximum",
            "difficulty": "easy",
            "type": "code",
            "desc": "Return the maximum element in the array",
            "code": "def solve(arr):\n    # Your code here\n    pass",
            "tests": [
                {"input": [3, 1, 2], "expected": 3},
                {"input": [9, 5, 12], "expected": 12}
            ],
            "base_xp": 50,
            "kb_key": "general_logic"
        },
        {
            "id": "AF_C4",
            "title": "Two Sum",
            "difficulty": "medium",
            "type": "code",
            "desc": "Return indices of two numbers that add up to target. Input: [arr, target]",
            "code": "def solve(data):\n    arr, target = data\n    # Return [index1, index2]\n    pass",
            "tests": [
                {"input": [[2, 7, 11, 15], 9], "expected": [0, 1]},
                {"input": [[3, 2, 4], 6], "expected": [1, 2]}
            ],
            "base_xp": 80,
            "kb_key": "general_logic"
        },
        {
            "id": "AF_BOSS",
            "title": "Second Largest",
            "difficulty": "boss",
            "type": "code",
            "desc": "Return the second largest element (handle duplicates)",
            "code": "def solve(arr):\n    # Example: [9, 9, 8] → 8\n    pass",
            "tests": [
                {"input": [1, 2, 3, 4], "expected": 3},
                {"input": [9, 9, 8], "expected": 8},
                {"input": [5, 1], "expected": 1}
            ],
            "base_xp": 120,
            "kb_key": "arrays_second_largest"
        }
    ],
    "recursion_cave": [
        {
            "id": "RC_C1",
            "title": "Factorial",
            "difficulty": "easy",
            "type": "code",
            "desc": "Return the factorial of n using recursion",
            "code": "def solve(n):\n    # Your recursive code here\n    pass",
            "tests": [
                {"input": 5, "expected": 120},
                {"input": 3, "expected": 6},
                {"input": 0, "expected": 1}
            ],
            "base_xp": 60,
            "kb_key": "recursion_base_case"
        },
        {
            "id": "RC_C2",
            "title": "Fibonacci",
            "difficulty": "medium",
            "type": "code",
            "desc": "Return the nth Fibonacci number (0-indexed)",
            "code": "def solve(n):\n    # 0, 1, 1, 2, 3, 5, 8...\n    pass",
            "tests": [
                {"input": 0, "expected": 0},
                {"input": 5, "expected": 5},
                {"input": 10, "expected": 55}
            ],
            "base_xp": 90,
            "kb_key": "recursion_base_case"
        },
        {
            "id": "RC_C3",
            "title": "Sum of Digits",
            "difficulty": "medium",
            "type": "code",
            "desc": "Return sum of all digits using recursion",
            "code": "def solve(n):\n    # Example: 123 → 6\n    pass",
            "tests": [
                {"input": 123, "expected": 6},
                {"input": 9999, "expected": 36}
            ],
            "base_xp": 80,
            "kb_key": "recursion_base_case"
        },
        {
            "id": "RC_BOSS",
            "title": "Power Function",
            "difficulty": "boss",
            "type": "code",
            "desc": "Implement pow(base, exp) using recursion. Input: [base, exp]",
            "code": "def solve(data):\n    base, exp = data\n    # Return base^exp\n    pass",
            "tests": [
                {"input": [2, 10], "expected": 1024},
                {"input": [3, 4], "expected": 81},
                {"input": [5, 0], "expected": 1}
            ],
            "base_xp": 150,
            "kb_key": "recursion_base_case"
        }
    ],
    "dp_castle": [
        {
            "id": "DP_C1",
            "title": "Climbing Stairs",
            "difficulty": "easy",
            "type": "code",
            "desc": "Count ways to climb n stairs (1 or 2 steps at a time)",
            "code": "def solve(n):\n    # Return number of ways\n    pass",
            "tests": [
                {"input": 2, "expected": 2},
                {"input": 3, "expected": 3},
                {"input": 5, "expected": 8}
            ],
            "base_xp": 80,
            "kb_key": "dp_overlapping"
        },
        {
            "id": "DP_C2",
            "title": "Coin Change",
            "difficulty": "medium",
            "type": "code",
            "desc": "Return minimum coins needed for amount. Input: [coins, amount]",
            "code": "def solve(data):\n    coins, amount = data\n    # Return min coins or -1\n    pass",
            "tests": [
                {"input": [[1, 2, 5], 11], "expected": 3},
                {"input": [[2], 3], "expected": -1}
            ],
            "base_xp": 120,
            "kb_key": "dp_overlapping"
        },
        {
            "id": "DP_BOSS",
            "title": "Longest Common Subsequence",
            "difficulty": "boss",
            "type": "code",
            "desc": "Return length of LCS of two strings. Input: [s1, s2]",
            "code": "def solve(data):\n    s1, s2 = data\n    # Return LCS length\n    pass",
            "tests": [
                {"input": ["abcde", "ace"], "expected": 3},
                {"input": ["abc", "def"], "expected": 0}
            ],
            "base_xp": 200,
            "kb_key": "dp_overlapping"
        }
    ]
}

# =====================
# ZONES CONFIG
# =====================
ZONES = {
    "training_camp": {"name": "Training Camp", "icon": "🎯", "unlock_intelligence": 0},
    "array_forest": {"name": "Array Forest", "icon": "🌲", "unlock_intelligence": 50},
    "recursion_cave": {"name": "Recursion Cave", "icon": "🦇", "unlock_intelligence": 100},
    "dp_castle": {"name": "DP Castle", "icon": "🏰", "unlock_intelligence": 200}
}

# =====================
# DIFFICULTY MULTIPLIERS
# =====================
DIFF_MULTI = {
    "easy": 1.0,
    "medium": 2.0,
    "hard": 3.5,
    "boss": 5.0
}

# =====================
# RANK THRESHOLDS
# =====================
RANKS = [
    {"xp": 0, "name": "Trainee", "symbol": "⚔️"},
    {"xp": 100, "name": "Operative", "symbol": "🔰"},
    {"xp": 300, "name": "Coder", "symbol": "🗡️"},
    {"xp": 600, "name": "DSA Fighter", "symbol": "⚔️"},
    {"xp": 1000, "name": "Algorithm Knight", "symbol": "🛡️"},
    {"xp": 2000, "name": "Code Master", "symbol": "👑"}
]

# =====================
# DEFAULT PLAYER STATE
# =====================
DEFAULT_PLAYER = {
    "name": "",
    "intelligence": 0,
    "coding_power": 0,
    "rank": "Trainee",
    "solved": [],
    "solved_mcq": [],
    "accuracy": 1.0,
    "mastery": {"training_camp": 0, "array_forest": 0, "recursion_cave": 0, "dp_castle": 0}
}

# =====================
# HELPER FUNCTIONS
# =====================
def load_player():
    """Load player data from file or return default"""
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, 'r') as f:
                player = json.load(f)
                # Ensure all keys exist
                for key in DEFAULT_PLAYER:
                    if key not in player:
                        player[key] = DEFAULT_PLAYER[key]
                return player
        except:
            pass
    return copy.deepcopy(DEFAULT_PLAYER)

def save_player(player):
    """Save player data to file"""
    with open(SAVE_FILE, 'w') as f:
        json.dump(player, f, indent=2)

def get_rank(total_xp):
    """Get rank based on total XP (intelligence + coding_power)"""
    for rank in reversed(RANKS):
        if total_xp >= rank["xp"]:
            return rank
    return RANKS[0]

def run_python_code(code, tests):
    """Execute Python code and run tests"""
    env = {}
    try:
        exec(code, {"__builtins__": {}}, env)
        if "solve" not in env:
            return {"accuracy": 0, "error": "Function solve() not found"}
        
        passed = 0
        for test in tests:
            try:
                input_copy = copy.deepcopy(test["input"])
                if input_copy is None:
                    result = env["solve"]()
                else:
                    result = env["solve"](input_copy)
                if result == test["expected"]:
                    passed += 1
            except Exception as e:
                pass
        
        accuracy = passed / len(tests)
        return {"accuracy": accuracy, "error": None}
    
    except Exception as e:
        return {"accuracy": 0, "error": str(e)}

def explain_failure(problem, accuracy, error):
    """Generate RAG explanation for failure"""
    if error:
        return f"Runtime Error Detected:\n{error}\n\n{KB['general_logic']}"
    
    if accuracy == 0:
        return KB.get(problem.get("kb_key", "general_logic"), KB["general_logic"])
    
    return (
        "Partial correctness detected.\n"
        "Likely missing edge cases.\n\n"
        + KB.get(problem.get("kb_key", "general_logic"), KB["general_logic"])
    )

# =====================
# API ROUTES - STATIC FILES
# =====================
@app.route('/')
def serve_immersive():
    return send_from_directory('.', 'immersive.html')

@app.route('/game')
def serve_game():
    return send_from_directory('.', 'index.html')

# =====================
# API ROUTES - PLAYER
# =====================
@app.route('/api/player', methods=['GET'])
def get_player():
    """Get player data"""
    player = load_player()
    total_xp = player["intelligence"] + player["coding_power"]
    rank = get_rank(total_xp)
    player["rank"] = rank["name"]
    player["rank_symbol"] = rank["symbol"]
    player["total_xp"] = total_xp
    
    # Calculate next rank
    next_rank = None
    for r in RANKS:
        if r["xp"] > total_xp:
            next_rank = r
            break
    player["next_rank_xp"] = next_rank["xp"] if next_rank else None
    
    return jsonify(player)

@app.route('/api/player', methods=['POST'])
def update_player():
    """Update player data"""
    player = request.json
    save_player(player)
    return jsonify({"success": True})

@app.route('/api/player/name', methods=['POST'])
def set_player_name():
    """Set player hero name"""
    data = request.json
    name = data.get("name", "").strip()
    if not name:
        return jsonify({"error": "Name cannot be empty"}), 400
    
    player = load_player()
    player["name"] = name
    save_player(player)
    return jsonify({"success": True, "name": name})

@app.route('/api/player/reset', methods=['POST'])
def reset_player():
    """Reset player to default state"""
    save_player(copy.deepcopy(DEFAULT_PLAYER))
    return jsonify({"success": True, "player": DEFAULT_PLAYER})

# =====================
# API ROUTES - ZONES
# =====================
@app.route('/api/zones', methods=['GET'])
def get_zones():
    """Get all zones with unlock status"""
    player = load_player()
    zones_data = {}
    
    for zone_id, zone in ZONES.items():
        mcqs = MCQS.get(zone_id, [])
        problems = PROBLEMS.get(zone_id, [])
        
        solved_mcq_count = len([m for m in mcqs if m["id"] in player["solved_mcq"]])
        solved_code_count = len([p for p in problems if p["id"] in player["solved"]])
        
        zones_data[zone_id] = {
            **zone,
            "unlocked": player["intelligence"] >= zone["unlock_intelligence"],
            "total_mcq": len(mcqs),
            "solved_mcq": solved_mcq_count,
            "total_problems": len(problems),
            "solved_count": solved_code_count,
            "mastery": player["mastery"].get(zone_id, 0)
        }
    
    return jsonify(zones_data)

# =====================
# API ROUTES - MCQ
# =====================
@app.route('/api/mcq/<zone>', methods=['GET'])
def get_mcqs(zone):
    """Get all MCQs for a zone"""
    if zone not in MCQS:
        return jsonify({"error": "Zone not found"}), 404
    
    player = load_player()
    mcqs = []
    
    for m in MCQS[zone]:
        mcqs.append({
            **m,
            "solved": m["id"] in player["solved_mcq"],
            "answer": None  # Hide answer from client
        })
    
    return jsonify(mcqs)

@app.route('/api/mcq/<zone>/next', methods=['GET'])
def get_next_mcq(zone):
    """Get next unsolved MCQ in zone"""
    if zone not in MCQS:
        return jsonify({"error": "Zone not found"}), 404
    
    player = load_player()
    
    for mcq in MCQS[zone]:
        if mcq["id"] not in player["solved_mcq"]:
            return jsonify({
                **mcq,
                "answer": None  # Hide answer from client
            })
    
    return jsonify({"message": "All MCQs cleared!", "cleared": True})

@app.route('/api/mcq/submit', methods=['POST'])
def submit_mcq():
    """Submit MCQ answer"""
    data = request.json
    mcq_id = data.get("mcq_id", "")
    selected = data.get("selected", -1)  # Index of selected option
    zone = data.get("zone", "")
    
    # Find the MCQ
    mcq = None
    for z, mcqs in MCQS.items():
        for m in mcqs:
            if m["id"] == mcq_id:
                mcq = m
                break
        if mcq:
            break
    
    if not mcq:
        return jsonify({"error": "MCQ not found"}), 404
    
    # Check answer
    correct = selected == mcq["answer"]
    
    if not correct:
        return jsonify({
            "success": False,
            "correct": False,
            "correct_answer": mcq["answer"],
            "explanation": "Incorrect! The correct answer was: " + mcq["options"][mcq["answer"]]
        })
    
    # Award intelligence XP
    player = load_player()
    xp = mcq["intelligence_xp"]
    player["intelligence"] += xp
    
    if mcq_id not in player["solved_mcq"]:
        player["solved_mcq"].append(mcq_id)
    
    player["mastery"][zone] = min(100, player["mastery"].get(zone, 0) + 10)
    player["rank"] = get_rank(player["intelligence"] + player["coding_power"])["name"]
    
    save_player(player)
    
    return jsonify({
        "success": True,
        "correct": True,
        "xp_earned": xp,
        "new_intelligence": player["intelligence"],
        "new_rank": player["rank"],
        "mastery": player["mastery"][zone]
    })

# =====================
# API ROUTES - CODE PROBLEMS
# =====================
@app.route('/api/problems/<zone>', methods=['GET'])
def get_problems(zone):
    """Get all code problems for a zone"""
    if zone not in PROBLEMS:
        return jsonify({"error": "Zone not found"}), 404
    
    player = load_player()
    problems = []
    
    for p in PROBLEMS[zone]:
        problems.append({
            **p,
            "solved": p["id"] in player["solved"],
            "potential_xp": int(p["base_xp"] * DIFF_MULTI[p["difficulty"]])
        })
    
    return jsonify(problems)

@app.route('/api/problems/<zone>/next', methods=['GET'])
def get_next_problem(zone):
    """Get next unsolved problem in zone"""
    if zone not in PROBLEMS:
        return jsonify({"error": "Zone not found"}), 404
    
    player = load_player()
    
    for problem in PROBLEMS[zone]:
        if problem["id"] not in player["solved"]:
            return jsonify({
                **problem,
                "potential_xp": int(problem["base_xp"] * DIFF_MULTI[problem["difficulty"]])
            })
    
    return jsonify({"message": "Zone cleared!", "cleared": True})

@app.route('/api/submit', methods=['POST'])
def submit_code():
    """Submit code for evaluation"""
    data = request.json
    code = data.get("code", "")
    problem_id = data.get("problem_id", "")
    zone = data.get("zone", "")
    
    # Find the problem
    problem = None
    for z, problems in PROBLEMS.items():
        for p in problems:
            if p["id"] == problem_id:
                problem = p
                break
        if problem:
            break
    
    if not problem:
        return jsonify({"error": "Problem not found"}), 404
    
    # Run the code
    result = run_python_code(code, problem["tests"])
    accuracy = result["accuracy"]
    error = result["error"]
    
    if accuracy < 0.5:
        explanation = explain_failure(problem, accuracy, error)
        return jsonify({
            "success": False,
            "accuracy": accuracy,
            "explanation": explanation
        })
    
    # Calculate XP
    xp = int(problem["base_xp"] * DIFF_MULTI[problem["difficulty"]] * accuracy)
    
    # Update player
    player = load_player()
    player["coding_power"] += xp
    player["accuracy"] = (player["accuracy"] + accuracy) / 2
    
    if problem_id not in player["solved"]:
        player["solved"].append(problem_id)
    
    player["mastery"][zone] = min(100, player["mastery"].get(zone, 0) + int(accuracy * 25))
    player["rank"] = get_rank(player["intelligence"] + player["coding_power"])["name"]
    
    save_player(player)
    
    return jsonify({
        "success": True,
        "accuracy": accuracy,
        "xp_earned": xp,
        "new_coding_power": player["coding_power"],
        "new_rank": player["rank"],
        "mastery": player["mastery"][zone]
    })

# =====================
# API ROUTES - LEADERBOARD
# =====================
@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get leaderboard"""
    player = load_player()
    total_xp = player["intelligence"] + player["coding_power"]
    return jsonify([
        {"name": player["name"] or "You", "xp": total_xp, "rank": get_rank(total_xp)["name"]},
        {"name": "CodeMaster42", "xp": 2500, "rank": "Code Master"},
        {"name": "ByteNinja", "xp": 1800, "rank": "Algorithm Knight"},
        {"name": "RecursiveRider", "xp": 950, "rank": "DSA Fighter"},
        {"name": "ArrayAce", "xp": 450, "rank": "Coder"}
    ])

# =====================
# RUN SERVER
# =====================
if __name__ == '__main__':
    print("\n" + "="*50)
    print("🎮 EngineerQuest RPG Server")
    print("="*50)
    print(f"🌐 Landing Page: http://localhost:5000/")
    print(f"🎯 Game Arena:   http://localhost:5000/game")
    print(f"📡 API Base:     http://localhost:5000/api/")
    print("="*50 + "\n")
    
    app.run(debug=True, port=5000)
