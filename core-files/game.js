/* ================================================
   ENGINEERQUEST RPG - GAME LOGIC (API-CONNECTED)
   ================================================ */

// API Base URL
const API_BASE = 'http://localhost:5000/api';

// =====================
// GAME STATE
// =====================
let player = null;
let zones = null;
let currentZone = "training_camp";
let currentProblem = null;
let currentMCQ = null;
let problemType = "mcq"; // "mcq" or "code"

// =====================
// DOM ELEMENTS
// =====================
const elements = {
    // Header stats
    rankSymbol: document.getElementById("rank-symbol"),
    playerRank: document.getElementById("player-rank"),
    intelligenceValue: document.getElementById("intelligence-value"),
    codingPowerValue: document.getElementById("coding-power-value"),

    // XP Display
    xpBar: document.getElementById("xp-bar"),
    xpText: document.getElementById("xp-text"),
    totalXp: document.getElementById("total-xp"),
    accuracy: document.getElementById("accuracy"),
    problemsSolved: document.getElementById("problems-solved"),

    // Zones
    zoneGrid: document.getElementById("zone-grid"),
    currentZone: document.getElementById("current-zone"),
    arenaZoneIcon: document.querySelector(".arena-zone-icon"),
    masteryBar: document.getElementById("mastery-bar"),
    masteryText: document.getElementById("mastery-text"),

    // Problem display
    difficultyBadge: document.getElementById("difficulty-badge"),
    problemTitle: document.getElementById("problem-title"),
    problemDescription: document.getElementById("problem-description"),
    xpReward: document.getElementById("xp-reward"),
    testCases: document.getElementById("test-cases"),

    // Editor/MCQ area
    codeEditor: document.getElementById("code-editor"),
    mcqContainer: document.getElementById("mcq-container"),

    // Buttons
    loadBtn: document.getElementById("load-btn"),
    loadMcqBtn: document.getElementById("load-mcq-btn"),
    submitBtn: document.getElementById("submit-btn"),
    resetBtn: document.getElementById("reset-btn"),
    copyBtn: document.getElementById("copy-btn"),

    // Modal
    modalOverlay: document.getElementById("modal-overlay"),
    modalIcon: document.getElementById("modal-icon"),
    modalTitle: document.getElementById("modal-title"),
    modalMessage: document.getElementById("modal-message"),
    modalStats: document.getElementById("modal-stats"),
    modalClose: document.getElementById("modal-close"),

    // Background
    particles: document.getElementById("particles")
};

// =====================
// API FUNCTIONS
// =====================
async function apiGet(endpoint) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        showModal("⚠️", "Connection Error", "Could not connect to server.\nMake sure the backend is running on port 5000.", [], "warning");
        return null;
    }
}

async function apiPost(endpoint, data) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        showModal("⚠️", "Connection Error", "Could not connect to server.\nMake sure the backend is running on port 5000.", [], "warning");
        return null;
    }
}

// =====================
// INITIALIZATION
// =====================
async function init() {
    createParticles();
    bindEvents();

    // Load data from API
    await loadPlayerData();
    await loadZones();

    updateUI();
}

function createParticles() {
    if (!elements.particles) return;
    for (let i = 0; i < 30; i++) {
        const particle = document.createElement("div");
        particle.className = "particle";
        particle.style.left = Math.random() * 100 + "%";
        particle.style.animationDelay = Math.random() * 8 + "s";
        particle.style.animationDuration = (6 + Math.random() * 4) + "s";
        elements.particles.appendChild(particle);
    }
}

function bindEvents() {
    if (elements.loadBtn) {
        elements.loadBtn.addEventListener("click", loadProblem);
    }
    if (elements.loadMcqBtn) {
        elements.loadMcqBtn.addEventListener("click", loadMCQ);
    }
    if (elements.submitBtn) {
        elements.submitBtn.addEventListener("click", submitAnswer);
    }
    if (elements.resetBtn) {
        elements.resetBtn.addEventListener("click", resetCode);
    }
    if (elements.copyBtn) {
        elements.copyBtn.addEventListener("click", copyCode);
    }
    if (elements.modalClose) {
        elements.modalClose.addEventListener("click", closeModal);
    }
    if (elements.modalOverlay) {
        elements.modalOverlay.addEventListener("click", (e) => {
            if (e.target === elements.modalOverlay) closeModal();
        });
    }

    // Initialize enhanced code editor
    setupCodeEditor();
}

// =====================
// ENHANCED CODE EDITOR
// =====================
const INDENT_SIZE = 4;
const INDENT = ' '.repeat(INDENT_SIZE);
const AUTO_PAIRS = {
    '(': ')',
    '[': ']',
    '{': '}',
    '"': '"',
    "'": "'",
    '`': '`'
};
const CLOSING_CHARS = Object.values(AUTO_PAIRS);

function setupCodeEditor() {
    const editor = document.getElementById('code-editor');
    const lineNumbers = document.getElementById('line-numbers');
    const syntaxHighlight = document.getElementById('syntax-highlight');
    const cursorLine = document.getElementById('cursor-line');
    const editorWrapper = document.getElementById('editor-wrapper');

    if (!editor) return;

    // Keydown handler for Tab, Enter, auto-pairs
    editor.addEventListener('keydown', (e) => {
        const start = editor.selectionStart;
        const end = editor.selectionEnd;
        const value = editor.value;
        const hasSelection = start !== end;

        // TAB - Insert spaces instead of changing focus
        if (e.key === 'Tab') {
            e.preventDefault();

            if (e.shiftKey) {
                // Shift+Tab: Outdent
                const lineStart = value.lastIndexOf('\n', start - 1) + 1;
                const lineText = value.substring(lineStart, start);

                if (lineText.startsWith(INDENT)) {
                    editor.value = value.substring(0, lineStart) + value.substring(lineStart + INDENT_SIZE);
                    editor.selectionStart = editor.selectionEnd = start - INDENT_SIZE;
                } else {
                    // Remove leading spaces
                    const spaces = lineText.match(/^ */)[0].length;
                    if (spaces > 0) {
                        editor.value = value.substring(0, lineStart) + value.substring(lineStart + spaces);
                        editor.selectionStart = editor.selectionEnd = start - spaces;
                    }
                }
            } else {
                // Tab: Insert indent
                if (hasSelection) {
                    // Indent selected lines
                    const selectedText = value.substring(start, end);
                    const indentedText = INDENT + selectedText.replace(/\n/g, '\n' + INDENT);
                    editor.value = value.substring(0, start) + indentedText + value.substring(end);
                    editor.selectionStart = start;
                    editor.selectionEnd = start + indentedText.length;
                } else {
                    insertText(editor, INDENT);
                }
            }
            updateEditor();
            return;
        }

        // ENTER - Auto-indentation
        if (e.key === 'Enter') {
            e.preventDefault();
            const lineStart = value.lastIndexOf('\n', start - 1) + 1;
            const currentLine = value.substring(lineStart, start);
            const indent = currentLine.match(/^\s*/)[0];

            // Check if previous char is an opening bracket
            const charBefore = value[start - 1];
            const charAfter = value[start];

            if (charBefore === '{' || charBefore === '[' || charBefore === '(') {
                if (charAfter === '}' || charAfter === ']' || charAfter === ')') {
                    // Cursor between brackets: add extra line
                    insertText(editor, '\n' + indent + INDENT + '\n' + indent);
                    editor.selectionStart = editor.selectionEnd = start + 1 + indent.length + INDENT_SIZE;
                } else {
                    insertText(editor, '\n' + indent + INDENT);
                }
            } else if (currentLine.trimEnd().endsWith(':')) {
                // Python: auto-indent after colon
                insertText(editor, '\n' + indent + INDENT);
            } else {
                insertText(editor, '\n' + indent);
            }
            updateEditor();
            return;
        }

        // BACKSPACE - Remove full indent if at indent start
        if (e.key === 'Backspace' && !hasSelection) {
            const lineStart = value.lastIndexOf('\n', start - 1) + 1;
            const textBeforeCursor = value.substring(lineStart, start);

            if (textBeforeCursor.length > 0 && textBeforeCursor.trim() === '' && textBeforeCursor.length % INDENT_SIZE === 0) {
                e.preventDefault();
                editor.value = value.substring(0, start - INDENT_SIZE) + value.substring(start);
                editor.selectionStart = editor.selectionEnd = start - INDENT_SIZE;
                updateEditor();
                return;
            }
        }

        // AUTO-CLOSING PAIRS
        if (AUTO_PAIRS[e.key]) {
            e.preventDefault();
            const closing = AUTO_PAIRS[e.key];

            if (hasSelection) {
                // Wrap selection
                const selected = value.substring(start, end);
                editor.value = value.substring(0, start) + e.key + selected + closing + value.substring(end);
                editor.selectionStart = start + 1;
                editor.selectionEnd = end + 1;
            } else {
                insertText(editor, e.key + closing);
                editor.selectionStart = editor.selectionEnd = start + 1;
            }
            updateEditor();
            return;
        }

        // OVERWRITE CLOSING CHARS
        if (CLOSING_CHARS.includes(e.key) && value[start] === e.key) {
            e.preventDefault();
            editor.selectionStart = editor.selectionEnd = start + 1;
            return;
        }
    });

    // Input handler for syntax highlighting
    editor.addEventListener('input', updateEditor);

    // Scroll sync for line numbers
    editor.addEventListener('scroll', () => {
        if (lineNumbers) lineNumbers.scrollTop = editor.scrollTop;
        if (syntaxHighlight) syntaxHighlight.scrollTop = editor.scrollTop;
    });

    // Cursor position tracking
    editor.addEventListener('click', updateCursorLine);
    editor.addEventListener('keyup', updateCursorLine);

    function updateEditor() {
        updateLineNumbers();
        updateSyntaxHighlight();
        updateCursorLine();
    }

    function updateLineNumbers() {
        if (!lineNumbers) return;
        const lines = editor.value.split('\n').length;
        const currentLine = editor.value.substring(0, editor.selectionStart).split('\n').length;

        let html = '';
        for (let i = 1; i <= lines; i++) {
            html += `<span class="line-num ${i === currentLine ? 'active' : ''}">${i}</span>`;
        }
        lineNumbers.innerHTML = html;
    }

    function updateSyntaxHighlight() {
        if (!syntaxHighlight) return;
        syntaxHighlight.innerHTML = highlightPython(editor.value) + '\n';
    }

    function updateCursorLine() {
        if (!cursorLine || !editorWrapper) return;
        const lineHeight = parseFloat(getComputedStyle(editor).lineHeight);
        const currentLine = editor.value.substring(0, editor.selectionStart).split('\n').length - 1;
        const top = 16 + (currentLine * lineHeight) - editor.scrollTop;
        cursorLine.style.top = top + 'px';
        cursorLine.style.height = lineHeight + 'px';
        updateLineNumbers();
    }

    // Initial update
    updateEditor();
}

function insertText(editor, text) {
    const start = editor.selectionStart;
    const end = editor.selectionEnd;
    editor.value = editor.value.substring(0, start) + text + editor.value.substring(end);
    editor.selectionStart = editor.selectionEnd = start + text.length;
}

// Python Syntax Highlighting
function highlightPython(code) {
    // Escape HTML
    let html = code
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');

    // Keywords (pink)
    const keywords = ['def', 'class', 'if', 'elif', 'else', 'for', 'while', 'try', 'except', 'finally', 'with', 'as', 'import', 'from', 'return', 'yield', 'raise', 'pass', 'break', 'continue', 'lambda', 'and', 'or', 'not', 'in', 'is', 'True', 'False', 'None', 'async', 'await'];
    keywords.forEach(kw => {
        html = html.replace(new RegExp('\\\\b' + kw + '\\\\b', 'g'), '<span class="keyword">' + kw + '</span>');
    });

    // Built-ins (cyan)
    const builtins = ['print', 'len', 'range', 'int', 'str', 'float', 'list', 'dict', 'set', 'tuple', 'bool', 'sum', 'max', 'min', 'abs', 'round', 'sorted', 'enumerate', 'zip', 'map', 'filter', 'input', 'open', 'self'];
    builtins.forEach(fn => {
        html = html.replace(new RegExp('\\\\b' + fn + '\\\\b', 'g'), '<span class="builtin">' + fn + '</span>');
    });

    // Numbers (purple)
    html = html.replace(/\\b(\\d+\\.?\\d*)\\b/g, '<span class="number">$1</span>');

    // Comments (gray)
    html = html.replace(/(#[^\\n]*)/g, '<span class="comment">$1</span>');

    return html;
}


// =====================
// DATA LOADING
// =====================
async function loadPlayerData() {
    player = await apiGet('/player');
    if (!player) {
        player = {
            name: "",
            intelligence: 0,
            coding_power: 0,
            rank: "Trainee",
            solved: [],
            solved_mcq: [],
            accuracy: 1.0,
            mastery: { training_camp: 0, array_forest: 0, recursion_cave: 0, dp_castle: 0 }
        };
    }
}

async function loadZones() {
    zones = await apiGet('/zones');
    if (zones) {
        renderZones();
    }
}

// =====================
// UI RENDERING
// =====================
function renderZones() {
    if (!elements.zoneGrid) return;
    elements.zoneGrid.innerHTML = "";

    Object.entries(zones).forEach(([key, zone]) => {
        const isActive = currentZone === key;

        const card = document.createElement("div");
        card.className = `zone-card ${isActive ? "active" : ""} ${!zone.unlocked ? "locked" : ""}`;
        card.innerHTML = `
            <span class="zone-icon">${zone.icon}</span>
            <div class="zone-info">
                <span class="zone-name">${zone.name}</span>
                <span class="zone-progress">${zone.unlocked ? `${zone.solved_mcq + zone.solved_count}/${zone.total_mcq + zone.total_problems} cleared` : `🔒 ${zone.unlock_intelligence} INT`}</span>
                <div class="zone-mastery-bar"><div class="zone-mastery-fill" style="width: ${zone.mastery || 0}%"></div></div>
            </div>
            ${!zone.unlocked ? '<span class="zone-lock">🔒</span>' : ''}
        `;

        if (zone.unlocked) {
            card.addEventListener("click", () => selectZone(key));
        }

        elements.zoneGrid.appendChild(card);
    });
}

async function selectZone(zone) {
    currentZone = zone;
    currentProblem = null;
    currentMCQ = null;

    if (elements.codeEditor) elements.codeEditor.value = "";
    if (elements.mcqContainer) elements.mcqContainer.innerHTML = "";
    if (elements.problemTitle) elements.problemTitle.textContent = "Select a Mission";
    if (elements.problemDescription) elements.problemDescription.textContent = "Click 'Load MCQ' for theory or 'Load Battle' for coding challenges!";
    if (elements.testCases) elements.testCases.innerHTML = "";
    if (elements.difficultyBadge) {
        elements.difficultyBadge.textContent = "---";
        elements.difficultyBadge.className = "difficulty-badge";
    }
    if (elements.xpReward) elements.xpReward.textContent = "+0 XP";

    await loadZones();
    updateArenaHeader();
}

function updateUI() {
    if (!player) return;

    // Update rank
    if (elements.rankSymbol) elements.rankSymbol.textContent = player.rank_symbol || "⚔️";
    if (elements.playerRank) elements.playerRank.textContent = player.rank;

    // Update Intelligence and Coding Power
    if (elements.intelligenceValue) elements.intelligenceValue.textContent = player.intelligence || 0;
    if (elements.codingPowerValue) elements.codingPowerValue.textContent = player.coding_power || 0;

    // Update XP bar (based on total XP)
    const totalXP = (player.intelligence || 0) + (player.coding_power || 0);
    const nextRankXP = player.next_rank_xp || totalXP;

    const RANKS = [
        { xp: 0, name: "Trainee" },
        { xp: 100, name: "Operative" },
        { xp: 300, name: "Coder" },
        { xp: 600, name: "DSA Fighter" },
        { xp: 1000, name: "Algorithm Knight" },
        { xp: 2000, name: "Code Master" }
    ];

    let currentThreshold = 0;
    for (const rank of RANKS) {
        if (totalXP >= rank.xp) {
            currentThreshold = rank.xp;
        }
    }

    const progress = player.next_rank_xp
        ? ((totalXP - currentThreshold) / (nextRankXP - currentThreshold)) * 100
        : 100;

    if (elements.xpBar) elements.xpBar.style.width = Math.min(100, progress) + "%";
    if (elements.xpText) {
        elements.xpText.textContent = player.next_rank_xp
            ? `${totalXP} / ${nextRankXP} XP`
            : `${totalXP} XP (MAX)`;
    }

    // Update stats
    if (elements.totalXp) elements.totalXp.textContent = totalXP;
    if (elements.accuracy) elements.accuracy.textContent = Math.round((player.accuracy || 1) * 100) + "%";
    if (elements.problemsSolved) elements.problemsSolved.textContent = (player.solved?.length || 0) + (player.solved_mcq?.length || 0);

    // Update arena header
    updateArenaHeader();
}

function updateArenaHeader() {
    if (!zones) return;

    const zone = zones[currentZone];
    if (!zone) return;

    if (elements.currentZone) elements.currentZone.textContent = zone.name;
    if (elements.arenaZoneIcon) elements.arenaZoneIcon.textContent = zone.icon;

    const mastery = zone.mastery || 0;
    if (elements.masteryBar) elements.masteryBar.style.width = mastery + "%";
    if (elements.masteryText) elements.masteryText.textContent = mastery + "%";
}

// =====================
// MCQ LOADING
// =====================
async function loadMCQ() {
    const result = await apiGet(`/mcq/${currentZone}/next`);

    if (!result) return;

    if (result.cleared) {
        showModal("🎉", "MCQs Cleared!", "You've mastered all theory questions in this zone.\n\nTry the coding challenges!", [], "victory");
        return;
    }

    currentMCQ = result;
    currentProblem = null;
    problemType = "mcq";

    // Update UI
    if (elements.difficultyBadge) {
        elements.difficultyBadge.textContent = result.difficulty.toUpperCase();
        elements.difficultyBadge.className = `difficulty-badge ${result.difficulty}`;
    }
    if (elements.problemTitle) elements.problemTitle.textContent = result.title;
    if (elements.problemDescription) elements.problemDescription.textContent = result.question;
    if (elements.xpReward) elements.xpReward.textContent = `+${result.intelligence_xp} INT`;

    // Hide code editor, show MCQ options
    if (elements.codeEditor) elements.codeEditor.style.display = "none";

    // Create MCQ options
    if (elements.testCases) {
        elements.testCases.innerHTML = "";
        result.options.forEach((option, i) => {
            const optionEl = document.createElement("div");
            optionEl.className = "mcq-option";
            optionEl.dataset.index = i;
            optionEl.innerHTML = `
                <span class="mcq-letter">${String.fromCharCode(65 + i)}.</span>
                <span class="mcq-text">${option}</span>
            `;
            optionEl.addEventListener("click", () => selectMCQOption(i));
            elements.testCases.appendChild(optionEl);
        });
    }
}

function selectMCQOption(index) {
    // Remove previous selection
    document.querySelectorAll('.mcq-option').forEach(el => el.classList.remove('selected'));
    // Add selection to clicked option
    document.querySelector(`.mcq-option[data-index="${index}"]`)?.classList.add('selected');
}

// =====================
// CODE PROBLEM LOADING
// =====================
async function loadProblem() {
    const result = await apiGet(`/problems/${currentZone}/next`);

    if (!result) return;

    if (result.cleared) {
        showModal("🎉", "Zone Cleared!", "Congratulations! You've mastered all problems in this zone.\n\nTry another zone to continue your journey!", [], "victory");
        return;
    }

    currentProblem = result;
    currentMCQ = null;
    problemType = "code";

    // Update UI
    if (elements.difficultyBadge) {
        elements.difficultyBadge.textContent = result.difficulty.toUpperCase();
        elements.difficultyBadge.className = `difficulty-badge ${result.difficulty}`;
    }
    if (elements.problemTitle) elements.problemTitle.textContent = result.title;
    if (elements.problemDescription) elements.problemDescription.textContent = result.desc;
    if (elements.xpReward) elements.xpReward.textContent = `+${result.potential_xp} XP`;

    // Show code editor
    if (elements.codeEditor) {
        elements.codeEditor.style.display = "block";
        elements.codeEditor.value = result.code;
    }

    // Show test cases
    if (elements.testCases) {
        elements.testCases.innerHTML = "";
        result.tests.forEach((test, i) => {
            const testEl = document.createElement("div");
            testEl.className = "test-case";
            testEl.innerHTML = `
                <span class="test-case-label">Test ${i + 1}:</span>
                <span class="test-case-value">${JSON.stringify(test.input)}</span>
                <span class="test-case-arrow">→</span>
                <span class="test-case-expected">${JSON.stringify(test.expected)}</span>
            `;
            elements.testCases.appendChild(testEl);
        });
    }
}

function resetCode() {
    if (currentProblem && elements.codeEditor) {
        elements.codeEditor.value = currentProblem.code;
    }
}

function copyCode() {
    if (elements.codeEditor) {
        navigator.clipboard.writeText(elements.codeEditor.value).then(() => {
            if (elements.copyBtn) {
                elements.copyBtn.textContent = "✅";
                setTimeout(() => elements.copyBtn.textContent = "📋", 1500);
            }
        });
    }
}

// =====================
// SUBMISSION
// =====================
async function submitAnswer() {
    if (problemType === "mcq" && currentMCQ) {
        await submitMCQ();
    } else if (problemType === "code" && currentProblem) {
        await submitCode();
    } else {
        showModal("⚠️", "No Problem Loaded", "Click 'Load MCQ' or 'Load Battle' first!", [], "warning");
    }
}

async function submitMCQ() {
    const selected = document.querySelector('.mcq-option.selected');
    if (!selected) {
        showModal("⚠️", "No Selection", "Please select an answer!", [], "warning");
        return;
    }

    const selectedIndex = parseInt(selected.dataset.index);

    // Show loading state
    if (elements.submitBtn) {
        elements.submitBtn.disabled = true;
        elements.submitBtn.innerHTML = '<span class="btn-icon-text">⏳</span><span>Checking...</span>';
    }

    const result = await apiPost('/mcq/submit', {
        mcq_id: currentMCQ.id,
        selected: selectedIndex,
        zone: currentZone
    });

    // Reset button
    if (elements.submitBtn) {
        elements.submitBtn.disabled = false;
        elements.submitBtn.innerHTML = '<span class="btn-icon-text">🚀</span><span>Submit</span>';
    }

    if (!result) return;

    if (!result.correct) {
        // Mark wrong and correct
        selected.classList.add('wrong');
        document.querySelector(`.mcq-option[data-index="${result.correct_answer}"]`)?.classList.add('correct');

        showModal("❌", "Incorrect!", result.explanation, [], "failure");
        return;
    }

    // Victory!
    selected.classList.add('correct');
    showModal("🧠", "Correct!", `Intelligence +${result.xp_earned}!\n\nYour knowledge grows stronger!`, [
        { label: "Intelligence", value: result.new_intelligence }
    ], "victory");

    // Reload data
    await loadPlayerData();
    await loadZones();

    currentMCQ = null;
    updateUI();
}

async function submitCode() {
    const code = elements.codeEditor?.value || "";

    // Show loading state
    if (elements.submitBtn) {
        elements.submitBtn.disabled = true;
        elements.submitBtn.innerHTML = '<span class="btn-icon-text">⏳</span><span>Evaluating...</span>';
    }

    const result = await apiPost('/submit', {
        code: code,
        problem_id: currentProblem.id,
        zone: currentZone
    });

    // Reset button
    if (elements.submitBtn) {
        elements.submitBtn.disabled = false;
        elements.submitBtn.innerHTML = '<span class="btn-icon-text">🚀</span><span>Submit</span>';
    }

    if (!result) return;

    if (!result.success) {
        showModal("❌", "Battle Failed!", result.explanation, [
            { label: "Accuracy", value: Math.round(result.accuracy * 100) + "%" }
        ], "failure");
        return;
    }

    // Victory!
    showModal("🏆", "Victory!", `You defeated "${currentProblem.title}"!\n\nKeep pushing your limits, warrior!`, [
        { label: "Accuracy", value: Math.round(result.accuracy * 100) + "%" },
        { label: "XP Earned", value: "+" + result.xp_earned }
    ], "victory");

    // Reload data
    await loadPlayerData();
    await loadZones();

    currentProblem = null;
    if (elements.codeEditor) elements.codeEditor.value = "";
    updateUI();
}

// =====================
// MODAL
// =====================
function showModal(icon, title, message, stats, type) {
    if (elements.modalIcon) elements.modalIcon.textContent = icon;
    if (elements.modalTitle) {
        elements.modalTitle.textContent = title;
        elements.modalTitle.className = `modal-title ${type}`;
    }
    if (elements.modalMessage) elements.modalMessage.textContent = message;

    if (elements.modalStats) {
        elements.modalStats.innerHTML = "";
        stats.forEach(stat => {
            const statEl = document.createElement("div");
            statEl.className = "modal-stat";
            statEl.innerHTML = `
                <span class="modal-stat-value">${stat.value}</span>
                <span class="modal-stat-label">${stat.label}</span>
            `;
            elements.modalStats.appendChild(statEl);
        });
    }

    if (elements.modalOverlay) elements.modalOverlay.classList.add("active");
}

function closeModal() {
    if (elements.modalOverlay) elements.modalOverlay.classList.remove("active");
}

// =====================
// START THE GAME
// =====================
init();
