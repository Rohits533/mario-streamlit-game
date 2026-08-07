import streamlit as st

st.set_page_config(
    page_title="Super Mario: Infinite Deluxe HD",
    page_icon="🍄",
    layout="centered"
)

st.markdown("""
<style>
    .stApp {
        background-color: #0d0d0d;
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

st.markdown("<h1 class='arcade-header'>🍄 SUPER MARIO: ULTIMATE HD DELUXE 🍄</h1>", unsafe_allow_html=True)

game_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        body {
            margin: 0;
            background: #0d0d0d;
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
            background: linear-gradient(to bottom, #5c94fc 0%, #b8d4fc 80%, #ffffff 100%);
            box-shadow: 0 0 35px rgba(92, 148, 252, 0.8);
            image-rendering: pixelated;
            image-rendering: crisp-edges;
        }
        .hud-panel {
            margin-top: 8px;
            display: flex;
            justify-content: space-between;
            width: 768px;
            font-size: 14px;
            font-weight: bold;
            background: rgba(30, 30, 30, 0.9);
            padding: 8px 12px;
            border: 2px solid #666;
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
        #storeModal {
            display: none;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 540px;
            background: rgba(10, 10, 15, 0.96);
            border: 4px solid #f1c40f;
            padding: 20px;
            z-index: 10;
            box-shadow: 0 0 60px rgba(241, 196, 15, 0.7);
            text-align: left;
            border-radius: 6px;
        }
        .store-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-top: 15px;
            max-height: 240px;
            overflow-y: auto;
        }
        .store-item {
            background: #1a1a1a;
            border: 2px solid #444;
            padding: 10px;
            text-align: center;
            border-radius: 4px;
        }
    </style>
</head>
<body>

<div class="game-wrapper">
    <canvas id="gameCanvas" width="768" height="432"></canvas>
    
    <div class="hud-panel">
        <div>CONTROLS: ARROWS / SPACE</div>
        <div>
            <button class="btn-arcade" onclick="openStore()">🍄 SHOP & CHARACTERS</button>
            <button class="btn-arcade" onclick="togglePause()" id="pauseBtn">PAUSE</button>
        </div>
    </div>

    <!-- Store & Character Selection Modal -->
    <div id="storeModal">
        <h2 style="color: #f1c40f; margin-top: 0; text-align: center; text-shadow: 1px 1px #000;">🍄 TOAD'S HD BOUTIQUE</h2>
        <div style="font-size: 12px; color: #ccc; text-align: center;">Spend your collected coins to upgrade heroes and unlock wardrobe skins!</div>
        
        <div style="margin-top: 15px; font-weight: bold; color: #3498db; font-size:13px;">CHOOSE HERO:</div>
        <div style="display: flex; gap: 8px; margin-top: 5px;">
            <button class="btn-arcade" onclick="selectCharacter('mario')" style="flex:1; background:#c84c0c;" id="charMario">Mario (Balanced)</button>
            <button class="btn-arcade" onclick="selectCharacter('luigi')" style="flex:1; background:#27ae60;" id="charLuigi">Luigi (Super Jump)</button>
            <button class="btn-arcade" onclick="selectCharacter('peach')" style="flex:1; background:#f39c12;" id="charPeach">Peach (Hover)</button>
        </div>

        <div style="margin-top: 15px; font-weight: bold; color: #f39c12; font-size:13px;">OUTFIT STYLES:</div>
        <div class="store-grid">
            <div class="store-item" id="skin_classic">
                <div style="font-weight:bold;">Classic Red</div>
                <div style="font-size:11px; color:#aaa;">Default Gear</div>
                <button class="btn-arcade" style="margin-top:8px; font-size:10px;" onclick="buySkin('classic', 0)">Equipped</button>
            </div>
            <div class="store-item" id="skin_fire">
                <div style="font-weight:bold;">Fire Power</div>
                <div style="font-size:11px; color:#aaa;">Cost: 40 Coins</div>
                <button class="btn-arcade" style="margin-top:8px; font-size:10px;" onclick="buySkin('fire', 40)">Unlock</button>
            </div>
            <div class="store-item" id="skin_gold">
                <div style="font-weight:bold;">Golden Star</div>
                <div style="font-size:11px; color:#aaa;">Cost: 100 Coins</div>
                <button class="btn-arcade" style="margin-top:8px; font-size:10px;" onclick="buySkin('gold', 100)">Unlock</button>
            </div>
            <div class="store-item" id="skin_dark">
                <div style="font-weight:bold;">Shadow Suit</div>
                <div style="font-size:11px; color:#aaa;">Cost: 200 Coins</div>
                <button class="btn-arcade" style="margin-top:8px; font-size:10px;" onclick="buySkin('dark', 200)">Unlock</button>
            </div>
        </div>

        <div style="text-align: center; margin-top: 18px;">
            <button class="btn-arcade" onclick="closeStore()" style="background: #27ae60; width: 100%;">RESUME GAME</button>
        </div>
    </div>
</div>

<script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    ctx.imageSmoothingEnabled = false;

    let score = 0;
    let coinsCollected = 0;
    let isPaused = false;
    const keys = {};

    let cameraX = 0;
    let lastGeneratedX = 0;

    let selectedChar = 'mario';
    let currentSkin = 'classic';
    let unlockedSkins = { classic: true, fire: false, gold: false, dark: false };

    const player = {
        x: 64,
        y: 200,
        width: 32,
        height: 32,
        vx: 0,
        vy: 0,
        speed: 4.0,
        jumpPower: -12.0,
        gravity: 0.5,
        grounded: false,
        facing: 'right'
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
            player.speed = 4.0;
            player.jumpPower = -12.0;
        } else if (selectedChar === 'luigi') {
            player.speed = 3.8;
            player.jumpPower = -14.2;
        } else if (selectedChar === 'peach') {
            player.speed = 3.6;
            player.jumpPower = -11.0;
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
                alert("Not enough coins! Keep running and collecting!");
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
        enemies.push({ x: x, y: y, width: 32, height: 32, vx: -1.3, alive: true, vy: 0 });
    }

    function spawnParticles(x, y, color) {
        for (let i = 0; i < 6; i++) {
            particles.push({
                x: x, y: y,
                vx: (Math.random() - 0.5) * 5,
                vy: (Math.random() - 0.7) * 5,
                color: color,
                life: 30
            });
        }
    }

    // High Density Procedural Generator with gorgeous obstacles & rich coin arcs
    function generateChunk() {
        let groundWidth = 720 + Math.random() * 350;
        let biomeRand = Math.random();
        
        let surfaceType = 'ground';
        if (biomeRand > 0.7) surfaceType = 'ice';
        else if (biomeRand > 0.45) surfaceType = 'quicksand';

        addGround(lastGeneratedX, groundWidth, surfaceType);

        decorations.push({ x: lastGeneratedX + Math.random() * 120, y: 50, type: 'cloud', scale: 1.2 });
        decorations.push({ x: lastGeneratedX + 350 + Math.random() * 150, y: 40, type: 'cloud', scale: 0.8 });
        decorations.push({ x: lastGeneratedX + Math.random() * 250, y: 352, type: 'bush' });
        decorations.push({ x: lastGeneratedX + 450 + Math.random() * 200, y: 352, type: 'hills' });

        // Plentiful flowing coin arches
        for (let cx = lastGeneratedX + 40; cx < lastGeneratedX + groundWidth - 80; cx += 70) {
            coins.push({ x: cx, y: 250 + Math.sin(cx * 0.05) * 45, radius: 9, collected: false });
        }

        let pattern = Math.floor(Math.random() * 6);
        
        if (pattern === 0) {
            addPipe(lastGeneratedX + 180, 56);
            addPipe(lastGeneratedX + 400, 80);
            addQuestionBlock(lastGeneratedX + 290, 260);
            addGoomba(lastGeneratedX + 260, 352);
            addGoomba(lastGeneratedX + 480, 352);
        } else if (pattern === 1) {
            addBrick(lastGeneratedX + 240, 270);
            addQuestionBlock(lastGeneratedX + 272, 270);
            addBrick(lastGeneratedX + 304, 270);
            hazards.push({ x: lastGeneratedX + 350, y: 368, width: 80, height: 16, type: 'spikes' });
            addGoomba(lastGeneratedX + 460, 352);
        } else if (pattern === 2) {
            thwomps.push({ x: lastGeneratedX + 320, y: 70, startY: 70, width: 40, height: 40, timer: 0, crushing: false });
            fireBars.push({ x: lastGeneratedX + 460, y: 310, angle: 0, length: 50, speed: 0.05 });
        } else if (pattern === 3) {
            movingPlatforms.push({ 
                x: lastGeneratedX + 160, y: 270, width: 75, height: 16, 
                minX: lastGeneratedX + 140, maxX: lastGeneratedX + 440, vx: 1.7 
            });
            hazards.push({ x: lastGeneratedX + 140, y: 392, width: 310, height: 40, type: 'lava' });
        } else if (pattern === 4) {
            fireBars.push({ x: lastGeneratedX + 260, y: 300, angle: 0, length: 45, speed: -0.06 });
            fireBars.push({ x: lastGeneratedX + 430, y: 300, angle: 1.5, length: 45, speed: 0.06 });
            addGoomba(lastGeneratedX + 340, 352);
        } else if (pattern === 5) {
            for (let i = 0; i < 4; i++) {
                addBrick(lastGeneratedX + 220 + (i*32), 352 - ((i+1)*32));
            }
            hazards.push({ x: lastGeneratedX + 380, y: 368, width: 64, height: 16, type: 'spikes' });
            addGoomba(lastGeneratedX + 480, 352);
        }

        lastGeneratedX += groundWidth;
        
        let pitSize = 80 + Math.random() * 80;
        if (Math.random() > 0.25) {
            hazards.push({ x: lastGeneratedX, y: 392, width: pitSize, height: 40, type: 'lava' });
        }
        lastGeneratedX += pitSize;
    }

    addGround(0, 900, 'ground');
    lastGeneratedX = 900;
    generateChunk();

    window.addEventListener("keydown", (e) => {
        keys[e.code] = true;
        if(["Space", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(e.code)) {
            e.preventDefault();
        }
    });

    window.addEventListener("keyup", (e) => {
        keys[e.code] = false;
    });

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

        let currentPlatformType = 'ground';
        platforms.forEach(p => {
            if (player.x + player.width > p.x && player.x < p.x + p.width && Math.abs((player.y + player.height) - p.y) < 6) {
                currentPlatformType = p.type;
            }
        });

        let acceleration = 0.4;
        let friction = 0.85;
        if (currentPlatformType === 'ice') friction = 0.98;
        else if (currentPlatformType === 'quicksand') player.vx *= 0.65;

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
            grav = 0.12; // Smooth hover trait
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
                player.x += mp.vx;
            }
        });

        if ((keys["ArrowUp"] || keys["Space"]) && player.grounded) {
            player.vy = player.jumpPower;
            player.grounded = false;
            spawnParticles(player.x + 16, player.y + 32, '#fff');
        }

        thwomps.forEach(t => {
            if (Math.abs(player.x - t.x) < 130) t.crushing = true;
            if (t.crushing) {
                t.y += 7;
                if (t.y >= 340) t.y = 340;
                setTimeout(() => { t.crushing = false; }, 750);
            } else if (t.y > t.startY) {
                t.y -= 2.5;
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
                    player.vy = -9.5;
                    score += 150;
                    spawnParticles(enemy.x + 16, enemy.y + 16, '#c84c0c');
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
                    score += 200;
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
    }

    // High-Detail Shaded Rendering & Custom HD Sprites
    function drawHDPlayer(x, y, facing) {
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
        }

        // Drop shadow for 3D realism
        ctx.fillStyle = 'rgba(0,0,0,0.25)';
        ctx.fillRect(x + 4, y + 30, 24, 4);

        // Cap / Head
        ctx.fillStyle = hatColor;
        ctx.fillRect(x + (facing === 'right' ? 8 : 4), y, 22, 9);
        ctx.fillStyle = skinTone;
        ctx.fillRect(x + (facing === 'right' ? 12 : 4), y + 9, 16, 9);

        // Eyes & Mustache detail
        ctx.fillStyle = '#000';
        ctx.fillRect(x + (facing === 'right' ? 20 : 6), y + 11, 3, 4);
        ctx.fillRect(x + (facing === 'right' ? 14 : 10), y + 15, 8, 3);

        // Shirt & Overalls with lighting gradients
        ctx.fillStyle = shirtColor;
        ctx.fillRect(x + 5, y + 18, 22, 10);
        ctx.fillStyle = overallColor;
        ctx.fillRect(x + 8, y + 22, 16, 6);

        // Golden buttons
        ctx.fillStyle = '#f1c40f';
        ctx.fillRect(x + 9, y + 23, 3, 3);
        ctx.fillRect(x + 20, y + 23, 3, 3);

        // Boots
        ctx.fillStyle = '#5d4037';
        ctx.fillRect(x + (facing === 'right' ? 17 : 2), y + 28, 13, 4);
    }

    function drawHDGoomba(x, y) {
        ctx.fillStyle = '#8d4004';
        ctx.fillRect(x + 3, y + 8, 26, 20);
        ctx.fillStyle = '#d7ccc8';
        ctx.fillRect(x + 6, y + 12, 20, 10);
        // Eyes
        ctx.fillStyle = '#000';
        ctx.fillRect(x + 8, y + 15, 3, 5);
        ctx.fillRect(x + 21, y + 15, 3, 5);
        // Feet
        ctx.fillStyle = '#3e2723';
        ctx.fillRect(x + 1, y + 28, 11, 4);
        ctx.fillRect(x + 20, y + 28, 11, 4);
    }

    function drawHDThwomp(x, y) {
        ctx.fillStyle = '#607d8b';
        ctx.fillRect(x, y, 40, 40);
        ctx.strokeStyle = '#37474f';
        ctx.lineWidth = 3;
        ctx.strokeRect(x, y, 40, 40);
        // Furious Face
        ctx.fillStyle = '#f44336';
        ctx.fillRect(x + 5, y + 10, 10, 6);
        ctx.fillRect(x + 25, y + 10, 10, 6);
        ctx.fillStyle = '#212121';
        ctx.fillRect(x + 8, y + 26, 24, 6);
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        ctx.save();
        ctx.translate(Math.floor(-cameraX), 0);

        // Parallax background elements
        decorations.forEach(dec => {
            if (dec.type === 'cloud') {
                ctx.fillStyle = "rgba(255, 255, 255, 0.9)";
                ctx.fillRect(dec.x, dec.y, 70, 20);
                ctx.fillRect(dec.x + 18, dec.y - 14, 36, 16);
            } else if (dec.type === 'bush') {
                ctx.fillStyle = "#27ae60";
                ctx.fillRect(dec.x, dec.y, 90, 32);
                ctx.fillStyle = "#2ecc71";
                ctx.fillRect(dec.x + 15, dec.y - 12, 60, 16);
            } else if (dec.type === 'hills') {
                ctx.fillStyle = "#16a085";
                ctx.beginPath();
                ctx.arc(dec.x + 40, dec.y + 32, 45, Math.PI, 0, false);
                ctx.fill();
            }
        });

        platforms.forEach(platform => {
            if (platform.x + platform.width >= cameraX - 100 && platform.x <= cameraX + canvas.width + 100) {
                if (platform.type === 'ground') {
                    ctx.fillStyle = '#b55214';
                    ctx.fillRect(platform.x, platform.y, platform.width, platform.height + 250);
                    ctx.fillStyle = '#2ecc71';
                    ctx.fillRect(platform.x, platform.y, platform.width, 10);
                    ctx.fillStyle = '#27ae60';
                    ctx.fillRect(platform.x, platform.y + 10, platform.width, 4);
                } else if (platform.type === 'ice') {
                    ctx.fillStyle = '#85c1e9';
                    ctx.fillRect(platform.x, platform.y, platform.width, platform.height + 250);
                    ctx.fillStyle = '#d4efdf';
                    ctx.fillRect(platform.x, platform.y, platform.width, 10);
                } else if (platform.type === 'quicksand') {
                    ctx.fillStyle = '#b7950b';
                    ctx.fillRect(platform.x, platform.y, platform.width, platform.height + 250);
                    ctx.fillStyle = '#f1c40f';
                    ctx.fillRect(platform.x, platform.y, platform.width, 10);
                } else if (platform.type === 'brick') {
                    ctx.fillStyle = '#c0392b';
                    ctx.fillRect(platform.x, platform.y, platform.width, platform.height);
                    ctx.strokeStyle = '#78281f';
                    ctx.lineWidth = 2;
                    ctx.strokeRect(platform.x, platform.y, platform.width, platform.height);
                } else if (platform.type === 'question') {
                    ctx.fillStyle = '#f39c12';
                    ctx.fillRect(platform.x, platform.y, platform.width, platform.height);
                    ctx.strokeStyle = '#b7950b';
                    ctx.lineWidth = 2;
                    ctx.strokeRect(platform.x, platform.y, platform.width, platform.height);
                    ctx.fillStyle = '#ffffff';
                    ctx.font = "bold 20px 'Courier New'";
                    ctx.fillText("?", platform.x + 9, platform.y + 24);
                } else if (platform.type === 'pipe') {
                    ctx.fillStyle = '#2ecc71';
                    ctx.fillRect(platform.x, platform.y, platform.width, platform.height);
                    ctx.fillRect(platform.x - 4, platform.y, platform.width + 8, 16);
                    ctx.fillStyle = '#27ae60';
                    ctx.fillRect(platform.x + 4, platform.y, 6, platform.height);
                    ctx.strokeStyle = '#145a32';
                    ctx.lineWidth = 2;
                    ctx.strokeRect(platform.x, platform.y, platform.width, platform.height);
                    ctx.strokeRect(platform.x - 4, platform.y, platform.width + 8, 16);
                }
            }
        });

        movingPlatforms.forEach(mp => {
            ctx.fillStyle = '#9b59b6';
            ctx.fillRect(mp.x, mp.y, mp.width, mp.height);
            ctx.strokeStyle = '#512e5f';
            ctx.lineWidth = 2;
            ctx.strokeRect(mp.x, mp.y, mp.width, mp.height);
        });

        hazards.forEach(h => {
            if (h.type === 'lava') {
                ctx.fillStyle = '#e74c3c';
                ctx.fillRect(h.x, h.y, h.width, h.height);
                ctx.fillStyle = '#f1c40f';
                ctx.fillRect(h.x, h.y, h.width, 10);
            } else if (h.type === 'spikes') {
                ctx.fillStyle = '#95a5a6';
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
            ctx.strokeStyle = '#f39c12';
            ctx.lineWidth = 5;
            ctx.beginPath();
            ctx.moveTo(fb.x, fb.y);
            let endX = fb.x + Math.cos(fb.angle) * fb.length;
            let endY = fb.y + Math.sin(fb.angle) * fb.length;
            ctx.lineTo(endX, endY);
            ctx.stroke();

            for (let r = 15; r <= fb.length; r += 15) {
                let bx = fb.x + Math.cos(fb.angle) * r;
                let by = fb.y + Math.sin(fb.angle) * r;
                ctx.fillStyle = '#e74c3c';
                ctx.beginPath();
                ctx.arc(bx, by, 7, 0, Math.PI * 2);
                ctx.fill();
                ctx.fillStyle = '#f1c40f';
                ctx.beginPath();
                ctx.arc(bx, by, 3, 0, Math.PI * 2);
                ctx.fill();
            }
        });

        thwomps.forEach(t => drawHDThwomp(t.x, t.y));

        coins.forEach(coin => {
            if (!coin.collected && coin.x >= cameraX - 50 && coin.x <= cameraX + canvas.width + 50) {
                ctx.fillStyle = '#f1c40f';
                ctx.beginPath();
                ctx.arc(coin.x, coin.y, coin.radius, 0, Math.PI * 2);
                ctx.fill();
                ctx.fillStyle = '#f9e79f';
                ctx.beginPath();
                ctx.arc(coin.x - 2, coin.y - 2, coin.radius * 0.4, 0, Math.PI * 2);
                ctx.fill();
                ctx.strokeStyle = '#7d6608';
                ctx.lineWidth = 2;
                ctx.stroke();
            }
        });

        enemies.forEach(enemy => {
            if (enemy.alive && enemy.x >= cameraX - 100 && enemy.x <= cameraX + canvas.width + 100) {
                drawHDGoomba(enemy.x, enemy.y);
            }
        });

        particles.forEach(p => {
            ctx.fillStyle = p.color;
            ctx.fillRect(p.x, p.y, 4, 4);
        });

        drawHDPlayer(player.x, player.y, player.facing);

        ctx.restore();

        // Sleek HD HUD Overlay Bar
        ctx.fillStyle = "rgba(10, 10, 10, 0.9)";
        ctx.fillRect(0, 0, canvas.width, 48);

        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 15px 'Courier New'";
        ctx.fillText("MARIO HD", 35, 28);
        ctx.fillText(String(score).padStart(6, '0'), 35, 44);

        ctx.fillText("COINS", 230, 28);
        ctx.fillText("x" + String(coinsCollected).padStart(2, '0'), 246, 44);

        ctx.fillText("HERO:", 430, 28);
        ctx.fillText(selectedChar.toUpperCase(), 430, 44);

        ctx.fillText("DISTANCE", 620, 28);
        ctx.fillText(Math.floor(cameraX / 10) + "m", 620, 44);
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

st.components.v1.html(game_html, height=520, scrolling=False)
