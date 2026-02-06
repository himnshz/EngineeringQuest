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
let currentZone = "arrays";
let currentProblem = null;

// =====================
// DOM ELEMENTS
// =====================
const elements = {
    rankSymbol: document.getElementById("rank-symbol"),
    playerRank: document.getElementById("player-rank"),
    xpBar: document.getElementById("xp-bar"),
    xpText: document.getElementById("xp-text"),
    totalXp: document.getElementById("total-xp"),
    accuracy: document.getElementById("accuracy"),
    problemsSolved: document.getElementById("problems-solved"),
    zoneGrid: document.getElementById("zone-grid"),
    currentZone: document.getElementById("current-zone"),
    arenaZoneIcon: document.querySelector(".arena-zone-icon"),
    masteryBar: document.getElementById("mastery-bar"),
    masteryText: document.getElementById("mastery-text"),
    difficultyBadge: document.getElementById("difficulty-badge"),
    problemTitle: document.getElementById("problem-title"),
    problemDescription: document.getElementById("problem-description"),
    xpReward: document.getElementById("xp-reward"),
    testCases: document.getElementById("test-cases"),
    codeEditor: document.getElementById("code-editor"),
    loadBtn: document.getElementById("load-btn"),
    submitBtn: document.getElementById("submit-btn"),
    resetBtn: document.getElementById("reset-btn"),
    copyBtn: document.getElementById("copy-btn"),
    modalOverlay: document.getElementById("modal-overlay"),
    modalIcon: document.getElementById("modal-icon"),
    modalTitle: document.getElementById("modal-title"),
    modalMessage: document.getElementById("modal-message"),
    modalStats: document.getElementById("modal-stats"),
    modalClose: document.getElementById("modal-close"),
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
    elements.loadBtn.addEventListener("click", loadProblem);
    elements.submitBtn.addEventListener("click", submitCode);
    elements.resetBtn.addEventListener("click", resetCode);
    elements.copyBtn.addEventListener("click", copyCode);
    elements.modalClose.addEventListener("click", closeModal);
    elements.modalOverlay.addEventListener("click", (e) => {
        if (e.target === elements.modalOverlay) closeModal();
    });
}

// =====================
// DATA LOADING
// =====================
async function loadPlayerData() {
    player = await apiGet('/player');
    if (!player) {
        // Fallback to default if API fails
        player = {
            coding_xp: 0,
            rank: "Trainee",
            solved: [],
            accuracy: 1.0,
            mastery: { arrays: 0, recursion: 0, strings: 0 }
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
    elements.zoneGrid.innerHTML = "";

    Object.entries(zones).forEach(([key, zone]) => {
        const isActive = currentZone === key;

        const card = document.createElement("div");
        card.className = `zone-card ${isActive ? "active" : ""} ${!zone.unlocked ? "locked" : ""}`;
        card.innerHTML = `
            <span class="zone-icon">${zone.icon}</span>
            <div class="zone-info">
                <span class="zone-name">${zone.name}</span>
                <span class="zone-progress">${zone.unlocked ? `${zone.solved_count}/${zone.total_problems} solved` : `Unlock at ${zone.unlockXP} XP`}</span>
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
    elements.codeEditor.value = "";
    elements.problemTitle.textContent = "Load a Battle";
    elements.problemDescription.textContent = "Click \"Load Battle\" to start your coding adventure!";
    elements.testCases.innerHTML = "";
    elements.difficultyBadge.textContent = "---";
    elements.difficultyBadge.className = "difficulty-badge";
    elements.xpReward.textContent = "+0 XP";

    await loadZones();
    updateArenaHeader();
}

function updateUI() {
    if (!player) return;

    // Update rank
    elements.rankSymbol.textContent = player.rank_symbol || "⚔️";
    elements.playerRank.textContent = player.rank;

    // Update XP bar
    const currentXP = player.coding_xp;
    const nextRankXP = player.next_rank_xp || currentXP;

    // Find current rank threshold
    const RANKS = [
        { xp: 0, name: "Trainee" },
        { xp: 300, name: "Coder" },
        { xp: 800, name: "DSA Fighter" },
        { xp: 1500, name: "Algorithm Knight" },
        { xp: 3000, name: "Code Master" }
    ];

    let currentThreshold = 0;
    for (const rank of RANKS) {
        if (currentXP >= rank.xp) {
            currentThreshold = rank.xp;
        }
    }

    const progress = player.next_rank_xp
        ? ((currentXP - currentThreshold) / (nextRankXP - currentThreshold)) * 100
        : 100;

    elements.xpBar.style.width = Math.min(100, progress) + "%";
    elements.xpText.textContent = player.next_rank_xp
        ? `${currentXP} / ${nextRankXP} XP`
        : `${currentXP} XP (MAX)`;

    // Update stats
    elements.totalXp.textContent = player.coding_xp;
    elements.accuracy.textContent = Math.round(player.accuracy * 100) + "%";
    elements.problemsSolved.textContent = player.solved.length;

    // Update arena header
    updateArenaHeader();
}

function updateArenaHeader() {
    if (!zones) return;

    const zone = zones[currentZone];
    if (!zone) return;

    elements.currentZone.textContent = zone.name;
    if (elements.arenaZoneIcon) {
        elements.arenaZoneIcon.textContent = zone.icon;
    }

    const mastery = zone.mastery || 0;
    if (elements.masteryBar) {
        elements.masteryBar.style.width = mastery + "%";
    }
    elements.masteryText.textContent = mastery + "%";
}

// =====================
// PROBLEM LOADING
// =====================
async function loadProblem() {
    const result = await apiGet(`/problems/${currentZone}/next`);

    if (!result) return;

    if (result.cleared) {
        showModal("🎉", "Zone Cleared!", "Congratulations! You've mastered all problems in this zone.\n\nTry another zone to continue your journey!", [], "victory");
        return;
    }

    currentProblem = result;

    // Update UI
    elements.difficultyBadge.textContent = result.difficulty.toUpperCase();
    elements.difficultyBadge.className = `difficulty-badge ${result.difficulty}`;
    elements.problemTitle.textContent = result.title;
    elements.problemDescription.textContent = result.desc;
    elements.xpReward.textContent = `+${result.potential_xp} XP`;

    // Show test cases
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

    // Load code template
    elements.codeEditor.value = result.code;
}

function resetCode() {
    if (currentProblem) {
        elements.codeEditor.value = currentProblem.code;
    }
}

function copyCode() {
    navigator.clipboard.writeText(elements.codeEditor.value).then(() => {
        elements.copyBtn.textContent = "✅";
        setTimeout(() => elements.copyBtn.textContent = "📋", 1500);
    });
}

// =====================
// CODE SUBMISSION
// =====================
async function submitCode() {
    if (!currentProblem) {
        showModal("⚠️", "No Problem Loaded", "Click 'Load Battle' first to get a problem!", [], "warning");
        return;
    }

    const code = elements.codeEditor.value;

    // Show loading state
    elements.submitBtn.disabled = true;
    elements.submitBtn.innerHTML = '<span class="btn-icon-text">⏳</span><span>Evaluating...</span>';

    const result = await apiPost('/submit', {
        code: code,
        problem_id: currentProblem.id,
        zone: currentZone
    });

    // Reset button
    elements.submitBtn.disabled = false;
    elements.submitBtn.innerHTML = '<span class="btn-icon-text">🚀</span><span>Submit Code</span>';

    if (!result) return;

    if (!result.success) {
        // Failed
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

    // Prepare for next problem
    currentProblem = null;
    elements.codeEditor.value = "";
    updateUI();
}

// =====================
// MODAL
// =====================
function showModal(icon, title, message, stats, type) {
    elements.modalIcon.textContent = icon;
    elements.modalTitle.textContent = title;
    elements.modalTitle.className = `modal-title ${type}`;
    elements.modalMessage.textContent = message;

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

    elements.modalOverlay.classList.add("active");
}

function closeModal() {
    elements.modalOverlay.classList.remove("active");
}

// =====================
// START THE GAME
// =====================
init();
