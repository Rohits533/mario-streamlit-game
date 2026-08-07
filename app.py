import streamlit as st

st.set_page_config(
    page_title="Super 2D Platformer",
    page_icon="🍄",
    layout="centered"
)

st.title("🍄 Super 2D Platformer")
st.write("A classic 2D platformer powered by JavaScript and wrapped in a Python Streamlit app.")

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
            font-family: Arial, sans-serif;
            color: white;
        }
        .game-container {
            text-align: center;
        }
        canvas {
            border: 4px solid #fff;
            background: #5c94fc;
            box-shadow: 0 0 20px rgba(0,0,0,0.5);
        }
        .instructions {
            margin-top: 10px;
            font-size: 14px;
            color: #ccc;
        }
    </style>
</head>
<body>

<div class="game-container">
    <canvas id="gameCanvas" width="750" height="400"></canvas>
    <div class="instructions">
        Controls: <strong>Arrow Left / Right</strong> to Move | <strong>Arrow Up</strong> or <strong>Spacebar</strong> to Jump
    </div>
</div>

<script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");

    let score = 0;
    const keys = {};

    const player = {
        x: 50, y: 200, width: 30, height: 40,
        vx: 0, vy: 0, speed: 4, jumpPower: -10,
        gravity: 0.5, grounded: false
    };

    const platforms = [
        { x: 0, y: 350, width: 750, height: 50, color: '#00aa00' },
        { x: 300, y: 260, width: 120, height: 20, color: '#c84c0c' },
        { x: 500, y: 180, width: 150, height: 20, color: '#c84c0c' },
        { x: 150, y: 180, width: 100, height: 20, color: '#c84c0c' }
    ];

    let coins = [
        { x: 345, y: 220, radius: 10, collected: false },
        { x: 565, y: 140, radius: 10, collected: false },
        { x: 190, y: 140, radius: 10, collected: false },
        { x: 380, y: 310, radius: 10, collected: false }
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
        if (keys["ArrowLeft"]) player.vx = -player.speed;
        else if (keys["ArrowRight"]) player.vx = player.speed;
        else player.vx = 0;

        player.x += player.vx;
        if (player.x < 0) player.x = 0;
        if (player.x + player.width > canvas.width) player.x = canvas.width - player.width;

        player.vy += player.gravity;
        player.y += player.vy;
        player.grounded = false;

        platforms.forEach(platform => {
            if (
                player.x < platform.x + platform.width &&
                player.x + player.width > platform.x &&
                player.y + player.height >= platform.y &&
                player.y + player.height - player.vy <= platform.y + 5 &&
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

        coins.forEach(coin => {
            if (!coin.collected) {
                let dist = Math.hypot(coin.x - (player.x + player.width / 2), coin.y - (player.y + player.height / 2));
                if (dist < coin.radius + player.width / 3) {
                    coin.collected = true;
                    score += 100;
                }
            }
        });

        if (player.y > canvas.height) {
            player.x = 50; player.y = 200; player.vy = 0;
            score = Math.max(0, score - 200);
            coins.forEach(c => c.collected = false);
        }
    }

    function draw() {
        ctx.fillStyle = "#5c94fc";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        platforms.forEach(platform => {
            ctx.fillStyle = platform.color;
            ctx.fillRect(platform.x, platform.y, platform.width, platform.height);
            ctx.fillStyle = "#f8f8f8";
            ctx.fillRect(platform.x, platform.y, platform.width, 4);
        });

        coins.forEach(coin => {
            if (!coin.collected) {
                ctx.fillStyle = "#ffd700";
                ctx.beginPath();
                ctx.arc(coin.x, coin.y, coin.radius, 0, Math.PI * 2);
                ctx.fill();
            }
        });

        ctx.fillStyle = "#e52521";
        ctx.fillRect(player.x, player.y, player.width, player.height);
        ctx.fillStyle = "#ffffff";
        ctx.fillRect(player.x + 18, player.y + 8, 8, 8);

        ctx.fillStyle = "#ffffff";
        ctx.font = "20px Arial";
        ctx.fillText("SCORE: " + score, 20, 30);
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

st.components.v1.html(game_html, height=500, scrolling=False)
