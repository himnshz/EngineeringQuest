# 🎮 EngineerQuest

An immersive RPG-style coding game where you level up by solving Python problems.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Flask-Backend-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

### 🏰 Game Zones
| Zone | Unlock | Problems |
|------|--------|----------|
| Training Camp | Default | 7 MCQs + 7 Code |
| Array Forest | 50 INT | 3 MCQs + 5 Code |
| Recursion Cave | 100 INT | 2 MCQs + 4 Code |
| DP Castle | 200 INT | 2 MCQs + 3 Code |

### 📊 Dual Stats System
- 🧠 **Intelligence** - Earned from MCQs
- ⚡ **Coding Power** - Earned from code problems

### ✏️ Professional Code Editor
- Tab handling (4 spaces, no focus loss)
- Auto-closing brackets: `()`, `[]`, `{}`, `""`, `''`
- Python syntax highlighting (Dracula theme)
- Line numbers with active line highlight
- Glassmorphism blur effect

### 🎨 Immersive UI
- 3D particle landing page (Three.js)
- Glassmorphism panels
- Animated hover effects
- Responsive design

## 🚀 Quick Start

```bash
# Install dependencies
pip install flask flask-cors

# Run the server
python server.py

# Open in browser
http://localhost:5000/
```

## 📁 Project Structure
```
EngineerQuest/
├── server.py         # Flask backend API
├── index.html        # Game arena UI
├── game.js           # Code editor & game logic
├── immersive.html    # 3D landing page
└── core-files/       # Portable components
```

## 🎯 Syntax Highlighting Colors
| Token | Color |
|-------|-------|
| Keywords (`def`, `if`, `for`) | Pink |
| Built-ins (`print`, `len`, `range`) | Cyan |
| Functions | Green |
| Strings | Yellow |
| Numbers | Purple |
| Comments | Gray |

## 📄 License
MIT License
