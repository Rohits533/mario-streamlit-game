import streamlit as st

st.set_page_config(
    page_title="Infinite Classic Mario - Deluxe Edition",
    page_icon="🍄",
    layout="centered"
)

# Custom Styling for Retro Arcade UI & Store Modal
st.markdown("""
<style>
    .stApp {
        background-color: #111;
        color: white;
    }
    .arcade-header {
        text-align: center;
        font-family: 'Courier New', Courier, monospace;
        color: #ffcc00;
        text-shadow: 2px 2px #ff0000;
        margin-bottom: 0px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='arcade-header'>🍄 SUPER MARIO: INFINITE DELUXE 🍄</h1>", unsafe_allow_html=True)

game_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        body {
            margin: 0;
            background: #111;
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
            background: #5c94fc;
            box-shadow: 0 0 30px rgba(92, 148, 252, 0.6);
            image-rendering: pixelated;
            image-rendering: crisp-edges;
        }
        .hud-panel {
            margin-top: 8px;
            display: flex;
            justify-content: space-between;
            width: 768px;
            font-size: 15px;
            font-weight: bold;
            background: #222;
            padding: 8px 12px;
            border: 2px solid #555;
            box-sizing: border-box;
        }
        .btn-arcade {
            background: #e74c3c;
            color: white;
            border: 2px solid #fff;
            padding: 6px 14px;
            font-family: 'Courier New', Courier, monospace;
            font-weight: bold;
            cursor: pointer;
            text-transform: uppercase;
            box-shadow: 0 4px #990000;
        }
        .btn-arcade:active {
            transform: translateY(2px);
            box-shadow: 0 2px #990000;
        }
        /* Store Overlay */
        #storeModal {
            display: none;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 520px;
            background: rgba(0, 0, 0, 0.95);
            border: 4px solid #f1c40f;
            padding: 20px;
            z-index: 10;
            box-shadow: 0 0 50px rgba(241, 196, 15, 0.6);
            text-align: left;
        }
        .store-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-top: 15px;
            max-height: 250px;
            overflow-y: auto;
        }
        .store-item {
            background: #222;
            border: 2px solid #444;
            padding: 10px;
            text-align: center;
        }
        .store-item.owned {
            border-color: #2ecc71;
        }
    </style>
</head>
<body>

<div class="game-wrapper">
    <canvas id="gameCanvas" width="768" height="432"></canvas>
    
    <div class="hud-panel">
        <div>CHOOSE CHARACTER & SHOP BELOW</div>
        <div>
            <button class="btn-arcade" onclick="openStore()">🍄 SHOP / OUTFITS</button>
            <button class="btn-arcade" onclick="togglePause()" id="pauseBtn">PAUSE</button>
        </div>
    </div>

    <!-- Store & Character Selection Modal -->
    <div id="storeModal">
        <h2 style="color: #f1c40f; margin-top: 0; text-align: center;">🍄 TOAD'S ITEM SHOP & CHARACTER SELECT</h2>
        <div style="font-size: 13px; color: #aaa; text-align: center;">Collect coins in-game to purchase custom characters and skins!</div>
        
        <div style="margin-top: 15px; font-weight: bold; color: #3498db;">SELECT CHARACTER:</div>
        <div style="display: flex; gap: 10px; margin-top: 5px;">
            <button class="btn-arcade" onclick="selectCharacter('mario')" style="flex:1; background:#c84c0c;" id="charMario">Mario (Balanced)</button>
            <button class="btn-arcade" onclick="selectCharacter('luigi')" style="flex:1; background:#27ae60;" id="charLuigi">Luigi (Super Jump)</button>
            <button class="btn-arcade" onclick="selectCharacter('peach')" style="flex:1; background:#f39c12;" id="charPeach">Peach (Float)</button>
        </div>

        <div style="margin-top: 15px; font-weight: bold; color: #f39c12;">OUTFIT PACKS:</div>
        <div class="store-grid">
            <div class="store-item" id="skin_classic">
                <div style="font-weight:bold;">Classic Red</div>
                <div style="font-size:12px; color:#aaa;">Default</div>
                <button class="btn-arcade" style="margin-top:8px; font-size:11px;" onclick="buySkin('classic', 0)">Equipped</button>
            </div>
            <div class="store-item" id="skin_fire">
                <div style="font-weight:bold;">Fire Mario</div>
                <div style="font-size:12px; color:#aaa;">Cost: 50 Coins</div>
                <button class="btn-arcade" style="margin-top:8px; font-size:11px;" onclick="buySkin('fire', 50)">Unlock</button>
            </div>
            <div class="store-item" id="skin_gold">
                <div style="font-weight:bold;">Golden Suit</div>
                <div style="font-size:12px; color:#aaa;">Cost: 150 Coins</div>
                <button class="btn-arcade" style="margin-top:8px; font-size:11px;" onclick="buySkin('gold', 150)">Unlock</button>
            </div>
            <div class="store-item" id="skin_dark">
                <div style="font-weight:bold;">Shadow Tuxedo</div>
                <div style="font-size:12px; color:#aaa;">Cost: 300 Coins</div>
                <button class="btn-arcade" style="margin-top:8px; font-size:11px;" onclick="buySkin('dark', 300)">Unlock</button>
            </div>
        </div>

        <div style="text-align: center; margin-top: 20px;">
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
    let totalCoinsEarned = 500; // Starting bonus coins to try out the store immediately
    let isPaused = false;
    const keys = {};

    let cameraX = 0;
    let lastGeneratedX = 0;

    // Player customization state
    let selectedChar = 'mario'; // 'mario', 'luigi', 'peach'
    let currentSkin = 'classic'; // 'classic', 'fire', 'gold', 'dark'
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
        facing: 'right',
        floating: false
    };

    let platforms = [];
    let enemies = [];
    let coins = [];
    let decorations = [];
    let hazards = [];
    let movingPlatforms = [];
    let thwomps = [];
    let fireBars = [];

    function updateCharacterStats() {
        if (selectedChar === 'mario') {
            player.speed = 4.0;
            player.jumpPower = -12.0;
        } else if (selectedChar === 'luigi') {
            player.speed = 3.8;
            player.jumpPower = -14.0; // Higher jump
        } else if (selectedChar === 'peach') {
            player.speed = 3.6;
            player.jumpPower = -11.0; // Float ability trait handled in gravity loop
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
                alert("Successfully purchased and equipped " + skinName + "!");
            } else {
                alert("Not enough coins! Collect more in the infinite runner.");
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
        if (hasCoin) coins.push({ x: x + 16, y: y - 24, radius: 10, collected: false });
    }

    function addBrick(x, y) {
        platforms.push({ x: x, y: y, width: 32, height: 32, type: 'brick' });
    }

    function addGoomba(x, y) {
        enemies.push({ x: x, y: y, width: 32, height: 32, vx: -1.4, alive: true, vy: 0 });
    }

    // Dense Procedural World Generator (Packed with obstacles and coins)
    function generateChunk() {
        let groundWidth = 700 + Math.random() * 350;
        let biomeRand = Math.random();
        
        let surfaceType = 'ground';
        if (biomeRand > 0.75) surfaceType = 'ice';
        else if (biomeRand > 0.5) surfaceType = 'quicksand';

        addGround(lastGeneratedX, groundWidth, surfaceType);

        decorations.push({ x: lastGeneratedX + Math.random() * 150, y: 60, type: 'cloud' });
        decorations.push({ x: lastGeneratedX + 400 + Math.random() * 150, y: 50, type: 'cloud' });
        decorations.push({ x: lastGeneratedX + Math.random() * 300, y: 352, type: 'bush' });

        // Add plentiful arches of coins across the chunk
        for (let cx = lastGeneratedX + 50; cx < lastGeneratedX + groundWidth - 100; cx += 80) {
            coins.push({ x: cx, y: 260 + Math.sin(cx) * 40, radius: 8, collected: false });
        }

        let pattern = Math.floor(Math.random() * 6);
        
        if (pattern === 0) {
            addPipe(lastGeneratedX + 200, 48);
            addPipe(lastGeneratedX + 420, 80);
            addGoomba(lastGeneratedX + 310, 352);
            addGoomba(lastGeneratedX + 520, 352);
        } else if (pattern === 1) {
            addBrick(lastGeneratedX + 250, 260);
            addQuestionBlock(lastGeneratedX + 282, 260);
            addBrick(lastGeneratedX + 314, 260);
            hazards.push({ x: lastGeneratedX + 350, y: 368, width: 64, height: 16, type: 'spikes' });
            addGoomba(lastGeneratedX + 440, 352);
        } else if (pattern === 2) {
            thwomps.push({ x: lastGeneratedX + 300, y: 80, startY: 80, width: 40, height: 40, timer: 0, crushing: false });
            fireBars.push({ x: lastGeneratedX + 450, y: 320, angle: 0, length: 45, speed: 0.05 });
        } else if (pattern === 3) {
            movingPlatforms.push({ 
                x: lastGeneratedX + 180, y: 270, width: 70, height: 16, 
                minX: lastGeneratedX + 150, maxX: lastGeneratedX + 420, vx: 1.8 
            });
            hazards.push({ x: lastGeneratedX + 150, y: 392, width: 290, height: 40, type: 'lava' });
        } else if (pattern === 4) {
            fireBars.push({ x: lastGeneratedX + 250, y: 300, angle: 0, length: 40, speed: -0.06 });
            fireBars.push({ x: lastGeneratedX + 420, y: 300, angle: 2.0, length: 40, speed: 0.06 });
            addGoomba(lastGeneratedX + 330, 352);
        } else if (pattern === 5) {
            // Staircase pattern with high coin cache
            for (let i = 0; i < 4; i++) {
                addBrick(lastGeneratedX + 200 + (i*32), 352 - ((i+1)*32));
            }
            addGoomba(lastGeneratedX + 400, 352);
        }

        lastGeneratedX += groundWidth;
        
        let pitSize = 80 + Math.random() * 70;
        if (Math.random() > 0.3) {
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
        player.x = cameraX + 64;
        player.y = 100;
        player.vy = 0;
        player.vx = 0;
        score = Math.max(0, score - 250);
    }

    function update() {
        if (isPaused) return;

        let currentPlatformType = 'ground';
        platforms.forEach(p => {
            if (player.x + player.width > p.x && player.x < p.x + p.width && Math.abs((player.y + player.height) - p.y) < 5) {
                currentPlatformType = p.type;
            }
        });

        let acceleration = 0.4;
        let friction = 0.85;
        if (currentPlatformType === 'ice') friction = 0.98;
        else if (currentPlatformType === 'quicksand') player.vx *= 0.7;

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

        // Gravity & Float trait for Peach
        let grav = player.gravity;
        if (selectedChar === 'peach' && keys["ArrowUp"] && player.vy > 0) {
            grav = 0.15; // Peach floating skill
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
                if (platform.type === 'quicksand') player.y += 1.5;
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
        }

        // Thwomps AI
        thwomps.forEach(t => {
            if (Math.abs(player.x - t.x) < 120) t.crushing = true;
            if (t.crushing) {
                t.y += 6;
                if (t.y >= 340) t.y = 340;
                setTimeout(() => { t.crushing = false; }, 800);
            } else if (t.y > t.startY) {
                t.y -= 2;
            }
            if (player.x < t.x + t.width && player.x + player.width > t.x && player.y < t.y + t.height && player.y + player.height > t.y) {
                resetPlayer();
            }
        });

        // Fire Bars
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

        // Enemies
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
                    player.vy = -9;
                    score += 100;
                } else {
                    resetPlayer();
                }
            }
        });

        // Coin Collection
        coins.forEach(coin => {
            if (!coin.collected) {
                let dist = Math.hypot(coin.x - (player.x + player.width / 2), coin.y - (player.y + player.height / 2));
                if (dist < coin.radius + player.width / 3) {
                    coin.collected = true;
                    score += 150;
                    coinsCollected += 1;
                }
            }
        });

        if (player.y > canvas.height + 80) resetPlayer();

        // Cleanup
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

    // Realistic Character & Outfit Skins Renderer
    function drawPlayerSkin(x, y, facing) {
        let shirtColor = '#c84c0c'; // Classic Red
        let overallColor = '#0070ec';
        let hatColor = '#c84c0c';

        if (selectedChar === 'luigi') {
            shirtColor = '#27ae60';
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
            shirtColor = '#2c3e50';
            overallColor = '#111111';
            hatColor = '#2c3e50';
        }

        // Body & Outfit rendering
        ctx.fillStyle = hatColor;
        ctx.fillRect(x + (facing === 'right' ? 8 : 4), y, 20, 8);
        
        ctx.fillStyle = '#f83800'; // Skin tone face
        ctx.fillRect(x + (facing === 'right' ? 12 : 4), y + 8, 16, 10);
        
        ctx.fillStyle = shirtColor;
        ctx.fillRect(x + 6, y + 18, 20, 10);

        ctx.fillStyle = overallColor;
        ctx.fillRect(x + 8, y + 22, 16, 6);

        ctx.fillStyle = '#8b4513'; // Boots
        ctx.fillRect(x + (facing === 'right' ? 18 : 2), y + 28, 12, 4);
    }

    function drawGoomba(x, y) {
        ctx.fillStyle = '#c84c0c';
        ctx.fillRect(x + 4, y + 8, 24, 20);
        ctx.fillStyle = '#000000';
        ctx.fillRect(x + 2, y + 28, 10, 4);
        ctx.fillRect(x + 20, y + 28, 10, 4);
        ctx.fillRect(x + 8, y + 14, 4, 6);
        ctx.fillRect(x + 20, y + 14, 4, 6);
    }

    function drawThwomp(x, y) {
        ctx.fillStyle = '#7f8c8d';
        ctx.fillRect(x, y, 40, 40);
        ctx.fillStyle = '#e74c3c';
        ctx.fillRect(x + 6, y + 12, 8, 6);
        ctx.fillRect(x + 26, y + 12, 8, 6);
        ctx.fillStyle = '#000000';
        ctx.fillRect(x + 8, y + 26, 24, 6);
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        ctx.save();
        ctx.translate(Math.floor(-cameraX), 0);

        decorations.forEach(dec => {
            if (dec.type === 'cloud') {
                ctx.fillStyle = "#ffffff";
                ctx.fillRect(dec.x, dec.y, 64, 16);
                ctx.fillRect(dec.x + 16, dec.y - 16, 32, 16);
            } else if (dec.type === 'bush') {
                ctx.fillStyle = "#00a800";
                ctx.fillRect(dec.x, dec.y, 96, 32);
                ctx.fillRect(dec.x + 16, dec.y - 16, 64, 16);
            }
        });

        platforms.forEach(platform => {
            if (platform.x + platform.width >= cameraX - 100 && platform.x <= cameraX + canvas.width + 100) {
                if (platform.type === 'ground') {
                    ctx.fillStyle = '#c84c0c';
                    ctx.fillRect(platform.x, platform.y, platform.width, platform.height + 200);
                    ctx.fillStyle = '#00a800';
                    ctx.fillRect(platform.x, platform.y, platform.width, 8);
                } else if (platform.type === 'ice') {
                    ctx.fillStyle = '#a9cce3';
                    ctx.fillRect(platform.x, platform.y, platform.width, platform.height + 200);
                    ctx.fillStyle = '#ebf5fb';
                    ctx.fillRect(platform.x, platform.y, platform.width, 8);
                } else if (platform.type === 'quicksand') {
                    ctx.fillStyle = '#d4ac0d';
                    ctx.fillRect(platform.x, platform.y, platform.width, platform.height + 200);
                    ctx.fillStyle = '#f1c40f';
                    ctx.fillRect(platform.x, platform.y, platform.width, 8);
                } else if (platform.type === 'brick') {
                    ctx.fillStyle = '#c84c0c';
                    ctx.fillRect(platform.x, platform.y, platform.width, platform.height);
                    ctx.strokeStyle = '#000000';
                    ctx.lineWidth = 2;
                    ctx.strokeRect(platform.x, platform.y, platform.width, platform.height);
                } else if (platform.type === 'question') {
                    ctx.fillStyle = '#fcbc3c';
                    ctx.fillRect(platform.x, platform.y, platform.width, platform.height);
                    ctx.strokeStyle = '#000000';
                    ctx.lineWidth = 2;
                    ctx.strokeRect(platform.x, platform.y, platform.width, platform.height);
                    ctx.fillStyle = '#000000';
                    ctx.font = "bold 18px monospace";
                    ctx.fillText("?", platform.x + 10, platform.y + 23);
                } else if (platform.type === 'pipe') {
                    ctx.fillStyle = '#00a800';
                    ctx.fillRect(platform.x, platform.y, platform.width, platform.height);
                    ctx.fillRect(platform.x - 4, platform.y, platform.width + 8, 16);
                    ctx.strokeStyle = '#000000';
                    ctx.lineWidth = 2;
                    ctx.strokeRect(platform.x, platform.y, platform.width, platform.height);
                    ctx.strokeRect(platform.x - 4, platform.y, platform.width + 8, 16);
                }
            }
        });

        movingPlatforms.forEach(mp => {
            ctx.fillStyle = '#8e44ad';
            ctx.fillRect(mp.x, mp.y, mp.width, mp.height);
            ctx.strokeStyle = '#000000';
            ctx.lineWidth = 2;
            ctx.strokeRect(mp.x, mp.y, mp.width, mp.height);
        });

        hazards.forEach(h => {
            if (h.type === 'lava') {
                ctx.fillStyle = '#e74c3c';
                ctx.fillRect(h.x, h.y, h.width, h.height);
                ctx.fillStyle = '#f39c12';
                ctx.fillRect(h.x, h.y, h.width, 8);
            } else if (h.type === 'spikes') {
                ctx.fillStyle = '#bdc3c7';
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
            ctx.lineWidth = 4;
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
                ctx.arc(bx, by, 6, 0, Math.PI * 2);
                ctx.fill();
            }
        });

        thwomps.forEach(t => drawThwomp(t.x, t.y));

        coins.forEach(coin => {
            if (!coin.collected && coin.x >= cameraX - 50 && coin.x <= cameraX + canvas.width + 50) {
                ctx.fillStyle = '#fcbc3c';
                ctx.beginPath();
                ctx.arc(coin.x, coin.y, coin.radius, 0, Math.PI * 2);
                ctx.fill();
                ctx.strokeStyle = '#000000';
                ctx.lineWidth = 2;
                ctx.stroke();
            }
        });

        enemies.forEach(enemy => {
            if (enemy.alive && enemy.x >= cameraX - 100 && enemy.x <= cameraX + canvas.width + 100) {
                drawGoomba(enemy.x, enemy.y);
            }
        });

        drawPlayerSkin(player.x, player.y, player.facing);

        ctx.restore();

        // Retro HUD Display Bar
        ctx.fillStyle = "#000000";
        ctx.fillRect(0, 0, canvas.width, 45);

        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 15px 'Courier New'";
        ctx.fillText("MARIO", 30, 28);
        ctx.fillText(String(score).padStart(6, '0'), 30, 44);

        ctx.fillText("COINS", 230, 28);
        ctx.fillText("x" + String(coinsCollected).padStart(2, '0'), 246, 44);

        ctx.fillText("CHAR:", 430, 28);
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
