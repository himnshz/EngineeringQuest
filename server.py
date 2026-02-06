"""
EngineerQuest RPG - Backend API Server
Flask-based REST API for the coding RPG game
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import os
import traceback

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
    "general_logic": (
        "Check:\n"
        "• Function returns a value\n"
        "• Correct variable updates\n"
        "• All test cases handled"
    )
}

# =====================
# PROBLEMS DATABASE
# =====================
PROBLEMS = {
    "arrays": [
        {
            "id": "A1",
            "title": "Sum of Array",
            "difficulty": "easy",
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
            "id": "A2",
            "title": "Reverse Array",
            "difficulty": "easy",
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
            "id": "A3",
            "title": "Find Minimum",
            "difficulty": "easy",
            "desc": "Return the minimum element in the array",
            "code": "def solve(arr):\n    # Your code here\n    pass",
            "tests": [
                {"input": [3, 1, 2], "expected": 1},
                {"input": [9, 5], "expected": 5}
            ],
            "base_xp": 50,
            "kb_key": "general_logic"
        },
        {
            "id": "A4",
            "title": "Two Sum",
            "difficulty": "medium",
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
            "id": "A_BOSS",
            "title": "Array Boss: Second Largest",
            "difficulty": "boss",
            "desc": "Return the second largest element (no duplicates in result)",
            "code": "def solve(arr):\n    # Find second largest element\n    # Example: [9, 9, 8] → 8\n    pass",
            "tests": [
                {"input": [1, 2, 3, 4], "expected": 3},
                {"input": [9, 9, 8], "expected": 8},
                {"input": [5, 1], "expected": 1}
            ],
            "base_xp": 120,
            "kb_key": "arrays_second_largest"
        }
    ],
    "recursion": [
        {
            "id": "R1",
            "title": "Factorial",
            "difficulty": "easy",
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
            "id": "R2",
            "title": "Fibonacci",
            "difficulty": "medium",
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
            "id": "R3",
            "title": "Sum of Digits",
            "difficulty": "medium",
            "desc": "Return the sum of all digits in a number using recursion",
            "code": "def solve(n):\n    # Example: 123 → 1 + 2 + 3 = 6\n    pass",
            "tests": [
                {"input": 123, "expected": 6},
                {"input": 9999, "expected": 36},
                {"input": 5, "expected": 5}
            ],
            "base_xp": 80,
            "kb_key": "recursion_base_case"
        },
        {
            "id": "R_BOSS",
            "title": "Recursion Boss: Power Function",
            "difficulty": "boss",
            "desc": "Implement pow(base, exp) using recursion. Input: [base, exp]",
            "code": "def solve(data):\n    base, exp = data\n    # Return base^exp using recursion\n    pass",
            "tests": [
                {"input": [2, 10], "expected": 1024},
                {"input": [3, 4], "expected": 81},
                {"input": [5, 0], "expected": 1}
            ],
            "base_xp": 150,
            "kb_key": "recursion_base_case"
        }
    ],
    "strings": [
        {
            "id": "S1",
            "title": "Reverse String",
            "difficulty": "easy",
            "desc": "Return the reversed string",
            "code": "def solve(s):\n    # Your code here\n    pass",
            "tests": [
                {"input": "hello", "expected": "olleh"},
                {"input": "world", "expected": "dlrow"}
            ],
            "base_xp": 40,
            "kb_key": "general_logic"
        },
        {
            "id": "S2",
            "title": "Palindrome Check",
            "difficulty": "medium",
            "desc": "Return True if the string is a palindrome, False otherwise",
            "code": "def solve(s):\n    # Ignore case and spaces\n    pass",
            "tests": [
                {"input": "racecar", "expected": True},
                {"input": "hello", "expected": False},
                {"input": "A man a plan a canal Panama", "expected": True}
            ],
            "base_xp": 70,
            "kb_key": "general_logic"
        }
    ]
}

# =====================
# ZONES CONFIG
# =====================
ZONES = {
    "arrays": {"name": "Arrays", "icon": "📦", "unlockXP": 0},
    "recursion": {"name": "Recursion", "icon": "🔄", "unlockXP": 150},
    "strings": {"name": "Strings", "icon": "📝", "unlockXP": 400}
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
    {"xp": 300, "name": "Coder", "symbol": "🗡️"},
    {"xp": 800, "name": "DSA Fighter", "symbol": "⚔️"},
    {"xp": 1500, "name": "Algorithm Knight", "symbol": "🛡️"},
    {"xp": 3000, "name": "Code Master", "symbol": "👑"}
]

# =====================
# DEFAULT PLAYER STATE
# =====================
DEFAULT_PLAYER = {
    "coding_xp": 0,
    "rank": "Trainee",
    "solved": [],
    "accuracy": 1.0,
    "mastery": {"arrays": 0, "recursion": 0, "strings": 0}
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
    return DEFAULT_PLAYER.copy()

def save_player(player):
    """Save player data to file"""
    with open(SAVE_FILE, 'w') as f:
        json.dump(player, f, indent=2)

def get_rank(xp):
    """Get rank based on XP"""
    for rank in reversed(RANKS):
        if xp >= rank["xp"]:
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
                # Deep copy input to prevent mutation
                import copy
                input_copy = copy.deepcopy(test["input"])
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
        return KB.get(problem["kb_key"], KB["general_logic"])
    
    return (
        "Partial correctness detected.\n"
        "Likely missing edge cases.\n\n"
        + KB.get(problem["kb_key"], KB["general_logic"])
    )

# =====================
# API ROUTES
# =====================

@app.route('/')
def serve_immersive():
    """Serve the immersive landing page"""
    return send_from_directory('.', 'immersive.html')

@app.route('/game')
def serve_game():
    """Serve the game page"""
    return send_from_directory('.', 'index.html')

@app.route('/api/player', methods=['GET'])
def get_player():
    """Get player data"""
    player = load_player()
    rank = get_rank(player["coding_xp"])
    player["rank"] = rank["name"]
    player["rank_symbol"] = rank["symbol"]
    
    # Calculate next rank
    next_rank = None
    for r in RANKS:
        if r["xp"] > player["coding_xp"]:
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

@app.route('/api/player/reset', methods=['POST'])
def reset_player():
    """Reset player to default state"""
    save_player(DEFAULT_PLAYER.copy())
    return jsonify({"success": True, "player": DEFAULT_PLAYER})

@app.route('/api/zones', methods=['GET'])
def get_zones():
    """Get all zones with unlock status"""
    player = load_player()
    zones_data = {}
    
    for zone_id, zone in ZONES.items():
        problems = PROBLEMS.get(zone_id, [])
        solved_count = len([p for p in problems if p["id"] in player["solved"]])
        
        zones_data[zone_id] = {
            **zone,
            "unlocked": player["coding_xp"] >= zone["unlockXP"],
            "total_problems": len(problems),
            "solved_count": solved_count,
            "mastery": player["mastery"].get(zone_id, 0)
        }
    
    return jsonify(zones_data)

@app.route('/api/problems/<zone>', methods=['GET'])
def get_problems(zone):
    """Get all problems for a zone"""
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
        # Failed
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
    player["coding_xp"] += xp
    player["accuracy"] = (player["accuracy"] + accuracy) / 2
    
    if problem_id not in player["solved"]:
        player["solved"].append(problem_id)
    
    player["mastery"][zone] = min(100, player["mastery"].get(zone, 0) + int(accuracy * 25))
    player["rank"] = get_rank(player["coding_xp"])["name"]
    
    save_player(player)
    
    return jsonify({
        "success": True,
        "accuracy": accuracy,
        "xp_earned": xp,
        "new_xp_total": player["coding_xp"],
        "new_rank": player["rank"],
        "mastery": player["mastery"][zone]
    })

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get leaderboard (placeholder for multiplayer)"""
    player = load_player()
    return jsonify([
        {"name": "You", "xp": player["coding_xp"], "rank": get_rank(player["coding_xp"])["name"]},
        {"name": "CodeMaster42", "xp": 2500, "rank": "Algorithm Knight"},
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
