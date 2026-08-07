import streamlit as st

st.set_page_config(
    page_title="Infinite Realistic Platformer",
    page_icon="🍄",
    layout="centered"
)

st.title("🍄 Infinite Realistic Platformer")
st.write("Endless scrolling platformer with 3D-styled graphics, dynamic camera, and procedural infinite generation!")

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
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: white;
        }
        .game-container {
            text-align: center;
        }
        canvas {
            border: 4px solid #333;
            background: linear-gradient(to bottom, #20b2aa, #87ceeb, #e0f6ff);
            box-shadow: 0 10px 30px rgba(0,0,0,0.6);
            border-radius: 6px;
        }
        .instructions {
            margin-top: 10px;
            font-size: 14px;
            color: #ddd;
            letter-spacing: 0.5px;
        }
    </style>
</head>
<body>

<div class="game-container">
    <canvas id="gameCanvas" width="800" height="450"></canvas>
    <div class="instructions">
        Controls: <strong>Arrow Left / Right</strong> to Run | <strong>Arrow Up</strong> or <strong>Spacebar</strong> to Jump
    </div>
</div>

<script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");

    let score = 0;
    let distanceTraveled = 0;
    const keys = {};

    let gameState = 'ENTERING';
    let entryTimer = 0;

    let cameraX = 0;

    const player = {
        x: 100,
        y: 340,
        width: 32,
        height: 48,
        vx: 0,
        vy: 0,
        speed: 5,
        jumpPower: -11.5,
        gravity: 0.55,
        grounded: false,
        facing: 'right'
    };

    // Infinite procedural world tracking
    let platforms = [
        { x: 0, y: 390, width: 1200, height: 60, type: 'ground' },
        { x: 300, y: 280, width: 140, height: 24, type: 'brick' },
        { x: 550, y: 200, width: 160, height: 24, type: 'brick' },
        { x: 800, y: 270, width: 130, height: 24, type: 'brick' }
    ];

    let coins = [
        { x: 350, y: 235, radius: 12, collected: false, angle: 0 },
        { x: 610, y: 155, radius: 12, collected: false, angle: 0 },
        { x: 850, y: 225, radius: 12, collected: false, angle: 0 }
    ];

    let lastGeneratedX = 1200;

    window.addEventListener("keydown", (e) => {
        keys[e.code] = true;
        if(["Space", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(e.code)) {
            e.preventDefault();
        }
    });

    window.addEventListener("keyup", (e) => {
        keys[e.code] = false;
    });

    function generateInfiniteWorld() {
        // If player approaches the end of generated map, create more chunks ahead
        if (player.x + canvas.width > lastGeneratedX - 400) {
            let chunkX = lastGeneratedX;
            
            // Continuous ground segments with gaps or hills
            platforms.push({ x: chunkX, y: 390, width: 1000, height: 60, type: 'ground' });

            // Random floating platforms & coins ahead
            for (let i = 1; i <= 3; i++) {
                let pWidth = 120 + Math.random() * 50;
                let pX = chunkX + i * 300 + Math.random() * 50;
                let pY = 160 + Math.random() * 140;
                
                platforms.push({ x: pX, y: pY, width: pWidth, height: 24, type: 'brick' });
                
                // Add coin above platform
                coins.push({ x: pX + pWidth / 2, y: pY - 45, radius: 12, collected: false, angle: Math.random() });
            }

            lastGeneratedX += 1000;
        }
    }

    function update() {
        if (gameState === 'ENTERING') {
            entryTimer += 0.03;
            player.y = 390 - 48 - Math.sin(entryTimer * Math.PI) * 70;
            player.x = 100 + (entryTimer * 10);
            if (entryTimer >= 1) {
                gameState = 'PLAYING';
                player.y = 390 - 48;
            }
            return;
        }

        // Horizontal movement
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
        
        // Prevent walking backwards past camera view
        if (player.x < cameraX + 20) {
            player.x = cameraX + 20;
        }

        // Track maximum distance traveled for score/distance meter
        if (player.x > distanceTraveled) {
            distanceTraveled = Math.floor(player.x);
        }

        // Smooth camera follow mechanics
        let targetCameraX = player.x - 250;
        if (targetCameraX > cameraX) {
            cameraX += (targetCameraX - cameraX) * 0.1;
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
                player.y + player.height - player.vy <= platform.y + 8 &&
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

        // Coin Collection & Animation
        coins.forEach(coin => {
            coin.angle += 0.05;
            if (!coin.collected) {
                let dist = Math.hypot(coin.x - (player.x + player.width / 2), coin.y - (player.y + player.height / 2));
                if (dist < coin.radius + player.width / 3) {
                    coin.collected = true;
                    score += 100;
                }
            }
        });

        // Procedural generation trigger
        generateInfiniteWorld();

        // Fall out of bounds check (Respawn checkpoint ahead)
        if (player.y > canvas.height) {
            player.x = cameraX + 100;
            player.y = 340;
            player.vy = 0;
            score = Math.max(0, score - 150);
            gameState = 'ENTERING';
            entryTimer = 0;
        }
    }

    function drawRealisticPlayer(x, y, w, h, facing) {
        ctx.save();
        ctx.fillStyle = "rgba(0,0,0,0.3)";
        ctx.beginPath();
        ctx.ellipse(x + w/2, y + h, w/2, 6, 0, 0, Math.PI * 2);
        ctx.fill();

        let bodyGrad = ctx.createLinearGradient(x, y + h/2, x + w, y + h);
        bodyGrad.addColorStop(0, '#1a5276');
        bodyGrad.addColorStop(1, '#2980b9');
        ctx.fillStyle = bodyGrad;
        ctx.fillRect(x + 4, y + h/2, w - 8, h/2);

        let shirtGrad = ctx.createLinearGradient(x, y + h/3, x + w, y + h/2);
        shirtGrad.addColorStop(0, '#c0392b');
        shirtGrad.addColorStop(1, '#e74c3c');
        ctx.fillStyle = shirtGrad;
        ctx.fillRect(x + 6, y + h/3, w - 12, h/3);

        ctx.fillStyle = '#c0392b';
        ctx.fillRect(x + (facing === 'right' ? 8 : 2), y + 2, w - 8, 12);
        ctx.fillStyle = '#922b21';
        ctx.fillRect(x + (facing === 'right' ? w - 10 : 2), y + 6, 10, 4);

        ctx.fillStyle = '#f5b041';
        ctx.fillRect(x + (facing === 'right' ? 12 : 6), y + 14, 14, 10);
        ctx.fillStyle = '#512e5f';
        ctx.fillRect(x + (facing === 'right' ? 14 : 4), y + 20, 12, 4);

        ctx.restore();
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        ctx.save();
        // Apply camera scroll translation
        ctx.translate(-cameraX, 0);

        // Parallax background clouds (moves slower than camera)
        ctx.fillStyle = "rgba(255, 255, 255, 0.6)";
        let cloudOffset = cameraX * 0.3;
        for (let i = -1; i < 5; i++) {
            let cx = i * 400 + (cloudOffset % 400);
            ctx.beginPath();
            ctx.arc(cx + 150, 80, 30, 0, Math.PI * 2);
            ctx.arc(cx + 180, 75, 40, 0, Math.PI * 2);
            ctx.arc(cx + 210, 85, 25, 0, Math.PI * 2);
            ctx.fill();
        }

        // Draw Platforms
        platforms.forEach(platform => {
            // Only render platforms visible on screen for optimization
            if (platform.x + platform.width >= cameraX && platform.x <= cameraX + canvas.width) {
                if (platform.type === 'ground') {
                    let groundGrad = ctx.createLinearGradient(0, platform.y, 0, platform.y + platform.height);
                    groundGrad.addColorStop(0, '#27ae60');
                    groundGrad.addColorStop(0.15, '#784212');
                    groundGrad.addColorStop(1, '#4a2306');
                    ctx.fillStyle = groundGrad;
                    ctx.fillRect(platform.x, platform.y, platform.width, platform.height);
                    
                    ctx.fillStyle = '#2ecc71';
                    ctx.fillRect(platform.x, platform.y, platform.width, 6);
                } else {
                    let brickGrad = ctx.createLinearGradient(platform.x, platform.y, platform.x, platform.y + platform.height);
                    brickGrad.addColorStop(0, '#e59866');
                    brickGrad.addColorStop(1, '#ba4a00');
                    ctx.fillStyle = brickGrad;
                    ctx.fillRect(platform.x, platform.y, platform.width, platform.height);

                    ctx.strokeStyle = '#78281f';
                    ctx.lineWidth = 2;
                    ctx.strokeRect(platform.x, platform.y, platform.width, platform.height);
                }
            }
        });

        // Draw Coins
        coins.forEach(coin => {
            if (!coin.collected && coin.x >= cameraX - 50 && coin.x <= cameraX + canvas.width + 50) {
                ctx.save();
                ctx.translate(coin.x, coin.y);
                let scaleX = Math.cos(coin.angle);
                ctx.scale(scaleX, 1);

                let coinGrad = ctx.createRadialGradient(0, 0, 2, 0, 0, coin.radius);
                coinGrad.addColorStop(0, '#f9e79f');
                coinGrad.addColorStop(0.7, '#f1c40f');
                coinGrad.addColorStop(1, '#b7950b');

                ctx.fillStyle = coinGrad;
                ctx.beginPath();
                ctx.arc(0, 0, coin.radius, 0, Math.PI * 2);
                ctx.fill();
                ctx.strokeStyle = '#7d6608';
                ctx.lineWidth = 2;
                ctx.stroke();

                ctx.restore();
            }
        });

        // Draw Player
        drawRealisticPlayer(player.x, player.y, player.width, player.height, player.facing);

        ctx.restore();

        // Draw Fixed HUD / UI (Score & Distance Tracking)
        ctx.fillStyle = "rgba(0, 0, 0, 0.5)";
        ctx.fillRect(15, 15, 260, 45);
        ctx.strokeStyle = "rgba(255, 255, 255, 0.3)";
        ctx.strokeRect(15, 15, 260, 45);

        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 16px 'Segoe UI'";
        ctx.fillText("SCORE: " + score + " | DIST: " + distanceTraveled + "m", 25, 43);
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
