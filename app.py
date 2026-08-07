import streamlit as st

st.set_page_config(
    page_title="Infinite Classic Mario - Balanced",
    page_icon="🍄",
    layout="centered"
)

st.title("🍄 Infinite Classic Mario")
st.write("An endlessly generating recreation with perfectly balanced jump physics, accessible obstacles, and classic NES mechanics.")

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

    let cameraX = 0;
    let lastGeneratedX = 0;

    const player = {
        x: 64,
        y: 200,
        width: 32,
        height: 32,
        vx: 0,
        vy: 0,
        speed: 3.8,
        jumpPower: -12.0, // Increased jump height to comfortably clear all standard blocks and pipes
        gravity: 0.5,     // Smoother gravity arc
        grounded: false,
        facing: 'right'
    };

    let platforms = [];
    let enemies = [];
    let coins = [];
    let decorations = [];

    // --- PROCEDURAL WORLD GENERATION (BALANCED HEIGHTS) ---

    function addGround(startX, width) {
        platforms.push({ x: startX, y: 384, width: width, height: 48, type: 'ground' });
    }

    function addPipe(x, height) {
        // Max pipe height kept safely within Mario's jump capability
        platforms.push({ x: x, y: 384 - height, width: 64, height: height, type: 'pipe' });
    }

    function addQuestionBlock(x, y, hasCoin=true) {
        platforms.push({ x: x, y: y, width: 32, height: 32, type: 'question' });
        if (hasCoin) coins.push({ x: x + 16, y: y - 24, radius: 10, collected: false });
    }

    function addBrick(x, y) {
        platforms.push({ x: x, y: y, width: 32, height: 32, type: 'brick' });
    }

    function addStaircase(startX, steps, ascend=true) {
        for (let i = 0; i < steps; i++) {
            let height = (ascend ? i + 1 : steps - i) * 32;
            let stepX = startX + (i * 32);
            platforms.push({ x: stepX, y: 384 - height, width: 32, height: height, type: 'brick' });
        }
    }

    function addGoomba(x, y) {
        enemies.push({ x: x, y: y, width: 32, height: 32, vx: -1.2, alive: true, vy: 0 });
    }

    function generateChunk() {
        let groundWidth = 900 + Math.random() * 500;
        addGround(lastGeneratedX, groundWidth);

        // Scenery decoration
        decorations.push({ x: lastGeneratedX + Math.random() * 250, y: 70, type: 'cloud' });
        decorations.push({ x: lastGeneratedX + 500 + Math.random() * 200, y: 60, type: 'cloud' });
        decorations.push({ x: lastGeneratedX + Math.random() * 400, y: 352, type: 'bush' });

        // Safe, fully interactive patterns
        let pattern = Math.floor(Math.random() * 4);
        
        if (pattern === 0) {
            // Standard Pipes & Goombas
            addPipe(lastGeneratedX + 280, 48); // Small pipe
            addPipe(lastGeneratedX + 550, 64); // Medium pipe
            addGoomba(lastGeneratedX + 420, 352);
            addGoomba(lastGeneratedX + 680, 352);
        } else if (pattern === 1) {
            // Accessible Question Blocks & Bricks
            addBrick(lastGeneratedX + 220, 272);
            addQuestionBlock(lastGeneratedX + 252, 272);
            addBrick(lastGeneratedX + 284, 272);
            addGoomba(lastGeneratedX + 350, 352);
        } else if (pattern === 2) {
            // Classic Staircase pyramid
            addStaircase(lastGeneratedX + 250, 4, true);
            addStaircase(lastGeneratedX + 378, 4, false);
            addGoomba(lastGeneratedX + 520, 352);
        } else if (pattern === 3) {
            // Coin row with low obstacle
            addPipe(lastGeneratedX + 300, 48);
            addQuestionBlock(lastGeneratedX + 300, 192);
            addQuestionBlock(lastGeneratedX + 332, 192);
            addGoomba(lastGeneratedX + 450, 352);
        }

        lastGeneratedX += groundWidth;
        
        // Balanced pit gaps (not too wide, fully jumpable)
        let pitSize = 80 + Math.random() * 70;
        lastGeneratedX += pitSize;
    }

    // Initialize starting area
    addGround(0, 1000);
    lastGeneratedX = 1000;
    generateChunk();

    // --- INPUT HANDLING ---
    window.addEventListener("keydown", (e) => {
        keys[e.code] = true;
        if(["Space", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(e.code)) {
            e.preventDefault();
        }
    });

    window.addEventListener("keyup", (e) => {
        keys[e.code] = false;
    });

    // --- GAME LOOP ---
    function update() {
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

        let targetCameraX = player.x - 250;
        if (targetCameraX > cameraX) {
            cameraX = targetCameraX;
        }

        if (player.x + canvas.width > lastGeneratedX - 700) {
            generateChunk();
        }

        // Physics & Platform Collision
        player.vy += player.gravity;
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
            }
        });

        // Jump trigger
        if ((keys["ArrowUp"] || keys["Space"]) && player.grounded) {
            player.vy = player.jumpPower;
            player.grounded = false;
        }

        // Enemy Physics & AI
        enemies.forEach(enemy => {
            if (!enemy.alive) return;
            
            enemy.vy += player.gravity;
            enemy.y += enemy.vy;
            
            platforms.forEach(platform => {
                if (
                    enemy.x < platform.x + platform.width &&
                    enemy.x + enemy.width > platform.x &&
                    enemy.y + enemy.height >= platform.y &&
                    enemy.y + enemy.height - enemy.vy <= platform.y + 14 &&
                    enemy.vy >= 0
                ) {
                    enemy.y = platform.y - enemy.height;
                    enemy.vy = 0;
                }
            });

            enemy.x += enemy.vx;

            // Player collision with Goomba
            if (
                player.x < enemy.x + enemy.width &&
                player.x + player.width > enemy.x &&
                player.y < enemy.y + enemy.height &&
                player.y + player.height > enemy.y
            ) {
                if (player.vy > 0 && player.y + player.height - player.vy <= enemy.y + 14) {
                    enemy.alive = false;
                    player.vy = -9; // Satisfying bounce
                    score += 100;
                } else {
                    player.x = cameraX + 64;
                    player.y = 100;
                    player.vy = 0;
                    score = Math.max(0, score - 150);
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
        if (player.y > canvas.height + 80) {
            player.x = cameraX + 64;
            player.y = 100;
            player.vy = 0;
            score = Math.max(0, score - 300);
        }

        // Cleanup offscreen objects
        if (platforms.length > 80 && platforms[0].x < cameraX - 1000) {
            platforms = platforms.filter(p => p.x + p.width > cameraX - 800);
            enemies = enemies.filter(e => e.x > cameraX - 800);
            coins = coins.filter(c => c.x > cameraX - 800);
            decorations = decorations.filter(d => d.x > cameraX - 800);
        }
    }

    // --- RENDERING ---
    function drawPixelMario(x, y, facing) {
        ctx.fillStyle = '#c84c0c';
        ctx.fillRect(x + (facing === 'right' ? 8 : 4), y, 20, 8);
        ctx.fillRect(x + (facing === 'right' ? 16 : 0), y + 4, 16, 4);
        
        ctx.fillStyle = '#f83800';
        ctx.fillRect(x + (facing === 'right' ? 12 : 4), y + 8, 16, 10);
        
        ctx.fillStyle = '#000000';
        ctx.fillRect(x + (facing === 'right' ? 16 : 4), y + 14, 12, 4);

        ctx.fillStyle = '#0070ec';
        ctx.fillRect(x + 6, y + 18, 20, 10);

        ctx.fillStyle = '#8b4513';
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

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        ctx.save();
        ctx.translate(Math.floor(-cameraX), 0);

        // Clouds & Bushes
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

        // Platforms & Obstacles
        platforms.forEach(platform => {
            if (platform.x + platform.width >= cameraX - 100 && platform.x <= cameraX + canvas.width + 100) {
                if (platform.type === 'ground') {
                    ctx.fillStyle = '#c84c0c';
                    ctx.fillRect(platform.x, platform.y, platform.width, platform.height + 200);
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

        // Coins
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

        // Enemies
        enemies.forEach(enemy => {
            if (enemy.alive && enemy.x >= cameraX - 100 && enemy.x <= cameraX + canvas.width + 100) {
                drawGoomba(enemy.x, enemy.y);
            }
        });

        // Player
        drawPixelMario(player.x, player.y, player.facing);

        ctx.restore();

        // HUD
        ctx.fillStyle = "#000000";
        ctx.fillRect(0, 0, canvas.width, 45);

        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 16px 'Courier New'";
        ctx.fillText("MARIO", 40, 28);
        ctx.fillText(String(score).padStart(6, '0'), 40, 44);

        ctx.fillText("COINS", 280, 28);
        ctx.fillText("x" + String(coinsCollected).padStart(2, '0'), 296, 44);

        ctx.fillText("DISTANCE", 550, 28);
        ctx.fillText(Math.floor(cameraX / 10) + "m", 550, 44);
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
