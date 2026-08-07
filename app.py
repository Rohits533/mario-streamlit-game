import streamlit as st

st.set_page_config(
    page_title="Super Mario Bros - World 1-1",
    page_icon="🍄",
    layout="centered"
)

st.title("🍄 Super Mario Bros - World 1-1")
st.write("An authentic recreation featuring the complete World 1-1 layout, Goomba enemies, staircases, pipes, and the end castle!")

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
            background: #5c94fc; /* Classic NES Blue */
            box-shadow: 0 0 25px rgba(92, 148, 252, 0.5);
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
    ctx.imageSmoothingEnabled = false;

    let score = 0;
    let coinsCollected = 0;
    const keys = {};

    let gameState = 'PLAYING';
    let cameraX = 0;

    const player = {
        x: 64,
        y: 300,
        width: 32,
        height: 32,
        vx: 0,
        vy: 0,
        speed: 3.2,
        jumpPower: -10,
        gravity: 0.5,
        grounded: false,
        facing: 'right'
    };

    // Authentic World 1-1 Layout Elements
    let platforms = [
        // Ground with gaps (Pit between x: 1344 and 1440)
        { x: 0, y: 384, width: 1344, height: 48, type: 'ground' },
        { x: 1440, y: 384, width: 650, height: 48, type: 'ground' },
        { x: 2176, y: 384, width: 1500, height: 48, type: 'ground' },

        // Pipes
        { x: 608, y: 320, width: 64, height: 64, type: 'pipe' },
        { x: 912, y: 288, width: 64, height: 96, type: 'pipe' },
        { x: 1136, y: 256, width: 64, height: 128, type: 'pipe' },
        { x: 1632, y: 256, width: 64, height: 128, type: 'pipe' },
        { x: 1984, y: 320, width: 64, height: 64, type: 'pipe' },

        // Question Blocks & Bricks
        { x: 512, y: 256, width: 32, height: 32, type: 'question' },
        { x: 672, y: 256, width: 32, height: 32, type: 'question' },
        { x: 704, y: 256, width: 32, height: 32, type: 'brick' },
        { x: 736, y: 256, width: 32, height: 32, type: 'question' },
        { x: 768, y: 256, width: 32, height: 32, type: 'brick' },
        { x: 800, y: 256, width: 32, height: 32, type: 'question' },

        // Elevated Block platform
        { x: 352, y: 256, width: 96, height: 32, type: 'brick' },

        // Staircases near end
        // First pyramid stairs
        { x: 2368, y: 352, width: 32, height: 32, type: 'brick' },
        { x: 2400, y: 320, width: 32, height: 64, type: 'brick' },
        { x: 2432, y: 288, width: 32, height: 96, type: 'brick' },
        { x: 2464, y: 256, width: 32, height: 128, type: 'brick' },

        // Second pyramid stairs
        { x: 2560, y: 256, width: 32, height: 128, type: 'brick' },
        { x: 2592, y: 288, width: 32, height: 96, type: 'brick' },
        { x: 2624, y: 320, width: 32, height: 64, type: 'brick' },
        { x: 2656, y: 352, width: 32, height: 32, type: 'brick' },

        // Flagpole Base block
        { x: 2816, y: 352, width: 32, height: 32, type: 'block' }
    ];

    let enemies = [
        { x: 700, y: 352, width: 32, height: 32, vx: -1, alive: true },
        { x: 1200, y: 352, width: 32, height: 32, vx: -1, alive: true },
        { x: 1750, y: 352, width: 32, height: 32, vx: -1, alive: true },
        { x: 1820, y: 352, width: 32, height: 32, vx: -1, alive: true }
    ];

    let coins = [
        { x: 512, y: 210, radius: 10, collected: false },
        { x: 704, y: 210, radius: 10, collected: false },
        { x: 736, y: 210, radius: 10, collected: false },
        { x: 768, y: 210, radius: 10, collected: false }
    ];

    window.addEventListener("keydown", (e) => {
        keys[e.code] = true;
        if(["Space", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(e.code)) {
            e.preventDefault();
        }
    });

    window.addEventListener("keyup", (e) => {
        keys[e.code] = false;
    });

    function update() {
        if (gameState !== 'PLAYING') return;

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

        let targetCameraX = player.x - 200;
        if (targetCameraX > cameraX && cameraX < 2400) {
            cameraX = targetCameraX;
        }

        player.vy += player.gravity;
        player.y += player.vy;
        player.grounded = false;

        platforms.forEach(platform => {
            if (
                player.x < platform.x + platform.width &&
                player.x + player.width > platform.x &&
                player.y + player.height >= platform.y &&
                player.y + player.height - player.vy <= platform.y + 12 &&
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

        // Enemy AI & Collision
        enemies.forEach(enemy => {
            if (!enemy.alive) return;
            enemy.x += enemy.vx;

            // Simple patrol bounds
            if (enemy.x < 200 || enemy.x > 2500) enemy.vx *= -1;

            // Player collision check
            if (
                player.x < enemy.x + enemy.width &&
                player.x + player.width > enemy.x &&
                player.y < enemy.y + enemy.height &&
                player.y + player.height > enemy.y
            ) {
                if (player.vy > 0 && player.y + player.height - player.vy <= enemy.y + 10) {
                    // Jumped on Goomba
                    enemy.alive = false;
                    player.vy = -7;
                    score += 100;
                } else {
                    // Hit by Goomba
                    player.x = cameraX + 64;
                    player.y = 300;
                    player.vy = 0;
                }
            }
        });

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

        // Pit Fall Check
        if (player.y > canvas.height) {
            player.x = cameraX + 64;
            player.y = 300;
            player.vy = 0;
            score = Math.max(0, score - 100);
        }
    }

    function drawPixelMario(x, y, facing) {
        ctx.fillStyle = '#c84c0c'; // Red cap & shirt
        ctx.fillRect(x + (facing === 'right' ? 8 : 4), y, 20, 8);
        ctx.fillRect(x + (facing === 'right' ? 16 : 0), y + 4, 16, 4);
        
        ctx.fillStyle = '#f83800'; // Skin tone
        ctx.fillRect(x + (facing === 'right' ? 12 : 4), y + 8, 16, 10);
        
        ctx.fillStyle = '#000000'; // Mustache
        ctx.fillRect(x + (facing === 'right' ? 16 : 4), y + 14, 12, 4);

        ctx.fillStyle = '#0070ec'; // Overalls
        ctx.fillRect(x + 6, y + 18, 20, 10);

        ctx.fillStyle = '#8b4513'; // Shoes
        ctx.fillRect(x + (facing === 'right' ? 18 : 2), y + 28, 12, 4);
    }

    function drawGoomba(x, y) {
        ctx.fillStyle = '#c84c0c'; // Brown body
        ctx.fillRect(x + 4, y + 8, 24, 20);
        ctx.fillStyle = '#000000'; // Feet & Eyes
        ctx.fillRect(x + 2, y + 28, 10, 4);
        ctx.fillRect(x + 20, y + 28, 10, 4);
        ctx.fillRect(x + 8, y + 14, 4, 6);
        ctx.fillRect(x + 20, y + 14, 4, 6);
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        ctx.save();
        ctx.translate(-cameraX, 0);

        // Clouds
        ctx.fillStyle = "#ffffff";
        let cloudPositions = [200, 600, 1000, 1400, 1800, 2200, 2600];
        cloudPositions.forEach(cx => {
            ctx.fillRect(cx, 80, 64, 16);
            ctx.fillRect(cx + 16, 64, 32, 16);
        });

        // Bushes
        ctx.fillStyle = "#00a800";
        let bushPositions = [300, 900, 1500, 2000];
        bushPositions.forEach(bx => {
            ctx.fillRect(bx, 352, 96, 32);
            ctx.fillRect(bx + 16, 336, 64, 16);
        });

        // Platforms, Bricks, Pipes
        platforms.forEach(platform => {
            if (platform.x + platform.width >= cameraX && platform.x <= cameraX + canvas.width) {
                if (platform.type === 'ground') {
                    ctx.fillStyle = '#c84c0c';
                    ctx.fillRect(platform.x, platform.y, platform.width, platform.height);
                    ctx.fillStyle = '#00a800';
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

        // Draw Flagpole at World End (around x: 2750)
        ctx.fillStyle = '#00a800';
        ctx.fillRect(2748, 128, 8, 256); // Pole
        ctx.fillStyle = '#fcbc3c';
        ctx.beginPath();
        ctx.arc(2752, 128, 8, 0, Math.PI * 2); // Finial ball
        ctx.fill();

        // Draw Castle at end (around x: 2850)
        ctx.fillStyle = '#c84c0c';
        ctx.fillRect(2850, 256, 128, 128);
        ctx.fillStyle = '#000000';
        ctx.fillRect(2898, 320, 32, 64); // Door

        // Coins
        coins.forEach(coin => {
            if (!coin.collected) {
                ctx.fillStyle = '#fcbc3c';
                ctx.beginPath();
                ctx.arc(coin.x, coin.y, coin.radius, 0, Math.PI * 2);
                ctx.fill();
                ctx.strokeStyle = '#000000';
                ctx.lineWidth = 2;
                ctx.stroke();
            }
        });

        // Enemies
        enemies.forEach(enemy => {
            if (enemy.alive) {
                drawGoomba(enemy.x, enemy.y);
            }
        });

        // Player
        drawPixelMario(player.x, player.y, player.facing);

        ctx.restore();

        // HUD Overlay
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
