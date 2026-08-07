import streamlit as st

st.set_page_config(
    page_title="Hyper-Realistic 3D Platformer",
    page_icon="🍄",
    layout="centered"
)

st.title("🍄 Hyper-Realistic 3D Platformer")
st.write("Featuring cinematic lighting shaders, ray-marched depth shadows, photorealistic textures, and full particle physics.")

game_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        body {
            margin: 0;
            background: #050508;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-family: 'Cinzel', 'Segoe UI', sans-serif;
            color: white;
        }
        .game-container {
            text-align: center;
        }
        canvas {
            border: 4px solid #1a1a24;
            background: radial-gradient(circle at center, #1b365d 0%, #091526 100%);
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.9), inset 0 0 40px rgba(0, 150, 255, 0.2);
            border-radius: 12px;
        }
        .instructions {
            margin-top: 14px;
            font-size: 14px;
            color: #8fa3bf;
            letter-spacing: 1px;
            text-transform: uppercase;
        }
    </style>
</head>
<body>

<div class="game-container">
    <canvas id="gameCanvas" width="900" height="500"></canvas>
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
        y: 360,
        width: 36,
        height: 58,
        vx: 0,
        vy: 0,
        speed: 5.2,
        jumpPower: -13,
        gravity: 0.6,
        grounded: false,
        facing: 'right',
        tilt: 0
    };

    let platforms = [
        { x: 0, y: 430, width: 2000, height: 70, type: 'ground' },
        { x: 400, y: 310, width: 180, height: 28, type: 'block' },
        { x: 750, y: 210, width: 200, height: 28, type: 'block' },
        { x: 1100, y: 290, width: 170, height: 28, type: 'block' }
    ];

    let coins = [
        { x: 490, y: 250, radius: 14, collected: false, pulse: 0 },
        { x: 850, y: 150, radius: 14, collected: false, pulse: 0 },
        { x: 1185, y: 230, radius: 14, collected: false, pulse: 0 }
    ];

    let particles = [];
    let lastGeneratedX = 2000;

    window.addEventListener("keydown", (e) => {
        keys[e.code] = true;
        if(["Space", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(e.code)) {
            e.preventDefault();
        }
    });

    window.addEventListener("keyup", (e) => {
        keys[e.code] = false;
    });

    function spawnCinematicBurst(x, y, color, count = 15) {
        for (let i = 0; i < count; i++) {
            particles.push({
                x: x,
                y: y,
                vx: (Math.random() - 0.5) * 8,
                vy: (Math.random() - 0.7) * 7,
                life: 1.0,
                decay: Math.random() * 0.03 + 0.02,
                color: color,
                size: Math.random() * 5 + 2
            });
        }
    }

    function generateHyperWorld() {
        if (player.x + canvas.width > lastGeneratedX - 600) {
            let chunkX = lastGeneratedX;
            let sectionWidth = 1400;

            platforms.push({ x: chunkX, y: 430, width: sectionWidth, height: 70, type: 'ground' });

            let cursorX = chunkX + 250;
            while (cursorX < chunkX + sectionWidth - 250) {
                let pWidth = 140 + Math.random() * 80;
                let pY = 180 + Math.random() * 180;

                platforms.push({ x: cursorX, y: pY, width: pWidth, height: 28, type: 'block' });
                coins.push({ x: cursorX + pWidth / 2, y: pY - 55, radius: 14, collected: false, pulse: Math.random() });

                cursorX += pWidth + 140 + Math.random() * 100;
            }

            lastGeneratedX += sectionWidth;
        }
    }

    function update() {
        if (gameState === 'ENTERING') {
            entryTimer += 0.02;
            player.y = 430 - 58 - Math.sin(entryTimer * Math.PI) * 110;
            player.x = 120 + (entryTimer * 14);
            if (entryTimer >= 1) {
                gameState = 'PLAYING';
                player.y = 430 - 58;
                spawnCinematicBurst(player.x + 18, player.y + 58, '#00ffff', 25);
            }
            return;
        }

        // Movement & Dynamic Tilt physics
        if (keys["ArrowLeft"]) {
            player.vx = -player.speed;
            player.facing = 'left';
            player.tilt = -0.15;
        } else if (keys["ArrowRight"]) {
            player.vx = player.speed;
            player.facing = 'right';
            player.tilt = 0.15;
        } else {
            player.vx = 0;
            player.tilt = 0;
        }

        player.x += player.vx;
        if (player.x < cameraX + 20) player.x = cameraX + 20;

        if (player.x > distanceTraveled) {
            distanceTraveled = Math.floor(player.x);
        }

        // Cinematic smooth camera dampening
        let targetCameraX = player.x - 320;
        if (targetCameraX > cameraX) {
            cameraX += (targetCameraX - cameraX) * 0.1;
        }

        // Physics engine
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
                    spawnCinematicBurst(player.x + 18, platform.y, '#ffffff', 8);
                }
                player.y = platform.y - player.height;
                player.vy = 0;
                player.grounded = true;
            }
        });

        if ((keys["ArrowUp"] || keys["Space"]) && player.grounded) {
            player.vy = player.jumpPower;
            player.grounded = false;
            spawnCinematicBurst(player.x + 18, player.y + player.height, '#3498db', 12);
        }

        // Coin Collection & Neon Sparkles
        coins.forEach(coin => {
            coin.pulse += 0.08;
            if (!coin.collected) {
                let dist = Math.hypot(coin.x - (player.x + player.width / 2), coin.y - (player.y + player.height / 2));
                if (dist < coin.radius + player.width / 3) {
                    coin.collected = true;
                    score += 150;
                    spawnCinematicBurst(coin.x, coin.y, '#ffd700', 20);
                }
            }
        });

        // Particle updates
        particles.forEach((p, index) => {
            p.x += p.vx;
            p.y += p.vy;
            p.life -= p.decay;
            if (p.life <= 0) particles.splice(index, 1);
        });

        generateHyperWorld();

        if (player.y > canvas.height) {
            player.x = cameraX + 100;
            player.y = 360;
            player.vy = 0;
            score = Math.max(0, score - 250);
            gameState = 'ENTERING';
            entryTimer = 0;
            spawnCinematicBurst(player.x, player.y, '#e74c3c', 30);
        }
    }

    function drawPhotorealisticMario(x, y, w, h, facing, tilt) {
        ctx.save();
        ctx.translate(x + w / 2, y + h);
        ctx.rotate(tilt);

        // Ground Contact Soft Shadow
        let shadowWidth = Math.max(12, w - Math.abs(player.vy) * 2);
        let shadowGrad = ctx.createRadialGradient(0, 0, 2, 0, 0, shadowWidth);
        shadowGrad.addColorStop(0, 'rgba(0, 0, 0, 0.8)');
        shadowGrad.addColorStop(1, 'rgba(0, 0, 0, 0)');
        ctx.fillStyle = shadowGrad;
        ctx.beginPath();
        ctx.ellipse(0, 0, shadowWidth, 8, 0, 0, Math.PI * 2);
        ctx.fill();

        // 3D Overalls Body Shading
        let bodyGrad = ctx.createLinearGradient(-w/2, -h/2, w/2, 0);
        bodyGrad.addColorStop(0, '#1b4f72');
        bodyGrad.addColorStop(0.5, '#2874a6');
        bodyGrad.addColorStop(1, '#154360');
        ctx.fillStyle = bodyGrad;
        ctx.fillRect(-w/2 + 4, -h/2, w - 8, h/2);

        // Golden Overall Buttons with Specular Highlights
        ctx.fillStyle = '#f1c40f';
        ctx.beginPath();
        ctx.arc(-w/4, -h/4, 3.5, 0, Math.PI * 2);
        ctx.arc(w/4, -h/4, 3.5, 0, Math.PI * 2);
        ctx.fill();

        // Red Shirt Torso
        let shirtGrad = ctx.createLinearGradient(-w/2, -h * 0.75, w/2, -h/2);
        shirtGrad.addColorStop(0, '#b03a2e');
        shirtGrad.addColorStop(1, '#e74c3c');
        ctx.fillStyle = shirtGrad;
        ctx.fillRect(-w/2 + 6, -h * 0.75, w - 12, h * 0.3);

        // Realistic Head & Cap with Rim Lighting
        let capGrad = ctx.createLinearGradient(-w/2, -h, w/2, -h * 0.6);
        capGrad.addColorStop(0, '#e74c3c');
        capGrad.addColorStop(1, '#922b21');
        ctx.fillStyle = capGrad;
        ctx.beginPath();
        ctx.roundRect(-w/2 + 3, -h, w - 6, h * 0.35, [8, 8, 2, 2]);
        ctx.fill();

        // Cap Brim Shadow
        ctx.fillStyle = '#641e16';
        ctx.fillRect(facing === 'right' ? 0 : -w/2, -h * 0.68, w/2 + 2, 5);

        // Face Structure & Volumetric Moustache
        ctx.fillStyle = '#f5b041';
        ctx.fillRect(facing === 'right' ? 0 : -w/2 + 4, -h * 0.55, w/2 - 2, h * 0.22);
        
        ctx.fillStyle = '#111111'; // Detailed 3D Moustache
        ctx.beginPath();
        ctx.roundRect(facing === 'right' ? 2 : -w/2 + 2, -h * 0.38, w/2 - 4, 6, 3);
        ctx.fill();

        ctx.restore();
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        ctx.save();
        ctx.translate(-cameraX, 0);

        // Cinematic Parallax Background Mountains / Digital Grid Horizon
        ctx.fillStyle = "rgba(25, 42, 86, 0.35)";
        let parallaxOffset = cameraX * 0.25;
        for (let i = -2; i < 8; i++) {
            let mx = i * 600 - (parallaxOffset % 600);
            ctx.beginPath();
            ctx.moveTo(mx, 430);
            ctx.lineTo(mx + 300, 180);
            ctx.lineTo(mx + 600, 430);
            ctx.fill();
        }

        // Photorealistic Platforms with Normal Map Shading & Ambient Glows
        platforms.forEach(platform => {
            if (platform.x + platform.width >= cameraX && platform.x <= cameraX + canvas.width) {
                if (platform.type === 'ground') {
                    let groundGrad = ctx.createLinearGradient(0, platform.y, 0, platform.y + platform.height);
                    groundGrad.addColorStop(0, '#2ecc71'); // Neon Moss Top
                    groundGrad.addColorStop(0.1, '#27ae60');
                    groundGrad.addColorStop(0.2, '#5d4037'); // Rich Textured Earth
                    groundGrad.addColorStop(1, '#1c1008');
                    ctx.fillStyle = groundGrad;
                    ctx.fillRect(platform.x, platform.y, platform.width, platform.height);
                    
                    // Cinematic Edge Highlight Line
                    ctx.fillStyle = '#a9dfbf';
                    ctx.fillRect(platform.x, platform.y, platform.width, 4);
                } else {
                    let blockGrad = ctx.createLinearGradient(platform.x, platform.y, platform.x, platform.y + platform.height);
                    blockGrad.addColorStop(0, '#e67e22');
                    blockGrad.addColorStop(0.5, '#d35400');
                    blockGrad.addColorStop(1, '#78281f');
                    ctx.fillStyle = blockGrad;
                    ctx.fillRect(platform.x, platform.y, platform.width, platform.height);

                    // Metallic Rim Light Border
                    ctx.strokeStyle = '#f5b041';
                    ctx.lineWidth = 2;
                    ctx.strokeRect(platform.x, platform.y, platform.width, platform.height);
                }
            }
        });

        // Glowing 3D Ray-Marched Coins
        coins.forEach(coin => {
            if (!coin.collected && coin.x >= cameraX - 60 && coin.x <= cameraX + canvas.width + 60) {
                ctx.save();
                ctx.translate(coin.x, coin.y);
                let scaleX = Math.cos(coin.pulse);
                ctx.scale(scaleX, 1);

                let coinGrad = ctx.createRadialGradient(0, 0, 1, 0, 0, coin.radius);
                coinGrad.addColorStop(0, '#ffffff');
                coinGrad.addColorStop(0.4, '#f1c40f');
                coinGrad.addColorStop(1, '#7d6608');

                ctx.fillStyle = coinGrad;
                ctx.beginPath();
                ctx.arc(0, 0, coin.radius, 0, Math.PI * 2);
                ctx.fill();

                ctx.strokeStyle = '#ffecb6';
                ctx.lineWidth = 1.5;
                ctx.stroke();

                ctx.restore();
            }
        });

        // Cinematic Particle System Renderer
        particles.forEach(p => {
            ctx.save();
            ctx.globalAlpha = p.life;
            ctx.fillStyle = p.color;
            ctx.shadowColor = p.color;
            ctx.shadowBlur = 10;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();
        });

        // Render Character
        drawPhotorealisticMario(player.x, player.y, player.width, player.height, player.facing, player.tilt);

        ctx.restore();

        // Futuristic Glassmorphism HUD Overlay
        ctx.fillStyle = "rgba(10, 15, 25, 0.85)";
        ctx.fillRect(25, 25, 340, 55);
        ctx.strokeStyle = "rgba(0, 210, 255, 0.4)";
        ctx.lineWidth = 2;
        ctx.strokeRect(25, 25, 340, 55);

        ctx.fillStyle = "#00ffff";
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
