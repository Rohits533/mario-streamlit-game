import streamlit as st

st.set_page_config(
    page_title="Next-Gen 2D Platformer",
    page_icon="🍄",
    layout="centered"
)

st.title("🍄 Next-Gen Cinematic Platformer")
st.write("A AAA-grade platformer featuring multi-layered parallax backgrounds, dynamic bloom lighting, fluid physics, and smooth procedural world generation.")

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
            border: 4px solid #1c1c28;
            background: linear-gradient(to bottom, #0f2027, #203a43, #2c5364);
            box-shadow: 0 25px 60px rgba(0,0,0,0.95), inset 0 0 30px rgba(0, 255, 200, 0.15);
            border-radius: 10px;
        }
        .instructions {
            margin-top: 12px;
            font-size: 14px;
            color: #8b9bb4;
            letter-spacing: 0.5px;
        }
    </style>
</head>
<body>

<div class="game-container">
    <canvas id="gameCanvas" width="920" height="500"></canvas>
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
        x: 120,
        y: 350,
        width: 38,
        height: 60,
        vx: 0,
        vy: 0,
        speed: 5.8,
        jumpPower: -13.5,
        gravity: 0.62,
        grounded: false,
        facing: 'right',
        tilt: 0
    };

    let platforms = [
        { x: 0, y: 420, width: 2200, height: 80, type: 'ground' },
        { x: 450, y: 300, width: 170, height: 26, type: 'block' },
        { x: 800, y: 190, width: 190, height: 26, type: 'block' },
        { x: 1150, y: 280, width: 160, height: 26, type: 'block' }
    ];

    let coins = [
        { x: 535, y: 240, radius: 14, collected: false, angle: 0 },
        { x: 895, y: 130, radius: 14, collected: false, angle: 0 },
        { x: 1230, y: 220, radius: 14, collected: false, angle: 0 }
    ];

    let particles = [];
    let lastGeneratedX = 2200;

    window.addEventListener("keydown", (e) => {
        keys[e.code] = true;
        if(["Space", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(e.code)) {
            e.preventDefault();
        }
    });

    window.addEventListener("keyup", (e) => {
        keys[e.code] = false;
    });

    function spawnParticles(x, y, color, count = 15) {
        for (let i = 0; i < count; i++) {
            particles.push({
                x: x,
                y: y,
                vx: (Math.random() - 0.5) * 9,
                vy: (Math.random() - 0.7) * 8,
                life: 1.0,
                decay: Math.random() * 0.03 + 0.02,
                color: color,
                size: Math.random() * 5 + 2
            });
        }
    }

    function generateCinematicWorld() {
        if (player.x + canvas.width > lastGeneratedX - 600) {
            let chunkX = lastGeneratedX;
            let sectionWidth = 1500;

            platforms.push({ x: chunkX, y: 420, width: sectionWidth, height: 80, type: 'ground' });

            let cursorX = chunkX + 250;
            while (cursorX < chunkX + sectionWidth - 250) {
                let pWidth = 140 + Math.random() * 80;
                let pY = 170 + Math.random() * 190;

                platforms.push({ x: cursorX, y: pY, width: pWidth, height: 26, type: 'block' });
                coins.push({ x: cursorX + pWidth / 2, y: pY - 50, radius: 14, collected: false, angle: Math.random() });

                cursorX += pWidth + 140 + Math.random() * 100;
            }

            lastGeneratedX += sectionWidth;
        }
    }

    function update() {
        if (gameState === 'ENTERING') {
            entryTimer += 0.025;
            player.y = 420 - 60 - Math.sin(entryTimer * Math.PI) * 120;
            player.x = 120 + (entryTimer * 15);
            if (entryTimer >= 1) {
                gameState = 'PLAYING';
                player.y = 420 - 60;
                spawnParticles(player.x + 19, player.y + 60, '#00ffcc', 30);
            }
            return;
        }

        if (keys["ArrowLeft"]) {
            player.vx = -player.speed;
            player.facing = 'left';
            player.tilt = -0.18;
        } else if (keys["ArrowRight"]) {
            player.vx = player.speed;
            player.facing = 'right';
            player.tilt = 0.18;
        } else {
            player.vx = 0;
            player.tilt = 0;
        }

        player.x += player.vx;
        if (player.x < cameraX + 20) player.x = cameraX + 20;

        if (player.x > distanceTraveled) {
            distanceTraveled = Math.floor(player.x);
        }

        let targetCameraX = player.x - 340;
        if (targetCameraX > cameraX) {
            cameraX += (targetCameraX - cameraX) * 0.12;
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
                if (!player.grounded && player.vy > 4) {
                    spawnParticles(player.x + 19, platform.y, '#ffffff', 8);
                }
                player.y = platform.y - player.height;
                player.vy = 0;
                player.grounded = true;
            }
        });

        if ((keys["ArrowUp"] || keys["Space"]) && player.grounded) {
            player.vy = player.jumpPower;
            player.grounded = false;
            spawnParticles(player.x + 19, player.y + player.height, '#00ffff', 14);
        }

        coins.forEach(coin => {
            coin.angle += 0.07;
            if (!coin.collected) {
                let dist = Math.hypot(coin.x - (player.x + player.width / 2), coin.y - (player.y + player.height / 2));
                if (dist < coin.radius + player.width / 3) {
                    coin.collected = true;
                    score += 200;
                    spawnParticles(coin.x, coin.y, '#ffd700', 25);
                }
            }
        });

        particles.forEach((p, index) => {
            p.x += p.vx;
            p.y += p.vy;
            p.life -= p.decay;
            if (p.life <= 0) particles.splice(index, 1);
        });

        generateCinematicWorld();

        if (player.y > canvas.height) {
            player.x = cameraX + 100;
            player.y = 350;
            player.vy = 0;
            score = Math.max(0, score - 300);
            gameState = 'ENTERING';
            entryTimer = 0;
            spawnParticles(player.x, player.y, '#ff3366', 35);
        }
    }

    function drawCinematicCharacter(x, y, w, h, facing, tilt) {
        ctx.save();
        ctx.translate(x + w / 2, y + h);
        ctx.rotate(tilt);

        // Soft Ground Shadow Glow
        let shadowGrad = ctx.createRadialGradient(0, 0, 2, 0, 0, w * 0.9);
        shadowGrad.addColorStop(0, 'rgba(0, 255, 200, 0.6)');
        shadowGrad.addColorStop(1, 'rgba(0, 0, 0, 0)');
        ctx.fillStyle = shadowGrad;
        ctx.beginPath();
        ctx.ellipse(0, 0, w * 0.9, 7, 0, 0, Math.PI * 2);
        ctx.fill();

        // Overalls Body Rendering
        let bodyGrad = ctx.createLinearGradient(-w/2, -h/2, w/2, 0);
        bodyGrad.addColorStop(0, '#103050');
        bodyGrad.addColorStop(0.5, '#1f4e79');
        bodyGrad.addColorStop(1, '#0d233a');
        ctx.fillStyle = bodyGrad;
        ctx.fillRect(-w/2 + 4, -h/2, w - 8, h/2);

        // Golden Buttons
        ctx.fillStyle = '#ffcc00';
        ctx.beginPath();
        ctx.arc(-w/4, -h/4, 4, 0, Math.PI * 2);
        ctx.arc(w/4, -h/4, 4, 0, Math.PI * 2);
        ctx.fill();

        // Red Shirt Torso
        let shirtGrad = ctx.createLinearGradient(-w/2, -h * 0.75, w/2, -h/2);
        shirtGrad.addColorStop(0, '#990000');
        shirtGrad.addColorStop(1, '#ff3333');
        ctx.fillStyle = shirtGrad;
        ctx.fillRect(-w/2 + 5, -h * 0.78, w - 10, h * 0.32);

        // Cap with Volumetric Specular Edge
        let capGrad = ctx.createLinearGradient(-w/2, -h, w/2, -h * 0.6);
        capGrad.addColorStop(0, '#ff4444');
        capGrad.addColorStop(1, '#880000');
        ctx.fillStyle = capGrad;
        ctx.beginPath();
        ctx.roundRect(-w/2 + 2, -h, w - 4, h * 0.38, [10, 10, 3, 3]);
        ctx.fill();

        ctx.fillStyle = '#550000';
        ctx.fillRect(facing === 'right' ? 2 : -w/2 - 2, -h * 0.68, w/2 + 4, 5);

        // Face Structure & Moustache
        ctx.fillStyle = '#ffcc99';
        ctx.fillRect(facing === 'right' ? 2 : -w/2 + 3, -h * 0.55, w/2 - 3, h * 0.24);

        ctx.fillStyle = '#111111';
        ctx.beginPath();
        ctx.roundRect(facing === 'right' ? 4 : -w/2 + 2, -h * 0.38, w/2 - 4, 7, 3.5);
        ctx.fill();

        ctx.restore();
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        ctx.save();
        ctx.translate(-cameraX, 0);

        // Multi-Layer Parallax Background Scenery (Distant Mountains & Glowing Nebula Lines)
        ctx.fillStyle = "rgba(30, 60, 90, 0.25)";
        let bgOffset1 = cameraX * 0.15;
        for (let i = -2; i < 10; i++) {
            let mx = i * 700 - (bgOffset1 % 700);
            ctx.beginPath();
            ctx.moveTo(mx, 420);
            ctx.lineTo(mx + 350, 150);
            ctx.lineTo(mx + 700, 420);
            ctx.fill();
        }

        // Platforms with Neon Bevel Shading
        platforms.forEach(platform => {
            if (platform.x + platform.width >= cameraX && platform.x <= cameraX + canvas.width) {
                if (platform.type === 'ground') {
                    let groundGrad = ctx.createLinearGradient(0, platform.y, 0, platform.y + platform.height);
                    groundGrad.addColorStop(0, '#00b09b'); // Glowing Emerald Top
                    groundGrad.addColorStop(0.12, '#96c93d');
                    groundGrad.addColorStop(0.25, '#3b220d'); // Rich Earth Depth
                    groundGrad.addColorStop(1, '#110903');
                    ctx.fillStyle = groundGrad;
                    ctx.fillRect(platform.x, platform.y, platform.width, platform.height);
                    
                    ctx.fillStyle = '#00ffcc';
                    ctx.fillRect(platform.x, platform.y, platform.width, 5);
                } else {
                    let blockGrad = ctx.createLinearGradient(platform.x, platform.y, platform.x, platform.y + platform.height);
                    blockGrad.addColorStop(0, '#ff7e5f');
                    blockGrad.addColorStop(1, '#feb47b');
                    ctx.fillStyle = blockGrad;
                    ctx.fillRect(platform.x, platform.y, platform.width, platform.height);

                    ctx.strokeStyle = '#ffffff';
                    ctx.lineWidth = 1.5;
                    ctx.strokeRect(platform.x, platform.y, platform.width, platform.height);
                }
            }
        });

        // 3D Spinning Cinematic Coins with Light Bloom
        coins.forEach(coin => {
            if (!coin.collected && coin.x >= cameraX - 60 && coin.x <= cameraX + canvas.width + 60) {
                ctx.save();
                ctx.translate(coin.x, coin.y);
                let scaleX = Math.cos(coin.angle);
                ctx.scale(scaleX, 1);

                let coinGrad = ctx.createRadialGradient(0, 0, 1, 0, 0, coin.radius);
                coinGrad.addColorStop(0, '#ffffff');
                coinGrad.addColorStop(0.5, '#ffcc00');
                coinGrad.addColorStop(1, '#ff9900');

                ctx.fillStyle = coinGrad;
                ctx.beginPath();
                ctx.arc(0, 0, coin.radius, 0, Math.PI * 2);
                ctx.fill();

                ctx.strokeStyle = '#fff5cc';
                ctx.lineWidth = 2;
                ctx.stroke();

                ctx.restore();
            }
        });

        // Particle System Renderer
        particles.forEach(p => {
            ctx.save();
            ctx.globalAlpha = p.life;
            ctx.fillStyle = p.color;
            ctx.shadowColor = p.color;
            ctx.shadowBlur = 12;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();
        });

        drawCinematicCharacter(player.x, player.y, player.width, player.height, player.facing, player.tilt);

        ctx.restore();

        // Cinematic Glassmorphism HUD Dashboard
        ctx.fillStyle = "rgba(10, 15, 25, 0.85)";
        ctx.fillRect(25, 25, 360, 55);
        ctx.strokeStyle = "rgba(0, 255, 200, 0.5)";
        ctx.lineWidth = 2;
        ctx.strokeRect(25, 25, 360, 55);

        ctx.fillStyle = "#00ffcc";
        ctx.font = "bold 16px 'Segoe UI'";
        ctx.fillText("SCORE: " + score + "   |   DISTANCE: " + distanceTraveled + "m", 42, 58);
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

st.components.v1.html(game_html, height=540, scrolling=False)
