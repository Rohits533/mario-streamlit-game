import streamlit as st

st.set_page_config(
    page_title="Next-Gen Realistic Platformer",
    page_icon="🍄",
    layout="centered"
)

st.title("🍄 Next-Gen Realistic Platformer")
st.write("Featuring dynamic vector shading, lighting reflections, particle bursts, and infinite procedural landscapes.")

game_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        body {
            margin: 0;
            background: #0a0a0c;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-family: 'Segoe UI', system-ui, sans-serif;
            color: white;
        }
        .game-container {
            text-align: center;
        }
        canvas {
            border: 4px solid #222;
            background: linear-gradient(to bottom, #1a2a6c, #b21f1f, #fdbb2d);
            box-shadow: 0 15px 40px rgba(0,0,0,0.8);
            border-radius: 8px;
        }
        .instructions {
            margin-top: 12px;
            font-size: 14px;
            color: #bbb;
            letter-spacing: 0.5px;
        }
    </style>
</head>
<body>

<div class="game-container">
    <canvas id="gameCanvas" width="850" height="480"></canvas>
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
        y: 350,
        width: 34,
        height: 52,
        vx: 0,
        vy: 0,
        speed: 5.5,
        jumpPower: -12.5,
        gravity: 0.58,
        grounded: false,
        facing: 'right',
        animFrame: 0
    };

    let platforms = [
        { x: 0, y: 410, width: 1500, height: 70, type: 'ground' },
        { x: 350, y: 290, width: 160, height: 26, type: 'brick' },
        { x: 650, y: 200, width: 180, height: 26, type: 'brick' },
        { x: 950, y: 270, width: 150, height: 26, type: 'brick' }
    ];

    let coins = [
        { x: 430, y: 240, radius: 13, collected: false, angle: 0 },
        { x: 740, y: 150, radius: 13, collected: false, angle: 0 },
        { x: 1025, y: 220, radius: 13, collected: false, angle: 0 }
    ];

    // Particle system array for realistic effects (dust, coin sparkles)
    let particles = [];

    let lastGeneratedX = 1500;

    window.addEventListener("keydown", (e) => {
        keys[e.code] = true;
        if(["Space", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(e.code)) {
            e.preventDefault();
        }
    });

    window.addEventListener("keyup", (e) => {
        keys[e.code] = false;
    });

    function spawnParticles(x, y, color, count = 10) {
        for (let i = 0; i < count; i++) {
            particles.push({
                x: x,
                y: y,
                vx: (Math.random() - 0.5) * 6,
                vy: (Math.random() - 0.5) * 6 - 2,
                alpha: 1.0,
                color: color,
                size: Math.random() * 4 + 2
            });
        }
    }

    function generateInfiniteWorld() {
        if (player.x + canvas.width > lastGeneratedX - 500) {
            let chunkX = lastGeneratedX;
            let groundWidth = 1000 + Math.random() * 400;
            
            platforms.push({ x: chunkX, y: 410, width: groundWidth, height: 70, type: 'ground' });

            let currentX = chunkX + 200;
            while (currentX < chunkX + groundWidth - 200) {
                let pWidth = 130 + Math.random() * 70;
                let pY = 180 + Math.random() * 160;
                
                platforms.push({ x: currentX, y: pY, width: pWidth, height: 26, type: 'brick' });
                coins.push({ x: currentX + pWidth / 2, y: pY - 45, radius: 13, collected: false, angle: Math.random() });
                
                currentX += pWidth + 120 + Math.random() * 80;
            }

            lastGeneratedX += groundWidth;
        }
    }

    function update() {
        if (gameState === 'ENTERING') {
            entryTimer += 0.025;
            player.y = 410 - 52 - Math.sin(entryTimer * Math.PI) * 90;
            player.x = 100 + (entryTimer * 12);
            if (entryTimer >= 1) {
                gameState = 'PLAYING';
                player.y = 410 - 52;
                spawnParticles(player.x + 17, player.y + 52, '#2ecc71', 15);
            }
            return;
        }

        // Horizontal Movement & Animation ticker
        if (keys["ArrowLeft"]) {
            player.vx = -player.speed;
            player.facing = 'left';
            player.animFrame += 0.2;
        } else if (keys["ArrowRight"]) {
            player.vx = player.speed;
            player.facing = 'right';
            player.animFrame += 0.2;
        } else {
            player.vx = 0;
            player.animFrame = 0;
        }

        player.x += player.vx;
        if (player.x < cameraX + 15) player.x = cameraX + 15;

        if (player.x > distanceTraveled) {
            distanceTraveled = Math.floor(player.x);
        }

        let targetCameraX = player.x - 300;
        if (targetCameraX > cameraX) {
            cameraX += (targetCameraX - cameraX) * 0.12;
        }

        // Physics & Gravity
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
                if (!player.grounded && player.vy > 4) {
                    spawnParticles(player.x + 17, platform.y, '#7f8c8d', 6); // Landing dust
                }
                player.y = platform.y - player.height;
                player.vy = 0;
                player.grounded = true;
            }
        });

        if ((keys["ArrowUp"] || keys["Space"]) && player.grounded) {
            player.vy = player.jumpPower;
            player.grounded = false;
            spawnParticles(player.x + 17, player.y + player.height, '#bdc3c7', 8);
        }

        // Coin Collection & Sparkle Burst
        coins.forEach(coin => {
            coin.angle += 0.06;
            if (!coin.collected) {
                let dist = Math.hypot(coin.x - (player.x + player.width / 2), coin.y - (player.y + player.height / 2));
                if (dist < coin.radius + player.width / 3) {
                    coin.collected = true;
                    score += 100;
                    spawnParticles(coin.x, coin.y, '#f1c40f', 16);
                }
            }
        });

        // Particle updates
        particles.forEach((p, index) => {
            p.x += p.vx;
            p.y += p.vy;
            p.alpha -= 0.03;
            if (p.alpha <= 0) particles.splice(index, 1);
        });

        generateInfiniteWorld();

        if (player.y > canvas.height) {
            player.x = cameraX + 80;
            player.y = 350;
            player.vy = 0;
            score = Math.max(0, score - 200);
            gameState = 'ENTERING';
            entryTimer = 0;
            spawnParticles(player.x, player.y, '#e74c3c', 20);
        }
    }

    function drawRealisticPlayer(x, y, w, h, facing, frame) {
        ctx.save();
        
        // Soft ground shadow with dynamic scaling based on jump height
        let shadowWidth = Math.max(10, w - Math.abs(player.vy) * 2);
        ctx.fillStyle = "rgba(0,0,0,0.4)";
        ctx.beginPath();
        ctx.ellipse(x + w/2, 410, shadowWidth/2, 5, 0, 0, Math.PI * 2);
        ctx.fill();

        // Bounce effect simulation using animFrame
        let bounce = player.grounded ? Math.sin(frame) * 2 : 0;
        let drawY = y + bounce;

        // Overalls (Multi-stop smooth shading)
        let overallsGrad = ctx.createLinearGradient(x, drawY + h/2, x + w, drawY + h);
        overallsGrad.addColorStop(0, '#154360');
        overallsGrad.addColorStop(0.5, '#1b4f72');
        overallsGrad.addColorStop(1, '#2471a3');
        ctx.fillStyle = overallsGrad;
        ctx.fillRect(x + 5, drawY + h/2, w - 10, h/2 - 2);

        // Straps & Buttons
        ctx.fillStyle = '#f1c40f'; // Gold buttons
        ctx.fillRect(x + 8, drawY + h/2 + 4, 4, 4);
        ctx.fillRect(x + w - 12, drawY + h/2 + 4, 4, 4);

        // Shirt
        let shirtGrad = ctx.createLinearGradient(x, drawY + h/3, x + w, drawY + h/2);
        shirtGrad.addColorStop(0, '#922b21');
        shirtGrad.addColorStop(1, '#e74c3c');
        ctx.fillStyle = shirtGrad;
        ctx.fillRect(x + 7, drawY + h/3, w - 14, h/3);

        // Head / Cap with realistic curvature highlight
        let capGrad = ctx.createLinearGradient(x, drawY, x, drawY + 14);
        capGrad.addColorStop(0, '#f1948a');
        capGrad.addColorStop(1, '#c0392b');
        ctx.fillStyle = capGrad;
        ctx.fillRect(x + (facing === 'right' ? 8 : 2), drawY, w - 8, 13);
        
        // Cap Visor
        ctx.fillStyle = '#922b21';
        ctx.fillRect(x + (facing === 'right' ? w - 10 : 2), drawY + 5, 12, 4);

        // Face & Detailed Moustache
        ctx.fillStyle = '#f5b041';
        ctx.fillRect(x + (facing === 'right' ? 13 : 5), drawY + 13, 14, 11);
        ctx.fillStyle = '#2c3e50';
        ctx.fillRect(x + (facing === 'right' ? 14 : 4), drawY + 20, 14, 5);

        ctx.restore();
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        ctx.save();
        ctx.translate(-cameraX, 0);

        // Dynamic Parallax Background Mountains / Hills
        ctx.fillStyle = "rgba(44, 62, 80, 0.25)";
        let hillOffset = cameraX * 0.2;
        for (let i = -1; i < 6; i++) {
            let hx = i * 500 - (hillOffset % 500);
            ctx.beginPath();
            ctx.moveTo(hx, 410);
            ctx.lineTo(hx + 250, 220);
            ctx.lineTo(hx + 500, 410);
            ctx.fill();
        }

        // Platforms with High-End Textures & Top Lighting Bevels
        platforms.forEach(platform => {
            if (platform.x + platform.width >= cameraX && platform.x <= cameraX + canvas.width) {
                if (platform.type === 'ground') {
                    let groundGrad = ctx.createLinearGradient(0, platform.y, 0, platform.y + platform.height);
                    groundGrad.addColorStop(0, '#1e8449'); // Vibrant Moss
                    groundGrad.addColorStop(0.1, '#27ae60');
                    groundGrad.addColorStop(0.2, '#6e2c00'); // Rich Soil
                    groundGrad.addColorStop(1, '#2b1b0e');
                    ctx.fillStyle = groundGrad;
                    ctx.fillRect(platform.x, platform.y, platform.width, platform.height);
                    
                    // Glossy top neon highlight border
                    ctx.fillStyle = '#58d68d';
                    ctx.fillRect(platform.x, platform.y, platform.width, 4);
                } else {
                    let brickGrad = ctx.createLinearGradient(platform.x, platform.y, platform.x, platform.y + platform.height);
                    brickGrad.addColorStop(0, '#dc7633');
                    brickGrad.addColorStop(1, '#935116');
                    ctx.fillStyle = brickGrad;
                    ctx.fillRect(platform.x, platform.y, platform.width, platform.height);

                    // Beveled Edge Light
                    ctx.fillStyle = '#edbb99';
                    ctx.fillRect(platform.x, platform.y, platform.width, 3);
                    
                    ctx.strokeStyle = '#512e5f';
                    ctx.lineWidth = 2;
                    ctx.strokeRect(platform.x, platform.y, platform.width, platform.height);
                }
            }
        });

        // Glowing 3D Coins
        coins.forEach(coin => {
            if (!coin.collected && coin.x >= cameraX - 50 && coin.x <= cameraX + canvas.width + 50) {
                ctx.save();
                ctx.translate(coin.x, coin.y);
                let scaleX = Math.cos(coin.angle);
                ctx.scale(scaleX, 1);

                let coinGrad = ctx.createRadialGradient(0, 0, 1, 0, 0, coin.radius);
                coinGrad.addColorStop(0, '#fef9e7');
                coinGrad.addColorStop(0.5, '#f1c40f');
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

        // Render Particle Effects
        particles.forEach(p => {
            ctx.save();
            ctx.globalAlpha = p.alpha;
            ctx.fillStyle = p.color;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();
        });

        // Draw Player Character
        drawRealisticPlayer(player.x, player.y, player.width, player.height, player.facing, player.animFrame);

        ctx.restore();

        // High-Tech Modern HUD Glassmorphism Display
        ctx.fillStyle = "rgba(15, 15, 20, 0.75)";
        ctx.fillRect(20, 20, 310, 50);
        ctx.strokeStyle = "rgba(255, 255, 255, 0.15)";
        ctx.lineWidth = 1.5;
        ctx.strokeRect(20, 20, 310, 50);

        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 15px 'Segoe UI'";
        ctx.fillText("SCORE: " + score + "   |   DIST: " + distanceTraveled + "m", 35, 51);
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

st.components.v1.html(game_html, height=530, scrolling=False)
