import streamlit as st

st.set_page_config(
    page_title="Realistic Super Platformer",
    page_icon="🍄",
    layout="centered"
)

st.title("🍄 Realistic Super Platformer")
st.write("A polished 2D platformer with 3D-styled graphics, dynamic lighting, and a pipe-entry animation!")

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
    const keys = {};

    // Game States: 'ENTERING', 'PLAYING'
    let gameState = 'ENTERING';
    let entryTimer = 0;

    const player = {
        x: 80,
        y: 340,
        width: 32,
        height: 48,
        vx: 0,
        vy: 0,
        speed: 4.5,
        jumpPower: -11,
        gravity: 0.55,
        grounded: false,
        facing: 'right'
    };

    // Realistic styled platforms / bricks
    const platforms = [
        { x: 0, y: 390, width: 800, height: 60, type: 'ground' },
        { x: 280, y: 280, width: 140, height: 24, type: 'brick' },
        { x: 480, y: 190, width: 160, height: 24, type: 'brick' },
        { x: 140, y: 190, width: 110, height: 24, type: 'brick' }
    ];

    let coins = [
        { x: 350, y: 235, radius: 12, collected: false, angle: 0 },
        { x: 560, y: 145, radius: 12, collected: false, angle: 0 },
        { x: 195, y: 145, radius: 12, collected: false, angle: 0 },
        { x: 420, y: 345, radius: 12, collected: false, angle: 0 }
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
        if (gameState === 'ENTERING') {
            entryTimer += 0.03;
            // Mario rises smoothly out of a pipe/spawn sequence
            player.y = 390 - 48 - Math.sin(entryTimer * Math.PI) * 70;
            player.x = 80 + (entryTimer * 15);
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
        if (player.x < 0) player.x = 0;
        if (player.x + player.width > canvas.width) player.x = canvas.width - player.width;

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
            coin.angle += 0.05; // Spin effect
            if (!coin.collected) {
                let dist = Math.hypot(coin.x - (player.x + player.width / 2), coin.y - (player.y + player.height / 2));
                if (dist < coin.radius + player.width / 3) {
                    coin.collected = true;
                    score += 100;
                }
            }
        });

        // Fall out of bounds check
        if (player.y > canvas.height) {
            resetPlayer();
        }
    }

    function resetPlayer() {
        player.x = 80;
        player.y = 340;
        player.vy = 0;
        score = Math.max(0, score - 200);
        coins.forEach(c => c.collected = false);
        gameState = 'ENTERING';
        entryTimer = 0;
    }

    function drawRealisticPlayer(x, y, w, h, facing) {
        ctx.save();
        // Shadow underneath
        ctx.fillStyle = "rgba(0,0,0,0.3)";
        ctx.beginPath();
        ctx.ellipse(x + w/2, y + h, w/2, 6, 0, 0, Math.PI * 2);
        ctx.fill();

        // Overalls / Body (Gradient blue)
        let bodyGrad = ctx.createLinearGradient(x, y + h/2, x + w, y + h);
        bodyGrad.addColorStop(0, '#1a5276');
        bodyGrad.addColorStop(1, '#2980b9');
        ctx.fillStyle = bodyGrad;
        ctx.fillRect(x + 4, y + h/2, w - 8, h/2);

        // Shirt (Gradient red)
        let shirtGrad = ctx.createLinearGradient(x, y + h/3, x + w, y + h/2);
        shirtGrad.addColorStop(0, '#c0392b');
        shirtGrad.addColorStop(1, '#e74c3c');
        ctx.fillStyle = shirtGrad;
        ctx.fillRect(x + 6, y + h/3, w - 12, h/3);

        // Cap
        ctx.fillStyle = '#c0392b';
        ctx.fillRect(x + (facing === 'right' ? 8 : 2), y + 2, w - 8, 12);
        ctx.fillStyle = '#922b21';
        ctx.fillRect(x + (facing === 'right' ? w - 10 : 2), y + 6, 10, 4); // Brim

        // Face & Moustache
        ctx.fillStyle = '#f5b041';
        ctx.fillRect(x + (facing === 'right' ? 12 : 6), y + 14, 14, 10);
        ctx.fillStyle = '#512e5f'; // Moustache
        ctx.fillRect(x + (facing === 'right' ? 14 : 4), y + 20, 12, 4);

        ctx.restore();
    }

    function draw() {
        // Clear sky gradient background
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw clouds / environment details
        ctx.fillStyle = "rgba(255, 255, 255, 0.6)";
        ctx.beginPath();
        ctx.arc(150, 80, 30, 0, Math.PI * 2);
        ctx.arc(180, 75, 40, 0, Math.PI * 2);
        ctx.arc(210, 85, 25, 0, Math.PI * 2);
        ctx.fill();

        ctx.beginPath();
        ctx.arc(600, 110, 35, 0, Math.PI * 2);
        ctx.arc(640, 100, 45, 0, Math.PI * 2);
        ctx.fill();

        // Draw Platforms / Blocks with Textures
        platforms.forEach(platform => {
            if (platform.type === 'ground') {
                // Realistic grass & dirt gradient
                let groundGrad = ctx.createLinearGradient(0, platform.y, 0, platform.y + platform.height);
                groundGrad.addColorStop(0, '#27ae60'); // Grass top
                groundGrad.addColorStop(0.15, '#784212'); // Dirt
                groundGrad.addColorStop(1, '#4a2306');
                ctx.fillStyle = groundGrad;
                ctx.fillRect(platform.x, platform.y, platform.width, platform.height);
                
                // Highlight grass border
                ctx.fillStyle = '#2ecc71';
                ctx.fillRect(platform.x, platform.y, platform.width, 6);
            } else {
                // 3D Realistic Bricks
                let brickGrad = ctx.createLinearGradient(platform.x, platform.y, platform.x, platform.y + platform.height);
                brickGrad.addColorStop(0, '#e59866');
                brickGrad.addColorStop(1, '#ba4a00');
                ctx.fillStyle = brickGrad;
                ctx.fillRect(platform.x, platform.y, platform.width, platform.height);

                // Brick grid lines
                ctx.strokeStyle = '#78281f';
                ctx.lineWidth = 2;
                ctx.strokeRect(platform.x, platform.y, platform.width, platform.height);
            }
        });

        // Draw 3D Spinning Coins
        coins.forEach(coin => {
            if (!coin.collected) {
                ctx.save();
                ctx.translate(coin.x, coin.y);
                // Simulate 3D spin by scaling width with Math.cos
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

        // Draw HUD / UI
        ctx.fillStyle = "rgba(0, 0, 0, 0.4)";
        ctx.fillRect(15, 15, 185, 40);
        ctx.strokeStyle = "rgba(255, 255, 255, 0.3)";
        ctx.strokeRect(15, 15, 185, 40);

        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 18px 'Segoe UI'";
        ctx.fillText("SCORE: " + score, 30, 42);
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
