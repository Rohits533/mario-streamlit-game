import streamlit as st

st.set_page_config(page_title="Super Mario: Infinite Deluxe Ultimate", page_icon="🍄", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #050508; color: white; }
    .arcade-header { text-align: center; font-family: 'Courier New', monospace; color: #ffcc00; text-shadow: 3px 3px #ff0000; margin-bottom: 0; letter-spacing: 2px; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='arcade-header'>🍄 SUPER MARIO: ULTIMATE INFINITE DELUXE 🍄</h1>", unsafe_allow_html=True)

game_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        body { margin: 0; background: #050508; display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh; font-family: 'Courier New', monospace; color: white; overflow: hidden; }
        .game-wrapper { position: relative; text-align: center; }
        canvas { border: 4px solid #fff; background: linear-gradient(to bottom, #2b6cb0 0%, #63b3ed 70%, #e2e8f0 100%); box-shadow: 0 0 50px rgba(43, 108, 176, 0.8); image-rendering: pixelated; }
        .hud-panel { margin-top: 8px; display: flex; justify-content: space-between; align-items: center; width: 768px; font-size: 13px; font-weight: bold; background: rgba(15, 15, 25, 0.95); padding: 8px 12px; border: 2px solid #555; box-sizing: border-box; border-radius: 4px; }
        .btn-arcade { background: #e74c3c; color: white; border: 2px solid #fff; padding: 6px 12px; font-family: 'Courier New', monospace; font-weight: bold; cursor: pointer; text-transform: uppercase; box-shadow: 0 4px #990000; border-radius: 3px; }
        .btn-arcade:active { transform: translateY(2px); box-shadow: 0 2px #990000; }
        .modal { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 580px; background: rgba(10, 10, 18, 0.98); border: 4px solid #f1c40f; padding: 25px; z-index: 20; box-shadow: 0 0 80px rgba(241, 196, 15, 0.8); text-align: center; border-radius: 8px; animation: modalZoomIn 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; }
        @keyframes modalZoomIn { 0% { transform: translate(-50%, -50%) scale(0.2); opacity: 0; } 100% { transform: translate(-50%, -50%) scale(1); opacity: 1; } }
        #gameOverScreen { display: none; border-color: #e74c3c; box-shadow: 0 0 80px rgba(231, 76, 60, 0.8); z-index: 30; }
        #settingsModal, #pauseModal, #achievementsModal, #characterSelectModal, #statsModal { display: none; z-index: 25; text-align: left; }
        #pauseModal { z-index: 35; }
        #characterSelectModal { z-index: 40; }
        .store-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 15px; }
        .form-control-group { margin-top: 10px; display: flex; flex-direction: column; gap: 4px; }
        .form-control-group label { font-size: 11px; color: #f1c40f; }
        .form-control-group input, .form-control-group select { background: #222; color: white; border: 1px solid #555; padding: 5px; font-family: 'Courier New'; border-radius: 3px; }
        #storeModal, #customMakerModal { display: none; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 580px; background: rgba(10, 10, 18, 0.98); border: 4px solid #f1c40f; padding: 20px; z-index: 10; box-shadow: 0 0 80px rgba(241, 196, 15, 0.8); text-align: left; border-radius: 6px; max-height: 420px; overflow-y: auto; }
        .achievement-item { background: #1a1a2e; border: 2px solid #333; padding: 8px; margin-bottom: 6px; border-radius: 4px; font-size: 11px; }
        .achievement-unlocked { border-color: #f1c40f; background: #2d2d1a; }
        .world-indicator { position: absolute; top: 10px; left: 10px; font-size: 14px; font-weight: bold; color: #f1c40f; text-shadow: 2px 2px #000; z-index: 15; }
        .mini-map { position: absolute; bottom: 10px; right: 10px; width: 150px; height: 80px; background: rgba(0,0,0,0.7); border: 2px solid #555; z-index: 15; }
        
        /* Loading Screen */
        #loadingScreen { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #050508; display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 9999; transition: opacity 0.8s ease-out; }
        #loadingScreen.hidden { opacity: 0; pointer-events: none; }
        .loading-title { font-size: 32px; color: #ffcc00; text-shadow: 3px 3px #ff0000, -2px -2px #2980b9; margin-bottom: 40px; animation: loadingPulse 1.5s infinite; }
        @keyframes loadingPulse { 0%, 100% { transform: scale(1); opacity: 1; } 50% { transform: scale(1.05); opacity: 0.8; } }
        .loading-bar-container { width: 400px; height: 30px; background: #1a1a2e; border: 3px solid #f1c40f; border-radius: 15px; overflow: hidden; box-shadow: 0 0 30px rgba(241, 196, 15, 0.6); }
        .loading-bar { height: 100%; width: 0%; background: linear-gradient(90deg, #e74c3c, #f1c40f, #2ecc71, #3498db, #e74c3c); background-size: 200% 100%; animation: loadingGradient 2s linear infinite; transition: width 0.3s ease; }
        @keyframes loadingGradient { 0% { background-position: 0% 50%; } 100% { background-position: 200% 50%; } }
        .loading-text { margin-top: 20px; font-size: 14px; color: #3498db; letter-spacing: 2px; }
        .loading-dots { display: inline-block; animation: dotsBlink 1.5s infinite; }
        @keyframes dotsBlink { 0%, 20% { opacity: 0; } 50% { opacity: 1; } 80%, 100% { opacity: 0; } }
        .pixel-mario { width: 64px; height: 64px; margin-bottom: 30px; animation: marioJump 1s infinite; }
        @keyframes marioJump { 0%, 100% { transform: translateY(0) scale(1); } 50% { transform: translateY(-20px) scale(1.1); } }
        .loading-tips { margin-top: 30px; font-size: 11px; color: #7f8c8d; max-width: 400px; line-height: 1.6; }
        .loading-tips span { color: #f1c40f; }
        
        /* Character Select */
        .char-select-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin: 20px 0; }
        .char-card { background: #1a1a2e; border: 3px solid #333; padding: 15px; border-radius: 8px; cursor: pointer; transition: all 0.3s; }
        .char-card:hover { transform: translateY(-5px); }
        .char-card.selected { border-color: #f1c40f; box-shadow: 0 0 20px rgba(241, 196, 15, 0.6); }
        .char-card h3 { margin: 10px 0 5px; font-size: 14px; }
        .char-card p { font-size: 10px; color: #7f8c8d; margin: 5px 0; }
        .char-stats { font-size: 9px; margin-top: 8px; }
        .stat-bar { display: flex; align-items: center; gap: 5px; margin: 3px 0; }
        .stat-dots { display: flex; gap: 2px; }
        .stat-dot { width: 8px; height: 8px; border-radius: 50%; background: #333; }
        .stat-dot.filled { background: #f1c40f; }
        
        /* Stats Display */
        .stats-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin: 15px 0; }
        .stat-box { background: #1a1a2e; border: 2px solid #333; padding: 10px; border-radius: 6px; text-align: center; }
        .stat-box h4 { margin: 0; font-size: 11px; color: #7f8c8d; }
        .stat-box .value { font-size: 18px; font-weight: bold; color: #f1c40f; margin-top: 5px; }
        
        /* HUD Icons */
        .hud-icon { cursor: pointer; font-size: 16px; margin-left: 8px; }
        .hud-icon:hover { transform: scale(1.2); }
        
        /* Power-up Inventory */
        .powerup-inventory { position: absolute; top: 10px; right: 10px; z-index: 15; display: flex; gap: 5px; }
        .powerup-item { background: rgba(0,0,0,0.8); border: 2px solid #f1c40f; padding: 4px 8px; border-radius: 4px; font-size: 11px; }
        
        /* Mobile Controls */
        .mobile-controls { display: none; position: absolute; bottom: 20px; left: 20px; z-index: 50; gap: 10px; }
        .mobile-controls button { width: 60px; height: 60px; font-size: 24px; background: rgba(231, 76, 60, 0.8); border: 3px solid #fff; border-radius: 10px; color: white; }
        .mobile-controls button:active { background: rgba(231, 76, 60, 1); }
        .mobile-controls-right { position: absolute; bottom: 20px; right: 20px; z-index: 50; display: flex; gap: 10px; }
        
        @media (max-width: 800px) {
            .mobile-controls, .mobile-controls-right { display: flex; }
        }
        
        /* Share Button */
        .btn-share { background: #3498db; margin-top: 10px; }
        .btn-share:active { box-shadow: 0 2px #1a5276; }
        
        /* Level Editor */
        .level-editor-grid { display: grid; grid-template-columns: repeat(8, 1fr); gap: 5px; margin: 15px 0; }
        .editor-cell { width: 50px; height: 50px; background: #1a1a2e; border: 2px solid #333; cursor: pointer; }
        .editor-cell:hover { border-color: #f1c40f; }
        .editor-cell.ground { background: #a04000; }
        .editor-cell.brick { background: #b03a2e; }
        .editor-cell.question { background: #d4ac0d; }
        .editor-cell.coin { background: #f1c40f; border-radius: 50%; }
        .editor-cell.enemy { background: #78281f; }
        .editor-cell.pipe { background: #27ae60; }
        .editor-cell.hazard { background: #c0392b; }
    </style>
</head>
<body>

<!-- Loading Screen -->
<div id="loadingScreen">
    <div class="loading-title">🍄 SUPER MARIO 🍄</div>
    <div style="font-size: 14px; color: #3498db; margin-bottom: 30px; letter-spacing: 3px;">INFINITE DELUXE ULTIMATE EDITION</div>
    <div class="pixel-mario" style="position: relative; width: 64px; height: 64px; margin: 0 auto 30px;">
        <div style="position: absolute; top: 0; left: 16px; width: 32px; height: 16px; background: #e74c3c;"></div>
        <div style="position: absolute; top: 16px; left: 12px; width: 40px; height: 16px; background: #f1c40f;"></div>
        <div style="position: absolute; top: 32px; left: 8px; width: 48px; height: 20px; background: #e74c3c;"></div>
        <div style="position: absolute; top: 52px; left: 12px; width: 16px; height: 12px; background: #2980b9;"></div>
        <div style="position: absolute; top: 52px; left: 36px; width: 16px; height: 12px; background: #2980b9;"></div>
    </div>
    <div class="loading-bar-container">
        <div class="loading-bar" id="loadingBar"></div>
    </div>
    <div class="loading-text">LOADING <span class="loading-dots">...</span></div>
    <div class="loading-tips">
        💡 <span>TIP:</span> Press Z to shoot fireballs!<br>
        💡 <span>TIP:</span> Build combos for 10x multiplier!<br>
        💡 <span>TIP:</span> Defeat bosses to advance worlds!
    </div>
</div>

<!-- Character Select Modal -->
<div id="characterSelectModal" class="modal">
    <h2 style="color: #f1c40f; margin-top: 0; text-align: center;">🎮 SELECT YOUR HERO</h2>
    <div class="char-select-grid">
        <div class="char-card selected" onclick="selectCharFromCard('mario')" id="card-mario">
            <div style="font-size: 32px;">🍄</div>
            <h3>MARIO</h3>
            <p>Balanced hero with dash ability</p>
            <div class="char-stats">
                <div class="stat-bar"><span>Speed</span><div class="stat-dots"><div class="stat-dot filled"></div><div class="stat-dot filled"></div><div class="stat-dot filled"></div><div class="stat-dot"></div></div></div>
                <div class="stat-bar"><span>Jump</span><div class="stat-dots"><div class="stat-dot filled"></div><div class="stat-dot filled"></div><div class="stat-dot filled"></div><div class="stat-dot"></div></div></div>
                <div class="stat-bar"><span>Power</span><div class="stat-dots"><div class="stat-dot filled"></div><div class="stat-dot filled"></div><div class="stat-dot"></div><div class="stat-dot"></div></div></div>
            </div>
        </div>
        <div class="char-card" onclick="selectCharFromCard('luigi')" id="card-luigi">
            <div style="font-size: 32px;">👻</div>
            <h3>LUIGI</h3>
            <p>Super high jumps, slippery</p>
            <div class="char-stats">
                <div class="stat-bar"><span>Speed</span><div class="stat-dots"><div class="stat-dot filled"></div><div class="stat-dot filled"></div><div class="stat-dot"></div><div class="stat-dot"></div></div></div>
                <div class="stat-bar"><span>Jump</span><div class="stat-dots"><div class="stat-dot filled"></div><div class="stat-dot filled"></div><div class="stat-dot filled"></div><div class="stat-dot filled"></div></div></div>
                <div class="stat-bar"><span>Power</span><div class="stat-dots"><div class="stat-dot filled"></div><div class="stat-dot filled"></div><div class="stat-dot"></div><div class="stat-dot"></div></div></div>
            </div>
        </div>
        <div class="char-card" onclick="selectCharFromCard('peach')" id="card-peach">
            <div style="font-size: 32px;">👸</div>
            <h3>PEACH</h3>
            <p>Hover in mid-air, floaty</p>
            <div class="char-stats">
                <div class="stat-bar"><span>Speed</span><div class="stat-dots"><div class="stat-dot filled"></div><div class="stat-dot filled"></div><div class="stat-dot"></div><div class="stat-dot"></div></div></div>
                <div class="stat-bar"><span>Jump</span><div class="stat-dots"><div class="stat-dot filled"></div><div class="stat-dot filled"></div><div class="stat-dot filled"></div><div class="stat-dot"></div></div></div>
                <div class="stat-bar"><span>Power</span><div class="stat-dots"><div class="stat-dot filled"></div><div class="stat-dot filled"></div><div class="stat-dot filled"></div><div class="stat-dot"></div></div></div>
            </div>
        </div>
        <div class="char-card" onclick="selectCharFromCard('yoshi')" id="card-yoshi">
            <div style="font-size: 32px;">🦎</div>
            <h3>YOSHI</h3>
            <p>Double jump, fast runner</p>
            <div class="char-stats">
                <div class="stat-bar"><span>Speed</span><div class="stat-dots"><div class="stat-dot filled"></div><div class="stat-dot filled"></div><div class="stat-dot filled"></div><div class="stat-dot filled"></div></div></div>
                <div class="stat-bar"><span>Jump</span><div class="stat-dots"><div class="stat-dot filled"></div><div class="stat-dot filled"></div><div class="stat-dot filled"></div><div class="stat-dot"></div></div></div>
                <div class="stat-bar"><span>Power</span><div class="stat-dots"><div class="stat-dot filled"></div><div class="stat-dot filled"></div><div class="stat-dot"></div><div class="stat-dot"></div></div></div>
            </div>
        </div>
    </div>
    <button class="btn-arcade" onclick="confirmCharacter()" style="background: #27ae60; font-size: 16px; padding: 12px; width: 100%;">▶ START ADVENTURE</button>
</div>

<div class="game-wrapper">
    <canvas id="gameCanvas" width="768" height="432"></canvas>
    <div class="world-indicator" id="worldDisplay">🌍 WORLD 1</div>
    <div class="powerup-inventory" id="powerupInventory"></div>
    
    <!-- Mobile Controls -->
    <div class="mobile-controls">
        <button onclick="mobilePress('left')">⬅️</button>
        <button onclick="mobilePress('right')">➡️</button>
        <button onclick="mobilePress('jump')">⬆️</button>
    </div>
    <div class="mobile-controls-right">
        <button onclick="mobilePress('x')">X</button>
        <button onclick="mobilePress('z')">Z</button>
    </div>

    <div id="entryScreen" class="modal" style="display: none;">
        <h1 style="color: #ffcc00; text-shadow: 2px 2px #ff0000; font-size: 26px; margin-top:0;">🍄 SUPER MARIO 🍄</h1>
        <div style="font-size: 13px; color: #3498db; margin-bottom: 25px; letter-spacing: 1px;">INFINITE DELUXE ULTIMATE EDITION</div>
        <div style="font-size: 12px; color: #2ecc71; margin-bottom: 15px;">⭐ High Score: <span id="menuHighScore">0</span> | 🪙 Coins: <span id="menuCoins">100</span> | ❤️ Lives: <span id="menuLives">3</span></div>
        <div style="display: flex; flex-direction: column; gap: 12px; width: 70%; margin: 0 auto;">
            <button class="btn-arcade" onclick="startGame()" style="background:#27ae60; font-size:16px; padding:12px;">▶ BEGIN GAME</button>
            <button class="btn-arcade" onclick="openAchievements()" style="background:#9b59b6; font-size:14px; padding:10px;">🏅 ACHIEVEMENTS</button>
            <button class="btn-arcade" onclick="openSettingsMenu()" style="background:#2980b9; font-size:14px; padding:10px;">⚙ SETTINGS</button>
        </div>
    </div>

    <div id="gameOverScreen" class="modal">
        <h1 style="color: #e74c3c; text-shadow: 2px 2px #000; font-size: 28px; margin-top:0;">💀 GAME OVER 💀</h1>
        <div style="font-size: 13px; color: #ccc; margin-bottom: 10px;">Hero fell into hazard or pit!</div>
        <div class="stats-grid">
            <div class="stat-box"><h4>SCORE</h4><div class="value" id="finalScoreVal">0</div></div>
            <div class="stat-box"><h4>COINS</h4><div class="value" id="finalCoins">0</div></div>
            <div class="stat-box"><h4>ENEMIES</h4><div class="value" id="finalEnemies">0</div></div>
        </div>
        <div style="font-size: 13px; color: #2ecc71; margin-bottom: 20px;">🏆 High Score: <span id="gameOverHighScore">0</span></div>
        <div style="display: flex; flex-direction: column; gap: 12px; width: 70%; margin: 0 auto;">
            <button class="btn-arcade" onclick="restartGame()" style="background:#27ae60; font-size:15px; padding:12px;">🔄 PLAY AGAIN</button>
            <button class="btn-arcade btn-share" onclick="shareScore()" style="font-size:14px; padding:10px;">📋 SHARE SCORE</button>
            <button class="btn-arcade" onclick="returnToMainMenu()" style="background:#2980b9; font-size:13px; padding:10px;">🏠 MAIN MENU</button>
        </div>
    </div>

    <div id="pauseModal" class="modal">
        <h2 style="color: #f39c12; margin-top: 0; text-align: center; text-shadow: 1px 1px #000;">⏸️ GAME PAUSED</h2>
        <div style="display: flex; flex-direction: column; gap: 12px; margin-top: 20px;">
            <button class="btn-arcade" onclick="togglePause()" style="background: #27ae60; font-size:15px; padding:12px;">▶ RESUME</button>
            <button class="btn-arcade" onclick="openSettingsMenu()" style="background: #2980b9; font-size:14px; padding:10px;">⚙ SETTINGS</button>
            <button class="btn-arcade" onclick="returnToMainMenu()" style="background: #e74c3c; font-size:14px; padding:10px;">🏠 QUIT TO MENU</button>
        </div>
    </div>

    <div id="achievementsModal" class="modal">
        <h2 style="color: #f1c40f; margin-top: 0; text-align: center; text-shadow: 1px 1px #000;">🏅 ACHIEVEMENTS</h2>
        <div id="achievementsList" style="max-height: 280px; overflow-y: auto; margin-top: 10px;"></div>
        <div style="text-align: center; margin-top: 15px;">
            <button class="btn-arcade" onclick="closeAchievements()" style="background: #27ae60; width: 100%;">CLOSE</button>
        </div>
    </div>

    <div id="settingsModal" class="modal">
        <h2 style="color: #2980b9; margin-top: 0; text-align: center; text-shadow: 1px 1px #000;">⚙ GAME SETTINGS</h2>
        <div class="form-control-group">
            <label>BGM Music Volume: <span id="volVal">50%</span></label>
            <input type="range" id="musicVol" min="0" max="100" value="50" oninput="updateMusicVolume(this.value)">
        </div>
        <div class="form-control-group">
            <label>SFX Sound Effects:</label>
            <select id="sfxToggle"><option value="on">Enabled</option><option value="off">Muted</option></select>
        </div>
        <div style="text-align: center; margin-top: 20px;">
            <button class="btn-arcade" onclick="closeSettingsMenu()" style="background: #27ae60; width: 100%;">SAVE & BACK</button>
        </div>
    </div>

    <div class="hud-panel">
        <div>
            <span>ARROWS/SPACE/X/Z | SCORE: <span id="hudScore">0</span> | BEST: <span id="hudHighScore">0</span> | COINS: <span id="hudCoins">100</span></span>
            <span style="margin-left: 10px;">❤️ <span id="hudLives">3</span> | x<span id="hudMultiplier">1</span></span>
            <span class="hud-icon" onclick="toggleSound()" id="soundIcon">🔊</span>
        </div>
        <div>
            <button class="btn-arcade" onclick="openStore()" style="background:#27ae60;">SHOP</button>
            <button class="btn-arcade" onclick="openCustomMaker()" style="background:#2980b9;">BUILDER</button>
            <button class="btn-arcade" onclick="togglePause()" id="pauseBtn">PAUSE</button>
        </div>
    </div>

    <div id="storeModal">
        <h2 style="color: #f1c40f; margin-top: 0; text-align: center; text-shadow: 1px 1px #000;">🍄 TOAD'S ULTIMATE BOUTIQUE</h2>
        <div style="font-size: 12px; color: #ccc; text-align: center;">Unlock elite heroes and legendary character outfits!</div>
        <div style="margin-top: 12px; font-weight: bold; color: #3498db; font-size:12px;">CHOOSE HERO:</div>
        <div style="display: flex; gap: 6px; margin-top: 4px;">
            <button class="btn-arcade" onclick="selectCharacter('mario')" style="flex:1; background:#c84c0c; font-size:10px;" id="charMario">Mario</button>
            <button class="btn-arcade" onclick="selectCharacter('luigi')" style="flex:1; background:#27ae60; font-size:10px;" id="charLuigi">Luigi</button>
            <button class="btn-arcade" onclick="selectCharacter('peach')" style="flex:1; background:#f39c12; font-size:10px;" id="charPeach">Peach</button>
            <button class="btn-arcade" onclick="selectCharacter('yoshi')" style="flex:1; background:#2ecc71; font-size:10px;" id="charYoshi">Yoshi</button>
        </div>
        <div style="margin-top: 12px; font-weight: bold; color: #f39c12; font-size:12px;">WARDROBE SKINS:</div>
        <div class="store-grid">
            <div class="store-item" id="skin_classic"><div style="font-weight:bold; font-size:11px;">Classic</div><button class="btn-arcade" style="margin-top:6px; font-size:9px;" onclick="buySkin('classic', 0)">Equipped</button></div>
            <div class="store-item" id="skin_fire"><div style="font-weight:bold; font-size:11px;">Fire (40c)</div><button class="btn-arcade" style="margin-top:6px; font-size:9px;" onclick="buySkin('fire', 40)">Unlock</button></div>
            <div class="store-item" id="skin_gold"><div style="font-weight:bold; font-size:11px;">Gold (90c)</div><button class="btn-arcade" style="margin-top:6px; font-size:9px;" onclick="buySkin('gold', 90)">Unlock</button></div>
            <div class="store-item" id="skin_dark"><div style="font-weight:bold; font-size:11px;">Dark (150c)</div><button class="btn-arcade" style="margin-top:6px; font-size:9px;" onclick="buySkin('dark', 150)">Unlock</button></div>
            <div class="store-item" id="skin_galaxy"><div style="font-weight:bold; font-size:11px;">Galaxy (250c)</div><button class="btn-arcade" style="margin-top:6px; font-size:9px;" onclick="buySkin('galaxy', 250)">Unlock</button></div>
            <div class="store-item" id="skin_rainbow"><div style="font-weight:bold; font-size:11px;">Rainbow (400c)</div><button class="btn-arcade" style="margin-top:6px; font-size:9px;" onclick="buySkin('rainbow', 400)">Unlock</button></div>
        </div>
        <div style="text-align: center; margin-top: 15px;">
            <button class="btn-arcade" onclick="closeStore()" style="background: #27ae60; width: 100%;">BACK TO GAME</button>
        </div>
    </div>

    <div id="customMakerModal">
        <h2 style="color: #2980b9; margin-top: 0; text-align: center; text-shadow: 1px 1px #000;">⚙️ CUSTOM GAME WORKSHOP</h2>
        <div style="font-size: 11px; color: #ccc; text-align: center;">Tweak physics, speed, gravity, and environment parameters in real-time!</div>
        <div class="form-control-group">
            <label>Player Movement Speed: <span id="valSpeed">4.2</span></label>
            <input type="range" id="customSpeed" min="2.0" max="8.0" step="0.1" value="4.2" oninput="updateCustomParam('speed', this.value)">
        </div>
        <div class="form-control-group">
            <label>Jump Power: <span id="valJump">-12.5</span></label>
            <input type="range" id="customJump" min="-18.0" max="-8.0" step="0.5" value="-12.5" oninput="updateCustomParam('jump', this.value)">
        </div>
        <div class="form-control-group">
            <label>Gravity Force: <span id="valGrav">0.5</span></label>
            <input type="range" id="customGrav" min="0.1" max="1.2" step="0.05" value="0.5" oninput="updateCustomParam('grav', this.value)">
        </div>
        <div class="form-control-group">
            <label>World Environment Theme:</label>
            <select id="customTheme" onchange="updateCustomParam('theme', this.value)">
                <option value="classic">Classic Overworld</option>
                <option value="midnight">Midnight Galaxy</option>
                <option value="neon">Neon Cyberpunk</option>
                <option value="sunset">Sunset Volcano</option>
            </select>
        </div>
        <div style="text-align: center; margin-top: 18px;">
            <button class="btn-arcade" onclick="closeCustomMaker()" style="background: #2980b9; width: 100%;">APPLY & PLAY</button>
        </div>
    </div>
</div>

<script>
    // Loading Screen Logic
    let loadingProgress = 0;
    const loadingBar = document.getElementById('loadingBar');
    const loadingScreen = document.getElementById('loadingScreen');
    const characterSelectModal = document.getElementById('characterSelectModal');
    const entryScreen = document.getElementById('entryScreen');
    let selectedChar = 'mario';
    let sessionCoins = 0, sessionEnemies = 0, gameTime = 0;

    function updateLoading() {
        loadingProgress += Math.random() * 15 + 5;
        if (loadingProgress > 100) loadingProgress = 100;
        loadingBar.style.width = loadingProgress + '%';
        if (loadingProgress < 100) {
            setTimeout(updateLoading, 200 + Math.random() * 300);
        } else {
            setTimeout(() => {
                loadingScreen.classList.add('hidden');
                setTimeout(() => {
                    loadingScreen.style.display = 'none';
                    characterSelectModal.style.display = 'block';
                }, 800);
            }, 500);
        }
    }
    window.addEventListener('load', () => { setTimeout(updateLoading, 500); });

    // Sound Toggle
    let soundEnabled = true;
    function toggleSound() {
        soundEnabled = !soundEnabled;
        document.getElementById('soundIcon').innerText = soundEnabled ? '🔊' : '🔇';
        document.getElementById('sfxToggle').value = soundEnabled ? 'on' : 'off';
        sfxEnabled = soundEnabled;
    }

    // Character Select
    function selectCharFromCard(char) {
        selectedChar = char;
        document.querySelectorAll('.char-card').forEach(c => c.classList.remove('selected'));
        document.getElementById('card-' + char).classList.add('selected');
    }

    function confirmCharacter() {
        characterSelectModal.style.display = 'none';
        entryScreen.style.display = 'block';
    }

    // Mobile Controls
    function mobilePress(key) {
        const codeMap = { 'left': 'ArrowLeft', 'right': 'ArrowRight', 'jump': 'Space', 'x': 'KeyX', 'z': 'KeyZ' };
        keys[codeMap[key]] = true;
        setTimeout(() => { keys[codeMap[key]] = false; }, 200);
    }

    // Share Score
    function shareScore() {
        const text = '🍄 My Super Mario Score: ' + score + ' points! 🪙 Coins: ' + sessionCoins + ' Enemies: ' + sessionEnemies;
        navigator.clipboard.writeText(text).then(() => {
            alert('Score copied to clipboard! 📋');
        });
    }

    // Rest of game code continues...
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    ctx.imageSmoothingEnabled = false;

    let gameStarted = false, gameOver = false, isPaused = true;
    score = 0; let highScore = parseInt(localStorage.getItem('mario_highscore') || '0');
    let coinsCollected = parseInt(localStorage.getItem('mario_coins') || '100');
    let lives = 3, comboMultiplier = 1, comboTimer = 0;
    let currentWorld = 1, worldScoreThreshold = 2000;
    let cameraX = 0, lastGeneratedX = 0;

    const player = { x: 64, y: 200, width: 32, height: 32, vx: 0, vy: 0, speed: 4.2, jumpPower: -12.5, gravity: 0.5, grounded: false, facing: 'right', canDoubleJump: false, dashCooldown: 0, poweredUp: false, powerTimer: 0, fireballCooldown: 0, hasFirePower: false, starPower: false, starTimer: 0 };
    let currentSkin = 'classic', unlockedSkins = { classic: true, fire: false, gold: false, dark: false, galaxy: false, rainbow: false }, currentTheme = 'classic';
    let platforms = [], enemies = [], coins = [], decorations = [], hazards = [], movingPlatforms = [], thwomps = [], fireBars = [], powerUps = [], particles = [], floatingTexts = [], fireballs = [], bossActive = false, bossHp = 100, bossX = 0, bossY = 0, bossPhase = 1, bossProjectiles = [];
    let activePowerups = [], levelSeed = Math.floor(Math.random() * 10000);

    const achievements = [
        { id: 'first_coin', name: 'First Coin!', desc: 'Collect your first coin', unlocked: false, check: () => coinsCollected >= 1 },
        { id: 'coin_collector', name: 'Coin Collector', desc: 'Collect 50 coins', unlocked: false, check: () => coinsCollected >= 50 },
        { id: 'score_1000', name: 'Rising Star', desc: 'Reach 1000 score', unlocked: false, check: () => score >= 1000 },
        { id: 'score_5000', name: 'Super Star', desc: 'Reach 5000 score', unlocked: false, check: () => score >= 5000 },
        { id: 'combo_master', name: 'Combo Master', desc: 'Reach 5x combo', unlocked: false, check: () => comboMultiplier >= 5 },
        { id: 'world_explorer', name: 'World Explorer', desc: 'Reach World 3', unlocked: false, check: () => currentWorld >= 3 }
    ];

    document.getElementById('menuHighScore').innerText = highScore;
    document.getElementById('menuCoins').innerText = coinsCollected;
    document.getElementById('menuLives').innerText = lives;
    document.getElementById('hudHighScore').innerText = highScore;
    document.getElementById('hudCoins').innerText = coinsCollected;
    document.getElementById('hudLives').innerText = lives;

    let audioCtx = null, musicInterval = null, musicVolume = 0.5, sfxEnabled = true;

    function initAudio() { if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)(); if (audioCtx.state === 'suspended') audioCtx.resume(); }
    function playNote(freq, duration, type='square') { if (!audioCtx || musicVolume === 0 || !soundEnabled) return; try { const osc = audioCtx.createOscillator(), gain = audioCtx.createGain(); osc.type = type; osc.frequency.value = freq; gain.gain.setValueAtTime(musicVolume * 0.15, audioCtx.currentTime); gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + duration); osc.connect(gain); gain.connect(audioCtx.destination); osc.start(); osc.stop(audioCtx.currentTime + duration); } catch(e) {} }
    function playSFX(type) { if (!audioCtx || !sfxEnabled || !soundEnabled) return; try { const osc = audioCtx.createOscillator(), gain = audioCtx.createGain(); if (type === 'jump') { osc.frequency.setValueAtTime(150, audioCtx.currentTime); osc.frequency.linearRampToValueAtTime(300, audioCtx.currentTime + 0.1); gain.gain.setValueAtTime(0.1, audioCtx.currentTime); gain.gain.linearRampToValueAtTime(0, audioCtx.currentTime + 0.1); } else if (type === 'coin') { osc.type = 'sine'; osc.frequency.setValueAtTime(988, audioCtx.currentTime); gain.gain.setValueAtTime(0.1, audioCtx.currentTime); gain.gain.linearRampToValueAtTime(0, audioCtx.currentTime + 0.15); } else if (type === 'stomp') { osc.type = 'sawtooth'; osc.frequency.setValueAtTime(200, audioCtx.currentTime); osc.frequency.linearRampToValueAtTime(100, audioCtx.currentTime + 0.08); gain.gain.setValueAtTime(0.1, audioCtx.currentTime); gain.gain.linearRampToValueAtTime(0, audioCtx.currentTime + 0.08); } else if (type === 'powerup') { osc.type = 'sine'; osc.frequency.setValueAtTime(400, audioCtx.currentTime); osc.frequency.linearRampToValueAtTime(800, audioCtx.currentTime + 0.2); gain.gain.setValueAtTime(0.1, audioCtx.currentTime); gain.gain.linearRampToValueAtTime(0, audioCtx.currentTime + 0.2); } else if (type === 'damage') { osc.type = 'sawtooth'; osc.frequency.setValueAtTime(150, audioCtx.currentTime); osc.frequency.linearRampToValueAtTime(80, audioCtx.currentTime + 0.15); gain.gain.setValueAtTime(0.15, audioCtx.currentTime); gain.gain.linearRampToValueAtTime(0, audioCtx.currentTime + 0.15); } osc.connect(gain); gain.connect(audioCtx.destination); osc.start(); osc.stop(audioCtx.currentTime + 0.2); } catch(e) {} }

    const melodyNotes = [659.25, 659.25, 0, 659.25, 0, 523.25, 659.25, 0, 783.99, 0, 0, 0, 392.00, 0, 0, 0, 523.25, 0, 0, 392.00, 0, 0, 329.63, 0, 0, 440.00, 0, 493.88, 0, 466.16, 440.00, 0];
    let noteIndex = 0;
    function startBGM() { if (musicInterval) clearInterval(musicInterval); musicInterval = setInterval(() => { if (!isPaused && gameStarted && !gameOver) { const freq = melodyNotes[noteIndex]; if (freq > 0) playNote(freq, 0.18, 'square'); noteIndex = (noteIndex + 1) % melodyNotes.length; } }, 140); }
    function updateMusicVolume(val) { musicVolume = val / 100; document.getElementById('volVal').innerText = val + '%'; }

    function startGame() { initAudio(); gameStarted = true; gameOver = false; isPaused = false; lives = 3; score = 0; currentWorld = 1; comboMultiplier = 1; sessionCoins = 0; sessionEnemies = 0; gameTime = 0; document.getElementById('hudLives').innerText = lives; document.getElementById('hudMultiplier').innerText = comboMultiplier; entryScreen.style.display = 'none'; gameOverScreen.style.display = 'none'; resetGameState(); startBGM(); }
    function restartGame() { gameOver = false; isPaused = false; lives = 3; score = 0; currentWorld = 1; comboMultiplier = 1; sessionCoins = 0; sessionEnemies = 0; document.getElementById('hudLives').innerText = lives; document.getElementById('hudMultiplier').innerText = comboMultiplier; document.getElementById('gameOverScreen').style.display = 'none'; resetGameState(); startBGM(); }
    function returnToMainMenu() { gameOver = false; gameStarted = false; isPaused = true; document.getElementById('gameOverScreen').style.display = 'none'; document.getElementById('pauseModal').style.display = 'none'; document.getElementById('menuHighScore').innerText = highScore; document.getElementById('menuCoins').innerText = coinsCollected; document.getElementById('menuLives').innerText = lives; entryScreen.style.display = 'block'; }

    function openAchievements() { const listEl = document.getElementById('achievementsList'); listEl.innerHTML = ''; achievements.forEach(ach => { const div = document.createElement('div'); div.className = 'achievement-item' + (ach.unlocked ? ' achievement-unlocked' : ''); div.innerHTML = '<strong>' + (ach.unlocked ? '✅' : '🔒') + ' ' + ach.name + '</strong><br>' + ach.desc; listEl.appendChild(div); }); document.getElementById('achievementsModal').style.display = 'block'; isPaused = true; }
    function closeAchievements() { document.getElementById('achievementsModal').style.display = 'none'; isPaused = false; }
    function openSettingsMenu() { document.getElementById('settingsModal').style.display = 'block'; document.getElementById('pauseModal').style.display = 'none'; }
    function closeSettingsMenu() { document.getElementById('settingsModal').style.display = 'none'; if (gameStarted && !gameOver) document.getElementById('pauseModal').style.display = 'block'; }

    function selectCharacter(char) { selectedChar = char; if (char === 'mario') { player.speed = 4.3; player.jumpPower = -12.5; } else if (char === 'luigi') { player.speed = 4.0; player.jumpPower = -14.5; } else if (char === 'peach') { player.speed = 3.8; player.jumpPower = -11.5; } else if (char === 'yoshi') { player.speed = 4.5; player.jumpPower = -12.0; } document.querySelectorAll('[id^=char]').forEach(b => b.style.border = "2px solid #fff"); document.getElementById('char' + char.charAt(0).toUpperCase() + char.slice(1)).style.border = "4px solid #f1c40f"; }
    function buySkin(skinName, cost) { if (unlockedSkins[skinName]) { currentSkin = skinName; alert("Equipped " + skinName + "!"); } else if (coinsCollected >= cost) { coinsCollected -= cost; unlockedSkins[skinName] = true; currentSkin = skinName; localStorage.setItem('mario_coins', coinsCollected); document.getElementById('menuCoins').innerText = coinsCollected; document.getElementById('hudCoins').innerText = coinsCollected; alert("Purchased and equipped " + skinName + "!"); } else { alert("Not enough coins!"); } }
    function openStore() { isPaused = true; document.getElementById("storeModal").style.display = "block"; }
    function closeStore() { isPaused = false; document.getElementById("storeModal").style.display = "none"; }
    function openCustomMaker() { isPaused = true; document.getElementById("customMakerModal").style.display = "block"; }
    function closeCustomMaker() { isPaused = false; document.getElementById("customMakerModal").style.display = "none"; }
    function updateCustomParam(param, val) { if (param === 'speed') { player.speed = parseFloat(val); document.getElementById('valSpeed').innerText = val; } else if (param === 'jump') { player.jumpPower = parseFloat(val); document.getElementById('valJump').innerText = val; } else if (param === 'grav') { player.gravity = parseFloat(val); document.getElementById('valGrav').innerText = val; } else if (param === 'theme') { currentTheme = val; } }
    function togglePause() { if (gameOver || !gameStarted) return; isPaused = !isPaused; document.getElementById("pauseBtn").innerText = isPaused ? "RESUME" : "PAUSE"; document.getElementById("pauseModal").style.display = isPaused ? "block" : "none"; }

    function addGround(startX, width, type='ground') { platforms.push({ x: startX, y: 384, width: width, height: 48, type: type }); }
    function addPipe(x, height) { platforms.push({ x: x, y: 384 - height, width: 64, height: height, type: 'pipe' }); }
    function addQuestionBlock(x, y) { platforms.push({ x: x, y: y, width: 32, height: 32, type: 'question' }); const rand = Math.random(); if (rand > 0.7) powerUps.push({ x: x + 8, y: y - 24, type: 'mushroom', collected: false, vy: 0 }); else if (rand > 0.5 && currentWorld >= 2) powerUps.push({ x: x + 8, y: y - 24, type: 'fireflower', collected: false, vy: 0 }); else coins.push({ x: x + 16, y: y - 24, radius: 9, collected: false }); }
    function addBrick(x, y) { platforms.push({ x: x, y: y, width: 32, height: 32, type: 'brick' }); }
    function addGoomba(x, y) { enemies.push({ x: x, y: y, width: 32, height: 32, vx: -1.5, alive: true, vy: 0, type: 'goomba' }); }
    function addKoopa(x, y) { enemies.push({ x: x, y: y, width: 32, height: 32, vx: -1.2, alive: true, vy: 0, type: 'koopa' }); }
    function addBulletBill(x, y) { enemies.push({ x: x, y: y, width: 32, height: 24, vx: -3.5, alive: true, vy: 0, type: 'bullet' }); }
    function spawnParticles(x, y, color) { for (let i = 0; i < 8; i++) particles.push({ x: x, y: y, vx: (Math.random() - 0.5) * 6, vy: (Math.random() - 0.7) * 6, color: color, life: 35 }); }
    function addFloatingText(x, y, text, color='#f1c40f') { floatingTexts.push({ x: x, y: y, text: text, color: color, life: 40 }); }

    function generateChunk() {
        if (score >= worldScoreThreshold * currentWorld && !bossActive && Math.random() > 0.4) {
            bossActive = true; bossHp = 100 + (currentWorld * 20); bossX = lastGeneratedX + 200; bossY = 300; bossPhase = 1;
            addGround(lastGeneratedX, 600, 'ground'); lastGeneratedX += 600; return;
        }
        const groundWidth = 700 + Math.random() * 350; const biomeRand = Math.random(); let surfaceType = 'ground';
        if (biomeRand > 0.65) surfaceType = 'ice'; else if (biomeRand > 0.35) surfaceType = 'quicksand';
        addGround(lastGeneratedX, groundWidth, surfaceType);
        decorations.push({ x: lastGeneratedX + Math.random() * 120, y: 40, type: 'cloud' });
        decorations.push({ x: lastGeneratedX + 350 + Math.random() * 150, y: 30, type: 'cloud' });
        decorations.push({ x: lastGeneratedX + Math.random() * 250, y: 352, type: 'bush' });
        decorations.push({ x: lastGeneratedX + 450 + Math.random() * 200, y: 352, type: 'castle' });
        for (let cx = lastGeneratedX + 40; cx < lastGeneratedX + groundWidth - 80; cx += 65) coins.push({ x: cx, y: 240 + Math.sin(cx * 0.06) * 50, radius: 9, collected: false });
        const pattern = Math.floor(Math.random() * 6);
        if (pattern === 0) { addPipe(lastGeneratedX + 160, 60); addPipe(lastGeneratedX + 380, 90); addQuestionBlock(lastGeneratedX + 270, 250); addGoomba(lastGeneratedX + 240, 352); if (currentWorld >= 2) addKoopa(lastGeneratedX + 460, 352); }
        else if (pattern === 1) { addBrick(lastGeneratedX + 220, 260); addQuestionBlock(lastGeneratedX + 252, 260); addBrick(lastGeneratedX + 284, 260); hazards.push({ x: lastGeneratedX + 330, y: 368, width: 90, height: 16, type: 'spikes' }); addGoomba(lastGeneratedX + 450, 352); }
        else if (pattern === 2) { thwomps.push({ x: lastGeneratedX + 300, y: 60, startY: 60, width: 40, height: 40, crushing: false }); fireBars.push({ x: lastGeneratedX + 440, y: 300, angle: 0, length: 55, speed: 0.055 }); }
        else if (pattern === 3) { movingPlatforms.push({ x: lastGeneratedX + 150, y: 260, width: 80, height: 16, minX: lastGeneratedX + 130, maxX: lastGeneratedX + 430, vx: 1.9 }); hazards.push({ x: lastGeneratedX + 130, y: 392, width: 320, height: 40, type: 'lava' }); }
        else if (pattern === 4) { fireBars.push({ x: lastGeneratedX + 240, y: 290, angle: 0, length: 45, speed: -0.07 }); fireBars.push({ x: lastGeneratedX + 410, y: 290, angle: 1.5, length: 45, speed: 0.07 }); addGoomba(lastGeneratedX + 330, 352); if (currentWorld >= 2) addBulletBill(lastGeneratedX + 500, 280); }
        else if (pattern === 5) { for (let i = 0; i < 4; i++) addBrick(lastGeneratedX + 200 + (i*32), 352 - ((i+1)*32)); hazards.push({ x: lastGeneratedX + 360, y: 368, width: 70, height: 16, type: 'spikes' }); addGoomba(lastGeneratedX + 470, 352); }
        lastGeneratedX += groundWidth; const pitSize = 80 + Math.random() * 80; if (Math.random() > 0.2) hazards.push({ x: lastGeneratedX, y: 392, width: pitSize, height: 40, type: 'lava' }); lastGeneratedX += pitSize;
    }

    function resetGameState() { cameraX = 0; lastGeneratedX = 0; platforms = []; enemies = []; coins = []; decorations = []; hazards = []; movingPlatforms = []; thwomps = []; fireBars = []; powerUps = []; particles = []; floatingTexts = []; fireballs = []; bossProjectiles = []; activePowerups = []; score = 0; bossActive = false; currentWorld = 1; addGround(0, 900, 'ground'); lastGeneratedX = 900; generateChunk(); player.x = 64; player.y = 200; player.vx = 0; player.vy = 0; player.dashCooldown = 0; player.poweredUp = false; player.powerTimer = 0; player.hasFirePower = false; player.starPower = false; player.starTimer = 0; selectCharacter(selectedChar); updateWorldDisplay(); }
    function updateWorldDisplay() { document.getElementById('worldDisplay').innerText = '🌍 WORLD ' + currentWorld; }

    function updatePowerupInventory() {
        const inv = document.getElementById('powerupInventory');
        inv.innerHTML = '';
        activePowerups.forEach(p => {
            const div = document.createElement('div');
            div.className = 'powerup-item';
            div.innerText = p.type === 'mushroom' ? '🍄' : (p.type === 'fireflower' ? '🌸' : '⭐') + ' ' + Math.ceil(p.timer / 60);
            inv.appendChild(div);
        });
    }

    function shootFireball() { fireballs.push({ x: player.x + (player.facing === 'right' ? 32 : 0), y: player.y + 16, vx: player.facing === 'right' ? 6 : -6, vy: 0, life: 60 }); player.fireballCooldown = 20; playSFX('jump'); }
    function triggerActiveSkill() { if (gameOver || isPaused || !gameStarted) return; if (selectedChar === 'mario' && player.dashCooldown <= 0) { player.vx += (player.facing === 'right' ? 14 : -14); player.dashCooldown = 60; spawnParticles(player.x + 16, player.y + 16, '#e74c3c'); } }

    function triggerGameOver() {
        if (player.starPower) return;
        if (player.poweredUp && !player.hasFirePower) { player.poweredUp = false; player.height = 32; player.y -= 16; spawnParticles(player.x + 16, player.y + 16, '#e74c3c'); playSFX('damage'); addFloatingText(player.x, player.y - 10, "SUPER LOSS!", "#e74c3c"); return; }
        if (player.hasFirePower) { player.hasFirePower = false; player.poweredUp = false; player.height = 32; spawnParticles(player.x + 16, player.y + 16, '#e74c3c'); playSFX('damage'); addFloatingText(player.x, player.y - 10, "POWER LOST!", "#e74c3c"); return; }
        lives--; document.getElementById('hudLives').innerText = lives; playSFX('damage');
        if (lives <= 0) {
            gameOver = true; spawnParticles(player.x + 16, player.y + 16, '#e74c3c');
            if (score > highScore) { highScore = score; localStorage.setItem('mario_highscore', highScore); }
            localStorage.setItem('mario_coins', coinsCollected);
            document.getElementById('finalScoreVal').innerText = score;
            document.getElementById('finalCoins').innerText = sessionCoins;
            document.getElementById('finalEnemies').innerText = sessionEnemies;
            document.getElementById('gameOverHighScore').innerText = highScore;
            document.getElementById('gameOverScreen').style.display = 'block';
        } else { player.x = cameraX + 64; player.y = 200; player.vx = 0; player.vy = 0; player.poweredUp = false; player.hasFirePower = false; player.height = 32; }
    }

    function checkAchievements() { achievements.forEach(ach => { if (!ach.unlocked && ach.check()) { ach.unlocked = true; addFloatingText(player.x, player.y - 40, "🏅 " + ach.name, "#f1c40f"); playSFX('powerup'); } }); }

    const keys = {};
    window.addEventListener("keydown", (e) => { keys[e.code] = true; if(["Space", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", "KeyX", "KeyZ"].includes(e.code)) e.preventDefault(); if (e.code === "KeyX") triggerActiveSkill(); if (e.code === "KeyZ" && player.hasFirePower && player.fireballCooldown <= 0) shootFireball(); });
    window.addEventListener("keyup", (e) => { keys[e.code] = false; });

    function update() {
        if (isPaused || gameOver || !gameStarted) return;
        gameTime++;
        if (player.dashCooldown > 0) player.dashCooldown--;
        if (player.fireballCooldown > 0) player.fireballCooldown--;
        if (player.poweredUp) { player.powerTimer--; if (player.powerTimer <= 0) { player.poweredUp = false; player.hasFirePower = false; player.height = 32; } }
        if (player.starPower) { player.starTimer--; if (player.starTimer <= 0) player.starPower = false; }
        if (comboTimer > 0) { comboTimer--; if (comboTimer <= 0) { comboMultiplier = 1; document.getElementById('hudMultiplier').innerText = comboMultiplier; } }
        
        // Update active powerups
        activePowerups.forEach((p, i) => { p.timer--; if (p.timer <= 0) activePowerups.splice(i, 1); });
        updatePowerupInventory();

        let currentPlatformType = 'ground';
        platforms.forEach(p => { if (player.x + player.width > p.x && player.x < p.x + p.width && Math.abs((player.y + player.height) - p.y) < 6) currentPlatformType = p.type; });
        let acceleration = 0.45, friction = 0.85;
        if (currentPlatformType === 'ice') friction = 0.98;
        else if (currentPlatformType === 'quicksand') player.vx *= 0.6;

        if (keys["ArrowLeft"]) { player.vx -= acceleration; if (player.vx < -player.speed) player.vx = -player.speed; player.facing = 'left'; }
        else if (keys["ArrowRight"]) { player.vx += acceleration; if (player.vx > player.speed) player.vx = player.speed; player.facing = 'right'; }
        else player.vx *= friction;

        player.x += player.vx;
        if (player.x < cameraX + 8) player.x = cameraX + 8;
        const targetCameraX = player.x - 250;
        if (targetCameraX > cameraX) cameraX = targetCameraX;
        if (player.x + canvas.width > lastGeneratedX - 700) generateChunk();

        if (score >= worldScoreThreshold * currentWorld) { currentWorld++; updateWorldDisplay(); addFloatingText(player.x, player.y - 60, "🌍 WORLD " + currentWorld + "!", "#f1c40f"); playSFX('powerup'); }

        let grav = player.gravity;
        if (selectedChar === 'peach' && keys["ArrowUp"] && player.vy > 0) grav = 0.1;
        player.vy += grav; player.y += player.vy; player.grounded = false;

        platforms.forEach(platform => { if (player.x < platform.x + platform.width && player.x + player.width > platform.x && player.y + player.height >= platform.y && player.y + player.height - player.vy <= platform.y + 14 && player.vy >= 0) { player.y = platform.y - player.height; player.vy = 0; player.grounded = true; player.canDoubleJump = true; if (platform.type === 'quicksand') player.y += 1.8; } });
        movingPlatforms.forEach(mp => { mp.x += mp.vx; if (mp.x < mp.minX || mp.x > mp.maxX) mp.vx *= -1; if (player.x < mp.x + mp.width && player.x + player.width > mp.x && player.y + player.height >= mp.y && player.y + player.height - player.vy <= mp.y + 12 && player.vy >= 0) { player.y = mp.y - player.height; player.vy = 0; player.grounded = true; player.canDoubleJump = true; player.x += mp.vx; } });

        if (keys["ArrowUp"] || keys["Space"]) { if (player.grounded) { player.vy = player.jumpPower; player.grounded = false; spawnParticles(player.x + 16, player.y + 32, '#fff'); playSFX('jump'); } else if (selectedChar === 'yoshi' && player.canDoubleJump) { player.vy = player.jumpPower * 0.9; player.canDoubleJump = false; spawnParticles(player.x + 16, player.y + 16, '#2ecc71'); playSFX('jump'); } }

        fireballs.forEach((fb, index) => { fb.x += fb.vx; fb.life--; if (fb.life <= 0) { fireballs.splice(index, 1); return; } enemies.forEach(enemy => { if (enemy.alive && fb.x < enemy.x + enemy.width && fb.x + 8 > enemy.x && fb.y < enemy.y + enemy.height && fb.y + 8 > enemy.y) { enemy.alive = false; score += 200 * comboMultiplier; coinsCollected += 1; sessionCoins++; sessionEnemies++; comboTimer = 120; comboMultiplier = Math.min(comboMultiplier + 1, 10); document.getElementById('hudMultiplier').innerText = comboMultiplier; addFloatingText(enemy.x, enemy.y - 15, "+200", "#f1c40f"); spawnParticles(enemy.x + 16, enemy.y + 16, '#f1c40f'); playSFX('stomp'); fireballs.splice(index, 1); } }); });

        // Boss with phases & projectiles
        if (bossActive) {
            if (Math.abs(player.x - bossX) < 200) bossX -= 0.8;
            // Boss phases
            if (bossHp < 60 && bossPhase === 1) { bossPhase = 2; addFloatingText(bossX, bossY - 60, "PHASE 2!", "#e74c3c"); }
            if (bossHp < 30 && bossPhase === 2) { bossPhase = 3; addFloatingText(bossX, bossY - 60, "RAGE MODE!", "#ff0000"); }
            // Boss shoots projectiles in phase 2+
            if (bossPhase >= 2 && Math.random() < 0.02) {
                bossProjectiles.push({ x: bossX + 24, y: bossY + 24, vx: player.x > bossX ? 4 : -4, vy: 0 });
            }
            if (player.x < bossX + 48 && player.x + player.width > bossX && player.y < bossY + 48 && player.y + player.height > bossY) {
                if (player.vy > 0 && player.y + player.height - player.vy <= bossY + 16) { bossHp -= 25; player.vy = -12; addFloatingText(bossX, bossY - 20, "-25 HP!", "#e74c3c"); spawnParticles(bossX + 24, bossY + 24, '#e74c3c'); playSFX('stomp'); if (bossHp <= 0) { bossActive = false; score += 2000 * comboMultiplier; coinsCollected += 20; sessionCoins += 20; addFloatingText(bossX, bossY - 40, "+2000 BOSS DEFEATED!", "#f1c40f"); playSFX('powerup'); bossProjectiles = []; } } else if (!player.starPower) triggerGameOver();
            }
        }
        
        // Boss projectiles
        bossProjectiles.forEach((bp, i) => { bp.x += bp.vx; bp.life = (bp.life || 60) - 1; if (bp.life <= 0) { bossProjectiles.splice(i, 1); return; } if (player.x < bp.x + 8 && player.x + player.width > bp.x && player.y < bp.y + 8 && player.y + player.height > bp.y) { if (!player.starPower) triggerGameOver(); } });

        thwomps.forEach(t => { if (Math.abs(player.x - t.x) < 130) t.crushing = true; if (t.crushing) { t.y += 8; if (t.y >= 340) t.y = 340; setTimeout(() => { t.crushing = false; }, 700); } else if (t.y > t.startY) t.y -= 3; if (player.x < t.x + t.width && player.x + player.width > t.x && player.y < t.y + t.height && player.y + player.height > t.y) if (!player.starPower) triggerGameOver(); });
        fireBars.forEach(fb => { fb.angle += fb.speed; const tipX = fb.x + Math.cos(fb.angle) * fb.length; const tipY = fb.y + Math.sin(fb.angle) * fb.length; if (Math.hypot((player.x + player.width/2) - tipX, (player.y + player.height/2) - tipY) < 18) if (!player.starPower) triggerGameOver(); });
        hazards.forEach(h => { if (player.x + player.width > h.x && player.x < h.x + h.width && player.y + player.height > h.y && player.y < h.y + h.height) if (!player.starPower) triggerGameOver(); });

        powerUps.forEach(pw => { if (!pw.collected) { pw.vy += player.gravity; pw.y += pw.vy; platforms.forEach(platform => { if (pw.x < platform.x + platform.width && pw.x + 20 > platform.x && pw.y + 20 >= platform.y && pw.y + 20 - pw.vy <= platform.y + 14 && pw.vy >= 0) { pw.y = platform.y - 20; pw.vy = 0; } }); const dist = Math.hypot((pw.x + 10) - (player.x + player.width / 2), (pw.y + 10) - (player.y + player.height / 2)); if (dist < 24) { pw.collected = true; if (pw.type === 'mushroom') { player.poweredUp = true; player.height = 48; player.powerTimer = 500; activePowerups.push({ type: 'mushroom', timer: 500 }); score += 500; addFloatingText(player.x, player.y - 20, "+500 SUPER MUSHROOM!", "#2ecc71"); playSFX('powerup'); } else if (pw.type === 'fireflower') { player.poweredUp = true; player.hasFirePower = true; player.height = 48; player.powerTimer = 500; activePowerups.push({ type: 'fireflower', timer: 500 }); score += 500; addFloatingText(player.x, player.y - 20, "+500 FIRE FLOWER!", "#e74c3c"); playSFX('powerup'); } spawnParticles(player.x, player.y, '#2ecc71'); } } });

        enemies.forEach(enemy => { if (!enemy.alive) return; enemy.vy += player.gravity; enemy.y += enemy.vy; platforms.forEach(platform => { if (enemy.x < platform.x + platform.width && enemy.x + enemy.width > platform.x && enemy.y + enemy.height >= platform.y && enemy.y + enemy.height - enemy.vy <= platform.y + 14 && enemy.vy >= 0) { enemy.y = platform.y - enemy.height; enemy.vy = 0; } }); if (enemy.type === 'bullet') { enemy.x += enemy.vx; if (enemy.x < cameraX - 100) enemy.alive = false; } else enemy.x += enemy.vx; if (player.x < enemy.x + enemy.width && player.x + player.width > enemy.x && player.y < enemy.y + enemy.height && player.y + player.height > enemy.y) { if (player.starPower) { enemy.alive = false; score += 200 * comboMultiplier; coinsCollected += 1; sessionCoins++; sessionEnemies++; comboTimer = 120; comboMultiplier = Math.min(comboMultiplier + 1, 10); document.getElementById('hudMultiplier').innerText = comboMultiplier; addFloatingText(enemy.x, enemy.y - 15, "+200", "#f1c40f"); spawnParticles(enemy.x + 16, enemy.y + 16, '#f1c40f'); playSFX('stomp'); } else if (player.vy > 0 && player.y + player.height - player.vy <= enemy.y + 14) { enemy.alive = false; player.vy = -10; score += 200 * comboMultiplier; coinsCollected += 1; sessionCoins++; sessionEnemies++; comboTimer = 120; comboMultiplier = Math.min(comboMultiplier + 1, 10); document.getElementById('hudMultiplier').innerText = comboMultiplier; addFloatingText(enemy.x, enemy.y - 15, "+200", "#f1c40f"); spawnParticles(enemy.x + 16, enemy.y + 16, '#f1c40f'); playSFX('stomp'); } else triggerGameOver(); } });

        coins.forEach(coin => { if (!coin.collected) { const dist = Math.hypot(coin.x - (player.x + player.width / 2), coin.y - (player.y + player.height / 2)); if (dist < coin.radius + player.width / 3) { coin.collected = true; score += 250 * comboMultiplier; coinsCollected += 1; sessionCoins++; comboTimer = 120; comboMultiplier = Math.min(comboMultiplier + 1, 10); document.getElementById('hudMultiplier').innerText = comboMultiplier; addFloatingText(coin.x, coin.y - 15, "+250", "#f1c40f"); spawnParticles(coin.x, coin.y, '#f1c40f'); playSFX('coin'); } } });

        particles.forEach((p, index) => { p.x += p.vx; p.y += p.vy; p.life--; if (p.life <= 0) particles.splice(index, 1); });
        floatingTexts.forEach((ft, index) => { ft.y -= 0.8; ft.life--; if (ft.life <= 0) floatingTexts.splice(index, 1); });
        if (player.y > canvas.height + 80) triggerGameOver();

        if (platforms.length > 80 && platforms[0].x < cameraX - 1000) { platforms = platforms.filter(p => p.x + p.width > cameraX - 800); enemies = enemies.filter(e => e.x > cameraX - 800); coins = coins.filter(c => c.x > cameraX - 800); hazards = hazards.filter(h => h.x + h.width > cameraX - 800); movingPlatforms = movingPlatforms.filter(mp => mp.x + mp.width > cameraX - 800); thwomps = thwomps.filter(t => t.x > cameraX - 800); fireBars = fireBars.filter(fb => fb.x > cameraX - 800); powerUps = powerUps.filter(pw => pw.x > cameraX - 800); decorations = decorations.filter(d => d.x > cameraX - 800); fireballs = fireballs.filter(fb => fb.x > cameraX - 800); bossProjectiles = bossProjectiles.filter(bp => bp.x > cameraX - 800); }

        checkAchievements();
        document.getElementById('hudScore').innerText = score;
        document.getElementById('hudHighScore').innerText = highScore;
        document.getElementById('hudCoins').innerText = coinsCollected;
    }

    function drawPlayer(x, y, facing, h) { let shirtColor = '#e74c3c', overallColor = '#2980b9', hatColor = '#c0392b', skinTone = '#ffdbac'; if (selectedChar === 'luigi') { shirtColor = '#2ecc71'; hatColor = '#27ae60'; } else if (selectedChar === 'peach') { shirtColor = '#f39c12'; overallColor = '#e74c3c'; hatColor = '#f1c40f'; } else if (selectedChar === 'yoshi') { shirtColor = '#27ae60'; overallColor = '#ffffff'; hatColor = '#2ecc71'; } if (player.hasFirePower) { shirtColor = '#ffffff'; overallColor = '#e74c3c'; hatColor = '#e74c3c'; } if (player.starPower) { shirtColor = Math.random() > 0.5 ? '#f1c40f' : '#e74c3c'; overallColor = Math.random() > 0.5 ? '#2ecc71' : '#3498db'; } if (currentSkin === 'fire') { shirtColor = '#ffffff'; overallColor = '#e74c3c'; hatColor = '#e74c3c'; } else if (currentSkin === 'gold') { shirtColor = '#f1c40f'; overallColor = '#d4ac0d'; hatColor = '#f1c40f'; } else if (currentSkin === 'dark') { shirtColor = '#34495e'; overallColor = '#111111'; hatColor = '#2c3e50'; } else if (currentSkin === 'galaxy') { shirtColor = '#8e44ad'; overallColor = '#2c3e50'; hatColor = '#9b59b6'; } else if (currentSkin === 'rainbow') { shirtColor = Math.random() > 0.5 ? '#e74c3c' : '#3498db'; overallColor = '#f1c40f'; hatColor = '#2ecc71'; } ctx.fillStyle = 'rgba(0,0,0,0.3)'; ctx.fillRect(x + 3, y + h - 2, 26, 4); ctx.fillStyle = hatColor; ctx.fillRect(x + (facing === 'right' ? 7 : 5), y, 22, 9); ctx.fillStyle = skinTone; ctx.fillRect(x + (facing === 'right' ? 11 : 5), y + 9, 16, 9); ctx.fillStyle = '#000'; ctx.fillRect(x + (facing === 'right' ? 19 : 7), y + 11, 3, 4); ctx.fillRect(x + (facing === 'right' ? 13 : 11), y + 15, 8, 3); ctx.fillStyle = shirtColor; ctx.fillRect(x + 5, y + 18, 22, h > 32 ? 20 : 10); ctx.fillStyle = overallColor; ctx.fillRect(x + 8, y + 22, 16, h > 32 ? 14 : 6); ctx.fillStyle = '#f1c40f'; ctx.fillRect(x + 9, y + 23, 3, 3); ctx.fillRect(x + 20, y + 23, 3, 3); ctx.fillStyle = '#4a2306'; ctx.fillRect(x + (facing === 'right' ? 16 : 2), y + h - 4, 14, 4); }
    function drawGoomba(x, y) { ctx.fillStyle = '#78281f'; ctx.fillRect(x + 2, y + 8, 28, 20); ctx.fillStyle = '#f5cba7'; ctx.fillRect(x + 5, y + 12, 22, 10); ctx.fillStyle = '#000'; ctx.fillRect(x + 8, y + 15, 3, 5); ctx.fillRect(x + 21, y + 15, 3, 5); ctx.fillStyle = '#512e5f'; ctx.fillRect(x, y + 28, 12, 4); ctx.fillRect(x + 20, y + 28, 12, 4); }
    function drawKoopa(x, y) { ctx.fillStyle = '#27ae60'; ctx.fillRect(x + 4, y + 4, 24, 24); ctx.fillStyle = '#f1c40f'; ctx.fillRect(x + 8, y + 8, 16, 14); ctx.fillStyle = '#000'; ctx.fillRect(x + 10, y + 10, 4, 4); ctx.fillRect(x + 18, y + 10, 4, 4); }
    function drawBulletBill(x, y) { ctx.fillStyle = '#2c3e50'; ctx.fillRect(x, y + 4, 32, 20); ctx.fillStyle = '#fff'; ctx.fillRect(x + 4, y + 8, 8, 8); ctx.fillStyle = '#e74c3c'; ctx.fillRect(x + 6, y + 10, 4, 4); }
    function drawBoss(x, y) { ctx.fillStyle = bossPhase === 3 ? '#ff0000' : (bossPhase === 2 ? '#e74c3c' : '#b03a2e'); ctx.fillRect(x, y, 48, 48); ctx.fillStyle = '#f1c40f'; ctx.fillRect(x + 6, y + 10, 10, 10); ctx.fillRect(x + 32, y + 10, 10, 10); ctx.fillStyle = '#ffffff'; ctx.fillRect(x + 12, y + 36, 24, 6); ctx.fillStyle = '#000'; ctx.fillRect(x - 10, y - 16, 68, 8); ctx.fillStyle = '#2ecc71'; ctx.fillRect(x - 8, y - 14, (bossHp / (100 + currentWorld * 20)) * 64, 4); }
    function drawThwomp(x, y) { ctx.fillStyle = '#34495e'; ctx.fillRect(x, y, 40, 40); ctx.strokeStyle = '#1b2631'; ctx.lineWidth = 3; ctx.strokeRect(x, y, 40, 40); ctx.fillStyle = '#e74c3c'; ctx.fillRect(x + 5, y + 10, 10, 6); ctx.fillRect(x + 25, y + 10, 10, 6); ctx.fillStyle = '#ffffff'; ctx.fillRect(x + 8, y + 26, 24, 6); }

    function draw() { ctx.clearRect(0, 0, canvas.width, canvas.height); ctx.save(); ctx.translate(Math.floor(-cameraX), 0); decorations.forEach(dec => { if (dec.type === 'cloud') { ctx.fillStyle = "rgba(255, 255, 255, 0.85)"; ctx.fillRect(dec.x, dec.y, 75, 22); ctx.fillRect(dec.x + 20, dec.y - 15, 35, 16); } else if (dec.type === 'bush') { ctx.fillStyle = currentTheme === 'neon' ? '#00ffcc' : '#1e8449'; ctx.fillRect(dec.x, dec.y, 95, 32); } else if (dec.type === 'castle') { ctx.fillStyle = '#566573'; ctx.fillRect(dec.x, dec.y - 30, 80, 62); } }); platforms.forEach(platform => { if (platform.x + platform.width >= cameraX - 100 && platform.x <= cameraX + canvas.width + 100) { if (platform.type === 'ground') { ctx.fillStyle = currentTheme === 'midnight' ? '#1b4f72' : (currentTheme === 'neon' ? '#8e44ad' : '#a04000'); ctx.fillRect(platform.x, platform.y, platform.width, platform.height + 250); ctx.fillStyle = currentTheme === 'neon' ? '#00ffff' : '#27ae60'; ctx.fillRect(platform.x, platform.y, platform.width, 10); } else if (platform.type === 'ice') { ctx.fillStyle = '#5499c7'; ctx.fillRect(platform.x, platform.y, platform.width, platform.height + 250); } else if (platform.type === 'quicksand') { ctx.fillStyle = '#9a7d0a'; ctx.fillRect(platform.x, platform.y, platform.width, platform.height + 250); } else if (platform.type === 'brick') { ctx.fillStyle = '#b03a2e'; ctx.fillRect(platform.x, platform.y, platform.width, platform.height); } else if (platform.type === 'question') { ctx.fillStyle = '#d4ac0d'; ctx.fillRect(platform.x, platform.y, platform.width, platform.height); ctx.fillStyle = '#ffffff'; ctx.font = "bold 20px 'Courier New'"; ctx.fillText("?", platform.x + 9, platform.y + 24); } else if (platform.type === 'pipe') { ctx.fillStyle = '#27ae60'; ctx.fillRect(platform.x, platform.y, platform.width, platform.height); ctx.fillRect(platform.x - 4, platform.y, platform.width + 8, 16); } } }); movingPlatforms.forEach(mp => { ctx.fillStyle = '#8e44ad'; ctx.fillRect(mp.x, mp.y, mp.width, mp.height); }); hazards.forEach(h => { if (h.type === 'lava') { ctx.fillStyle = '#c0392b'; ctx.fillRect(h.x, h.y, h.width, h.height); } else if (h.type === 'spikes') { ctx.fillStyle = '#7f8c8d'; for (let sx = h.x; sx < h.x + h.width; sx += 16) { ctx.beginPath(); ctx.moveTo(sx, h.y + h.height); ctx.lineTo(sx + 8, h.y); ctx.lineTo(sx + 16, h.y + h.height); ctx.fill(); } } }); fireBars.forEach(fb => { ctx.fillStyle = '#7f8c8d'; ctx.beginPath(); ctx.arc(fb.x, fb.y, 6, 0, Math.PI * 2); ctx.fill(); for (let r = 12; r <= fb.length; r += 14) { const px = fb.x + Math.cos(fb.angle) * r; const py = fb.y + Math.sin(fb.angle) * r; ctx.fillStyle = '#e67e22'; ctx.beginPath(); ctx.arc(px, py, 6, 0, Math.PI * 2); ctx.fill(); } }); thwomps.forEach(t => { drawThwomp(t.x, t.y); }); if (bossActive) drawBoss(bossX, bossY); enemies.forEach(enemy => { if (enemy.alive) { if (enemy.type === 'koopa') drawKoopa(enemy.x, enemy.y); else if (enemy.type === 'bullet') drawBulletBill(enemy.x, enemy.y); else drawGoomba(enemy.x, enemy.y); } }); powerUps.forEach(pw => { if (!pw.collected) { if (pw.type === 'mushroom') { ctx.fillStyle = '#e74c3c'; ctx.fillRect(pw.x, pw.y, 20, 20); ctx.fillStyle = '#fff'; ctx.fillRect(pw.x + 4, pw.y + 4, 4, 4); ctx.fillRect(pw.x + 12, pw.y + 4, 4, 4); } else if (pw.type === 'fireflower') { ctx.fillStyle = '#e74c3c'; ctx.beginPath(); ctx.arc(pw.x + 10, pw.y + 10, 10, 0, Math.PI * 2); ctx.fill(); ctx.fillStyle = '#f1c40f'; ctx.beginPath(); ctx.arc(pw.x + 10, pw.y + 10, 5, 0, Math.PI * 2); ctx.fill(); } } }); fireballs.forEach(fb => { ctx.fillStyle = '#e74c3c'; ctx.beginPath(); ctx.arc(fb.x + 4, fb.y + 4, 6, 0, Math.PI * 2); ctx.fill(); }); bossProjectiles.forEach(bp => { ctx.fillStyle = '#ff0000'; ctx.beginPath(); ctx.arc(bp.x, bp.y, 6, 0, Math.PI * 2); ctx.fill(); }); coins.forEach(coin => { if (!coin.collected) { ctx.fillStyle = '#f1c40f'; ctx.beginPath(); ctx.arc(coin.x, coin.y, coin.radius, 0, Math.PI * 2); ctx.fill(); ctx.fillStyle = '#f39c12'; ctx.beginPath(); ctx.arc(coin.x, coin.y, coin.radius - 3, 0, Math.PI * 2); ctx.fill(); } }); particles.forEach(p => { ctx.fillStyle = p.color; ctx.fillRect(p.x, p.y, 4, 4); }); floatingTexts.forEach(ft => { ctx.fillStyle = ft.color; ctx.font = "bold 13px 'Courier New'"; ctx.fillText(ft.text, ft.x, ft.y); }); if (!gameOver) drawPlayer(player.x, player.y, player.facing, player.height); ctx.restore(); }
    function gameLoop() { update(); draw(); requestAnimationFrame(gameLoop); }
    requestAnimationFrame(gameLoop);
</script>
</body>
</html>"""

st.components.v1.html(game_html, height=540, scrolling=False)
