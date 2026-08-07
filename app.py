import streamlit as st

st.set_page_config(
    page_title="Super Mario: Infinite Deluxe Ultimate",
    page_icon="🍄",
    layout="wide"
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
    /* Expand Streamlit container width */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100% !important;
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
            width: 100vw;
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        canvas {
            border: 4px solid #fff;
            background: linear-gradient(to bottom, #2b6cb0 0%, #63b3ed 70%, #e2e8f0 100%);
            box-shadow: 0 0 50px rgba(43, 108, 176, 0.8);
            image-rendering: pixelated;
            image-rendering: crisp-edges;
            width: 95vw;
            max-width: 1280px;
            height: auto;
            aspect-ratio: 16 / 9;
        }
        .hud-panel {
            margin-top: 10px;
            display: flex;
            justify-content: space-between;
            width: 95vw;
            max-width: 1280px;
            font-size: 14px;
            font-weight: bold;
            background: rgba(15, 15, 25, 0.95);
            padding: 10px 16px;
            border: 2px solid #555;
            box-sizing: border-box;
            border-radius: 4px;
        }
        .btn-arcade {
            background: #e74c3c;
            color: white;
            border: 2px solid #fff;
            padding: 8px 14px;
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
        #storeModal, #customMakerModal {
            display: none;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 620px;
            background: rgba(10, 10, 18, 0.98);
            border: 4px solid #f1c40f;
            padding: 25px;
            z-index: 10;
            box-shadow: 0 0 80px rgba(241, 196, 15, 0.8);
            text-align: left;
            border-radius: 6px;
            max-height: 85vh;
            overflow-y: auto;
        }
        .store-grid {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 12px;
            margin-top: 15px;
        }
        .store-item {
            background: #161622;
            border: 2px solid #333;
            padding: 10px;
            text-align: center;
            border-radius: 4px;
        }
        .form-control-group {
            margin-top: 12px;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }
        .form-control-group label {
            font-size: 12px;
            color: #f1c40f;
        }
        .form-control-group input, .form-control-group select {
            background: #222;
            color: white;
            border: 1px solid #555;
            padding: 8px;
            font-family: 'Courier New';
            border-radius: 3px;
        }
    </style>
</head>
<body>

<div class="game-wrapper">
    <canvas id="gameCanvas" width="1024" height="576"></canvas>
    
    <div class="hud-panel">
        <div>KEYS: ARROWS / SPACE / X (SKILL)</div>
        <div>
            <button class="btn-arcade" onclick="openStore()" style="background:#27ae60;">SHOP</button>
            <button class="btn-arcade" onclick="openCustomMaker()" style="background:#2980b9;">CUSTOM BUILDER</button>
            <button class="btn-arcade" onclick="togglePause()" id="pauseBtn">PAUSE</button>
        </div>
    </div>

    <!-- Store Modal -->
    <div id="storeModal">
        <h2 style="color: #f1c40f; margin-top: 0; text-align: center; text-shadow: 1px 1px #000;">🍄 TOAD'S ULTIMATE BOUTIQUE</h2>
        <div style="font-size: 13px; color: #ccc; text-align: center;">Unlock elite heroes and legendary character outfits!</div>
        
        <div style="margin-top: 15px; font-weight: bold; color: #3498db; font-size:13px;">CHOOSE HERO:</div>
        <div style="display: flex; gap: 8px; margin-top: 6px;">
            <button class="btn-arcade" onclick="selectCharacter('mario')" style="flex:1; background:#c84c0c; font-size:11px;" id="charMario">Mario (Dash)</button>
            <button class="btn-arcade" onclick="selectCharacter('luigi')" style="flex:1; background:#27ae60; font-size:11px;" id="charLuigi">Luigi (MegaJump)</button>
            <button class="btn-arcade" onclick="selectCharacter('peach')" style="flex:1; background:#f39c12; font-size:11px;" id="charPeach">Peach (Hover)</button>
            <button class="btn-arcade" onclick="selectCharacter('yoshi')" style="flex:1; background:#2ecc71; font-size:11px;" id="charYoshi">Yoshi (Double)</button>
        </div>

        <div style="margin-top: 15px; font-weight: bold; color: #f39c12; font-size:13px;">WARDROBE SKINS:</div>
        <div class="store-grid">
            <div class="store-item" id="skin_classic">
                <div style="font-weight:bold; font-size:12px;">Classic</div>
                <button class="btn-arcade" style="margin-top:8px; font-size:10px;" onclick="buySkin('classic', 0)">Equipped</button>
            </div>
            <div class="store-item" id="skin_fire">
                <div style="font-weight:bold; font-size:12px;">Fire (40c)</div>
                <button class="btn-arcade" style="margin-top:8px; font-size:10px;" onclick="buySkin('fire', 40)">Unlock</button>
            </div>
            <div class="store-item" id="skin_gold">
                <div style="font-weight:bold; font-size:12px;">Gold (90c)</div>
                <button class="btn-arcade" style="margin-top:8px; font-size:10px;" onclick="buySkin('gold', 90)">Unlock</button>
            </div>
            <div class="store-item" id="skin_dark">
                <div style="font-weight:bold; font-size:12px;">Dark (150c)</div>
                <button class="btn-arcade" style="margin-top:8px; font-size:10px;" onclick="buySkin('dark', 150)">Unlock</button>
            </div>
            <div class="store-item" id="skin_galaxy">
                <div style="font-weight:bold; font-size:12px;">Galaxy (250c)</div>
                <button class="btn-arcade" style="margin-top:8px; font-size:10px;" onclick="buySkin('galaxy', 250)">Unlock</button>
            </div>
            <div class="store-item" id="skin_rainbow">
                <div style="font-weight:bold; font-size:12px;">Rainbow (400c)</div>
                <button class="btn-arcade" style="margin-top:8px; font-size:10px;" onclick="buySkin('rainbow', 400)">Unlock</button>
            </div>
        </div>

        <div style="text-align: center; margin-top: 20px;">
            <button class="btn-arcade" onclick="closeStore()" style="background: #27ae60; width: 100%;">BACK TO GAME</button>
        </div>
    </div>

    <!-- Custom Level & Rule Maker Form Modal -->
    <div id="customMakerModal">
        <h2 style="color: #2980b9; margin-top: 0; text-align: center; text-shadow: 1px 1px #000;">⚙️ CUSTOM GAME WORKSHOP</h2>
        <div style="font-size: 12px; color: #ccc; text-align: center;">Tweak physics, speed, gravity, and environment parameters in real-time!</div>
        
        <div class="form-control-group">
            <label>Player Movement Speed: <span id="valSpeed">4.5</span></label>
            <input type="range" id="customSpeed" min="2.0" max="9.0" step="0.1" value="4.5" oninput="updateCustomParam('speed', this.value)">
        </div>

        <div class="form-control-group">
            <label>Jump Power: <span id="valJump">-13.5</span></label>
            <input type="range" id="customJump" min="-20.0" max="-9.0" step="0.5" value="-13.5" oninput="updateCustomParam('jump', this.value)">
        </div>

        <div class="form-control-group">
            <label>Gravity Force: <span id="valGrav">0.55</span></label>
            <input type="range" id="customGrav" min="0.1" max="1.2" step="0.05" value="0.55" oninput="updateCustomParam('grav', this.value)">
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

        <div style="text-align: center; margin-top: 20px;">
            <button class="btn-arcade" onclick="closeCustomMaker()" style="background: #2980b9; width: 100%;">APPLY & PLAY</button>
        </div>
    </div>
</div>

<script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    ctx.imageSmoothingEnabled = false;

    let score = 0;
    let coinsCollected = 100;
    let isPaused = false;
    const keys = {};

    let cameraX = 0;
    let lastGeneratedX = 0;

    let selectedChar = 'mario';
    let currentSkin = 'classic';
    let unlockedSkins = { classic: true, fire: false, gold: false, dark: false, galaxy: false, rainbow: false };

    let currentTheme = 'classic';

    const player = {
        x: 64,
        y: 300,
        width: 36,
        height: 36,
        vx: 0,
        vy: 0,
        speed: 4.5,
        jumpPower: -13.5,
        gravity: 0.55,
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
            player.speed = 4.6;
            player.jumpPower = -13.5;
        } else if (selectedChar === 'luigi') {
            player.speed = 4.3;
            player.jumpPower = -15.5;
        } else if (selectedChar === 'peach') {
            player.speed = 4.0;
            player.jumpPower = -12.5;
        } else if (selectedChar === 'yoshi') {
            player.speed = 4.8;
            player.jumpPower = -13.0;
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
        platforms.push({ x: startX, y: 500, width: width, height: 76, type: type });
    }

    function addPipe(x, height) {
        platforms.push({ x: x, y: 500 - height, width: 72, height: height, type: 'pipe' });
    }

    function addQuestionBlock(x, y, hasCoin=true) {
        platforms.push({ x: x, y: y, width: 36, height: 36, type: 'question' });
        if (hasCoin) coins.push({ x: x + 18, y: y - 26, radius: 10, collected: false });
    }

    function addBrick(x, y) {
        platforms.push({ x: x, y: y, width: 36, height: 36, type: 'brick' });
    }

    function addGoomba(x, y) {
        enemies.push({ x: x, y: y, width: 36, height: 36, vx: -1.8, alive: true, vy: 0 });
    }

    function spawnParticles(x, y, color) {
        for (let i = 0; i < 10; i++) {
            particles.push({
                x: x, y: y,
                vx: (Math.random() - 0.5) * 7,
                vy: (Math.random() - 0.7) * 7,
                color: color,
                life: 40
            });
        }
    }

    function generateChunk() {
        let groundWidth = 900 + Math.random() * 450;
        let biomeRand = Math.random();
        
        let surfaceType = 'ground';
        if (biomeRand > 0.65) surfaceType = 'ice';
        else if (biomeRand > 0.35) surfaceType = 'quicksand';

        addGround(lastGeneratedX, groundWidth, surfaceType);

        decorations.push({ x: lastGeneratedX + Math.random() * 150, y: 50, type: 'cloud', scale: 1.3 });
        decorations.push({ x: lastGeneratedX + 450 + Math.random() * 200, y: 40, type: 'cloud', scale: 1.0 });
        decorations.push({ x: lastGeneratedX + Math.random() * 300, y: 464, type: 'bush' });
        decorations.push({ x: lastGeneratedX + 600 + Math.random() * 250, y: 464, type: 'castle' });

        for (let cx = lastGeneratedX + 50; cx < lastGeneratedX + groundWidth - 100; cx += 75) {
            coins.push({ x: cx, y: 320 + Math.sin(cx * 0.05) * 70, radius: 10, collected: false });
        }

        let pattern = Math.floor(Math.random() * 6);
        
        if (pattern === 0) {
            addPipe(lastGeneratedX + 200, 75);
            addPipe(lastGeneratedX + 480, 110);
            addQuestionBlock(lastGeneratedX + 340, 320);
            addGoomba(lastGeneratedX + 300, 500);
            addGoomba(lastGeneratedX + 580, 500);
        } else if (pattern === 1) {
            addBrick(lastGeneratedX + 260, 330);
            addQuestionBlock(lastGeneratedX + 296, 330);
            addBrick(lastGeneratedX + 332, 330);
            hazards.push({ x: lastGeneratedX + 400, y: 480, width: 110, height: 20, type: 'spikes' });
            addGoomba(lastGeneratedX + 560, 500);
        } else if (pattern === 2) {
            thwomps.push({ x: lastGeneratedX + 380, y: 80, startY: 80, width: 48, height: 48, timer: 0, crushing: false });
            fireBars.push({ x: lastGeneratedX + 560, y: 380, angle: 0, length: 70, speed: 0.05 });
        } else if (pattern === 3) {
            movingPlatforms.push({ 
                x: lastGeneratedX + 200, y: 340, width: 100, height: 20, 
                minX: lastGeneratedX + 160, maxX: lastGeneratedX + 540, vx: 2.1 
            });
            hazards.push({ x: lastGeneratedX + 160, y: 536, width: 400, height: 40, type: 'lava' });
        } else if (pattern === 4) {
            fireBars.push({ x: lastGeneratedX + 300, y: 360, angle: 0, length: 60, speed: -0.06 });
            fireBars.push({ x: lastGeneratedX + 520, y: 360, angle: 1.5, length: 60, speed: 0.06 });
            addGoomba(lastGeneratedX + 410, 500);
        } else if (pattern === 5) {
            for (let i = 0; i < 5; i++) {
                addBrick(lastGeneratedX + 240 + (i*36), 500 - ((i+1)*36));
            }
            hazards.push({ x: lastGeneratedX + 450, y: 480, width: 90, height: 20, type: 'spikes' });
            addGoomba(lastGeneratedX + 600, 500);
        }

        lastGeneratedX += groundWidth;
        
        let pitSize = 100 + Math.random() * 100;
        if (Math.random() > 0.2) {
            hazards.push({ x: lastGeneratedX, y: 536, width: pitSize, height: 40, type: 'lava' });
        }
        lastGeneratedX += pitSize;
    }

    addGround(0, 1100, 'ground');
    lastGeneratedX = 1100;
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
            player.vx += (player.facing === 'right' ? 16 : -16);
            player.dashCooldown = 60;
            spawnParticles(player.x + 18, player.y + 18, '#e74c3c');
        }
    }

    function resetPlayer() {
        spawnParticles(player.x + 18, player.y + 18, '#e74c3c');
        player.x = cameraX + 80;
        player.y = 150;
        player.vy = 0;
        player.vx = 0;
        score = Math.max(0, score - 200);
    }

    function update() {
        if (isPaused) return;

        if (player.dashCooldown > 0) player.dashCooldown--;

        let currentPlatformType = 'ground';
        platforms.forEach(p => {
            if (player.x + player.width > p.x && player.x < p.x + p.width && Math.abs((player.y + player.height) - p.y) < 8) {
                currentPlatformType = p.type;
            }
        });

        let acceleration = 0.5;
        let friction = 0.84;
        if (currentPlatformType === 'ice') friction = 0.985;
        else if (currentPlatformType === 'quicksand') player.vx *= 0.55;

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
        if (player.x < cameraX + 10) player.x = cameraX + 10;

        let targetCameraX = player.x - 320;
        if (targetCameraX > cameraX) {
            cameraX = targetCameraX;
        }

        if (player.x + canvas.width > lastGeneratedX - 900) {
            generateChunk();
        }

        let grav = player.gravity;
        if (selectedChar === 'peach' && keys["ArrowUp"] && player.vy > 0) {
            grav = 0.12;
        }

        player.vy += grav;
        player.y += player.vy;
        
        player.grounded = false;

        platforms.forEach(platform => {
            if (
                player.x < platform.x + platform.width &&
                player.x + player.width > platform.x &&
                player.y + player.height >= platform.y &&
                player.y + player.height - player.vy <= platform.y + 16 &&
                player.vy >= 0
            ) {
                player.y = platform.y - player.height;
                player.vy = 0;
                player.grounded = true;
                player.canDoubleJump = true;
                if (platform.type === 'quicksand') player.y += 2.0;
            }
        });

        movingPlatforms.forEach(mp => {
            mp.x += mp.vx;
            if (mp.x < mp.minX || mp.x > mp.maxX) mp.vx *= -1;

            if (
                player.x < mp.x + mp.width &&
                player.x + player.width > mp.x &&
                player.y + player.height >= mp.y &&
                player.y + player.height - player.vy <= mp.y + 14 &&
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
                spawnParticles(player.x + 18, player.y + 36, '#fff');
            } else if (selectedChar === 'yoshi' && player.canDoubleJump) {
                player.vy = player.jumpPower * 0.9;
                player.canDoubleJump = false;
                spawnParticles(player.x + 18, player.y + 18, '#2ecc71');
            }
        }

        thwomps.forEach(t => {
            if (Math.abs(player.x - t.x) < 160) t.crushing = true;
            if (t.crushing) {
                t.y += 10;
                if (t.y >= 440) t.y = 440;
                setTimeout(() => { t.crushing = false; }, 700);
            } else if (t.y > t.startY) {
                t.y -= 4;
            }
            if (player.x < t.x + t.width && player.x + player.width > t.x && player.y < t.y + t.height && player.y + player.height > t.y) {
                resetPlayer();
            }
        });

        fireBars.forEach(fb => {
            fb.angle += fb.speed;
            let tipX = fb.x + Math.cos(fb.angle) * fb.length;
            let tipY = fb.y + Math.sin(fb.angle) * fb.length;
            if (Math.hypot((player.x + player.width/2) - tipX, (player.y + player.height/2) - tipY) < 20) {
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
                if (enemy.x < platform.x + platform.width && enemy.x + enemy.width > platform.x && enemy.y + enemy.height >= platform.y && enemy.y + enemy.height - enemy.vy <= platform.y + 16 && enemy.vy >= 0) {
                    enemy.y = platform.y - enemy.height;
                    enemy.vy = 0;
                }
            });

            enemy.x += enemy.vx;

            if (player.x < enemy.x + enemy.width && player.x + player.width > enemy.x && player.y < enemy.y + enemy.height && player.y + player.height > enemy.y) {
                if (player.vy > 0 && player.y + player.height - player.vy <= enemy.y + 16) {
                    enemy.alive = false;
                    player.vy = -12;
                    score += 200;
                    coinsCollected += 1;
                    spawnParticles(enemy.x + 18, enemy.y + 18, '#f1c40f');
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

        if (player.y > canvas.height + 100) resetPlayer();

        if (platforms.length > 90 && platforms[0].x < cameraX - 1200) {
            platforms = platforms.filter(p => p.x + p.width > cameraX - 1000);
            enemies = enemies.filter(e => e.x > cameraX - 1000);
            coins = coins.filter(c => c.x > cameraX - 1000);
            hazards = hazards.filter(h => h.x + h.width > cameraX - 1000);
            movingPlatforms = movingPlatforms.filter(mp => mp.x + mp.width > cameraX - 1000);
            thwomps = thwomps.filter(t => t.x > cameraX - 1000);
            fireBars = fireBars.filter(fb => fb.x > cameraX - 1000);
            decorations = decorations.filter(d => d.x > cameraX - 1000);
        }
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
        ctx.fillRect(x + 4, y + 32, 28, 4);

        ctx.fillStyle = hatColor;
        ctx.fillRect(x + (facing === 'right' ? 8 : 6), y, 24, 10);
        ctx.fillStyle = skinTone;
        ctx.fillRect(x + (facing === 'right' ? 12 : 6), y + 10, 18, 10);

        ctx.fillStyle = '#000';
        ctx.fillRect(x + (facing === 'right' ? 21 : 8), y + 12, 3, 4);
        ctx.fillRect(x + (facing === 'right' ? 14 : 12), y + 17, 9, 3);

        ctx.fillStyle = shirtColor;
        ctx.fillRect(x + 6, y + 20, 24, 11);
        ctx.fillStyle = overallColor;
        ctx.fillRect(x + 9, y + 24, 18, 7);

        ctx.fillStyle = '#f1c40f';
        ctx.fillRect(x + 10, y + 25, 3, 3);
        ctx.fillRect(x + 23, y + 25, 3, 3);

        ctx.fillStyle = '#4a2306';
        ctx.fillRect(x + (facing === 'right' ? 18 : 2), y + 31, 16, 5);
    }

    function drawGoomba(x, y) {
        ctx.fillStyle = '#78281f';
        ctx.fillRect(x + 2, y + 8, 32, 24);
        ctx.fillStyle = '#f5cba7';
        ctx.fillRect(x + 6, y + 13, 24, 11);
        ctx.fillStyle = '#000';
        ctx.fillRect(x + 9, y + 16, 3, 5);
        ctx.fillRect(x + 24, y + 16, 3, 5);
        ctx.fillStyle = '#512e5f';
        ctx.fillRect(x, y + 32, 14, 4);
        ctx.fillRect(x + 22, y + 32, 14, 4);
    }

    function drawThwomp(x, y) {
        ctx.fillStyle = '#34495e';
        ctx.fillRect(x, y, 48, 48);
        ctx.strokeStyle = '#1b2631';
        ctx.lineWidth = 3;
        ctx.strokeRect(x, y, 48, 48);
        ctx.fillStyle = '#e74c3c';
        ctx.fillRect(x + 6, y + 12, 12, 6);
        ctx.fillRect(x + 30, y + 12, 12, 6);
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(x + 9, y + 31, 30, 8);
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        ctx.save();
        ctx.translate(Math.floor(-cameraX), 0);

        decorations.forEach(dec => {
            if (dec.type === 'cloud') {
                ctx.fillStyle = "rgba(255, 255, 255, 0.85)";
                ctx.fillRect(dec.x, dec.y, 90, 26);
                ctx.fillRect(dec.x + 24, dec.y - 18, 42, 18);
            } else if (dec.type === 'bush') {
                ctx.fillStyle = currentTheme === 'neon' ? '#00ffcc' : '#1e8449';
                ctx.fillRect(dec.x, dec.y, 110, 36);
            } else if (dec.type === 'castle') {
                ctx.fillStyle = '#566573';
                ctx.fillRect(dec.x, dec.y - 35, 90, 71);
            }
        });

        platforms.forEach(platform => {
            if (platform.x + platform.width >= cameraX - 1200 && platform.x <= cameraX + canvas.width + 1200) {
                if (platform.type === 'ground') {
                    ctx.fillStyle = currentTheme === 'midnight' ? '#1b4f72' : (currentTheme === 'neon' ? '#8e44ad' : '#a04000');
                    ctx.fillRect(platform.x, platform.y, platform.width, platform.height + 300);
                    ctx.fillStyle = currentTheme === 'neon' ? '#00ffff' : '#27ae60';
                    ctx.fillRect(platform.x, platform.y, platform.width, 12);
                } else if (platform.type === 'ice') {
                    ctx.fillStyle = '#5499c7';
                    ctx.fillRect(platform.x, platform.y, platform.width, platform.height + 300);
                } else if (platform.type === 'quicksand') {
                    ctx.fillStyle = '#9a7d0a';
                    ctx.fillRect(platform.x, platform.y, platform.width, platform.height + 300);
                } else if (platform.type === 'brick') {
                    ctx.fillStyle = '#b03a2e';
                    ctx.fillRect(platform.x, platform.y, platform.width, platform.height);
                } else if (platform.type === 'question') {
                    ctx.fillStyle = '#d4ac0d';
                    ctx.fillRect(platform.x, platform.y, platform.width, platform.height);
                    ctx.fillStyle = '#ffffff';
                    ctx.font = "bold 22px 'Courier New'";
                    ctx.fillText("?", platform.x + 11, platform.y + 26);
                } else if (platform.type === 'pipe') {
                    ctx.fillStyle = '#27ae60';
                    ctx.fillRect(platform.x, platform.y, platform.width, platform.height);
                    ctx.fillRect(platform.x - 5, platform.y, platform.width + 10, 18);
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
                for (let sx = h.x; sx < h.x + h.width; sx += 18) {
                    ctx.beginPath();
                    ctx.moveTo(sx, h.y + h.height);
                    ctx.lineTo(sx + 9, h.y);
                    ctx.lineTo(sx + 18, h.y + h.height);
                    ctx.fill();
                }
            }
        });

        fireBars.forEach(fb => {
            ctx.strokeStyle = '#f39c12';
            ctx.lineWidth = 7;
            ctx.beginPath();
            ctx.moveTo(fb.x, fb.y);
            let endX = fb.x + Math.cos(fb.angle) * fb.length;
            let endY = fb.y + Math.sin(fb.angle) * fb.length;
            ctx.lineTo(endX, endY);
            ctx.stroke();
        });

        thwomps.forEach(t => drawThwomp(t.x, t.y));

        coins.forEach(coin => {
            if (!coin.collected && coin.x >= cameraX - 60 && coin.x <= cameraX + canvas.width + 60) {
                ctx.fillStyle = '#f1c40f';
                ctx.beginPath();
                ctx.arc(coin.x, coin.y, coin.radius, 0, Math.PI * 2);
                ctx.fill();
            }
        });

        enemies.forEach(enemy => {
            if (enemy.alive && enemy.x >= cameraX - 120 && enemy.x <= cameraX + canvas.width + 120) {
                drawGoomba(enemy.x, enemy.y);
            }
        });

        particles.forEach(p => {
            ctx.fillStyle = p.color;
            ctx.fillRect(p.x, p.y, 6, 6);
        });

        drawPlayer(player.x, player.y, player.facing);

        ctx.restore();

        ctx.fillStyle = "rgba(10, 10, 16, 0.95)";
        ctx.fillRect(0, 0, canvas.width, 56);

        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 15px 'Courier New'";
        ctx.fillText("MARIO WORKSHOP", 25, 32);
        ctx.fillText(String(score).padStart(6, '0'), 25, 50);

        ctx.fillText("COINS", 260, 32);
        ctx.fillText("x" + String(coinsCollected).padStart(2, '0'), 270, 50);

        ctx.fillText("THEME: " + currentTheme.toUpperCase(), 480, 32);
        ctx.fillText("HERO: " + selectedChar.toUpperCase(), 480, 50);

        ctx.fillText("DIST: " + Math.floor(cameraX / 10) + "m", 850, 42);
    }

    function loop() {
        update();
        draw();
        requestAnimationFrame(loop);
    }

    loop();
</script>

</body>
</html>
"""

st.components.v1.html(game_html, height=700, scrolling=False)
