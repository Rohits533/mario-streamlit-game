import streamlit as st

st.set_page_config(
    page_title="Infinite Classic Mario - Advanced Biomes",
    page_icon="🍄",
    layout="centered"
)

st.title("🍄 Infinite Classic Mario - Advanced Biomes")
st.write("An infinite procedural runner featuring balanced jump physics, interactive obstacles, moving platform gaps, slippery ice, and instant-death hazards!")

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
            background: #5c94fc;
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
        jumpPower: -12.0,
        gravity: 0.5,
        grounded: false,
        facing: 'right'
    };

    let platforms = [];
    let enemies = [];
    let coins = [];
    let decorations = [];
    let hazards = []; // Spikes, Lava, Quicksand pools
    let movingPlatforms = [];
    let thwomps = [];

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
        enemies.push({ x: x, y: y, width: 32, height: 32, vx: -1.2, alive: true, vy: 0 });
    }

    function generateChunk() {
        let groundWidth = 800 + Math.random() * 400;
        let biomeType = Math.random();
        
        let surfaceType = 'ground';
        if (biomeType > 0.75) surfaceType = 'ice'; // Slippery ice
        else if (biomeType > 0.5) surfaceType = 'quicksand'; // Sinking quicksand

        addGround(lastGeneratedX, groundWidth, surfaceType);

        // Scenery
        decorations.push({ x: lastGeneratedX + Math.random() * 200, y: 70, type: 'cloud' });
        decorations.push({ x: lastGeneratedX + 450 + Math.random() * 200, y: 60, type: 'cloud' });

        let pattern = Math.floor(Math.random() * 5);
        
        if (pattern === 0) {
            // Standard Pipes & Goombas
            addPipe(lastGeneratedX + 250, 48);
            addPipe(lastGeneratedX + 500, 64);
            addGoomba(lastGeneratedX + 380, 352);
        } else if (pattern === 1) {
            // Sharp Spikes on ground or blocks
            addBrick(lastGeneratedX + 300, 272);
            addQuestionBlock(lastGeneratedX + 332, 272);
            // Spikes below
            hazards.push({ x: lastGeneratedX + 380, y: 368, width: 64, height: 16, type: 'spikes' });
            addGoomba(lastGeneratedX + 480, 352);
        } else if (pattern === 2) {
            // Crushing Thwomp from above
            thwomps.push({ x: lastGeneratedX + 350, y: 80, startY: 80, width: 40, height: 40, timer: 0, crushing: false });
            addGoomba(lastGeneratedX + 360, 352);
        } else if (pattern === 3) {
            // Moving platform gap
            movingPlatforms.push({ 
                x: lastGeneratedX + 250, y: 280, width: 80, height: 16, 
                minX: lastGeneratedX + 200, maxX: lastGeneratedX + 450, vx: 1.5 
            });
            // Instant death lava pit beneath moving platform
            hazards.push({ x: lastGeneratedX + 200, y: 392, width: 280, height: 40, type: 'lava' });
        } else if (pattern === 4) {
            // Standard Blocks and Goombas
            addBrick(lastGeneratedX + 200, 256);
            addBrick(lastGeneratedX + 232, 256);
            addGoomba(lastGeneratedX + 320, 352);
            addGoomba(lastGeneratedX + 360, 352);
        }

        lastGeneratedX += groundWidth;
        
        // Bottomless pit gap or lava gap
        let pitSize = 90 + Math.random() * 80;
        if (Math.random() > 0.5) {
            // Fill pit with instant-death lava
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
        score = Math.max(0, score - 300);
    }

    function update() {
        // Horizontal Movement with Ice Slipping / Quicksand Drag
        let currentPlatformType = 'ground';
        platforms.forEach(p => {
            if (player.x + player.width > p.x && player.x < p.x + p.width && Math.abs((player.y + player.height) - p.y) < 5) {
                currentPlatformType = p.type;
            }
        });

        let acceleration = 0.4;
        let friction = 0.85;
        if (currentPlatformType === 'ice') {
            friction = 0.98; // Very slippery
        } else if (currentPlatformType === 'quicksand') {
            player.vx *= 0.7; // Slow movement in quicksand
        }

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

        // Gravity & Physics
        player.vy += player.gravity;
        player.y += player.vy;
        player.grounded = false;

        // Platform Collisions
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
                if (platform.type === 'quicksand') {
                    player.y += 1.5; // Sinking effect
                }
            }
        });

        // Moving Platforms Collision
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
                player.x += mp.vx; // Carry player along
            }
        });

        // Jump
        if ((keys["ArrowUp"] || keys["Space"]) && player.grounded) {
            player.vy = player.jumpPower;
            player.grounded = false;
        }

        // Thwomp AI (Crushing hazard)
        thwomps.forEach(t => {
            let distToPlayer = Math.abs(player.x - t.x);
            if (distToPlayer < 120) {
                t.crushing = true;
            }
            if (t.crushing) {
                t.y += 6; // Slam down fast
                if (t.y >= 340) t.y = 340;
                // Return slowly after slam
                setTimeout(() => { t.crushing = false; }, 800);
            } else if (t.y > t.startY) {
                t.y -= 2; // Rise back up
            }

            // Thwomp collision with player
            if (
                player.x < t.x + t.width &&
                player.x + player.width > t.x &&
                player.y < t.y + t.height &&
                player.y + player.height > t.y
            ) {
                resetPlayer();
            }
        });

        // Hazard Collision (Spikes & Lava = Instant Death)
        hazards.forEach(h => {
            if (
                player.x + player.width > h.x &&
                player.x < h.x + h.width &&
                player.y + player.height > h.y &&
                player.y < h.y + h.height
            ) {
                resetPlayer();
            }
        });

        // Enemy AI & Physics
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

            if (
                player.x < enemy.x + enemy.width &&
                player.x + player.width > enemy.x &&
                player.y < enemy.y + enemy.height &&
                player.y + player.height > enemy.y
            ) {
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
                    score += 200;
                    coinsCollected += 1;
                }
            }
        });

        // Bottomless Pit Fall
        if (player.y > canvas.height + 80) {
            resetPlayer();
        }

        // Cleanup offscreen objects
        if (platforms.length > 80 && platforms[0].x < cameraX - 1000) {
            platforms = platforms.filter(p => p.x + p.width > cameraX - 800);
            enemies = enemies.filter(e => e.x > cameraX - 800);
            coins = coins.filter(c => c.x > cameraX - 800);
            hazards = hazards.filter(h => h.x + h.width > cameraX - 800);
            movingPlatforms = movingPlatforms.filter(mp => mp.x + mp.width > cameraX - 800);
            thwomps = thwomps.filter(t => t.x > cameraX - 800);
            decorations = decorations.filter(d => d.x > cameraX - 800);
        }
    }

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

    function drawThwomp(x, y) {
        ctx.fillStyle = '#7f8c8d'; // Grey stone block
        ctx.fillRect(x, y, 40, 40);
        ctx.fillStyle = '#e74c3c'; // Angry Red Eyes
        ctx.fillRect(x + 6, y + 12, 8, 6);
        ctx.fillRect(x + 26, y + 12, 8, 6);
        ctx.fillStyle = '#000000';
        ctx.fillRect(x + 8, y + 26, 24, 6); // Mouth
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        ctx.save();
        ctx.translate(Math.floor(-cameraX), 0);

        // Clouds
        decorations.forEach(dec => {
            if (dec.type === 'cloud') {
                ctx.fillStyle = "#ffffff";
                ctx.fillRect(dec.x, dec.y, 64, 16);
                ctx.fillRect(dec.x + 16, dec.y - 16, 32, 16);
            }
        });

        // Platforms, Ground, Biomes (Ice, Quicksand)
        platforms.forEach(platform => {
            if (platform.x + platform.width >= cameraX - 100 && platform.x <= cameraX + canvas.width + 100) {
                if (platform.type === 'ground') {
                    ctx.fillStyle = '#c84c0c';
                    ctx.fillRect(platform.x, platform.y, platform.width, platform.height + 200);
                    ctx.fillStyle = '#00a800';
                    ctx.fillRect(platform.x, platform.y, platform.width, 8);
                } else if (platform.type === 'ice') {
                    ctx.fillStyle = '#a9cce3'; // Ice Blue Surface
                    ctx.fillRect(platform.x, platform.y, platform.width, platform.height + 200);
                    ctx.fillStyle = '#ebf5fb';
                    ctx.fillRect(platform.x, platform.y, platform.width, 8);
                } else if (platform.type === 'quicksand') {
                    ctx.fillStyle = '#d4ac0d'; // Muddy Quicksand
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

        // Moving Platforms
        movingPlatforms.forEach(mp => {
            ctx.fillStyle = '#8e44ad'; // Purple moving platform
            ctx.fillRect(mp.x, mp.y, mp.width, mp.height);
            ctx.strokeStyle = '#000000';
            ctx.lineWidth = 2;
            ctx.strokeRect(mp.x, mp.y, mp.width, mp.height);
        });

        // Hazards (Lava & Spikes)
        hazards.forEach(h => {
            if (h.type === 'lava') {
                ctx.fillStyle = '#e74c3c'; // Glowing Red Lava
                ctx.fillRect(h.x, h.y, h.width, h.height);
                ctx.fillStyle = '#f39c12';
                ctx.fillRect(h.x, h.y, h.width, 8); // Bubbling top layer
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

        // Thwomps
        thwomps.forEach(t => {
            drawThwomp(t.x, t.y);
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
