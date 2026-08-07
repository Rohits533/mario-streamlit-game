import streamlit as st

st.set_page_config(
    page_title="Super Mario: Infinite Deluxe Ultimate",
    page_icon="🍄",
    layout="centered"
)

st.markdown("""
<style>
    .stApp {
        background-color: #050508;
        color: white;
    }
    .arcade-header {
        text-align: center;
        font-family: 'Courier New', Courier, monospace;
        color: #ffcc00;
        text-shadow: 3px 3px #ff0000;
        margin-bottom: 0px;
        letter-spacing: 2px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='arcade-header'>🍄 SUPER MARIO: ULTIMATE INFINITE DELUXE 🍄</h1>", unsafe_allow_html=True)

game_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        body {
            margin: 0;
            background: #050508;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-family: 'Courier New', Courier, monospace;
            color: white;
            overflow: hidden;
        }
        .game-wrapper {
            position: relative;
            text-align: center;
        }
        canvas {
            border: 4px solid #fff;
            background: linear-gradient(to bottom, #2b6cb0 0%, #63b3ed 70%, #e2e8f0 100%);
            box-shadow: 0 0 50px rgba(43, 108, 176, 0.8);
            image-rendering: pixelated;
            image-rendering: crisp-edges;
        }
        .hud-panel {
            margin-top: 8px;
            display: flex;
            justify-content: space-between;
            width: 768px;
            font-size: 13px;
            font-weight: bold;
            background: rgba(15, 15, 25, 0.95);
            padding: 8px 12px;
            border: 2px solid #555;
            box-sizing: border-box;
            border-radius: 4px;
        }
        .btn-arcade {
            background: #e74c3c;
            color: white;
            border: 2px solid #fff;
            padding: 6px 12px;
            font-family: 'Courier New', Courier, monospace;
            font-weight: bold;
            cursor: pointer;
            text-transform: uppercase;
            box-shadow: 0 4px #990000;
            border-radius: 3px;
        }
        .btn-arcade:active {
            transform: translateY(2px);
            box-shadow: 0 2px #990000;
        }
        /* Entry Menu & Settings Overlays */
        #entryScreen, #settingsModal {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 580px;
            background: rgba(10, 10, 18, 0.98);
            border: 4px solid #f1c40f;
            padding: 25px;
            z-index: 20;
            box-shadow: 0 0 80px rgba(241, 196, 15, 0.8);
            text-align: center;
            border-radius: 8px;
        }
        #settingsModal {
            display: none;
            z-index: 25;
            text-align: left;
        }
        .store-grid {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 10px;
            margin-top: 15px;
        }
        .store-item {
            background: #161622;
            border: 2px solid #333;
            padding: 8px;
            text-align: center;
            border-radius: 4px;
        }
        .form-control-group {
            margin-top: 10px;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }
        .form-control-group label {
            font-size: 11px;
            color: #f1c40f;
        }
        .form-control-group input, .form-control-group select {
            background: #222;
            color: white;
            border: 1px solid #555;
            padding: 5px;
            font-family: 'Courier New';
            border-radius: 3px;
        }
        #storeModal, #customMakerModal {
            display: none;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 580px;
            background: rgba(10, 10, 18, 0.98);
            border: 4px solid #f1c40f;
            padding: 20px;
            z-index: 10;
            box-shadow: 0 0 80px rgba(241, 196, 15, 0.8);
            text-align: left;
            border-radius: 6px;
            max-height: 420px;
            overflow-y: auto;
        }
    </style>
</head>
<body>

<div class="game-wrapper">
    <canvas id="gameCanvas" width="768" height="432"></canvas>
    
    <!-- Entry / Main Menu Screen -->
    <div id="entryScreen">
        <h1 style="color: #ffcc00; text-shadow: 2px 2px #ff0000; font-size: 26px; margin-top:0;">🍄 SUPER MARIO 🍄</h1>
        <div style="font-size: 13px; color: #3498db; margin-bottom: 25px; letter-spacing: 1px;">INFINITE DELUXE ULTIMATE EDITION</div>
        <div style="display: flex; flex-direction: column; gap: 12px; width: 70%; margin: 0 auto;">
            <button class="btn-arcade" onclick="startGame()" style="background:#27ae60; font-size:16px; padding:12px;">▶ BEGIN GAME</button>
            <button class="btn-arcade" onclick="openSettingsMenu()" style="background:#2980b9; font-size:14px; padding:10px;">⚙ SETTINGS</button>
        </div>
    </div>

    <!-- Settings Menu Modal -->
    <div id="settingsModal">
        <h2 style="color: #2980b9; margin-top: 0; text-align: center; text-shadow: 1px 1px #000;">⚙ GAME SETTINGS</h2>
        <div class="form-control-group">
            <label>BGM Music Volume: <span id="volVal">50%</span></label>
            <input type="range" id="musicVol" min="0" max="100" value="50" oninput="updateMusicVolume(this.value)">
        </div>
        <div class="form-control-group">
            <label>SFX Sound Effects:</label>
            <select id="sfxToggle">
                <option value="on">Enabled</option>
                <option value="off">Muted</option>
            </select>
        </div>
        <div style="text-align: center; margin-top: 20px;">
            <button class="btn-arcade" onclick="closeSettingsMenu()" style="background: #27ae60; width: 100%;">SAVE & BACK</button>
        </div>
    </div>

    <div class="hud-panel">
        <div>KEYS: ARROWS / SPACE / X (SKILL) | SCORE: <span id="hudScore">0</span> | COINS: <span id="hudCoins">100</span></div>
        <div>
            <button class="btn-arcade" onclick="openStore()" style="background:#27ae60;">SHOP</button>
            <button class="btn-arcade" onclick="openCustomMaker()" style="background:#2980b9;">BUILDER</button>
            <button class="btn-arcade" onclick="togglePause()" id="pauseBtn">PAUSE</button>
        </div>
    </div>

    <!-- Store Modal -->
    <div id="storeModal">
        <h2 style="color: #f1c40f; margin-top: 0; text-align: center; text-shadow: 1px 1px #000;">🍄 TOAD'S ULTIMATE BOUTIQUE</h2>
        <div style="font-size: 12px; color: #ccc; text-align: center;">Unlock elite heroes and legendary character outfits!</div>
        
        <div style="margin-top: 12px; font-weight: bold; color: #3498db; font-size:12px;">CHOOSE HERO:</div>
        <div style="display: flex; gap: 6px; margin-top: 4px;">
            <button class="btn-arcade" onclick="selectCharacter('mario')" style="flex:1; background:#c84c0c; font-size:10px;" id="charMario">Mario (Dash)</button>
            <button class="btn-arcade" onclick="selectCharacter('luigi')" style="flex:1; background:#27ae60; font-size:10px;" id="charLuigi">Luigi (MegaJump)</button>
            <button class="btn-arcade" onclick="selectCharacter('peach')" style="flex:1; background:#f39c12; font-size:10px;" id="charPeach">Peach (Hover)</button>
            <button class="btn-arcade" onclick="selectCharacter('yoshi')" style="flex:1; background:#2ecc71; font-size:10px;" id="charYoshi">Yoshi (Double)</button>
        </div>

        <div style="margin-top: 12px; font-weight: bold; color: #f39c12; font-size:12px;">WARDROBE SKINS:</div>
        <div class="store-grid">
            <div class="store-item" id="skin_classic">
                <div style="font-weight:bold; font-size:11px;">Classic</div>
                <button class="btn-arcade" style="margin-top:6px; font-size:9px;" onclick="buySkin('classic', 0)">Equipped</button>
            </div>
            <div class="store-item" id="skin_fire">
                <div style="font-weight:bold; font-size:11px;">Fire (40c)</div>
                <button class="btn-arcade" style="margin-top:6px; font-size:9px;" onclick="buySkin('fire', 40)">Unlock</button>
            </div>
            <div class="store-item" id="skin_gold">
                <div style="font-weight:bold; font-size:11px;">Gold (90c)</div>
                <button class="btn-arcade" style="margin-top:6px; font-size:9px;" onclick="buySkin('gold', 90)">Unlock</button>
            </div>
            <div class="store-item" id="skin_dark">
                <div style="font-weight:bold; font-size:11px;">Dark (150c)</div>
                <button class="btn-arcade" style="margin-top:6px; font-size:9px;" onclick="buySkin('dark', 150)">Unlock</button>
            </div>
            <div class="store-item" id="skin_galaxy">
                <div style="font-weight:bold; font-size:11px;">Galaxy (250c)</div>
                <button class="btn-arcade" style="margin-top:6px; font-size:9px;" onclick="buySkin('galaxy', 250)">Unlock</button>
            </div>
            <div class="store-item" id="skin_rainbow">
                <div style="font-weight:bold; font-size:11px;">Rainbow (400c)</div>
                <button class="btn-arcade" style="margin-top:6px; font-size:9px;" onclick="buySkin('rainbow', 400)">Unlock</button>
            </div>
        </div>

        <div style="text-align: center; margin-top: 15px;">
            <button class="btn-arcade" onclick="closeStore()" style="background: #27ae60; width: 100%;">BACK TO GAME</button>
        </div>
    </div>

    <!-- Custom Level & Rule Maker Form Modal -->
    <div id="customMakerModal">
        <h2 style="color: #2980b9; margin-top: 0; text-align: center; text-shadow: 1px 1px #000;">⚙️ CUSTOM GAME WORKSHOP</h2>
        <div style="font-size: 11px; color: #ccc; text-align: center;">Tweak physics, speed, gravity, and environment parameters in real-time!</div>
        
        <div class="form-control-group">
            <label>Player Movement Speed: <span id="valSpeed">4.2</span></label>
            <input type="range" id="customSpeed" min="2.0" max="8.0" step="0.1" value="4.2" oninput="updateCustomParam('speed', this.value)">
        </div>

        <div class="form-control-group">
            <label>Jump Power: <span id="valJump">-12.5</span></label>
            <input type="range" id="customJump" min="-18.0" max="-8.0" step="0.5" value="-12.5" oninput="updateCustomParam('jump', this.value)">
        </div>

        <div class="form-control-group">
            <label>Gravity Force: <span id="valGrav">0.5</span></label>
            <input type="range" id="customGrav" min="0.1" max="1.2" step="0.05" value="0.5" oninput="updateCustomParam('grav', this.value)">
        </div>

        <div class="form-control-group">
            <label>World Environment Theme:</label>
            <select id="customTheme" onchange="updateCustomParam('theme', this.value)">
                <option value="classic">Classic Overworld</option>
                <option value="midnight">Midnight Galaxy</option>
                <option value="neon">Neon Cyberpunk</option>
                <option value="sunset">Sunset Volcano</option>
            </select>
        </div>

        <div style="text-align: center; margin-top: 18px;">
            <button class="btn-arcade" onclick="closeCustomMaker()" style="background: #2980b9; width: 100%;">APPLY & PLAY</button>
        </div>
    </div>
</div>

<script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    ctx.imageSmoothingEnabled = false;

    let gameStarted = false;
    let score = 0;
    let coinsCollected = 100;
    let isPaused = true;
    const keys = {};

    let cameraX = 0;
    let lastGeneratedX = 0;

    let selectedChar = 'mario';
    let currentSkin = 'classic';
    let unlockedSkins = { classic: true, fire: false, gold: false, dark: false, galaxy: false, rainbow: false };

    let currentTheme = 'classic';

    // Official Synth/BGM Music Generator via Web Audio API
    let audioCtx = null;
    let musicInterval = null;
    let musicVolume = 0.5;

    function initMusic() {
        if (!audioCtx) {
            audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        }
        if (audioCtx.state === 'suspended') {
            audioCtx.resume();
        }
    }

    function playNote(freq, duration, type='square') {
        if (!audioCtx || musicVolume === 0) return;
        try {
            let osc = audioCtx.createOscillator();
            let gain = audioCtx.createGain();
            osc.type = type;
            osc.frequency.value = freq;
            
            gain.gain.setValueAtTime(musicVolume * 0.15, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + duration);
            
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            
            osc.start();
            osc.stop(audioCtx.currentTime + duration);
        } catch(e) {}
    }

    // Official Classic Overworld Theme Melody Pattern
    const melodyNotes = [
        659.25, 659.25, 0, 659.25, 0, 523.25, 659.25, 0, 783.99, 0, 0, 0, 392.00, 0, 0, 0,
        523.25, 0, 0, 392.00, 0, 0, 329.63, 0, 0, 440.00, 0, 493.88, 0, 466.16, 440.00, 0
    ];
    let noteIndex = 0;

    function startBGM() {
        if (musicInterval) clearInterval(musicInterval);
        musicInterval = setInterval(() => {
            if (!isPaused && gameStarted) {
                let freq = melodyNotes[noteIndex];
                if (freq > 0) {
                    playNote(freq, 0.18, 'square');
                }
                noteIndex = (noteIndex + 1) % melodyNotes.length;
            }
        }, 140);
    }

    function updateMusicVolume(val) {
        musicVolume = val / 100;
        document.getElementById('volVal').innerText = val + '%';
    }

    function startGame() {
        initMusic();
        gameStarted = true;
        isPaused = false;
        document.getElementById('entryScreen').style.display = 'none';
        startBGM();
    }

    function openSettingsMenu() {
        document.getElementById('settingsModal').style.display = 'block';
    }

    function closeSettingsMenu() {
        document.getElementById('settingsModal').style.display = 'none';
    }

    const player = {
        x: 64,
        y: 200,
        width: 32,
        height: 32,
        vx: 0,
        vy: 0,
        speed: 4.2,
        jumpPower: -12.5,
        gravity: 0.5,
        grounded: false,
        facing: 'right',
        canDoubleJump: false,
        dashCooldown: 0
    };

    let platforms = [];
    let enemies = [];
    let coins = [];
    let decorations = [];
    let hazards = [];
    let movingPlatforms = [];
    let thwomps = [];
    let fireBars = [];
    let particles = [];

    function updateCharacterStats() {
        if (selectedChar === 'mario') {
            player.speed = 4.3;
            player.jumpPower = -12.5;
        } else if (selectedChar === 'luigi') {
            player.speed = 4.0;
            player.jumpPower = -14.5;
        } else if (selectedChar === 'peach') {
            player.speed = 3.8;
            player.jumpPower = -11.5;
        } else if (selectedChar === 'yoshi') {
            player.speed = 4.5;
            player.jumpPower = -12.0;
        }
    }

    function selectCharacter(char) {
        selectedChar = char;
        updateCharacterStats();
        document.querySelectorAll('[id^=char]').forEach(b => b.style.border = "2px solid #fff");
        document.getElementById('char' + char.charAt(0).toUpperCase() + char.slice(1)).style.border = "4px solid #f1c40f";
    }

    function buySkin(skinName, cost) {
        if (unlockedSkins[skinName]) {
            currentSkin = skinName;
            alert("Equipped " + skinName + "!");
        } else {
            if (coinsCollected >= cost) {
                coinsCollected -= cost;
                unlockedSkins[skinName] = true;
                currentSkin = skinName;
                alert("Purchased and equipped " + skinName + "!");
            } else {
                alert("Not enough coins! Collect more in the game!");
            }
        }
    }

    function openStore() {
        isPaused = true;
        document.getElementById("storeModal").style.display = "block";
    }

    function closeStore() {
        isPaused = false;
        document.getElementById("storeModal").style.display = "none";
    }

    function openCustomMaker() {
        isPaused = true;
        document.getElementById("customMakerModal").style.display = "block";
    }

    function closeCustomMaker() {
        isPaused = false;
        document.getElementById("customMakerModal").style.display = "none";
    }

    function updateCustomParam(param, val) {
        if (param === 'speed') {
            player.speed = parseFloat(val);
            document.getElementById('valSpeed').innerText = val;
        } else if (param === 'jump') {
            player.jumpPower = parseFloat(val);
            document.getElementById('valJump').innerText = val;
        } else if (param === 'grav') {
            player.gravity = parseFloat(val);
            document.getElementById('valGrav').innerText = val;
        } else if (param === 'theme') {
            currentTheme = val;
        }
    }

    function togglePause() {
        isPaused = !isPaused;
        document.getElementById("pauseBtn").innerText = isPaused ? "RESUME" : "PAUSE";
    }

    function addGround(startX, width, type='ground') {
        platforms.push({ x: startX, y: 384, width: width, height: 48, type: type });
    }

    function addPipe(x, height) {
        platforms.push({ x: x, y: 384 - height, width: 64, height: height, type: 'pipe' });
    }

    function addQuestionBlock(x, y, hasCoin=true) {
        platforms.push({ x: x, y: y, width: 32, height: 32, type: 'question' });
        if (hasCoin) coins.push({ x: x + 16, y: y - 24, radius: 9, collected: false });
    }

    function addBrick(x, y) {
        platforms.push({ x: x, y: y, width: 32, height: 32, type: 'brick' });
    }

    function addGoomba(x, y) {
        enemies.push({ x: x, y: y, width: 32, height: 32, vx: -1.5, alive: true, vy: 0 });
    }

    function spawnParticles(x, y, color) {
        for (let i = 0; i < 8; i++) {
            particles.push({
                x: x, y: y,
                vx: (Math.random() - 0.5) * 6,
                vy: (Math.random() - 0.7) * 6,
                color: color,
                life: 35
            });
        }
    }

    function generateChunk() {
        let groundWidth = 700 + Math.random() * 350;
        let biomeRand = Math.random();
        
        let surfaceType = 'ground';
        if (biomeRand > 0.65) surfaceType = 'ice';
        else if (biomeRand > 0.35) surfaceType = 'quicksand';

        addGround(lastGeneratedX, groundWidth, surfaceType);

        decorations.push({ x: lastGeneratedX + Math.random() * 120, y: 40, type: 'cloud', scale: 1.2 });
        decorations.push({ x: lastGeneratedX + 350 + Math.random() * 150, y: 30, type: 'cloud', scale: 0.9 });
        decorations.push({ x: lastGeneratedX + Math.random() * 250, y: 352, type: 'bush' });
        decorations.push({ x: lastGeneratedX + 450 + Math.random() * 200, y: 352, type: 'castle' });

        for (let cx = lastGeneratedX + 40; cx < lastGeneratedX + groundWidth - 80; cx += 65) {
            coins.push({ x: cx, y: 240 + Math.sin(cx * 0.06) * 50, radius: 9, collected: false });
        }

        let pattern = Math.floor(Math.random() * 6);
        
        if (pattern === 0) {
            addPipe(lastGeneratedX + 160, 60);
            addPipe(lastGeneratedX + 380, 90);
            addQuestionBlock(lastGeneratedX + 270, 250);
            addGoomba(lastGeneratedX + 240, 352);
            addGoomba(lastGeneratedX + 460, 352);
        } else if (pattern === 1) {
            addBrick(lastGeneratedX + 220, 260);
            addQuestionBlock(lastGeneratedX + 252, 260);
            addBrick(lastGeneratedX + 284, 260);
            hazards.push({ x: lastGeneratedX + 330, y: 368, width: 90, height: 16, type: 'spikes' });
            addGoomba(lastGeneratedX + 450, 352);
        } else if (pattern === 2) {
            thwomps.push({ x: lastGeneratedX + 300, y: 60, startY: 60, width: 40, height: 40, timer: 0, crushing: false });
            fireBars.push({ x: lastGeneratedX + 440, y: 300, angle: 0, length: 55, speed: 0.055 });
        } else if (pattern === 3) {
            movingPlatforms.push({ 
                x: lastGeneratedX + 150, y: 260, width: 80, height: 16, 
                minX: lastGeneratedX + 130, maxX: lastGeneratedX + 430, vx: 1.9 
            });
            hazards.push({ x: lastGeneratedX + 130, y: 392, width: 320, height: 40, type: 'lava' });
        } else if (pattern === 4) {
            fireBars.push({ x: lastGeneratedX + 240, y: 290, angle: 0, length: 45, speed: -0.07 });
            fireBars.push({ x: lastGeneratedX + 410, y: 290, angle: 1.5, length: 45, speed: 0.07 });
            addGoomba(lastGeneratedX + 330, 352);
        } else if (pattern === 5) {
            for (let i = 0; i < 4; i++) {
                addBrick(lastGeneratedX + 200 + (i*32), 352 - ((i+1)*32));
            }
            hazards.push({ x: lastGeneratedX + 360, y: 368, width: 70, height: 16, type: 'spikes' });
            addGoomba(lastGeneratedX + 470, 352);
        }

        lastGeneratedX += groundWidth;
        
        let pitSize = 80 + Math.random() * 80;
        if (Math.random() > 0.2) {
            hazards.push({ x: lastGeneratedX, y: 392, width: pitSize, height: 40, type: 'lava' });
        }
        lastGeneratedX += pitSize;
    }

    addGround(0, 900, 'ground');
    lastGeneratedX = 900;
    generateChunk();

    window.addEventListener("keydown", (e) => {
        keys[e.code] = true;
        if(["Space", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", "KeyX"].includes(e.code)) {
            e.preventDefault();
        }
        if (e.code === "KeyX") {
            triggerActiveSkill();
        }
    });

    window.addEventListener("keyup", (e) => {
        keys[e.code] = false;
    });

    function triggerActiveSkill() {
        if (selectedChar === 'mario' && player.dashCooldown <= 0) {
            player.vx += (player.facing === 'right' ? 14 : -14);
            player.dashCooldown = 60;
            spawnParticles(player.x + 16, player.y + 16, '#e74c3c');
        }
    }

    function resetPlayer() {
        spawnParticles(player.x + 16, player.y + 16, '#e74c3c');
        player.x = cameraX + 64;
        player.y = 100;
        player.vy = 0;
        player.vx = 0;
        score = Math.max(0, score - 200);
    }

    function update() {
        if (isPaused) return;

        if (player.dashCooldown > 0) player.dashCooldown--;

        let currentPlatformType = 'ground';
        platforms.forEach(p => {
            if (player.x + player.width > p.x && player.x < p.x + p.width && Math.abs((player.y + player.height) - p.y) < 6) {
                currentPlatformType = p.type;
            }
        });

        let acceleration = 0.45;
        let friction = 0.85;
        if (currentPlatformType === 'ice') friction = 0.98;
        else if (currentPlatformType === 'quicksand') player.vx *= 0.6;

        if (keys["ArrowLeft"]) {
            player.vx -= acceleration;
            if (player.vx < -player.speed) player.vx = -player.speed;
            player.facing = 'left';
        } else if (keys["ArrowRight"]) {
            player.vx += acceleration;
            if (player.vx > player.speed) player.vx = player.speed;
            player.facing = 'right';
        } else {
            player.vx *= friction;
        }

        player.x += player.vx;
        if (player.x < cameraX + 8) player.x = cameraX + 8;

        let targetCameraX = player.x - 250;
        if (targetCameraX > cameraX) {
            cameraX = targetCameraX;
        }

        if (player.x + canvas.width > lastGeneratedX - 700) {
            generateChunk();
        }

        let grav = player.gravity;
        if (selectedChar === 'peach' && keys["ArrowUp"] && player.vy > 0) {
            grav = 0.1;
        }

        player.vy += grav;
        player.y += player.vy;
        
        player.grounded = false;

        platforms.forEach(platform => {
            if (
                player.x < platform.x + platform.width &&
                player.x + player.width > platform.x &&
                player.y + player.height >= platform.y &&
                player.y + player.height - player.vy <= platform.y + 14 &&
                player.vy >= 0
            ) {
                player.y = platform.y - player.height;
                player.vy = 0;
                player.grounded = true;
                player.canDoubleJump = true;
                if (platform.type === 'quicksand') player.y += 1.8;
            }
        });

        movingPlatforms.forEach(mp => {
            mp.x += mp.vx;
            if (mp.x < mp.minX || mp.x > mp.maxX) mp.vx *= -1;

            if (
                player.x < mp.x + mp.width &&
                player.x + player.width > mp.x &&
                player.y + player.height >= mp.y &&
                player.y + player.height - player.vy <= mp.y + 12 &&
                player.vy >= 0
            ) {
                player.y = mp.y - player.height;
                player.vy = 0;
                player.grounded = true;
                player.canDoubleJump = true;
                player.x += mp.vx;
            }
        });

        if (keys["ArrowUp"] || keys["Space"]) {
            if (player.grounded) {
                player.vy = player.jumpPower;
                player.grounded = false;
                spawnParticles(player.x + 16, player.y + 32, '#fff');
            } else if (selectedChar === 'yoshi' && player.canDoubleJump) {
                player.vy = player.jumpPower * 0.9;
                player.canDoubleJump = false;
                spawnParticles(player.x + 16, player.y + 16, '#2ecc71');
            }
        }

        thwomps.forEach(t => {
            if (Math.abs(player.x - t.x) < 130) t.crushing = true;
            if (t.crushing) {
                t.y += 8;
                if (t.y >= 340) t.y = 340;
                setTimeout(() => { t.crushing = false; }, 700);
            } else if (t.y > t.startY) {
                t.y -= 3;
            }
            if (player.x < t.x + t.width && player.x + player.width > t.x && player.y < t.y + t.height && player.y + player.height > t.y) {
                resetPlayer();
            }
        });

        fireBars.forEach(fb => {
            fb.angle += fb.speed;
            let tipX = fb.x + Math.cos(fb.angle) * fb.length;
            let tipY = fb.y + Math.sin(fb.angle) * fb.length;
            if (Math.hypot((player.x + player.width/2) - tipX, (player.y + player.height/2) - tipY) < 18) {
                resetPlayer();
            }
        });

        hazards.forEach(h => {
            if (player.x + player.width > h.x && player.x < h.x + h.width && player.y + player.height > h.y && player.y < h.y + h.height) {
                resetPlayer();
            }
        });

        enemies.forEach(enemy => {
            if (!enemy.alive) return;
            enemy.vy += player.gravity;
            enemy.y += enemy.vy;
            
            platforms.forEach(platform => {
                if (enemy.x < platform.x + platform.width && enemy.x + enemy.width > platform.x && enemy.y + enemy.height >= platform.y && enemy.y + enemy.height - enemy.vy <= platform.y + 14 && enemy.vy >= 0) {
                    enemy.y = platform.y - enemy.height;
                    enemy.vy = 0;
                }
            });

            enemy.x += enemy.vx;

            if (player.x < enemy.x + enemy.width && player.x + player.width > enemy.x && player.y < enemy.y + enemy.height && player.y + player.height > enemy.y) {
                if (player.vy > 0 && player.y + player.height - player.vy <= enemy.y + 14) {
                    enemy.alive = false;
                    player.vy = -10;
                    score += 200;
                    coinsCollected += 1;
                    spawnParticles(enemy.x + 16, enemy.y + 16, '#f1c40f');
                } else {
                    resetPlayer();
                }
            }
        });

        coins.forEach(coin => {
            if (!coin.collected) {
                let dist = Math.hypot(coin.x - (player.x + player.width / 2), coin.y - (player.y + player.height / 2));
                if (dist < coin.radius + player.width / 3) {
                    coin.collected = true;
                    score += 250;
                    coinsCollected += 1;
                    spawnParticles(coin.x, coin.y, '#f1c40f');
                }
            }
        });

        particles.forEach((p, index) => {
            p.x += p.vx;
            p.y += p.vy;
            p.life--;
            if (p.life <= 0) particles.splice(index, 1);
        });

        if (player.y > canvas.height + 80) resetPlayer();

        if (platforms.length > 80 && platforms[0].x < cameraX - 1000) {
            platforms = platforms.filter(p => p.x + p.width > cameraX - 800);
            enemies = enemies.filter(e => e.x > cameraX - 800);
            coins = coins.filter(c => c.x > cameraX - 800);
            hazards = hazards.filter(h => h.x + h.width > cameraX - 800);
            movingPlatforms = movingPlatforms.filter(mp => mp.x + mp.width > cameraX - 800);
            thwomps = thwomps.filter(t => t.x > cameraX - 800);
            fireBars = fireBars.filter(fb => fb.x > cameraX - 800);
            decorations = decorations.filter(d => d.x > cameraX - 800);
        }

        document.getElementById('hudScore').innerText = score;
        document.getElementById('hudCoins').innerText = coinsCollected;
    }

    function drawPlayer(x, y, facing) {
        let shirtColor = '#e74c3c';
        let overallColor = '#2980b9';
        let hatColor = '#c0392b';
        let skinTone = '#ffdbac';

        if (selectedChar === 'luigi') {
            shirtColor = '#2ecc71';
            hatColor = '#27ae60';
        } else if (selectedChar === 'peach') {
            shirtColor = '#f39c12';
            overallColor = '#e74c3c';
            hatColor = '#f1c40f';
        } else if (selectedChar === 'yoshi') {
            shirtColor = '#27ae60';
            overallColor = '#ffffff';
            hatColor = '#2ecc71';
        }

        if (currentSkin === 'fire') {
            shirtColor = '#ffffff';
            overallColor = '#e74c3c';
            hatColor = '#e74c3c';
        } else if (currentSkin === 'gold') {
            shirtColor = '#f1c40f';
            overallColor = '#d4ac0d';
            hatColor = '#f1c40f';
        } else if (currentSkin === 'dark') {
            shirtColor = '#34495e';
            overallColor = '#111111';
            hatColor = '#2c3e50';
        } else if (currentSkin === 'galaxy') {
            shirtColor = '#8e44ad';
            overallColor = '#2c3e50';
            hatColor = '#9b59b6';
        } else if (currentSkin === 'rainbow') {
            shirtColor = Math.random() > 0.5 ? '#e74c3c' : '#3498db';
            overallColor = '#f1c40f';
            hatColor = '#2ecc71';
        }

        ctx.fillStyle = 'rgba(0,0,0,0.3)';
        ctx.fillRect(x + 3, y + 30, 26, 4);

        ctx.fillStyle = hatColor;
        ctx.fillRect(x + (facing === 'right' ? 7 : 5), y, 22, 9);
        ctx.fillStyle = skinTone;
        ctx.fillRect(x + (facing === 'right' ? 11 : 5), y + 9, 16, 9);

        ctx.fillStyle = '#000';
        ctx.fillRect(x + (facing === 'right' ? 19 : 7), y + 11, 3, 4);
        ctx.fillRect(x + (facing === 'right' ? 13 : 11), y + 15, 8, 3);

        ctx.fillStyle = shirtColor;
        ctx.fillRect(x + 5, y + 18, 22, 10);
        ctx.fillStyle = overallColor;
        ctx.fillRect(x + 8, y + 22, 16, 6);

        ctx.fillStyle = '#f1c40f';
        ctx.fillRect(x + 9, y + 23, 3, 3);
        ctx.fillRect(x + 20, y + 23, 3, 3);

        ctx.fillStyle = '#4a2306';
        ctx.fillRect(x + (facing === 'right' ? 16 : 2), y + 28, 14, 4);
    }

    function drawGoomba(x, y) {
        ctx.fillStyle = '#78281f';
        ctx.fillRect(x + 2, y + 8, 28, 20);
        ctx.fillStyle = '#f5cba7';
        ctx.fillRect(x + 5, y + 12, 22, 10);
        ctx.fillStyle = '#000';
        ctx.fillRect(x + 8, y + 15, 3, 5);
        ctx.fillRect(x + 21, y + 15, 3, 5);
        ctx.fillStyle = '#512e5f';
        ctx.fillRect(x, y + 28, 12, 4);
        ctx.fillRect(x + 20, y + 28, 12, 4);
    }

    function drawThwomp(x, y) {
        ctx.fillStyle = '#34495e';
        ctx.fillRect(x, y, 40, 40);
        ctx.strokeStyle = '#1b2631';
        ctx.lineWidth = 3;
        ctx.strokeRect(x, y, 40, 40);
        ctx.fillStyle = '#e74c3c';
        ctx.fillRect(x + 5, y + 10, 10, 6);
        ctx.fillRect(x + 25, y + 10, 10, 6);
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(x + 8, y + 26, 24, 6);
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        ctx.save();
        ctx.translate(Math.floor(-cameraX), 0);

        decorations.forEach(dec => {
            if (dec.type === 'cloud') {
                ctx.fillStyle = "rgba(255, 255, 255, 0.85)";
                ctx.fillRect(dec.x, dec.y, 75, 22);
                ctx.fillRect(dec.x + 20, dec.y - 15, 35, 16);
            } else if (dec.type === 'bush') {
                ctx.fillStyle = currentTheme === 'neon' ? '#00ffcc' : '#1e8449';
                ctx.fillRect(dec.x, dec.y, 95, 32);
            } else if (dec.type === 'castle') {
                ctx.fillStyle = '#566573';
                ctx.fillRect(dec.x, dec.y - 30, 80, 62);
            }
        });

        platforms.forEach(platform => {
            if (platform.x + platform.width >= cameraX - 100 && platform.x <= cameraX + canvas.width + 100) {
                if (platform.type === 'ground') {
                    ctx.fillStyle = currentTheme === 'midnight' ? '#1b4f72' : (currentTheme === 'neon' ? '#8e44ad' : '#a04000');
                    ctx.fillRect(platform.x, platform.y, platform.width, platform.height + 250);
                    ctx.fillStyle = currentTheme === 'neon' ? '#00ffff' : '#27ae60';
                    ctx.fillRect(platform.x, platform.y, platform.width, 10);
                } else if (platform.type === 'ice') {
                    ctx.fillStyle = '#5499c7';
                    ctx.fillRect(platform.x, platform.y, platform.width, platform.height + 250);
                } else if (platform.type === 'quicksand') {
                    ctx.fillStyle = '#9a7d0a';
                    ctx.fillRect(platform.x, platform.y, platform.width, platform.height + 250);
                } else if (platform.type === 'brick') {
                    ctx.fillStyle = '#b03a2e';
                    ctx.fillRect(platform.x, platform.y, platform.width, platform.height);
                } else if (platform.type === 'question') {
                    ctx.fillStyle = '#d4ac0d';
                    ctx.fillRect(platform.x, platform.y, platform.width, platform.height);
                    ctx.fillStyle = '#ffffff';
                    ctx.font = "bold 20px 'Courier New'";
                    ctx.fillText("?", platform.x + 9, platform.y + 24);
                } else if (platform.type === 'pipe') {
                    ctx.fillStyle = '#27ae60';
                    ctx.fillRect(platform.x, platform.y, platform.width, platform.height);
                    ctx.fillRect(platform.x - 4, platform.y, platform.width + 8, 16);
                }
            }
        });

        movingPlatforms.forEach(mp => {
            ctx.fillStyle = '#8e44ad';
            ctx.fillRect(mp.x, mp.y, mp.width, mp.height);
        });

        hazards.forEach(h => {
            if (h.type === 'lava') {
                ctx.fillStyle = '#c0392b';
                ctx.fillRect(h.x, h.y, h.width, h.height);
            } else if (h.type === 'spikes') {
                ctx.fillStyle = '#7f8c8d';
                for (let sx = h.x; sx < h.x + h.width; sx += 16) {
                    ctx.beginPath();
                    ctx.moveTo(sx, h.y + h.height);
                    ctx.lineTo(sx + 8, h.y);
                    ctx.lineTo(sx + 16, h.y + h.height);
                    ctx.fill();
                }
            }
        });

        fireBars.forEach(fb => {
            ctx.fillStyle = '#7f8c8d';
            ctx.beginPath();
            ctx.arc(fb.x, fb.y, 6, 0, Math.PI * 2);
            ctx.fill();
            for (let r = 12; r <= fb.length; r += 14) {
                let px = fb.x + Math.cos(fb.angle) * r;
                let py = fb.y + Math.sin(fb.angle) * r;
                ctx.fillStyle = '#e67e22';
                ctx.beginPath();
                ctx.arc(px, py, 6, 0, Math.PI * 2);
                ctx.fill();
            }
        });

        thwomps.forEach(t => {
            drawThwomp(t.x, t.y);
        });

        enemies.forEach(enemy => {
            if (enemy.alive) {
                drawGoomba(enemy.x, enemy.y);
            }
        });

        coins.forEach(coin => {
            if (!coin.collected) {
                ctx.fillStyle = '#f1c40f';
                ctx.beginPath();
                ctx.arc(coin.x, coin.y, coin.radius, 0, Math.PI * 2);
                ctx.fill();
                ctx.fillStyle = '#f39c12';
                ctx.beginPath();
                ctx.arc(coin.x, coin.y, coin.radius - 3, 0, Math.PI * 2);
                ctx.fill();
            }
        });

        particles.forEach(p => {
            ctx.fillStyle = p.color;
            ctx.fillRect(p.x, p.y, 4, 4);
        });

        drawPlayer(player.x, player.y, player.facing);

        ctx.restore();
    }

    function gameLoop() {
        update();
        draw();
        requestAnimationFrame(gameLoop);
    }

    requestAnimationFrame(gameLoop);
</script>

</body>
</html>
"""

st.components.v1.html(game_html, height=540, scrolling=False)
