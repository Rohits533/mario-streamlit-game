import streamlit as st

st.set_page_config(
    page_title="Classic Retro Mario Bros",
    page_icon="🍄",
    layout="centered"
)

st.title("🍄 Classic Retro Mario Bros")
st.write("An authentic recreation of the classic NES 2D platformer with infinite side-scrolling levels.")

game_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        body {
            margin: 0;
            background: #000;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-family: 'Courier New', Courier, monospace;
            color: white;
        }
        .game-container {
            text-align: center;
        }
        canvas {
            border: 4px solid #fff;
            background: #5c94fc; /* Classic NES Mario Blue Sky */
            box-shadow: 0 0 25px rgba(92, 148, 252, 0.4);
            image-rendering: pixelated;
            image-rendering: crisp-edges;
        }
        .instructions {
            margin-top: 10px;
            font-size: 14px;
            color: #ddd;
        }
    </style>
</head>
<body>

<div class="game-container">
    <canvas id="gameCanvas" width="768" height="432"></canvas>
    <div class="instructions">
        Controls: <strong>Arrow Left / Right</strong> to Walk | <strong>Arrow Up</strong> or <strong>Spacebar</strong> to Jump
    </div>
</div>

<script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");

    // Disable anti-aliasing for retro pixelated look
    ctx.imageSmoothingEnabled = false;

    let score = 0;
    let coinsCollected = 0;
    let timeRemaining = 400;
    const keys = {};

    let gameState = 'ENTERING';
    let entryTimer = 0;
    let cameraX = 0;

    const player = {
        x: 64,
        y: 300,
        width: 32,
        height: 32,
        vx: 0,
        vy: 0,
        speed: 3.5,
        jumpPower: -10.5,
        gravity: 0.5,
        grounded: false,
        facing: 'right'
    };

    // Classic NES Level Layout (Ground + Bricks + Question Blocks + Pipes)
    let platforms = [
        { x: 0, y: 384, width: 2500, height: 48, type: 'ground' },
        { x: 256, y: 256, width: 32, height: 32, type: 'question' },
        { x: 352, y: 256, width: 96, height: 32, type: 'brick' },
        { x: 384, y: 256, width: 32, height: 32, type: 'question' },
        { x: 608, y: 320, width: 64, height: 64, type: 'pipe' }, // Green Pipe
        { x: 800, y: 256, width: 128, height: 32, type: 'brick' },
        { x: 1050, y: 288, width: 64, height: 96, type: 'pipe' }
    ];

    let coins = [
        { x: 384, y: 210, radius: 10, collected: false, bounce: 0 },
        { x: 832, y: 210, radius: 10, collected: false, bounce: 0 },
        { x: 864, y: 210, radius: 10, collected: false, bounce: 0 }
    ];

    let lastGeneratedX = 2500;

    window.addEventListener("keydown", (e) => {
        keys[e.code] = true;
        if(["Space", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(e.code)) {
            e.preventDefault();
        }
    });

    window.addEventListener("keyup", (e) => {
        keys[e.code] = false;
    });

    // Infinite procedural retro world generation
    function generateRetroWorld() {
        if (player.x + canvas.width > lastGeneratedX - 500) {
            let chunkX = lastGeneratedX;
            let groundWidth = 1200;
            
            platforms.push({ x: chunkX, y: 384, width: groundWidth, height: 48, type: 'ground' });

            // Add pipes and block structures ahead
            platforms.push({ x: chunkX + 300, y: 320, width: 64, height: 64, type: 'pipe' });
            platforms.push({ x: chunkX + 600, y: 256, width: 160, height: 32, type: 'brick' });
            
            coins.push({ x: chunkX + 650, y: 210, radius: 10, collected: false, bounce: 0 });
            coins.push({ x: chunkX + 682, y: 210, radius: 10, collected: false, bounce: 0 });

            platforms.push({ x: chunkX + 900, y: 288, width: 64, height: 96, type: 'pipe' });

            lastGeneratedX += groundWidth;
        }
    }

    function update() {
        if (gameState === 'ENTERING') {
            entryTimer += 0.03;
            player.y = 384 - 32 - Math.sin(entryTimer * Math.PI) * 60;
            player.x = 64 + (entryTimer * 10);
            if (entryTimer >= 1) {
                gameState = 'PLAYING';
                player.y = 384 - 32;
            }
            return;
        }

        // Horizontal Movement
        if (keys["ArrowLeft"]) {
            player.vx = -player.speed;
            player.facing = 'left';
        } else if (keys["ArrowRight"]) {
            player.vx = player.speed;
            player.facing = 'right';
        } else {
            player.vx = 0;
        }

        player.x += player.vx;
        if (player.x < cameraX + 8) player.x = cameraX + 8;

        // Classic Camera scroll
        let targetCameraX = player.x - 200;
        if (targetCameraX > cameraX) {
            cameraX = targetCameraX;
        }

        // Gravity & Physics
        player.vy += player.gravity;
        player.y += player.vy;
        player.grounded = false;

        platforms.forEach(platform => {
            if (
                player.x < platform.x + platform.width &&
                player.x + player.width > platform.x &&
                player.y + player.height >= platform.y &&
                player.y + player.height - player.vy <= platform.y + 10 &&
                player.vy >= 0
            ) {
                player.y = platform.y - player.height;
                player.vy = 0;
                player.grounded = true;
            }
        });

        if ((keys["ArrowUp"] || keys["Space"]) && player.grounded) {
            player.vy = player.jumpPower;
            player.grounded = false;
        }

        // Coin Collection
        coins.forEach(coin => {
            if (!coin.collected) {
                let dist = Math.hypot(coin.x - (player.x + player.width / 2), coin.y - (player.y + player.height / 2));
                if (dist < coin.radius + player.width / 3) {
                    coin.collected = true;
                    score += 200;
                    coinsCollected += 1;
                }
            }
        });

        generateRetroWorld();

        // Pit Fall Check
        if (player.y > canvas.height) {
            player.x = cameraX + 64;
            player.y = 300;
            player.vy = 0;
            score = Math.max(0, score - 100);
            gameState = 'ENTERING';
            entryTimer = 0;
        }
    }

    function drawPixelMario(x, y, facing) {
        // Classic NES Mario 8-bit / 16-bit pixel block representation
        ctx.fillStyle = '#c84c0c'; // Red cap & shirt
        // Hat
        ctx.fillRect(x + (facing === 'right' ? 8 : 4), y, 20, 8);
        ctx.fillRect(x + (facing === 'right' ? 16 : 0), y + 4, 16, 4);
        
        // Face/Skin
        ctx.fillStyle = '#f83800'; // Face skin tone approximation
        ctx.fillRect(x + (facing === 'right' ? 12 : 4), y + 8, 16, 10);
        
        // Mustache / Eyes
        ctx.fillStyle = '#000000';
        ctx.fillRect(x + (facing === 'right' ? 16 : 4), y + 14, 12, 4);

        // Overalls (Blue)
        ctx.fillStyle = '#0070ec';
        ctx.fillRect(x + 6, y + 18, 20, 10);

        // Shoes (Brown)
        ctx.fillStyle = '#8b4513';
        ctx.fillRect(x + (facing === 'right' ? 18 : 2), y + 28, 12, 4);
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        ctx.save();
        ctx.translate(-cameraX, 0);

        // Retro Pixel Clouds & Bushes Background Elements
        ctx.fillStyle = "#ffffff";
        for (let i = -1; i < 10; i++) {
            let cx = i * 400 + 100;
            // Pixel Cloud 1
            ctx.fillRect(cx, 80, 64, 16);
            ctx.fillRect(cx + 16, 64, 32, 16);
        }

        // Retro Green Bushes
        ctx.fillStyle = "#00a800";
        for (let i = -1; i < 10; i++) {
            let bx = i * 450 + 250;
            ctx.fillRect(bx, 352, 96, 32);
            ctx.fillRect(bx + 16, 336, 64, 16);
        }

        // Draw Platforms / Blocks / Pipes
        platforms.forEach(platform => {
            if (platform.x + platform.width >= cameraX && platform.x <= cameraX + canvas.width) {
                if (platform.type === 'ground') {
                    // Classic Brown/Orange NES Brick Ground Pattern
                    ctx.fillStyle = '#c84c0c';
                    ctx.fillRect(platform.x, platform.y, platform.width, platform.height);
                    // Top green grass border line
                    ctx.fillStyle = '#00a800';
                    ctx.fillRect(platform.x, platform.y, platform.width, 8);
                } else if (platform.type === 'brick') {
                    // NES Brick Block
                    ctx.fillStyle = '#c84c0c';
                    ctx.fillRect(platform.x, platform.y, platform.width, platform.height);
                    ctx.strokeStyle = '#000000';
                    ctx.lineWidth = 2;
                    ctx.strokeRect(platform.x, platform.y, platform.width, platform.height);
                } else if (platform.type === 'question') {
                    // Question Block (?)
                    ctx.fillStyle = '#fcbc3c';
                    ctx.fillRect(platform.x, platform.y, platform.width, platform.height);
                    ctx.strokeStyle = '#000000';
                    ctx.lineWidth = 2;
                    ctx.strokeRect(platform.x, platform.y, platform.width, platform.height);
                    
                    ctx.fillStyle = '#000000';
                    ctx.font = "bold 18px monospace";
                    ctx.fillText("?", platform.x + 10, platform.y + 23);
                } else if (platform.type === 'pipe') {
                    // Classic Green Mario Pipe
                    ctx.fillStyle = '#00a800';
                    ctx.fillRect(platform.x, platform.y, platform.width, platform.height);
                    // Pipe rim
                    ctx.fillRect(platform.x - 4, platform.y, platform.width + 8, 16);
                    ctx.strokeStyle = '#000000';
                    ctx.lineWidth = 2;
                    ctx.strokeRect(platform.x, platform.y, platform.width, platform.height);
                    ctx.strokeRect(platform.x - 4, platform.y, platform.width + 8, 16);
                }
            }
        });

        // Draw Coins
        coins.forEach(coin => {
            if (!coin.collected && coin.x >= cameraX - 30 && coin.x <= cameraX + canvas.width + 30) {
                ctx.fillStyle = '#fcbc3c';
                ctx.beginPath();
                ctx.arc(coin.x, coin.y, coin.radius, 0, Math.PI * 2);
                ctx.fill();
                ctx.strokeStyle = '#000000';
                ctx.lineWidth = 2;
                ctx.stroke();
            }
        });

        // Draw Player
        drawPixelMario(player.x, player.y, player.facing);

        ctx.restore();

        // Classic NES HUD Top Banner Overlay
        ctx.fillStyle = "#000000";
        ctx.fillRect(0, 0, canvas.width, 45);

        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 16px 'Courier New'";
        ctx.fillText("MARIO", 40, 28);
        ctx.fillText(String(score).padStart(6, '0'), 40, 44);

        ctx.fillText("WORLD", 280, 28);
        ctx.fillText("1-1", 296, 44);

        ctx.fillText("TIME", 450, 28);
        ctx.fillText("399", 466, 44);
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

st.components.v1.html(game_html, height=480, scrolling=False)
