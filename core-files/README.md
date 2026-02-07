# EngineerQuest Core Files

Portable components for building immersive coding games.

## Files Included

| File | Description |
|------|-------------|
| `index.html` | Game arena UI with glassmorphism, code editor CSS/HTML |
| `game.js` | Code editor logic, API calls, game state |
| `server.py` | Flask backend with zones, MCQs, code execution |
| `immersive.html` | 3D landing page with Three.js particles |

---

## Features

### 🎮 Game System
- **4 Zones**: Training Camp → Array Forest → Recursion Cave → DP Castle
- **MCQ + Code Problems**: Intelligence from MCQs, Coding Power from code
- **Rank Progression**: Trainee → Operative → Coder → DSA Fighter → Algorithm Knight → Code Master

### ✏️ Code Editor
- Tab inserts 4 spaces (no focus loss)
- Shift+Tab outdent
- Auto-closing pairs: `()`, `[]`, `{}`, `""`, `''`
- Smart bracket overwrite
- Auto-indent after `:` (Python)
- Line numbers with active highlight
- Python syntax highlighting
- Glassmorphism blur background

### 🎨 UI Design
- 3D particle backgrounds
- Glassmorphism panels (`backdrop-filter: blur`)
- Dracula color scheme for syntax
- Responsive three-column layout
- Animated hover effects

---

## Usage

1. Copy files to your project
2. Run `python server.py` (needs Flask: `pip install flask flask-cors`)
3. Open `http://localhost:5000/`

## Dependencies
- Flask + Flask-CORS (backend)
- Three.js (3D graphics, loaded via CDN)
- Google Fonts: Orbitron, Inter, JetBrains Mono
