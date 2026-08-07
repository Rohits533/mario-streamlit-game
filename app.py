import streamlit as st

st.set_page_config(
    page_title="Super Mario: Infinite Dimensional Rift",
    page_icon="🌌",
    layout="centered"
)

st.markdown("""
<style>
    .stApp {
        background-color: #030305;
        color: white;
    }
    .arcade-header {
        text-align: center;
        font-family: 'Courier New', Courier, monospace;
        color: #00ffff;
        text-shadow: 3px 3px #ff00ff;
        margin-bottom: 0px;
        letter-spacing: 2px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='arcade-header'>🌌 SUPER MARIO: DIMENSIONAL RIFT 🌌</h1>", unsafe_allow_html=True)

game_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        body {
            margin: 0;
            background: #030305;
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
            border: 4px solid #00ffff;
            background: #0b0b16;
            box-shadow: 0 0 60px rgba(0, 255, 255, 0.6);
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
            background: rgba(10, 10, 20, 0.95);
            padding: 8px 12px;
            border: 2px solid #00ffff;
            box-sizing: border-box;
            border-radius: 4px;
        }
        .btn-arcade {
            background: #ff00ff;
            color: white;
            border: 2px solid #fff;
            padding: 6px 12px;
            font-family: 'Courier New', Courier, monospace;
            font-weight: bold;
            cursor: pointer;
            text-transform: uppercase;
            box-shadow: 0 4px #990099;
            border-radius: 3px;
        }
        .btn-arcade:active {
            transform: translateY(2px);
            box-shadow: 0 2px #990099;
        }
        #entryScreen, #gameOverScreen, #riftScreen {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 580px;
            background: rgba(10, 10, 20, 0.98);
            border: 4px solid #00ffff;
            padding: 25px;
            z-index: 20;
            box-shadow: 0 0 80px rgba(0, 255, 255, 0.8);
            text-align: center;
            border-radius: 8px;
            animation: modalZoomIn 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
        }
        @keyframes modalZoomIn {
            0% { transform: translate(-50%, -50%) scale(0.2); opacity: 0; }
            100% { transform: translate(-50%, -50%) scale(1); opacity: 1; }
        }
        #gameOverScreen {
            display: none;
            border: 4px solid #ff0055;
            box-shadow: 0 0 80px rgba(255, 0, 85, 0.8);
            z-index: 30;
        }
        #riftScreen {
            display: none;
            border: 4px solid #ffff00;
            background: rgba(20, 10, 30, 0.98);
            box-shadow: 0 0 90px rgba(255, 255, 0, 0.9);
            z-index: 40;
            animation: riftPulse 0.5s infinite alternate;
        }
        @keyframes riftPulse {
            0% { box-shadow: 0 0 40px rgba(255, 0, 255, 0.6); }
            100% { box-shadow: 0 0 90px rgba(0, 255, 255, 0.9); }
        }
    </style>
</head>
<body>

<div class="game-wrapper">
    <canvas id="gameCanvas" width="768" height="432"></canvas>
    
    <!-- Entry / Main Menu -->
    <div id="entryScreen">
        <h1 style="color: #00ffff; text-shadow: 2px 2px #ff00ff; font-size: 24px; margin-top:0;">🌌 DIMENSIONAL RIFT 🌌</h1>
        <div style="font-size: 12px; color: #ffff00; margin-bottom: 20px; letter-spacing: 1px;">PROCEDURAL MULTIVERSE EDITION</div>
        <div style="font-size: 12px; color: #2ecc71; margin-bottom: 15px;">⭐ High Score: <span id="menuHighScore">0</span> | 🪙 Crystals: <span id="menuCoins">100</span></div>
        <div style="display: flex; flex-direction: column; gap: 12px; width: 70%; margin: 0 auto;">
            <button class="btn-arcade" onclick="startGame()" style="background:#00b894; font-size:16px; padding:12px;">▶ ENTER RIFT</button>
        </div>
    </div>

    <!-- Rift Transition Warning Modal -->
    <div id="riftScreen">
        <h1 style="color: #ffff00; text-shadow: 2px 2px #ff00ff; font-size: 24px; margin-top:0;" id="riftTitle">⚡ RIFT TEARING OPEN! ⚡</h1>
        <div style="font-size: 13px; color: #fff; margin-bottom: 15px;" id="riftDesc">Reality collapsing... Shifting multiverse physics & aesthetic!</div>
        <div style="font-size: 14px; color: #00ffff; margin-bottom: 20px;">New Dimension: <span id="nextDimName" style="color:#ff00ff; font-weight:bold;">NEON MATRIX</span></div>
        <button class="btn-arcade" onclick="resumeFromRift()" style="background:#e84393; font-size:14px; padding:10px; width:100%;">STABILIZE & DIVE IN</button>
    </div>

    <!-- Game Over Screen -->
    <div id="gameOverScreen">
        <h1 style="color: #ff0055; text-shadow: 2px 2px #000; font-size: 28px; margin-top:0;">💀 TIMELINE COLLAPSED 💀</h1>
        <div style="font-size: 13px; color: #ccc; margin-bottom: 10px;">Hero lost in the void!</div>
        <div style="font-size: 14px; color: #ffff00; margin-bottom: 5px;">Final Score: <span id="finalScoreVal">0</span></div>
        <div style="font-size: 13px; color: #2ecc71; margin-bottom: 20px;">🏆 Best Score: <span id="gameOverHighScore">0</span></div>
        <div style="display: flex; flex-direction: column; gap: 12px; width: 70%; margin: 0 auto;">
            <button class="btn-arcade" onclick="restartGame()" style="background:#00b894; font-size:15px; padding:12px;">🔄 REBOOT TIMELINE</button>
            <button class="btn-arcade" onclick="returnToMainMenu()" style="background:#0984e3; font-size:13px; padding:10px;">🏠 MAIN MENU</button>
        </div>
    </div>

    <div class="hud-panel">
        <div>DIMENSION: <span id="hudDim" style="color:#00ffff;">OVERWORLD</span> | SCORE: <span id="hudScore">0</span> | BEST: <span id="hudHighScore">0</span> | CRYSTALS: <span id="hudCoins">100</span></div>
        <div>
            <button class="btn-arcade" onclick="togglePause()" id="pauseBtn">PAUSE</button>
        </div>
    </div>
</div>

<script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    ctx.imageSmoothingEnabled = false;

    let gameStarted = false;
    let gameOver = false;
    let score = 0;
    let highScore = parseInt(localStorage.getItem('rift_highscore') || '0');
    let crystals = parseInt(localStorage.getItem('rift_crystals') || '100');
    let isPaused = true;
    const keys = {};

    let cameraX = 0;
    let lastGeneratedX = 0;

    // Dimensions / Biomes System
    // 0: Classic Overworld, 1: Neon Matrix, 2: Underworld Magma, 3: Cosmic Galaxy
    let currentDimensionIndex = 0;
    const dimensions = [
        { name: "OVERWORLD", bg: "#1a1a2e", ground: "#2b6cb0", accent: "#38a169", gravity: 0.5 },
        { name: "NEON MATRIX", bg: "#05050f", ground: "#00ffff", accent: "#ff00ff", gravity: 0.45 },
        { name: "MAGMA CORE", bg: "#1f0a0a", ground: "#c0392b", accent: "#f39c12", gravity: 0.6 },
        { name: "COSMIC GALAXY", bg: "#080214", ground: "#8e44ad", accent: "#f1c40f", gravity: 0.32 }
    ];

    document.getElementById('menuHighScore').innerText = highScore;
    document.getElementById('menuCoins').innerText = crystals;
    document.getElementById('hudHighScore').innerText = highScore;
    document.getElementById('hudCoins').innerText = crystals;

    let audioCtx = null;
    let musicInterval = null;

    function initMusic() {
        if (!audioCtx) {
            audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        }
        if (audioCtx.state === 'suspended') audioCtx.resume();
    }

    function playNote(freq, duration) {
        if (!audioCtx) return;
        try {
            let osc = audioCtx.createOscillator();
            let gain = audioCtx.createGain();
            osc.type = 'triangle';
            osc.frequency.value = freq;
            gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + duration);
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + duration);
        } catch(e) {}
    }

    const notes = [440, 523, 659, 783, 880, 659, 523, 392];
    let noteIdx = 0;
    function startBGM() {
        if (musicInterval) clearInterval(musicInterval);
        musicInterval = setInterval(() => {
            if (!isPaused && gameStarted && !gameOver) {
                playNote(notes[noteIdx], 0.15);
                noteIdx = (noteIdx + 1) % notes.length;
            }
        }, 160);
    }

    const player = {
        x: 64, y: 200, width: 32, height: 32, vx: 0, vy: 0, speed: 4.5, jumpPower: -12.5, grounded: false, facing: 'right'
    };

    let platforms = [];
    let enemies = [];
    let crystalsList = [];
    let particles = [];
    let floatingTexts = [];

    function startGame() {
        initMusic();
        gameStarted = true;
        gameOver = false;
        isPaused = false;
        currentDimensionIndex = 0;
        document.getElementById('entryScreen').style.display = 'none';
        document.getElementById('gameOverScreen').style.display = 'none';
        resetGameState();
        startBGM();
    }

    function restartGame() {
        gameOver = false;
        isPaused = false;
        currentDimensionIndex = 0;
        document.getElementById('gameOverScreen').style.display = 'none';
        resetGameState();
        startBGM();
    }

    function returnToMainMenu() {
        gameOver = false;
        gameStarted = false;
        isPaused = true;
        document.getElementById('gameOverScreen').style.display = 'none';
        document.getElementById('entryScreen').style.display = 'block';
    }

    function togglePause() {
        if (gameOver || !gameStarted) return;
        isPaused = !isPaused;
        document.getElementById("pauseBtn").innerText = isPaused ? "RESUME" : "PAUSE";
    }

    function resetGameState() {
        cameraX = 0;
        lastGeneratedX = 0;
        platforms = [];
        enemies = [];
        crystalsList = [];
        particles = [];
        floatingTexts = [];
        score = 0;

        addGround(0, 900);
        lastGeneratedX = 900;
        generateChunk();

        player.x = 64;
        player.y = 200;
        player.vx = 0;
        player.vy = 0;
    }

    function addGround(startX, width) {
        platforms.push({ x: startX, y: 384, width: width, height: 48 });
    }

    function addPlatform(x, y, width) {
        platforms.push({ x: x, y: y, width: width, height: 24 });
    }

    function addEnemy(x, y) {
        enemies.push({ x: x, y: y, width: 32, height: 32, vx: -2.0, alive: true, vy: 0 });
    }

    function spawnParticles(x, y, color) {
        for (let i = 0; i < 8; i++) {
            particles.push({
                x: x, y: y,
                vx: (Math.random() - 0.5) * 6,
                vy: (Math.random() - 0.7) * 6,
                color: color,
                life: 30
            });
        }
    }

    function addFloatingText(x, y, text, color='#ffff00') {
        floatingTexts.push({ x: x, y: y, text: text, color: color, life: 40 });
    }

    function triggerRiftTransition() {
        isPaused = true;
        currentDimensionIndex = (currentDimensionIndex + 1) % dimensions.length;
        let nextDim = dimensions[currentDimensionIndex];
        document.getElementById('nextDimName').innerText = nextDim.name;
        document.getElementById('riftTitle').innerText = "⚡ ENTERING " + nextDim.name + " ⚡";
        document.getElementById('riftScreen').style.display = 'block';
        spawnParticles(player.x, player.y, nextDim.accent);
    }

    function resumeFromRift() {
        document.getElementById('riftScreen').style.display = 'none';
        isPaused = false;
    }

    function generateChunk() {
        let groundWidth = 700 + Math.random() * 250;
        addGround(lastGeneratedX, groundWidth);

        for (let cx = lastGeneratedX + 60; cx < lastGeneratedX + groundWidth - 60; cx += 80) {
            if (Math.random() > 0.3) {
                crystalsList.push({ x: cx, y: 240 + Math.sin(cx * 0.05) * 45, radius: 8, collected: false });
            }
        }

        if (Math.random() > 0.4) {
            addPlatform(lastGeneratedX + 220, 260, 120);
            addPlatform(lastGeneratedX + 420, 190, 100);
            addEnemy(lastGeneratedX + 280, 228);
        } else {
            addEnemy(lastGeneratedX + 350, 352);
        }

        lastGeneratedX += groundWidth;
        let pitSize = 90 + Math.random() * 60;
        lastGeneratedX += pitSize;
    }

    addGround(0, 900);
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

    function triggerGameOver() {
        gameOver = true;
        spawnParticles(player.x + 16, player.y + 16, '#ff0055');
        if (score > highScore) {
            highScore = score;
            localStorage.setItem('rift_highscore', highScore);
        }
        localStorage.setItem('rift_crystals', crystals);
        document.getElementById('finalScoreVal').innerText = score;
        document.getElementById('gameOverHighScore').innerText = highScore;
        document.getElementById('gameOverScreen').style.display = 'block';
    }

    function update() {
        if (isPaused || gameOver || !gameStarted) return;

        let dim = dimensions[currentDimensionIndex];

        if (keys["ArrowLeft"]) {
            player.vx -= 0.5;
            if (player.vx < -player.speed) player.vx = -player.speed;
            player.facing = 'left';
        } else if (keys["ArrowRight"]) {
            player.vx += 0.5;
            if (player.vx > player.speed) player.vx = player.speed;
            player.facing = 'right';
        } else {
            player.vx *= 0.85;
        }

        player.x += player.vx;
        if (player.x < cameraX + 8) player.x = cameraX + 8;

        let targetCameraX = player.x - 250;
        if (targetCameraX > cameraX) cameraX = targetCameraX;

        if (player.x + canvas.width > lastGeneratedX - 700) {
            generateChunk();
            score += 500;
            if (score > 0 && score % 2000 === 0) {
                triggerRiftTransition();
            }
        }

        player.vy += dim.gravity;
        player.y += player.vy;
        player.grounded = false;

        platforms.forEach(p => {
            if (
                player.x < p.x + p.width &&
                player.x + player.width > p.x &&
                player.y + player.height >= p.y &&
                player.y + player.height - player.vy <= p.y + 14 &&
                player.vy >= 0
            ) {
                player.y = p.y - player.height;
                player.vy = 0;
                player.grounded = true;
            }
        });

        if ((keys["ArrowUp"] || keys["Space"]) && player.grounded) {
            player.vy = player.jumpPower;
            player.grounded = false;
            spawnParticles(player.x + 16, player.y + 32, dim.accent);
        }

        enemies.forEach(en => {
            if (!en.alive) return;
            en.vy += dim.gravity;
            en.y += en.vy;
            platforms.forEach(p => {
                if (en.x < p.x + p.width && en.x + en.width > p.x && en.y + en.height >= p.y && en.y + en.height - en.vy <= p.y + 14 && en.vy >= 0) {
                    en.y = p.y - en.height;
                    en.vy = 0;
                }
            });
            en.x += en.vx;

            if (player.x < en.x + en.width && player.x + player.width > en.x && player.y < en.y + en.height && player.y + player.height > en.y) {
                if (player.vy > 0 && player.y + player.height - player.vy <= en.y + 14) {
                    en.alive = false;
                    player.vy = -10;
                    score += 300;
                    crystals += 2;
                    addFloatingText(en.x, en.y - 15, "+300 CRITICAL STOMP", "#00ffff");
                    spawnParticles(en.x + 16, en.y + 16, '#00ffff');
                } else {
                    triggerGameOver();
                }
            }
        });

        crystalsList.forEach(cr => {
            if (!cr.collected) {
                let dist = Math.hypot(cr.x - (player.x + player.width/2), cr.y - (player.y + player.height/2));
                if (dist < cr.radius + 14) {
                    cr.collected = true;
                    score += 200;
                    crystals += 1;
                    addFloatingText(cr.x, cr.y - 15, "+200", "#ffff00");
                    spawnParticles(cr.x, cr.y, '#ffff00');
                }
            }
        });

        particles.forEach((p, idx) => {
            p.x += p.vx; p.y += p.vy; p.life--;
            if (p.life <= 0) particles.splice(idx, 1);
        });

        floatingTexts.forEach((ft, idx) => {
            ft.y -= 0.8; ft.life--;
            if (ft.life <= 0) floatingTexts.splice(idx, 1);
        });

        if (player.y > canvas.height + 60) triggerGameOver();

        document.getElementById('hudDim').innerText = dim.name;
        document.getElementById('hudScore').innerText = score;
        document.getElementById('hudHighScore').innerText = highScore;
        document.getElementById('hudCoins').innerText = crystals;
    }

    function draw() {
        let dim = dimensions[currentDimensionIndex];
        ctx.fillStyle = dim.bg;
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.save();
        ctx.translate(Math.floor(-cameraX), 0);

        // Draw Platforms
        platforms.forEach(p => {
            if (p.x + p.width >= cameraX - 100 && p.x <= cameraX + canvas.width + 100) {
                ctx.fillStyle = dim.ground;
                ctx.fillRect(p.x, p.y, p.width, p.height + 200);
                ctx.fillStyle = dim.accent;
                ctx.fillRect(p.x, p.y, p.width, 8);
            }
        });

        // Draw Crystals
        crystalsList.forEach(cr => {
            if (!cr.collected) {
                ctx.fillStyle = '#ffff00';
                ctx.beginPath();
                ctx.arc(cr.x, cr.y, cr.radius, 0, Math.PI * 2);
                ctx.fill();
                ctx.fillStyle = '#ff00ff';
                ctx.beginPath();
                ctx.arc(cr.x, cr.y, cr.radius - 3, 0, Math.PI * 2);
                ctx.fill();
            }
        });

        // Draw Enemies
        enemies.forEach(en => {
            if (en.alive) {
                ctx.fillStyle = dim.accent;
                ctx.fillRect(en.x, en.y, en.width, en.height);
                ctx.fillStyle = '#ffffff';
                ctx.fillRect(en.x + 6, en.y + 8, 6, 6);
                ctx.fillRect(en.x + 20, en.y + 8, 6, 6);
            }
        });

        // Draw Player
        ctx.fillStyle = dim.accent;
        ctx.fillRect(player.x, player.y, player.width, player.height);
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(player.x + (player.facing === 'right' ? 18 : 6), player.y + 8, 8, 6);

        particles.forEach(p => {
            ctx.fillStyle = p.color;
            ctx.fillRect(p.x, p.y, 4, 4);
        });

        floatingTexts.forEach(ft => {
            ctx.fillStyle = ft.color;
            ctx.font = "bold 12px 'Courier New'";
            ctx.fillText(ft.text, ft.x, ft.y);
        });

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
