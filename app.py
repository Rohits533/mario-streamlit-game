import streamlit as st

st.set_page_config(
    page_title="Infinite Classic Mario",
    page_icon="🍄",
    layout="centered"
)

st.title("🍄 Infinite Classic Mario")
st.write("An endlessly generating recreation of the classic NES visual style. Dodge Goombas, jump over pits, and scale staircases forever!")

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
        speed: 4.0,
        jumpPower: -10.5,
        gravity: 0.55,
        grounded: false,
        facing: 'right'
    };

    let platforms = [];
    let enemies = [];
    let coins = [];
    let decorations = [];

    // --- PROCEDURAL WORLD GENERATION ---

    function addGround(startX, width) {
        platforms.push({ x: startX, y: 384, width: width, height: 48, type: 'ground' });
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

    function addStaircase(startX, steps, ascend=true) {
        for (let i = 0; i < steps; i++) {
            let height = (ascend ? i + 1 : steps - i) * 32;
            let stepX = startX + (i * 32);
            platforms.push({ x: stepX, y: 384 - height, width: 32, height: height, type: 'brick' });
        }
    }

    function addGoomba(x, y) {
        enemies.push({ x: x, y: y, width: 32, height: 32, vx: -1.5, alive: true });
    }

    function generateChunk() {
        // Base ground size for this chunk
        let groundWidth = 800 + Math.random() * 600;
        addGround(lastGeneratedX, groundWidth);

        // Decorate sky and ground
        decorations.push({ x: lastGeneratedX + Math.random() * 200, y: 60 + Math.random() * 40, type: 'cloud' });
        decorations.push({ x: lastGeneratedX + 400 + Math.random() * 200, y: 60 + Math.random() * 40, type: 'cloud' });
        decorations.push({ x: lastGeneratedX + Math.random() * 300, y: 352, type: 'bush' });

        // Add Obstacles based on random pattern
        let pattern = Math.floor(Math.random() * 4);
        
        if (pattern === 0) {
            // Pattern 0: Pipes & Goombas
            addPipe(lastGeneratedX + 300, 64);
            addPipe(lastGeneratedX + 600, 96);
            addGoomba(lastGeneratedX + 500, 352);
            addGoomba(lastGeneratedX + 750, 352);
        } else if (pattern === 1) {
            // Pattern 1: Question Blocks & Floating Bricks
            addBrick(lastGeneratedX + 200, 256);
            addQuestionBlock(lastGeneratedX + 232, 256);
            addBrick(lastGeneratedX + 264, 256);
            addQuestionBlock(lastGeneratedX + 232, 160); // High block
            addGoomba(lastGeneratedX + 300, 352);
            addGoomba(lastGeneratedX + 350, 352);
        } else if (pattern === 2) {
            // Pattern 2: The Classic Block Staircase
            addStaircase(lastGeneratedX + 300, 5, true);
            // Gap then descend
            addStaircase(lastGeneratedX + 524, 5, false);
            addGoomba(lastGeneratedX + 700, 352);
        } else if (pattern === 3) {
            // Pattern 3: Harder Pipe Jumps
            addPipe(lastGeneratedX + 200, 128);
            addPipe(lastGeneratedX + 400, 128);
            addGoomba(lastGeneratedX + 300, 352); // Trapped Goomba
            addQuestionBlock(lastGeneratedX + 600, 256);
        }

        // Advance generator and add a pit (gap in ground)
        lastGeneratedX += groundWidth;
        
        // Add a pit (gap) of varying size
        let pitSize = 100 + Math.random() * 120;
        lastGeneratedX += pitSize;
    }

    // Initialize first safe chunk
    addGround(0, 1200);
    lastGeneratedX = 1200;
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
        // Player Movement
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
        
        // Prevent walking backwards off camera
        if (player.x < cameraX + 8) player.x = cameraX + 8;

        // Infinite Camera Scroll
        let targetCameraX = player.x - 250;
        if (targetCameraX > cameraX) {
            cameraX = targetCameraX;
        }

        // Generate more level ahead
        if (player.x + canvas.width > lastGeneratedX - 800) {
            generateChunk();
        }

        // Physics & Collision
        player.vy += player.gravity;
        player.y += player.vy;
        player.grounded = false;

        platforms.forEach(platform => {
            if (
                player.x < platform.x + platform.width &&
                player.x + player.width > platform.x &&
                player.y + player.height >= platform.y &&
                player.y + player.height - player.vy <= platform.y + 16 && // Floor tolerance
                player.vy >= 0
            ) {
                player.y = platform.y - player.height;
                player.vy = 0;
                player.grounded = true;
            }
        });

        // Jump
        if ((keys["ArrowUp"] || keys["Space"]) && player.grounded) {
            player.vy = player.jumpPower;
            player.grounded = false;
        }

        // Enemy Logic
        enemies.forEach(enemy => {
            if (!enemy.alive) return;
            
            // Apply gravity to enemy
            enemy.vy = (enemy.vy || 0) + player.gravity;
            enemy.y += enemy.vy;
            
            // Enemy Floor Collision
            let enemyGrounded = false;
            platforms.forEach(platform => {
                if (
                    enemy.x < platform.x + platform.width &&
                    enemy.x + enemy.width > platform.x &&
                    enemy.y + enemy.height >= platform.y &&
                    enemy.y + enemy.height - enemy.vy <= platform.y + 16 &&
                    enemy.vy >= 0
                ) {
                    enemy.y = platform.y - enemy.height;
                    enemy.vy = 0;
                    enemyGrounded = true;
                }
            });

            // Enemy Wall Collision (Pipes/Bricks)
            platforms.forEach(platform => {
                if (platform.type !== 'ground' && 
                    enemy.y + enemy.height > platform.y && 
                    enemy.y < platform.y + platform.height) {
                    if (enemy.x < platform.x + platform.width && enemy.x + enemy.width > platform.x) {
                        enemy.vx *= -1; // Turn around
                        enemy.x += enemy.vx * 2;
                    }
                }
            });

            enemy.x += enemy.vx;

            // Player vs Enemy Collision
            if (
                player.x < enemy.x + enemy.width &&
                player.x + player.width > enemy.x &&
                player.y < enemy.y + enemy.height &&
                player.y + player.height > enemy.y
            ) {
                // Stomp check
                if (player.vy > 0 && player.y + player.height - player.vy <= enemy.y + 16) {
                    enemy.alive = false;
                    player.vy = -8; // Bounce off enemy
                    score += 100;
                } else {
                    // Damage - Reset Player (For infinite run, push back)
                    player.x = cameraX + 64;
                    player.y = 100;
                    player.vy = 0;
                    score = Math.max(0, score - 200);
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

        // Pit Fall Check (Death)
        if (player.y > canvas.height + 100) {
            player.x = cameraX + 64;
            player.y = 100; // Drop from sky
            player.vy = 0;
            score = Math.max(0, score - 500);
        }

        // Garbage Collection: Remove objects far behind the camera to prevent lag
        if (platforms.length > 100 && platforms[0].x < cameraX - 1000) {
            platforms = platforms.filter(p => p.x + p.width > cameraX - 800);
            enemies = enemies.filter(e => e.x > cameraX - 800);
            coins = coins.filter(c => c.x > cameraX - 800);
            decorations = decorations.filter(d => d.x > cameraX - 800);
        }
    }

    // --- RENDERING ---
    function drawPixelMario(x, y, facing) {
        ctx.fillStyle = '#c84c0c'; // Red
        ctx.fillRect(x + (facing === 'right' ? 8 : 4), y, 20, 8);
        ctx.fillRect(x + (facing === 'right' ? 16 : 0), y + 4, 16, 4);
        
        ctx.fillStyle = '#f83800'; // Skin
        ctx.fillRect(x + (facing === 'right' ? 12 : 4), y + 8, 16, 10);
        
        ctx.fillStyle = '#000000'; // Mustache/Eye
        ctx.fillRect(x + (facing === 'right' ? 16 : 4), y + 14, 12, 4);

        ctx.fillStyle = '#0070ec'; // Blue Overalls
        ctx.fillRect(x + 6, y + 18, 20, 10);

        ctx.fillStyle = '#8b4513'; // Boots
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
        ctx.translate(Math.floor(-cameraX), 0);

        // Draw Scenery (Clouds & Bushes)
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

        // Draw Level Elements
        platforms.forEach(platform => {
            if (platform.x + platform.width >= cameraX - 100 && platform.x <= cameraX + canvas.width + 100) {
                if (platform.type === 'ground') {
                    ctx.fillStyle = '#c84c0c';
                    ctx.fillRect(platform.x, platform.y, platform.width, platform.height + 200); // Fill deep down
                    ctx.fillStyle = '#00a800';
                    ctx.fillRect(platform.x, platform.y, platform.width, 8); // Grass top
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
                    ctx.fillRect(platform.x - 4, platform.y, platform.width + 8, 16); // Pipe rim
                    ctx.strokeStyle = '#000000';
                    ctx.lineWidth = 2;
                    ctx.strokeRect(platform.x, platform.y, platform.width, platform.height);
                    ctx.strokeRect(platform.x - 4, platform.y, platform.width + 8, 16);
                }
            }
        });

        // Draw Coins
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

        // Draw Enemies
        enemies.forEach(enemy => {
            if (enemy.alive && enemy.x >= cameraX - 100 && enemy.x <= cameraX + canvas.width + 100) {
                drawGoomba(enemy.x, enemy.y);
            }
        });

        // Draw Player
        drawPixelMario(player.x, player.y, player.facing);

        ctx.restore();

        // Authentic HUD
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
