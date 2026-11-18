# -*- coding: utf-8 -*-
"""
Generator za nadograđenu verziju:
- Boja temeljena na udžbeniku Alfa (I. DOBA PROSVJETITELJSTVA - #60AA75 i #478B5C)
- Dark Mode i Light Mode s trenutnim prebacivanjem (☀️ / 🌙)
- Pucanj topa (period cannon blast) za točan odgovor
- Zvuk sudara sablji/mačeva (period sword clash) za netočan odgovor
- Kraljevska salva i fanfara za rijetke odgovore (>1200 km)
- Karta s realističnim geografskim obalama Europe i Hrvatske, ružom vjetrova i kartušom
"""

import json

with open('dokle_games_bilingual.json', 'r', encoding='utf-8') as f:
    games_json = f.read()

HTML_CONTENT = r'''<!DOCTYPE html>
<html lang="hr" class="theme-dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <meta name="referrer" content="no-referrer">
  <meta name="theme-color" content="#1a3b24">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="format-detection" content="telephone=no">

  <title>Povijesni Dokle? – Doba prosvjetiteljstva (Povijest 3, Alfa)</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Cinzel:wght@600;700;800;900&family=JetBrains+Mono:wght@500;700&display=swap');
    
    :root {
      --app-height: 100dvh;
      /* Boje iz udžbenika Alfa (Povijest 3, cjelina I) */
      --alfa-green: #60AA75;
      --alfa-dark-green: #478B5C;
      --alfa-deep: #1e4028;
      --alfa-tint: #eaf4ed;
    }

    * {
      box-sizing: border-box;
      -webkit-tap-highlight-color: transparent;
    }

    /* TEMA: DARK MODE (Zeleno-šumski prosvjetiteljski stil) */
    html.theme-dark body {
      background: radial-gradient(circle at 50% 15%, #0f2417 0%, #06110a 100%);
      color: #f1f7f3;
    }
    html.theme-dark .bg-surface {
      background-color: rgba(15, 36, 23, 0.92);
      border-color: rgba(35, 74, 51, 0.8);
    }
    html.theme-dark .bg-card-inner {
      background-color: rgba(6, 17, 10, 0.7);
      border-color: rgba(35, 74, 51, 0.6);
    }
    html.theme-dark .text-muted {
      color: #94b8a0;
    }

    /* TEMA: LIGHT MODE (Udžbenička stranica – čisto, svijetlo s zelenim vrpcama) */
    html.theme-light body {
      background: #f4f8f5;
      color: #1e293b;
    }
    html.theme-light .bg-surface {
      background-color: #ffffff;
      border-color: #d1e5d7;
      box-shadow: 0 4px 20px rgba(96, 170, 117, 0.08);
    }
    html.theme-light .bg-card-inner {
      background-color: #f8fbf9;
      border-color: #e2ebe4;
    }
    html.theme-light .text-muted {
      color: #475569;
    }
    html.theme-light .text-white {
      color: #0f172a !important;
    }
    html.theme-light .map-container {
      background: #e6f0ea;
      border-color: #c5dfce;
      box-shadow: inset 0 0 30px rgba(96, 170, 117, 0.15);
    }
    html.theme-light .map-land {
      fill: #f4f8f5;
      stroke: #60aa75;
    }
    html.theme-light .map-water {
      fill: #d5ecdc;
    }
    html.theme-light .map-route {
      stroke: #2d633d;
    }
    html.theme-light #cityInfoBadge {
      background-color: rgba(255, 255, 255, 0.96);
      border-color: #60aa75;
      color: #0f172a;
    }
    html.theme-light #cityInfoBadge p {
      color: #334155 !important;
    }

    body {
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      min-height: 100vh;
      min-height: var(--app-height);
      overflow-x: hidden;
      touch-action: manipulation;
      padding-top: max(8px, env(safe-area-inset-top));
      padding-bottom: max(16px, env(safe-area-inset-bottom));
      padding-left: max(8px, env(safe-area-inset-left));
      padding-right: max(8px, env(safe-area-inset-right));
      transition: background 0.3s ease, color 0.3s ease;
    }

    .font-serif-title {
      font-family: 'Cinzel', Georgia, serif;
    }

    .font-mono-num {
      font-family: 'JetBrains Mono', monospace;
    }

    /* Karta */
    .map-container {
      position: relative;
      background: #091712;
      border: 1px solid #1d422a;
      border-radius: 1rem;
      overflow: hidden;
      box-shadow: inset 0 0 30px rgba(0,0,0,0.6), 0 8px 20px -5px rgba(0,0,0,0.4);
    }

    .map-water {
      fill: #061510;
    }
    .map-land {
      fill: #0f2619;
      stroke: #235234;
      stroke-width: 1.2;
    }

    .route-path {
      stroke: #60aa75;
      stroke-width: 2.5;
      stroke-dasharray: 6 6;
      animation: dashMove 30s linear infinite;
    }

    .active-route {
      stroke: #ffd700;
      stroke-width: 3.5;
      filter: drop-shadow(0 0 8px rgba(255, 215, 0, 0.8));
      transition: stroke-dashoffset 1.5s ease-in-out;
    }

    @keyframes dashMove {
      to { stroke-dashoffset: -100; }
    }

    .city-node {
      cursor: pointer;
      transition: transform 0.3s ease, filter 0.3s ease;
    }
    .city-node:hover, .city-node:active {
      transform: scale(1.4);
      filter: drop-shadow(0 0 10px #ffd700);
    }

    .traveler-pin {
      transition: all 1.2s cubic-bezier(0.34, 1.56, 0.64, 1);
    }

    .timer-critical {
      animation: pulseAlert 0.7s infinite alternate;
    }
    @keyframes pulseAlert {
      from { transform: scale(1); box-shadow: 0 0 8px rgba(239, 68, 68, 0.5); }
      to { transform: scale(1.08); box-shadow: 0 0 20px rgba(239, 68, 68, 0.9); }
    }

    .shake-anim {
      animation: shake 0.4s cubic-bezier(.36,.07,.19,.97) both;
    }
    @keyframes shake {
      10%, 90% { transform: translate3d(-2px, 0, 0); }
      20%, 80% { transform: translate3d(4px, 0, 0); }
      30%, 50%, 70% { transform: translate3d(-5px, 0, 0); }
      40%, 60% { transform: translate3d(5px, 0, 0); }
    }

    .rare-glow {
      animation: goldGlow 1.2s ease-out;
    }
    @keyframes goldGlow {
      0% { box-shadow: 0 0 0px #60aa75; }
      50% { box-shadow: 0 0 30px #60aa75; }
      100% { box-shadow: 0 0 10px rgba(96, 170, 117, 0.2); }
    }

    details > summary {
      list-style: none;
      cursor: pointer;
    }
    details > summary::-webkit-details-marker {
      display: none;
    }

    /* ================================================================= */
    /* RESPONSIVE DIZAJN & FORMATIRANJE NA RAZLIČITIM VELIČINAMA EKRANA  */
    /* ================================================================= */

    /* Okvir za unos odgovora - iznimno prilagodljiv na svim uređajima */
    .dokle-answer-container {
      display: flex;
      flex-direction: row;
      align-items: center;
      gap: 0.5rem;
      width: 100%;
    }

    .dokle-input-wrapper {
      position: relative;
      flex: 1 1 auto;
      min-width: 0;
    }

    .dokle-answer-input {
      width: 100%;
      height: 48px;
      font-size: 16px !important; /* Sprječava automatski iOS zoom */
      font-weight: 600;
      border-radius: 0.875rem;
      padding: 0.625rem 2.25rem 0.625rem 0.875rem;
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
      outline: none;
      font-family: inherit;
      -webkit-appearance: none;
    }

    @media (min-width: 640px) {
      .dokle-answer-input {
        height: 52px;
        padding-left: 1.125rem;
        padding-right: 2.75rem;
        font-size: 17px !important;
        border-radius: 1rem;
      }
    }

    /* Dark Mode: okvir unosa */
    html.theme-dark .dokle-answer-input {
      background-color: rgba(6, 20, 12, 0.9);
      color: #ffffff;
      border: 2px solid rgba(96, 170, 117, 0.5);
      box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.4);
    }
    html.theme-dark .dokle-answer-input::placeholder {
      color: #72967e;
      font-weight: 400;
    }
    html.theme-dark .dokle-answer-input:focus {
      border-color: #60aa75;
      box-shadow: 0 0 0 3px rgba(96, 170, 117, 0.35), inset 0 1px 2px rgba(0, 0, 0, 0.3);
      background-color: rgba(8, 26, 16, 0.98);
    }

    /* Light Mode: okvir unosa */
    html.theme-light .dokle-answer-input {
      background-color: #ffffff;
      color: #0f172a;
      border: 2px solid #60aa75;
      box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05), 0 2px 6px rgba(96, 170, 117, 0.1);
    }
    html.theme-light .dokle-answer-input::placeholder {
      color: #64748b;
      font-weight: 400;
    }
    html.theme-light .dokle-answer-input:focus {
      border-color: #2d633d;
      box-shadow: 0 0 0 3px rgba(45, 99, 61, 0.25), inset 0 1px 2px rgba(0, 0, 0, 0.05);
      background-color: #ffffff;
    }

    /* Dugme za brisanje (Clear ✖) */
    .dokle-clear-btn {
      position: absolute;
      right: 0.5rem;
      top: 50%;
      transform: translateY(-50%);
      width: 26px;
      height: 26px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 12px;
      font-weight: bold;
      cursor: pointer;
      border: none;
      background: rgba(148, 184, 160, 0.25);
      color: #94b8a0;
      transition: all 0.15s ease;
      padding: 0;
      z-index: 10;
    }
    @media (min-width: 640px) {
      .dokle-clear-btn {
        right: 0.75rem;
        width: 28px;
        height: 28px;
        font-size: 13px;
      }
    }
    .dokle-clear-btn:hover {
      background: rgba(239, 68, 68, 0.35);
      color: #fca5a5;
    }
    html.theme-light .dokle-clear-btn {
      background: rgba(100, 116, 139, 0.15);
      color: #64748b;
    }

    /* Gumb za potvrdu odgovora */
    .dokle-submit-btn {
      height: 48px;
      padding: 0 0.875rem;
      border-radius: 0.875rem;
      font-weight: 800;
      font-size: 0.8125rem;
      letter-spacing: 0.025em;
      white-space: nowrap;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 0.35rem;
      flex-shrink: 0;
      cursor: pointer;
      border: none;
      background: linear-gradient(135deg, #478b5c 0%, #60aa75 100%);
      color: #ffffff !important;
      box-shadow: 0 4px 12px rgba(71, 139, 92, 0.35);
      transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
    }
    @media (min-width: 640px) {
      .dokle-submit-btn {
        height: 52px;
        padding: 0 1.25rem;
        font-size: 0.875rem;
        border-radius: 1rem;
      }
    }
    .dokle-submit-btn:hover:not(:disabled) {
      background: linear-gradient(135deg, #3d774f 0%, #529465 100%);
      box-shadow: 0 6px 16px rgba(71, 139, 92, 0.45);
      transform: translateY(-1px);
    }
    .dokle-submit-btn:active:not(:disabled) {
      transform: scale(0.96);
    }
    .dokle-submit-btn:disabled {
      opacity: 0.55;
      cursor: not-allowed;
      filter: grayscale(0.5);
      transform: none;
    }

    /* Inputi za modalne prozore (Ime, Lozinka) */
    .dokle-modal-input {
      width: 100%;
      height: 48px;
      font-size: 16px !important;
      font-weight: 500;
      border-radius: 0.75rem;
      padding: 0.625rem 1rem;
      transition: all 0.2s ease;
      outline: none;
    }
    html.theme-dark .dokle-modal-input {
      background-color: rgba(6, 17, 10, 0.85);
      color: #ffffff;
      border: 2px solid rgba(96, 170, 117, 0.4);
    }
    html.theme-dark .dokle-modal-input:focus {
      border-color: #60aa75;
      box-shadow: 0 0 0 3px rgba(96, 170, 117, 0.3);
    }
    html.theme-light .dokle-modal-input {
      background-color: #ffffff;
      color: #0f172a;
      border: 2px solid #60aa75;
    }
    html.theme-light .dokle-modal-input:focus {
      border-color: #2d633d;
      box-shadow: 0 0 0 3px rgba(45, 99, 61, 0.2);
    }

    /* Prilagodbe za male ekrane (mobiteli < 640px) */
    @media (max-width: 639px) {
      #europeMapSvg {
        max-height: 180px;
      }
      .map-container {
        border-radius: 0.75rem;
      }
      /* U vodoravnom prikazu na mobitelu smanji kartu radi unosa odgovora */
      @media (orientation: landscape) and (max-height: 480px) {
        #mapViewport {
          height: 60px !important;
        }
      }
    }

    /* Sprječavanje prelijevanja tablica na uskim ekranima */
    .table-responsive {
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
    }

    input[type="text"], input[type="email"], input[type="password"] {
      font-size: 16px !important;
    }
  </style>
</head>
<body class="p-2 sm:p-4 md:p-6 flex flex-col justify-between">

  <!-- GLAVNI KONTEJNER -->
  <div class="max-w-6xl mx-auto w-full space-y-4 md:space-y-6">

    <!-- TOP BAR SA ZELENIM UĐBENIČKIM AKCENTOM -->
    <header class="bg-surface backdrop-blur-md rounded-2xl p-3 sm:p-5 shadow-xl flex items-center justify-between gap-2 border">
      <!-- LOGO & NASLOV S TIPKOM POČETNA -->
      <div class="flex items-center space-x-2.5 sm:space-x-3 min-w-0">
        <button onclick="returnToHome()" title="Povratak na početnu stranicu / izbor modula" 
                class="w-10 h-10 sm:w-12 sm:h-12 rounded-xl bg-gradient-to-tr from-[#2d633d] to-[#60aa75] hover:opacity-90 flex items-center justify-center text-xl sm:text-2xl shadow-lg shadow-[#60aa75]/25 shrink-0 text-white font-serif-title font-bold transition active:scale-95">
          🏠
        </button>
        <div class="w-10 h-10 sm:w-12 sm:h-12 rounded-xl bg-gradient-to-tr from-[#2d633d] to-[#60aa75] flex items-center justify-center text-xl sm:text-2xl shadow-lg shadow-[#60aa75]/25 shrink-0 text-white font-serif-title font-bold">
          I.
        </div>
        <div class="min-w-0">
          <h1 class="text-base sm:text-xl md:text-2xl font-serif-title font-bold tracking-tight text-white flex items-center gap-1.5 truncate">
            <span class="truncate">Povijesni Dokle?</span>
            <span class="text-[10px] sm:text-xs font-mono-num font-normal px-2 py-0.5 rounded-full bg-[#60aa75]/20 text-[#60aa75] border border-[#60aa75]/30 hidden xs:inline shrink-0 font-bold">
              Alfa · 3. r
            </span>
          </h1>
          <p class="text-[10px] sm:text-xs text-muted truncate" id="headerSubtitle">
            Gimnazijski kurikulum (Prosvjetiteljstvo) & Dan sjećanja (Vukovar i Škabrnja)
          </p>
        </div>
      </div>

      <!-- KONTROLE: POČETNA, DARK/LIGHT, SKRIPTA, ZVUK, JEZIK, PROFIL, NASTAVNIK -->
      <div class="flex items-center gap-1.5 sm:gap-2 shrink-0">
        <!-- Dugme Početna -->
        <button onclick="returnToHome()" title="Povratak na izbor kvizova i modula"
                class="px-2.5 py-2 sm:px-3 sm:py-2 bg-[#60aa75]/20 hover:bg-[#60aa75]/30 text-[#60aa75] rounded-xl text-xs font-bold border border-[#60aa75]/40 flex items-center gap-1.5 transition active:scale-95 min-h-[38px]">
          <span>🏠</span>
          <span class="hidden md:inline">Početna</span>
        </button>
        <!-- Prekidač Dark / Light Mode -->
        <button id="themeToggleBtn" onclick="toggleTheme()" title="Promijeni temu (Svijetlo / Tamno)"
                class="p-2 sm:px-3 sm:py-2 bg-surface hover:border-[#60aa75] rounded-xl text-xs font-semibold border flex items-center gap-1 transition active:scale-95 min-h-[38px] min-w-[38px] justify-center">
          <span id="themeIcon">☀️</span>
        </button>

        <!-- Dugme za Skriptu -->
        <button id="viewToggleBtn" onclick="toggleMainView()" 
                class="px-2.5 py-2 sm:px-3 sm:py-2 bg-[#60aa75]/20 hover:bg-[#60aa75]/30 text-[#60aa75] rounded-xl text-xs font-bold border border-[#60aa75]/40 flex items-center gap-1.5 transition active:scale-95 min-h-[38px]">
          <span id="viewToggleIcon">📖</span>
          <span id="viewToggleLabel" class="font-bold">Skripta</span>
        </button>

        <!-- Zvuk (Top / Sablja / Ticking) -->
        <button id="soundToggleBtn" onclick="toggleAudio()" title="Uključi/isključi zvuk"
                class="p-2 sm:px-3 sm:py-2 bg-surface hover:border-[#60aa75] rounded-xl text-xs font-semibold border flex items-center gap-1 transition active:scale-95 min-h-[38px] min-w-[38px] justify-center">
          <span id="soundIcon">🔊</span>
          <span id="soundLabel" class="hidden md:inline">Zvuk</span>
        </button>

        <!-- Jezik HR / EN -->
        <button id="langToggleBtn" onclick="toggleLanguage()" title="Promijeni jezik"
                class="px-2.5 py-2 sm:px-3 sm:py-2 bg-[#60aa75]/15 hover:bg-[#60aa75]/25 text-[#60aa75] rounded-xl text-xs font-bold border border-[#60aa75]/30 flex items-center gap-1 transition active:scale-95 min-h-[38px]">
          <span id="langFlag">🇭🇷</span>
          <span id="langLabel" class="text-[11px] font-mono-num font-bold">HR</span>
        </button>

        <!-- Profil Učenika (klik za odjavu / promjenu profila) -->
        <div id="userBadge" onclick="handleLogout()" title="Kliknite za promjenu učenika / odjavu"
             class="hidden items-center gap-1.5 px-2.5 py-1.5 bg-[#60aa75]/20 hover:bg-[#60aa75]/30 cursor-pointer border border-[#60aa75]/50 rounded-xl text-xs max-w-[120px] sm:max-w-none transition">
          <span class="w-2 h-2 rounded-full bg-[#60aa75] animate-pulse shrink-0"></span>
          <span id="userDisplayName" class="font-bold text-[#60aa75] truncate text-[11px]">Učenik</span>
        </div>

        <button id="loginBtn" onclick="openLoginModal()"
                class="px-3 py-2 bg-[#478b5c] hover:bg-[#3d774f] text-white rounded-xl text-xs font-bold transition shadow-lg shadow-[#478b5c]/30 active:scale-95 min-h-[38px] flex items-center gap-1">
          <span>👤</span>
          <span id="loginBtnText" class="hidden sm:inline">Prijava</span>
        </button>

        <!-- Nastavnik -->
        <button onclick="openTeacherModal()" title="Nastavnički portal"
                class="p-2 sm:px-3 sm:py-2 bg-surface hover:border-[#60aa75] rounded-xl text-xs font-semibold border transition active:scale-95 min-h-[38px] min-w-[38px] flex items-center justify-center">
          <span>⚙️</span>
        </button>
      </div>
    </header>

    <!-- OBAVIJEST O PRAVILIMA ZA OCJENU (U STILU UDŽBENIKA) -->
    <div id="gradingNotice" class="bg-surface border-l-4 border-[#60aa75] rounded-xl p-3 text-[11px] sm:text-xs text-muted flex items-start gap-2.5 shadow-md border">
      <span class="text-base sm:text-lg shrink-0 text-[#60aa75]">📖</span>
      <div class="space-y-0.5 min-w-0">
        <strong class="text-[#60aa75] block font-bold" id="gradingNoticeTitle">Nastavna cjelina I: Doba prosvjetiteljstva</strong>
        <p id="gradingNoticeBody" class="leading-relaxed">
          Igra i skripta usklađeni su s udžbenikom <em>Povijest 3 (Alfa, str. 12–21)</em>. Za ocjenu je obvezan unos <strong>stvarnoga imena</strong>. Rezultati se svaka 24h šalju profesoru na ocjenjivanje i trajno brišu iz baze radi zaštite podataka.
        </p>
      </div>
    </div>

    <!-- GLAVNI POGLEDI -->
    <main class="space-y-4 md:space-y-6">

      <!-- ============================================================== -->
      <!-- SKRIPTA ZA PONAVLJANJE GRADIVA                                 -->
      <!-- ============================================================== -->
      <section id="studySection" class="hidden space-y-4 sm:space-y-5">
        <div class="bg-surface rounded-2xl p-4 sm:p-7 shadow-xl space-y-3 border">
          <!-- GORNJA NAVIGACIJA SKRIPTE -->
          <div class="flex items-center justify-between gap-2 border-b pb-3 mb-2 flex-wrap">
            <button onclick="returnToHome()" class="px-3.5 py-2 bg-card-inner hover:border-[#60aa75] rounded-xl text-xs font-bold border flex items-center gap-1.5 transition text-muted hover:text-white">
              <span>🏠</span> <span>Početna</span>
            </button>
            <div class="flex items-center gap-1.5 overflow-x-auto text-xs">
              <button onclick="filterStudyScript('all')" id="studyTabAll" class="study-tab-btn active px-3 py-1.5 rounded-xl font-bold bg-[#60aa75] text-white">Sve lekcije (1–8)</button>
              <button onclick="filterStudyScript('enlightenment')" id="studyTabEnl" class="study-tab-btn px-3 py-1.5 rounded-xl font-bold bg-card-inner text-muted hover:text-white border">🏛️ Prosvjetiteljstvo</button>
              <button onclick="filterStudyScript('vukovar')" id="studyTabVuk" class="study-tab-btn px-3 py-1.5 rounded-xl font-bold bg-card-inner text-muted hover:text-white border">🕯️ Vukovar & Škabrnja</button>
            </div>
            <button onclick="switchToGameLobby()" class="px-4 py-2 bg-[#478b5c] hover:bg-[#3d774f] text-white font-bold rounded-xl text-xs flex items-center gap-1.5 shadow">
              <span>🎮 Kviz</span> <span>➔</span>
            </button>
          </div>

          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b pb-4 border-slate-700/40">
            <div>
              <span class="text-xs uppercase font-mono-num font-bold text-[#60aa75] tracking-wider">
                NASTAVNA SKRIPTA ZA UČENIKE · POVIJEST 3 (ALFA, STR. 12–21)
              </span>
              <h2 class="text-xl sm:text-2xl font-serif-title font-bold text-white mt-1">
                Od apsolutizma do prosvjetiteljstva i novih gospodarskih ideja
              </h2>
              <p class="text-xs text-muted mt-0.5">
                Pomoć za učenje i ponavljanje prije igranja kviza „Povijesni Dokle?”.
              </p>
            </div>
            <button onclick="switchToGameLobby()" class="px-5 py-2.5 bg-[#478b5c] hover:bg-[#3d774f] text-white font-black rounded-xl text-xs transition shadow-lg shadow-[#478b5c]/30 shrink-0 flex items-center gap-1.5 self-start sm:self-center">
              <span>🎮 KRENI NA KVIZ</span>
              <span>➔</span>
            </button>
          </div>

          <div class="p-3 bg-[#60aa75]/15 border border-[#60aa75]/40 rounded-xl text-xs text-[#60aa75] font-semibold leading-relaxed">
            💡 <strong>Uputa za učenje:</strong> Pročitaj lekcije, ponovi kronologiju i pojmove te provjeri ishode pri dnu stranice.
          </div>
        </div>

        <div class="space-y-3">
          <details class="group bg-surface rounded-2xl overflow-hidden transition border" open>
            <summary class="p-4 sm:p-5 flex items-center justify-between bg-card-inner font-bold text-sm sm:text-base text-slate-200">
              <span class="flex items-center gap-2">
                <span class="w-6 h-6 rounded-lg bg-[#60aa75]/20 text-[#60aa75] flex items-center justify-center font-mono-num text-xs font-bold">1</span>
                Kako nastaje snažnija država ranoga novog vijeka?
              </span>
              <span class="text-[#60aa75] group-open:rotate-180 transition-transform">▼</span>
            </summary>
            <div class="p-4 sm:p-6 text-xs sm:text-sm text-muted space-y-3 border-t leading-relaxed border-slate-700/30">
              <p>Od 16. stoljeća u europskim državama jačaju centralizacija, stalniji prihodi i plaćene državne službe.</p>
              <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse text-xs">
                  <tbody class="divide-y divide-slate-700/30">
                    <tr><td class="p-2 font-bold text-[#60aa75]">Društveni:</td><td class="p-2">Jačanje gradova i trgovaca, složenije društvo.</td></tr>
                    <tr><td class="p-2 font-bold text-[#60aa75]">Ekonomski:</td><td class="p-2">Novčana privreda, trgovina, ubiranje poreza.</td></tr>
                    <tr><td class="p-2 font-bold text-[#60aa75]">Demografski:</td><td class="p-2">Rast stanovništva, više poreznih obveznika i vojnika.</td></tr>
                    <tr><td class="p-2 font-bold text-[#60aa75]">Tehnološki:</td><td class="p-2">Vatreno oružje, topništvo, tiskarstvo, utvrde.</td></tr>
                  </tbody>
                </table>
              </div>
              <p><strong>Vestfalski mir (1648.):</strong> završetak Tridesetogodišnjeg rata.<br>
              <strong>Nikola Vitov Gučetić (1549.–1610.):</strong> dubrovački mislilac, autor djela <em>O ustroju država u Aristotelovu duhu</em> (1591.).</p>
            </div>
          </details>

          <details class="group bg-surface rounded-2xl overflow-hidden transition border">
            <summary class="p-4 sm:p-5 flex items-center justify-between bg-card-inner font-bold text-sm sm:text-base text-slate-200">
              <span class="flex items-center gap-2">
                <span class="w-6 h-6 rounded-lg bg-[#60aa75]/20 text-[#60aa75] flex items-center justify-center font-mono-num text-xs font-bold">2</span>
                Apsolutizam, suverenitet i prirodno pravo
              </span>
              <span class="text-[#60aa75] group-open:rotate-180 transition-transform">▼</span>
            </summary>
            <div class="p-4 sm:p-6 text-xs sm:text-sm text-muted space-y-3 border-t leading-relaxed border-slate-700/30">
              <div class="my-3 p-3 bg-card-inner rounded-2xl border max-w-sm mx-auto sm:mx-0 shadow-md">
                <img src="assets/udzbenik_povijest3_cjelina1.jpg"
                     data-fallback="udzbenik_povijest3_cjelina1.jpg"
                     alt="Udžbenik Povijest 3 – Cjelina I: Doba prosvjetiteljstva"
                     class="w-full h-44 object-cover object-top rounded-xl"
                     loading="lazy" onerror="handleImgError(this, 'textbook')" />
                <p class="text-[10px] text-muted mt-1.5 italic text-center leading-snug">
                  Udžbenik Povijest 3 (Alfa d.d.) – Cjelina I (str. 10–11)<br>
                  <span class="opacity-75">Palača Sanssouci u Potsdamu – ishodi učenja cjeline</span>
                </p>
              </div>
              <p><strong>Luj XIV.:</strong> „Država to sam ja” – apsolutistička monarhija.<br>
              <strong>Niccolò Machiavelli:</strong> <em>Vladar</em> (1513./1532.) – stabilnost vlasti i politička djelotvornost.<br>
              <strong>Jean Bodin:</strong> <em>Šest knjiga o republici</em> (1576.) – pojam suvereniteta.<br>
              <strong>Thomas Hobbes:</strong> <em>Levijatan</em> (1651.) – društveni ugovor radi reda i sigurnosti.<br>
              <strong>John Locke:</strong> <em>Dvije rasprave o vladavini</em> (1689./1690.) – prirodna prava na život, slobodu i vlasništvo.</p>
            </div>
          </details>

          <details class="group bg-surface rounded-2xl overflow-hidden transition border">
            <summary class="p-4 sm:p-5 flex items-center justify-between bg-card-inner font-bold text-sm sm:text-base text-slate-200">
              <span class="flex items-center gap-2">
                <span class="w-6 h-6 rounded-lg bg-[#60aa75]/20 text-[#60aa75] flex items-center justify-center font-mono-num text-xs font-bold">3</span>
                Prosvjetiteljstvo: razum, prava i ograničenje vlasti
              </span>
              <span class="text-[#60aa75] group-open:rotate-180 transition-transform">▼</span>
            </summary>
            <div class="p-4 sm:p-6 text-xs sm:text-sm text-muted space-y-3 border-t leading-relaxed border-slate-700/30">
              <p><strong>Montesquieu:</strong> <em>O duhu zakona</em> (1748.) – dioba vlasti na zakonodavnu, izvršnu i sudbenu.<br>
              <strong>Jean-Jacques Rousseau:</strong> <em>Društveni ugovor</em> (1762.) – pojam opće volje i narodni suverenitet.</p>
              
              <div class="my-3 p-3 bg-card-inner rounded-2xl border max-w-sm mx-auto sm:mx-0">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/Encyclopedie_frontispice_full.jpg/640px-Encyclopedie_frontispice_full.jpg"
                     data-fallback="https://upload.wikimedia.org/wikipedia/commons/f/fd/Encyclopedie_frontispice_full.jpg"
                     alt="Frontispis Enciklopedije"
                     referrerpolicy="no-referrer"
                     crossorigin="anonymous"
                     class="w-full h-44 object-cover rounded-xl"
                     loading="lazy" onerror="handleImgError(this, 'enlightenment')" />
                <p class="text-[10px] text-muted mt-1.5 italic text-center leading-snug">
                  Frontispis Francuske enciklopedije (Cochin, 1772.)<br>
                  <span class="opacity-75">Izvor: Wikimedia Commons (Javno dobro)</span>
                </p>
              </div>
              <p><strong>Immanuel Kant:</strong> <em>Kritika čistoga uma</em> (1781.), <em>Prema vječnom miru</em> (1795.).<br>
              <strong>Voltaire:</strong> vjerska tolerancija i sloboda govora.<br>
              <strong>Cesare Beccaria:</strong> <em>O zločinima i kaznama</em> (1764.) – razmjernost kazni, protiv torture.</p>
            </div>
          </details>

          <details class="group bg-surface rounded-2xl overflow-hidden transition border">
            <summary class="p-4 sm:p-5 flex items-center justify-between bg-card-inner font-bold text-sm sm:text-base text-slate-200">
              <span class="flex items-center gap-2">
                <span class="w-6 h-6 rounded-lg bg-[#60aa75]/20 text-[#60aa75] flex items-center justify-center font-mono-num text-xs font-bold">4</span>
                Prosvijećeni apsolutizam i hrvatske zemlje
              </span>
              <span class="text-[#60aa75] group-open:rotate-180 transition-transform">▼</span>
            </summary>
            <div class="p-4 sm:p-6 text-xs sm:text-sm text-muted space-y-3 border-t leading-relaxed border-slate-700/30">
              <div class="my-3 p-3 bg-card-inner rounded-2xl border max-w-sm mx-auto sm:mx-0">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Kaiserin_Maria_Theresia_%28HRR%29.jpg/640px-Kaiserin_Maria_Theresia_%28HRR%29.jpg"
                     data-fallback="https://upload.wikimedia.org/wikipedia/commons/3/3e/Kaiserin_Maria_Theresia_%28HRR%29.jpg"
                     alt="Portret carice Marije Terezije"
                     referrerpolicy="no-referrer"
                     crossorigin="anonymous"
                     class="w-full h-48 object-cover object-top rounded-xl"
                     loading="lazy" onerror="handleImgError(this, 'terezija')" />
                <p class="text-[10px] text-muted mt-1.5 italic text-center leading-snug">
                  Carica Marija Terezija (Martin van Meytens, 1759.)<br>
                  <span class="opacity-75">Izvor: Wikimedia Commons (Javno dobro)</span>
                </p>
              </div>
              <p><strong>Marija Terezija (1740.–1780.):</strong> urbari, porezi, vojska, školstvo.<br>
              <strong>Josip II. (1780.–1790.):</strong> Patent o toleranciji (1781.), ukidanje samostana.<br>
              <strong>Školstvo:</strong> <em>Opći školski red (1774.)</em> za austrijske zemlje i Vojnu krajinu; <em>Ratio educationis (1777.)</em> za Ugarsku, civilnu Hrvatsku i Slavoniju.</p>
            </div>
          </details>

          <details class="group bg-surface rounded-2xl overflow-hidden transition border">
            <summary class="p-4 sm:p-5 flex items-center justify-between bg-card-inner font-bold text-sm sm:text-base text-slate-200">
              <span class="flex items-center gap-2">
                <span class="w-6 h-6 rounded-lg bg-[#60aa75]/20 text-[#60aa75] flex items-center justify-center font-mono-num text-xs font-bold">5-6</span>
                Gospodarske teorije, Adam Smith i Ivan Kapistran Adamović
              </span>
              <span class="text-[#60aa75] group-open:rotate-180 transition-transform">▼</span>
            </summary>
            <div class="p-4 sm:p-6 text-xs sm:text-sm text-muted space-y-3 border-t leading-relaxed border-slate-700/30">
              <p><strong>Merkantilizam:</strong> Colbert (Francuska), Navigacijski zakoni (Engleska), izvoz, carine, manufakture.<br>
              <strong>Kameralizam:</strong> Sonnenfels, Becher, Hornigk (Habsburška Monarhija – riznica i činovnici).<br>
              <strong>Fiziokratizam:</strong> François Quesnay (poljoprivreda, laissez-faire).<br>
              <strong>Adam Smith:</strong> <em>Bogatstvo naroda</em> (1776.) – rad, podjela rada, tržišna razmjena.<br>
              <strong>Ivan Kapistran Adamović Čepinski I. (1726.–1808.):</strong> posjedi Čepin, Erdut, Aljmaš, Sarvaš, Tenja, valpovački zakup, autor <em>Gospodarskog pravilnika (1774.)</em>.</p>
            </div>
          </details>

          <!-- LEKCIJE: VUKOVAR I ŠKABRNJA (DOMOVINSKI RAT) -->
          <div class="p-3 bg-gradient-to-r from-red-950/30 to-blue-950/30 border border-amber-500/40 rounded-2xl flex items-center justify-between mt-4">
            <div class="flex items-center gap-2">
              <span class="text-lg">🕯️</span>
              <strong class="text-amber-400 text-xs sm:text-sm font-serif-title">Spomen-cjelina: Vukovar i Škabrnja u Domovinskom ratu 1991.</strong>
            </div>
            <span class="text-[10px] text-muted font-mono-num">18. studenoga</span>
          </div>

          <details class="group bg-surface rounded-2xl overflow-hidden transition border border-amber-500/30">
            <summary class="p-4 sm:p-5 flex items-center justify-between bg-card-inner font-bold text-sm sm:text-base text-slate-200">
              <span class="flex items-center gap-2">
                <span class="w-6 h-6 rounded-lg bg-amber-500/20 text-amber-400 flex items-center justify-center font-mono-num text-xs font-bold">5</span>
                Bitka za Vukovar i herojska obrana 1991.
              </span>
              <span class="text-amber-400 group-open:rotate-180 transition-transform">▼</span>
            </summary>
            <div class="p-4 sm:p-6 text-xs sm:text-sm text-muted space-y-3 border-t leading-relaxed border-slate-700/30">
              <div class="my-3 p-3 bg-card-inner rounded-2xl border max-w-sm mx-auto sm:mx-0 shadow-md">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Vukovar_water_tower.jpg/640px-Vukovar_water_tower.jpg"
                     data-fallback="https://upload.wikimedia.org/wikipedia/commons/8/87/Vukovar_water_tower.jpg"
                     alt="Vukovarski vodotoranj"
                     referrerpolicy="no-referrer"
                     crossorigin="anonymous"
                     class="w-full h-44 object-cover rounded-xl"
                     loading="lazy" onerror="handleImgError(this, 'vukovar')" />
                <p class="text-[10px] text-muted mt-1.5 italic text-center leading-snug">
                  Vukovarski vodotoranj – simbol herojske obrane 1991.<br>
                  <span class="opacity-75">Izvor: Wikimedia Commons (CC BY-SA 3.0)</span>
                </p>
              </div>
              <p><strong>Kronologija bitke:</strong> Opsada Vukovara trajala je 87 dana (od 25. kolovoza do 18. studenoga 1991.). Grad je branilo oko 1.800 branitelja (204. vukovarska brigada, MUP, HOS, dragovoljci) protiv višestruko nadmoćnijih snaga JNA i paravojnih postrojbi.</p>
              <p><strong>Ključni položaji:</strong> Trpinjska cesta („groblje tenkova”), Borovo naselje, Sajmište, Mitnica, Lužac i Kukuruzni put (jedina veza prema Bogdanovcima i Vinkovcima).</p>
              <p><strong>Zapovjednici i heroji:</strong> Blago Zadro (zapovjednik obrane Borova naselja i Trpinjske ceste), Mile Dedaković Jastreb i Branko Borković Mladi Jastreb (zapovjednici obrane), Marko Babić, Alfred Hill, Jean-Michel Nicolier.</p>
              <p><strong>Humanitarni heroji:</strong> Medicinsko osoblje vukovarske bolnice na čelu s dr. Vesnom Bosanac i dr. Jurajem Njavrom.</p>
            </div>
          </details>

          <details class="group bg-surface rounded-2xl overflow-hidden transition border border-amber-500/30">
            <summary class="p-4 sm:p-5 flex items-center justify-between bg-card-inner font-bold text-sm sm:text-base text-slate-200">
              <span class="flex items-center gap-2">
                <span class="w-6 h-6 rounded-lg bg-amber-500/20 text-amber-400 flex items-center justify-center font-mono-num text-xs font-bold">6</span>
                Stradanje i otpor Škabrnje i zadarskog zaleđa
              </span>
              <span class="text-amber-400 group-open:rotate-180 transition-transform">▼</span>
            </summary>
            <div class="p-4 sm:p-6 text-xs sm:text-sm text-muted space-y-3 border-t leading-relaxed border-slate-700/30">
              <div class="my-3 p-3 bg-card-inner rounded-2xl border max-w-sm mx-auto sm:mx-0">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Skabrnja-spomenik.JPG/640px-Skabrnja-spomenik.JPG"
                     data-fallback="https://upload.wikimedia.org/wikipedia/commons/7/7d/Skabrnja-spomenik.JPG"
                     alt="Spomen-obilježje u Škabrnji"
                     referrerpolicy="no-referrer"
                     crossorigin="anonymous"
                     class="w-full h-44 object-cover rounded-xl"
                     loading="lazy" onerror="handleImgError(this, 'skabrnja')" />
                <p class="text-[10px] text-muted mt-1.5 italic text-center leading-snug">
                  Spomen-obilježje masovne grobnice u Škabrnji<br>
                  <span class="opacity-75">Izvor: Wikimedia Commons (CC BY-SA 3.0)</span>
                </p>
              </div>
              <p><strong>18. i 19. studenoga 1991.:</strong> Istoga dana kada je slomljen otpor u Vukovaru, postrojbe 9. korpusa JNA i paravojne formacije izvele su brutalan napad na ravnokotarsko selo Škabrnju i susjedni Nadin.</p>
              <p><strong>Položaji otpora i zaseoci:</strong> Ambar, Ražovljeva glavica, Ulica Slavka Šegarića, crkva Uznesenja BDM.</p>
              <p><strong>Posljedice:</strong> Ubijena su 43 civila i 15 branitelja u samom napadu (tijekom rata ukupno 84 škabrnjske žrtve). Škabrnja je uz Vukovar postala trajni simbol hrvatske žrtve i otpora.</p>
            </div>
          </details>

          <details class="group bg-surface rounded-2xl overflow-hidden transition border border-amber-500/30">
            <summary class="p-4 sm:p-5 flex items-center justify-between bg-card-inner font-bold text-sm sm:text-base text-slate-200">
              <span class="flex items-center gap-2">
                <span class="w-6 h-6 rounded-lg bg-amber-500/20 text-amber-400 flex items-center justify-center font-mono-num text-xs font-bold">7</span>
                Domovinski rat, oslobađanje i međunarodno priznanje
              </span>
              <span class="text-amber-400 group-open:rotate-180 transition-transform">▼</span>
            </summary>
            <div class="p-4 sm:p-6 text-xs sm:text-sm text-muted space-y-3 border-t leading-relaxed border-slate-700/30">
              <p><strong>Diplomacija:</strong> Odluka o raskidu državnopravnih sveza (8. listopada 1991.). Ključno međunarodno priznanje 15. siječnja 1992. (članice Europske zajednice, Sveta Stolica, Island, Njemačka, Austrija).</p>
              <p><strong>Gardijske brigade ZNG/HV:</strong> 1. gbr Tigrovi, 2. gbr Gromovi, 3. gbr Kune, 4. gbr Pauci, 7. gbr Pume, 9. gbr Vukovi.</p>
              <p><strong>Oslobodilačke operacije:</strong> Otkos 10, Orkan 91, Maslenica (1993.), Medački džep (1993.), Bljesak (svibanj 1995.) i vojno-redarstvena operacija Oluja (kolovoz 1995.).</p>
            </div>
          </details>

          <details class="group bg-surface rounded-2xl overflow-hidden transition border border-amber-500/30">
            <summary class="p-4 sm:p-5 flex items-center justify-between bg-card-inner font-bold text-sm sm:text-base text-slate-200">
              <span class="flex items-center gap-2">
                <span class="w-6 h-6 rounded-lg bg-amber-500/20 text-amber-400 flex items-center justify-center font-mono-num text-xs font-bold">8</span>
                Mirna reintegracija Podunavlja i kultura sjećanja
              </span>
              <span class="text-amber-400 group-open:rotate-180 transition-transform">▼</span>
            </summary>
            <div class="p-4 sm:p-6 text-xs sm:text-sm text-muted space-y-3 border-t leading-relaxed border-slate-700/30">
              <p><strong>Mirna reintegracija (1996.–1998.):</strong> Na temelju Erdutskog sporazuma (1995.), pod prijelaznom upravom UN-a (UNTAES) na čelu s generalom Jacquesom Paulom Kleinom, hrvatsko Podunavlje mirno je vraćeno u ustavnopravni poredak RH 15. siječnja 1998.</p>
              <p><strong>Mjesta posebnog domovinskog pijeteta:</strong> Vukovarski vodotoranj, Memorijalno groblje žrtava iz Domovinskog rata, Spomen-dom Ovčara, Mjesto sjećanja – Vukovarska bolnica 1991., spomen-obilježje u Škabrnji, Bijeli križ na ušću Vuke u Dunav.</p>

              <div class="my-3 p-3 bg-card-inner rounded-2xl border max-w-sm mx-auto sm:mx-0 shadow-md">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/The_White_Cross_Vukovar_Croatia.jpg/640px-The_White_Cross_Vukovar_Croatia.jpg"
                     data-fallback="https://upload.wikimedia.org/wikipedia/commons/a/a2/The_White_Cross_Vukovar_Croatia.jpg"
                     alt="Bijeli križ u Vukovaru"
                     referrerpolicy="no-referrer"
                     crossorigin="anonymous"
                     class="w-full h-44 object-cover rounded-xl"
                     loading="lazy" onerror="handleImgError(this, 'cross')" />
                <p class="text-[10px] text-muted mt-1.5 italic text-center leading-snug">
                  Spomen-križ za sve žrtve Domovinskog rata na ušću Vuke u Dunav<br>
                  <span class="opacity-75">Izvor: Wikimedia Commons (CC BY-SA)</span>
                </p>
              </div>
              <p><strong>Historiografija:</strong> Hrvatski memorijalno-dokumentacijski centar Domovinskog rata (HMDCDR), radovi povjesničara i kritička analiza povijesnih izvora.</p>
            </div>
          </details>
        </div>
      </section>

      <!-- ============================================================== -->
      <!-- PREDVORJE (LOBBY)                                              -->
      <!-- ============================================================== -->
      <section id="lobbySection" class="space-y-4 md:space-y-6">
        <!-- DVIJE GLAVNE TEMATSKE CJELINE (MODULI) S WIKIPEDIA SLIKAMA -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6 pt-1">
          
          <!-- MODUL 1: REDOVNA NASTAVA (PROSVJETITELJSTVO) -->
          <div onclick="setLobbySection('enlightenment')"
               class="group cursor-pointer rounded-3xl bg-surface border-2 border-[#60aa75]/40 hover:border-[#60aa75] p-4 sm:p-6 shadow-xl transition-all duration-300 hover:shadow-2xl hover:scale-[1.01] flex flex-col justify-between">
            <div class="space-y-3">
              <div class="relative h-44 sm:h-52 w-full rounded-2xl overflow-hidden border border-[#60aa75]/30 bg-black/40">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/Encyclopedie_frontispice_full.jpg/640px-Encyclopedie_frontispice_full.jpg"
                     data-fallback="https://upload.wikimedia.org/wikipedia/commons/f/fd/Encyclopedie_frontispice_full.jpg"
                     alt="Frontispis Francuske enciklopedije (1772)"
                     referrerpolicy="no-referrer"
                     crossorigin="anonymous"
                     class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                     loading="lazy" onerror="handleImgError(this, 'enlightenment')" />
                <div class="absolute inset-0 bg-gradient-to-t from-black/90 via-black/30 to-transparent"></div>
                <div class="absolute bottom-3 left-3 right-3 text-white">
                  <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-[#478b5c] text-white">
                    🏛️ Redovna nastava · Povijest 3
                  </span>
                  <h3 class="text-base sm:text-xl font-serif-title font-bold mt-1 text-white">
                    Doba prosvjetiteljstva u Europi i Hrvatskoj
                  </h3>
                </div>
              </div>
              <p class="text-xs text-muted leading-relaxed">
                Apsolutizam, birokracija, stajaća vojska, prosvjetiteljski mislioci (Locke, Montesquieu, Rousseau, Voltaire), reforme Marije Terezije i Josipa II., merkantilizam i fiziokrati.
              </p>
              <div class="text-[10px] text-muted opacity-75 italic pt-0.5">
                📷 Slika: Frontispis Encyclopédie (Cochin, 1772) · Izvor: Wikimedia Commons (Javno dobro)
              </div>
            </div>
            <div class="pt-3.5 flex items-center justify-between border-t border-slate-700/30 mt-3">
              <span class="text-xs font-mono-num font-bold text-[#60aa75]">Kvizovi 1–4 · 32 kategorije</span>
              <button class="px-4 py-2 bg-[#478b5c] group-hover:bg-[#3d774f] text-white font-black rounded-xl text-xs transition shadow-lg shadow-[#478b5c]/30 flex items-center gap-1.5">
                <span>Otvori kvizove 1–4</span>
                <span>➔</span>
              </button>
            </div>
          </div>

          <!-- MODUL 2: DAN SJEĆANJA (VUKOVAR I ŠKABRNJA) -->
          <div onclick="setLobbySection('vukovar')"
               class="group cursor-pointer rounded-3xl bg-surface border-2 border-amber-500/40 hover:border-amber-400 p-4 sm:p-6 shadow-xl transition-all duration-300 hover:shadow-2xl hover:scale-[1.01] flex flex-col justify-between">
            <div class="space-y-3">
              <div class="relative h-44 sm:h-52 w-full rounded-2xl overflow-hidden border border-amber-500/30 bg-black/40">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Vukovar_water_tower.jpg/640px-Vukovar_water_tower.jpg"
                     data-fallback="https://upload.wikimedia.org/wikipedia/commons/8/87/Vukovar_water_tower.jpg"
                     alt="Vukovarski vodotoranj"
                     referrerpolicy="no-referrer"
                     crossorigin="anonymous"
                     class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                     loading="lazy" onerror="handleImgError(this, 'vukovar')" />
                <div class="absolute inset-0 bg-gradient-to-t from-black/90 via-black/30 to-transparent"></div>
                <div class="absolute bottom-3 left-3 right-3 text-white">
                  <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-amber-700 text-white">
                    🕯️ 18. studenoga · Dan sjećanja
                  </span>
                  <h3 class="text-base sm:text-xl font-serif-title font-bold mt-1 text-white">
                    Vukovar i Škabrnja – Domovinski rat
                  </h3>
                </div>
              </div>
              <p class="text-xs text-muted leading-relaxed">
                Herojska obrana Vukovara, 204. brigada, bolnica, stradanje Škabrnje u zadarskom zaleđu, osamostaljenje, međunarodno priznanje Republike Hrvatske i kultura trajnog sjećanja.
              </p>
              <div class="text-[10px] text-muted opacity-75 italic pt-0.5">
                📷 Slika: Vukovarski vodotoranj · Izvor: Wikimedia Commons (CC BY-SA 4.0)
              </div>
            </div>
            <div class="pt-3.5 flex items-center justify-between border-t border-slate-700/30 mt-3">
              <span class="text-xs font-mono-num font-bold text-amber-400">Kvizovi 5–8 · 32 kategorije</span>
              <button class="px-4 py-2 bg-gradient-to-r from-amber-600 to-amber-500 group-hover:from-amber-500 group-hover:to-amber-400 text-slate-950 font-black rounded-xl text-xs transition shadow-lg shadow-amber-500/20 flex items-center gap-1.5">
                <span>Otvori kvizove 5–8</span>
                <span>➔</span>
              </button>
            </div>
          </div>
        </div>

        <!-- TRENUTNO AKTIVNI MODUL S BRZIM PRIJELAZOM I BREADCRUMBOM -->
        <div id="moduleStatusBanner" class="p-3.5 sm:p-4 rounded-2xl border transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-surface shadow-md">
          <!-- Dinamički se popunjava u JS -->
        </div>

        <!-- POPIS IGARA ZA ODABRANI MODUL -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4" id="gamesGrid">
          <!-- Popunjava se u JS -->
        </div>
<div class="bg-surface rounded-3xl p-4 sm:p-6 shadow-2xl space-y-4 border-2 border-[#60aa75]/40">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2.5 border-b pb-3 border-slate-700/30">
            <div>
              <div class="flex items-center gap-2">
                <span class="w-8 h-8 rounded-xl bg-amber-500/15 border border-amber-500/30 text-amber-400 flex items-center justify-center text-lg">🏆</span>
                <div>
                  <h3 class="text-base sm:text-lg font-serif-title font-bold text-white flex items-center gap-1.5">
                    <span id="lbHeading">Dnevna rang lista natjecanja</span>
                    <span class="text-[10px] bg-red-950/60 text-red-300 border border-red-500/30 px-2 py-0.5 rounded-full font-mono-num">24h ciklus</span>
                  </h3>
                  <p class="text-[11px] text-muted">
                    Podaci se čuvaju 24 sata do slanja profesoru. Učenici se natječu unutar dnevne grupe!
                  </p>
                </div>
              </div>
            </div>
            <div class="flex items-center gap-2 self-start sm:self-center">
              <button onclick="fetchLeaderboard()" class="px-3 py-1.5 bg-card-inner hover:border-[#60aa75] rounded-xl text-xs font-semibold border flex items-center gap-1 transition active:scale-95 text-muted hover:text-white">
                <span>🔄</span>
                <span>Osvježi</span>
              </button>
            </div>
          </div>

          <!-- Filter po igrama (Prosvjetiteljstvo + Vukovar & Škabrnja) -->
          <div class="flex items-center gap-1.5 overflow-x-auto pb-1 text-xs" id="lbFilterTabs">
            <button onclick="changeLbFilter('all')" class="lb-tab-btn active px-3 py-1.5 rounded-xl font-bold transition text-[11px] bg-[#60aa75] text-white shrink-0">Sve igre (1–8)</button>
            <button onclick="changeLbFilter(1)" class="lb-tab-btn px-3 py-1.5 rounded-xl font-bold transition text-[11px] bg-card-inner text-muted hover:text-white border shrink-0">1. Država</button>
            <button onclick="changeLbFilter(2)" class="lb-tab-btn px-3 py-1.5 rounded-xl font-bold transition text-[11px] bg-card-inner text-muted hover:text-white border shrink-0">2. Ideje</button>
            <button onclick="changeLbFilter(3)" class="lb-tab-btn px-3 py-1.5 rounded-xl font-bold transition text-[11px] bg-card-inner text-muted hover:text-white border shrink-0">3. Habsburzi</button>
            <button onclick="changeLbFilter(4)" class="lb-tab-btn px-3 py-1.5 rounded-xl font-bold transition text-[11px] bg-card-inner text-muted hover:text-white border shrink-0">4. Gospodarstvo</button>
            <button onclick="changeLbFilter(5)" class="lb-tab-btn px-3 py-1.5 rounded-xl font-bold transition text-[11px] bg-amber-950/40 text-amber-300 hover:text-white border border-amber-500/40 shrink-0">5. Vukovar 1991.</button>
            <button onclick="changeLbFilter(6)" class="lb-tab-btn px-3 py-1.5 rounded-xl font-bold transition text-[11px] bg-amber-950/40 text-amber-300 hover:text-white border border-amber-500/40 shrink-0">6. Škabrnja 1991.</button>
            <button onclick="changeLbFilter(7)" class="lb-tab-btn px-3 py-1.5 rounded-xl font-bold transition text-[11px] bg-amber-950/40 text-amber-300 hover:text-white border border-amber-500/40 shrink-0">7. Domovinski rat</button>
            <button onclick="changeLbFilter(8)" class="lb-tab-btn px-3 py-1.5 rounded-xl font-bold transition text-[11px] bg-amber-950/40 text-amber-300 hover:text-white border border-amber-500/40 shrink-0">8. Sjećanje</button>
          </div>

          <!-- Pobjednički podij za top 3 -->
          <div id="lbPodium" class="grid grid-cols-1 sm:grid-cols-3 gap-2.5 pt-1">
            <!-- Dinamički podij -->
          </div>

          <!-- Detaljna tablica ostalih natjecatelja -->
          <div class="bg-card-inner rounded-2xl border overflow-hidden">
            <div class="overflow-x-auto">
              <table class="w-full text-left border-collapse text-xs">
                <thead>
                  <tr class="border-b border-slate-700/40 text-muted font-mono-num text-[10px] uppercase tracking-wider bg-surface/50">
                    <th class="p-2.5 sm:px-3 text-center w-10">Rang</th>
                    <th class="p-2.5 sm:px-3">Učenik</th>
                    <th class="p-2.5 sm:px-3">Igra</th>
                    <th class="p-2.5 sm:px-3 text-right">Udaljenost</th>
                    <th class="p-2.5 sm:px-3 text-center">Točnost</th>
                    <th class="p-2.5 sm:px-3 text-right hidden sm:table-cell">Odredište</th>
                  </tr>
                </thead>
                <tbody id="leaderboardTbody" class="divide-y divide-slate-700/20 text-xs">
                  <tr><td colspan="6" class="p-4 text-center text-muted">Učitavanje rezultata natjecanja...</td></tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </section>

      <!-- ============================================================== -->
      <!-- AKTIVNA IGRA S REALISTIČNOM KARTOM I ZVUKOVIMA                -->
      <!-- ============================================================== -->
      <section id="gameSection" class="hidden space-y-4 md:space-y-6">
        <!-- REALISTIČNA KARTA EUROPE I HRVATSKE -->
        <div class="map-container p-2.5 sm:p-4">
          <div class="flex items-center justify-between mb-2 text-[11px] sm:text-xs">
            <div class="flex items-center gap-1.5 min-w-0">
              <span class="w-2.5 h-2.5 rounded-full bg-[#60aa75] animate-ping shrink-0"></span>
              <span class="font-bold text-[#60aa75] uppercase tracking-wider font-mono-num truncate" id="mapStatusText">
                Ruta: Zagreb ➔ Pariz ➔ Petrograd
              </span>
            </div>
            <div class="text-muted flex items-center gap-2 font-mono-num shrink-0">
              <span class="hidden xs:inline">Odredište: <strong class="text-white" id="currentMilestoneName">Zagreb</strong></span>
              <strong class="text-[#60aa75] text-xs sm:text-sm font-bold" id="mapOdometer">0 km</strong>
              <button onclick="toggleMapFold()" class="p-1 text-muted hover:text-white rounded sm:hidden" title="Prikaži/sakrij kartu">
                <span id="mapFoldIcon">▲</span>
              </button>
            </div>
          </div>

          <!-- REALISTIČNI KARTOGRAFSKI SVG PRIKAZ -->
          <div id="mapViewport" class="relative w-full h-[200px] xs:h-[240px] sm:h-[300px] md:h-[360px] rounded-xl overflow-hidden border border-slate-700/40 transition-all duration-300">
            <svg id="europeMapSvg" viewBox="0 0 1000 620" class="w-full h-full select-none" preserveAspectRatio="xMidYMid slice">
              <defs>
                <pattern id="compassGrid" width="100" height="100" patternUnits="userSpaceOnUse">
                  <path d="M 100 0 L 0 0 0 100" fill="none" stroke="rgba(96, 170, 117, 0.15)" stroke-width="0.5" stroke-dasharray="3 3"/>
                </pattern>
                <radialGradient id="pinGlow" cx="50%" cy="50%" r="50%">
                  <stop offset="0%" stop-color="#ffd700" stop-opacity="1" />
                  <stop offset="50%" stop-color="#60aa75" stop-opacity="0.6" />
                  <stop offset="100%" stop-color="#1e4028" stop-opacity="0" />
                </radialGradient>
              </defs>

              <!-- More / Vodene površine -->
              <rect width="1000" height="620" class="map-water"/>
              <rect width="1000" height="620" fill="url(#compassGrid)"/>

              <!-- Pomorske loxodrome (nautičke navigacijske linije) -->
              <g stroke="rgba(96, 170, 117, 0.2)" stroke-width="0.5" stroke-dasharray="1 4">
                <line x1="120" y1="200" x2="800" y2="400" />
                <line x1="120" y1="200" x2="600" y2="550" />
                <line x1="120" y1="200" x2="900" y2="100" />
                <line x1="560" y1="420" x2="100" y2="580" />
                <line x1="560" y1="420" x2="850" y2="50" />
              </g>

              <!-- KOPNENE MASE EUROPE (Geografske konture) -->
              <!-- Skandinavija & Baltik -->
              <path class="map-land" d="M 440,60 Q 480,20 540,40 T 600,80 L 590,180 Q 560,160 520,190 L 490,140 Q 450,110 440,60 Z" />
              <!-- Velika Britanija i Irska -->
              <path class="map-land" d="M 160,140 Q 180,100 200,120 T 235,170 L 225,230 Q 190,250 170,220 L 150,170 Z" />
              <path class="map-land" d="M 125,160 Q 145,150 145,190 T 120,210 Z" />
              <!-- Pirinejski poluotok (Španjolska & Portugal) -->
              <path class="map-land" d="M 40,540 L 130,510 Q 180,510 210,545 L 200,590 Q 150,615 60,605 Z" />
              <!-- Zapadna Europa (Francuska & Nizozemska) -->
              <path class="map-land" d="M 210,545 Q 240,440 260,360 L 330,240 Q 380,230 420,250 L 430,370 Q 370,410 300,430 L 220,530 Z" />
              <!-- Apeninski poluotok (Italija & Sicilija) -->
              <path class="map-land" d="M 390,380 Q 450,380 470,420 L 520,490 Q 530,530 490,550 L 460,500 Q 430,440 390,380 Z" />
              <path class="map-land" d="M 460,560 Q 480,550 490,575 T 450,580 Z" /> <!-- Sicilija -->
              <!-- Srednja i Istočna Europa -->
              <path class="map-land" d="M 420,250 Q 580,210 700,210 T 920,80 L 960,340 Q 750,380 640,440 L 520,380 L 430,370 Z" />
              
                            <!-- Glavne europske rijeke 18. stoljeća (žile kucavice prosvjetiteljstva) -->
              <g stroke="rgba(96, 170, 117, 0.45)" stroke-width="1.3" fill="none" stroke-linecap="round" stroke-linejoin="round">
                <!-- Dunav: od Schwarzwalda preko Beča, Požuna, Budima, Osijeka/Vukovara do Crnog mora -->
                <path d="M 460,345 Q 515,350 567,358 T 614,427 T 710,445 T 820,430 T 930,370" stroke-width="1.8" />
                <!-- Rajna: kroz carstvo i Nizozemsku prema Amsterdamu -->
                <path d="M 430,380 Q 415,330 380,290 T 338,250" />
                <!-- Sena: kroz Pariz prema La Mancheu -->
                <path d="M 330,370 Q 305,350 287,341 T 250,320" />
                <!-- Sava i Drava: kroz Hrvatsku i Slavoniju prema Dunavu -->
                <path d="M 505,435 Q 535,428 560,420 T 610,432 T 650,442" stroke-width="1.2" />
                <!-- Temza: kroz London -->
                <path d="M 210,270 Q 230,271 238,272 T 265,270" />
              </g>

              <!-- Natpisi mora i oceana (18. st. kartografska nomenklatura) -->
              <text x="110" y="220" font-size="9" font-family="Cinzel" letter-spacing="2" fill="rgba(96, 170, 117, 0.35)" font-style="italic">OCEANUS ATLANTICUS</text>
              <text x="495" y="465" font-size="8.5" font-family="Cinzel" letter-spacing="1.5" fill="rgba(96, 170, 117, 0.5)" font-style="italic" transform="rotate(-32 495 465)">MARE ADRIATICUM</text>
              <text x="350" y="580" font-size="9" font-family="Cinzel" letter-spacing="2" fill="rgba(96, 170, 117, 0.35)" font-style="italic">MARE MEDITERRANEUM</text>
              <text x="600" y="110" font-size="8.5" font-family="Cinzel" letter-spacing="2" fill="rgba(96, 170, 117, 0.35)" font-style="italic">MARE BALTICUM</text>

              <!-- Graticule koordinatni okvir s oznakama geografske širine i dužine -->
              <rect x="2" y="2" width="996" height="616" fill="none" stroke="rgba(96, 170, 117, 0.4)" stroke-width="1" />
              <rect x="6" y="6" width="988" height="608" fill="none" stroke="rgba(96, 170, 117, 0.2)" stroke-width="0.5" stroke-dasharray="4 4" />

              <!-- HRVATSKI POVIJESNI PROSTOR (Banska Hrvatska, Slavonija, Istra i Dalmacija) -->
              <path d="M 520,425 Q 550,400 580,410 T 635,425 L 630,455 Q 580,470 545,465 T 525,435 Z" fill="#60aa75" fill-opacity="0.45" stroke="#60aa75" stroke-width="2" />

              <!-- RUTA PUTOVANJA PROSVJETITELJSTVA -->
              <path id="baseRouteLine" d="M 560,420 L 567,407 L 614,427 L 567,358 L 529,309 L 508,246 L 338,250 L 287,341 L 238,272 L 176,157 L 57,604 L 847,54" fill="none" class="route-path" opacity="0.6" />
              <path id="activeRouteLine" d="M 560,420 L 567,407 L 614,427 L 567,358 L 529,309 L 508,246 L 338,250 L 287,341 L 238,272 L 176,157 L 57,604 L 847,54" fill="none" class="active-route" stroke-dasharray="2500" stroke-dashoffset="2500" />

              <!-- Ruža vjetrova (Baroque Compass Rose u Atlantiku) -->
              <g transform="translate(90, 320) scale(0.65)" opacity="0.7">
                <circle cx="0" cy="0" r="42" fill="none" stroke="#60aa75" stroke-width="1.5" stroke-dasharray="2 3"/>
                <polygon points="0,-48 8,-12 0,0 -8,-12" fill="#60aa75" />
                <polygon points="0,48 8,12 0,0 -8,12" fill="#2d633d" />
                <polygon points="48,0 12,8 0,0 12,-8" fill="#478b5c" />
                <polygon points="-48,0 -12,8 0,0 -12,-8" fill="#2d633d" />
                <text x="0" y="-53" font-size="14" font-weight="bold" fill="#60aa75" text-anchor="middle" font-family="Cinzel">N</text>
              </g>

              <!-- Kartuša / Natpis u kutu -->
              <g transform="translate(740, 560)" opacity="0.85">
                <rect x="0" y="0" width="235" height="42" rx="8" fill="rgba(6, 17, 10, 0.85)" stroke="#60aa75" stroke-width="1.2"/>
                <text x="117" y="18" font-size="10" font-weight="bold" fill="#60aa75" text-anchor="middle" font-family="Cinzel" letter-spacing="1.5">EUROPA & CROATIA</text>
                <text x="117" y="32" font-size="8.5" fill="#a3d4b2" text-anchor="middle" font-family="Plus Jakarta Sans">Doba prosvjetiteljstva (18. st.)</text>
              </g>

              <!-- GRADOVI I ČVOROVI S TOUCH HITBOXOVIMA -->
              <g id="cityNodesGroup">
                <!-- Zagreb -->
                <circle cx="560" cy="420" r="20" fill="transparent" onclick="showCityInfo('Zagreb')"/>
                <circle cx="560" cy="420" r="5.5" fill="#ffd700" class="city-node" onclick="showCityInfo('Zagreb')"/>
                <text x="560" y="438" font-size="11" font-weight="bold" fill="#ffd700" text-anchor="middle">Zagreb</text>

                <!-- Varaždin -->
                <circle cx="567" cy="407" r="20" fill="transparent" onclick="showCityInfo('Varaždin')"/>
                <circle cx="567" cy="407" r="4.5" fill="#60aa75" class="city-node" onclick="showCityInfo('Varaždin')"/>
                <text x="592" y="407" font-size="9" fill="#94b8a0" text-anchor="start">Varaždin</text>

                <!-- Osijek / Čepin -->
                <circle cx="614" cy="427" r="20" fill="transparent" onclick="showCityInfo('Osijek')"/>
                <circle cx="614" cy="427" r="4.5" fill="#60aa75" class="city-node" onclick="showCityInfo('Osijek')"/>
                <text x="625" y="433" font-size="9" fill="#94b8a0">Osijek / Čepin</text>

                <!-- Beč -->
                <circle cx="567" cy="358" r="22" fill="transparent" onclick="showCityInfo('Beč')"/>
                <circle cx="567" cy="358" r="6" fill="#60aa75" class="city-node" onclick="showCityInfo('Beč')"/>
                <text x="567" y="348" font-size="11" font-weight="bold" fill="#60aa75" text-anchor="middle">Beč</text>

                <!-- Prag -->
                <circle cx="529" cy="309" r="20" fill="transparent" onclick="showCityInfo('Prag')"/>
                <circle cx="529" cy="309" r="5" fill="#60aa75" class="city-node" onclick="showCityInfo('Prag')"/>
                <text x="529" y="299" font-size="9" fill="#94b8a0" text-anchor="middle">Prag</text>

                <!-- Berlin -->
                <circle cx="508" cy="246" r="20" fill="transparent" onclick="showCityInfo('Berlin')"/>
                <circle cx="508" cy="246" r="5" fill="#60aa75" class="city-node" onclick="showCityInfo('Berlin')"/>
                <text x="508" y="236" font-size="9" fill="#94b8a0" text-anchor="middle">Berlin</text>

                <!-- Amsterdam -->
                <circle cx="338" cy="250" r="20" fill="transparent" onclick="showCityInfo('Amsterdam')"/>
                <circle cx="338" cy="250" r="5" fill="#60aa75" class="city-node" onclick="showCityInfo('Amsterdam')"/>
                <text x="338" y="240" font-size="9" fill="#94b8a0" text-anchor="middle">Amsterdam</text>

                <!-- Pariz -->
                <circle cx="287" cy="341" r="24" fill="transparent" onclick="showCityInfo('Pariz')"/>
                <circle cx="287" cy="341" r="7" fill="#ffd700" class="city-node" onclick="showCityInfo('Pariz')"/>
                <text x="287" y="362" font-size="11" font-weight="bold" fill="#ffd700" text-anchor="middle">Pariz & Versailles</text>

                <!-- London -->
                <circle cx="238" cy="272" r="22" fill="transparent" onclick="showCityInfo('London')"/>
                <circle cx="238" cy="272" r="6" fill="#60aa75" class="city-node" onclick="showCityInfo('London')"/>
                <text x="238" y="260" font-size="10" font-weight="bold" fill="#60aa75" text-anchor="middle">London</text>

                <!-- Edinburgh -->
                <circle cx="176" cy="157" r="20" fill="transparent" onclick="showCityInfo('Edinburgh')"/>
                <circle cx="176" cy="157" r="5" fill="#60aa75" class="city-node" onclick="showCityInfo('Edinburgh')"/>
                <text x="176" y="147" font-size="9" fill="#94b8a0" text-anchor="middle">Edinburgh</text>

                <!-- Lisabon -->
                <circle cx="57" cy="604" r="20" fill="transparent" onclick="showCityInfo('Lisabon')"/>
                <circle cx="57" cy="604" r="5" fill="#60aa75" class="city-node" onclick="showCityInfo('Lisabon')"/>
                <text x="75" y="612" font-size="9" fill="#94b8a0">Lisabon</text>

                <!-- Petrograd -->
                <circle cx="847" cy="54" r="22" fill="transparent" onclick="showCityInfo('Petrograd')"/>
                <circle cx="847" cy="54" r="6" fill="#ffd700" class="city-node" onclick="showCityInfo('Petrograd')"/>
                <text x="835" y="44" font-size="10" font-weight="bold" fill="#ffd700" text-anchor="middle">Sankt-Peterburg</text>
              </g>

              <!-- Putnik -->
              <g id="travelerPin" class="traveler-pin" transform="translate(560, 420)">
                <circle cx="0" cy="0" r="18" fill="url(#pinGlow)"/>
                <circle cx="0" cy="0" r="6" fill="#ffd700" stroke="#1e4028" stroke-width="2"/>
                <circle cx="0" cy="0" r="2" fill="#60aa75"/>
              </g>
            </svg>

            <!-- Prekrivni opis grada -->
            <div id="cityInfoBadge" class="absolute bottom-2 left-2 right-2 md:left-4 md:right-auto md:max-w-sm bg-surface backdrop-blur-md rounded-xl p-2.5 shadow-2xl text-xs space-y-1 hidden border">
              <div class="flex items-center justify-between text-[#60aa75] font-bold">
                <span id="badgeCityTitle">📍 Zagreb</span>
                <span class="text-[10px] text-muted font-mono-num" id="badgeCityKm">0 km</span>
              </div>
              <p class="text-muted leading-snug text-[11px]" id="badgeCityDesc">
                Polazište vašeg prosvjetiteljskog putovanja.
              </p>
            </div>
          </div>
        </div>

        <!-- PITANJE I UNOS ODGOVORA (POTPUNO RESPONSIVE ZA MOBITELE, TABLETE I DESKTOP) -->
        <div id="questionCard" class="bg-surface rounded-2xl sm:rounded-3xl p-3.5 xs:p-4 sm:p-6 md:p-8 shadow-2xl space-y-3 sm:space-y-5 border transition-all">
          
          <!-- ZAGLAVLJE KARTICE: IZLAZ + KATEGORIJA/NASLOV + OSVOJENO + TAJMER -->
          <div class="flex items-center justify-between gap-2 border-b pb-2.5 sm:pb-3 border-slate-700/30">
            <div class="flex items-center gap-2 sm:gap-3 min-w-0 flex-1">
              <button onclick="confirmExitGame()" title="Prekini kviz i vrati se na izbor" class="p-2 sm:px-2.5 sm:py-1.5 bg-card-inner hover:bg-red-950/40 hover:border-red-500/40 border rounded-xl text-muted hover:text-red-300 transition shrink-0 text-xs flex items-center gap-1 min-h-[38px] active:scale-95">
                <span>🏠</span>
                <span class="hidden sm:inline">Izlaz</span>
              </button>
              <div class="min-w-0 flex-1">
                <span class="text-[10px] sm:text-xs uppercase tracking-widest font-mono-num text-[#60aa75] font-bold block truncate" id="gameCatBadge">
                  Igra 1 · Pitanje 1 / 8
                </span>
                <h3 class="text-xs sm:text-base md:text-lg font-bold text-white truncate mt-0.5" id="gameActiveTitle">
                  Nastanak moderne države
                </h3>
              </div>
            </div>

            <div class="flex items-center gap-2.5 sm:gap-4 shrink-0">
              <div class="text-right">
                <div class="text-[9px] text-muted font-mono-num uppercase font-semibold">Osvojeno</div>
                <div class="text-base sm:text-2xl font-black font-mono-num text-[#60aa75]" id="liveKmCounter">
                  0 <span class="text-[10px] font-normal text-muted">km</span>
                </div>
              </div>

              <!-- Tajmer (25s) -->
              <div id="timerContainer" class="w-11 h-11 sm:w-14 sm:h-14 rounded-xl sm:rounded-2xl bg-card-inner border-2 border-[#60aa75]/50 flex flex-col items-center justify-center font-mono-num shadow-lg transition shrink-0">
                <span id="timerSeconds" class="text-base sm:text-xl font-black text-[#60aa75] leading-none">25</span>
                <span class="text-[8px] sm:text-[9px] uppercase tracking-tighter text-muted mt-0.5">sek</span>
              </div>
            </div>
          </div>

          <!-- PROGRESS BAR VREMENA -->
          <div class="w-full h-1.5 sm:h-2 bg-card-inner rounded-full overflow-hidden">
            <div id="timerProgressBar" class="h-full bg-gradient-to-r from-[#2d633d] to-[#60aa75] transition-all duration-100 ease-linear" style="width: 100%;"></div>
          </div>

          <!-- TEKST PITANJA I UPUTA -->
          <div class="space-y-1 py-0.5 sm:py-1">
            <h2 id="questionText" class="text-base sm:text-xl md:text-2xl font-serif-title font-bold text-white leading-snug">
              Učitavanje pitanja...
            </h2>
            <p id="questionHint" class="text-xs sm:text-sm text-muted italic">
              Navedi pojam, osobu, djelo ili državu...
            </p>
          </div>

          <!-- OKVIR ZA UNOS ODGOVORA (LINIJSKI FORM, CLEAR GUMB, POTPUNO RESPONZIVNO) -->
          <form id="answerForm" onsubmit="handleAnswerSubmit(event)" class="w-full pt-1">
            <div class="dokle-answer-container">
              <div class="dokle-input-wrapper">
                <input type="text" id="answerInput" 
                       autocomplete="off" autocorrect="off" autocapitalize="none" spellcheck="false"
                       inputmode="text" enterkeyhint="go"
                       placeholder="Upiši svoj odgovor ovdje..."
                       class="dokle-answer-input" />
                <button type="button" id="clearAnswerBtn" onclick="clearAnswerInput()" class="dokle-clear-btn hidden" title="Izbriši unos" aria-label="Izbriši unos">
                  ✕
                </button>
              </div>
              <button type="submit" id="submitBtn" class="dokle-submit-btn">
                <span class="hidden xs:inline">POTVRDI</span>
                <span>➔</span>
              </button>
            </div>
          </form>

          <!-- POVRATNA INFORMACIJA -->
          <div id="feedbackBanner" class="hidden rounded-xl p-3.5 sm:p-4 transition-all">
          </div>
        </div>
      </section>

      <!-- ============================================================== -->
      <!-- ZAVRŠETAK IGRE                                                 -->
      <!-- ============================================================== -->
      <section id="resultsSection" class="hidden space-y-4 md:space-y-6">
        <div class="bg-surface rounded-3xl p-5 sm:p-8 shadow-2xl text-center space-y-5 border">
          <div class="w-16 h-16 sm:w-20 sm:h-20 mx-auto rounded-3xl bg-gradient-to-tr from-[#2d633d] to-[#60aa75] flex items-center justify-center text-3xl sm:text-4xl shadow-xl shadow-[#60aa75]/30 text-white">
            🎓
          </div>

          <div class="space-y-1.5">
            <span class="text-[10px] sm:text-xs uppercase font-mono-num font-bold text-[#60aa75] tracking-widest" id="resSummaryBadge">
              KVIZ USPJEŠNO ZAVRŠEN
            </span>
            <h2 class="text-2xl sm:text-3xl md:text-4xl font-serif-title font-black text-white" id="resTitle">
              Izvanredno putovanje!
            </h2>
            <p class="text-xs sm:text-sm text-muted max-w-lg mx-auto" id="resSubtitle">
              Tvoj rezultat je trajno zabilježen u školskoj bazi podataka.
            </p>
          </div>

          <div class="grid grid-cols-3 gap-2 sm:gap-4 max-w-2xl mx-auto">
            <div class="bg-card-inner rounded-xl sm:rounded-2xl p-2.5 sm:p-4 border">
              <div class="text-[9px] sm:text-xs text-muted font-mono-num uppercase">Prevaljeno</div>
              <div class="text-lg sm:text-3xl font-black font-mono-num text-[#60aa75] mt-1" id="resTotalKm">0 km</div>
            </div>
            <div class="bg-card-inner rounded-xl sm:rounded-2xl p-2.5 sm:p-4 border">
              <div class="text-[9px] sm:text-xs text-muted font-mono-num uppercase">Točnost</div>
              <div class="text-lg sm:text-3xl font-black font-mono-num text-emerald-400 mt-1" id="resAccuracy">0 / 8</div>
            </div>
            <div class="bg-card-inner rounded-xl sm:rounded-2xl p-2.5 sm:p-4 border">
              <div class="text-[9px] sm:text-xs text-muted font-mono-num uppercase truncate">Odredište</div>
              <div class="text-xs sm:text-base font-bold text-yellow-300 mt-1 sm:mt-2 truncate" id="resFinalDest">Pariz</div>
            </div>
          </div>

          <div class="max-w-3xl mx-auto text-left bg-card-inner rounded-2xl border p-4 space-y-2">
            <h4 class="text-[10px] sm:text-xs uppercase font-mono-num font-bold text-muted tracking-wider">
              Pregled svih 8 odgovora:
            </h4>
            <div class="divide-y divide-slate-700/20 text-xs max-h-60 overflow-y-auto" id="answersDetailList">
            </div>
          </div>

          <div class="flex flex-col sm:flex-row justify-center gap-3 pt-2">
            <button onclick="backToLobby()" class="px-5 py-3 bg-card-inner hover:border-[#60aa75] font-bold rounded-xl text-xs sm:text-sm transition border min-h-[44px]">
              🏠 Natrag na odabir igara
            </button>
            <button onclick="replayCurrentGame()" class="px-5 py-3 bg-gradient-to-r from-[#478b5c] to-[#60aa75] hover:from-[#3d774f] hover:to-[#529465] text-white font-black rounded-xl text-xs sm:text-sm transition shadow-lg shadow-[#478b5c]/30 min-h-[44px]">
              🔄 Igraj ponovno
            </button>
          </div>
        </div>
      </section>

            <!-- ============================================================== -->
      <!-- OBAVEZNO ISTAKNUTI ISHODI PRI DNU STRANICE                      -->
      <!-- ============================================================== -->
      <section id="outcomesFooterCard" class="bg-surface rounded-2xl p-5 sm:p-7 shadow-2xl space-y-6 border-2 border-[#60aa75]">
        <!-- KARTICA PREMA UDŽBENIKU (ALFA, str. 11) -->
        <div class="bg-[#60AA75] text-white p-5 sm:p-6 rounded-2xl shadow-xl space-y-3.5 border border-[#478B5C]">
          <div class="flex items-center justify-between border-b border-white/30 pb-2.5">
            <div class="flex items-center gap-2.5">
              <span class="w-8 h-8 rounded-lg bg-white/20 flex items-center justify-center text-lg font-bold">🎯</span>
              <h3 class="text-base sm:text-lg font-serif-title font-extrabold tracking-wide uppercase">
                NAUČIT ĆEŠ:
              </h3>
            </div>
            <span class="text-[11px] font-mono-num bg-white/20 px-2.5 py-0.5 rounded-full font-semibold">Alfa: Povijest 3, str. 11</span>
          </div>

          <ul class="space-y-2.5 text-xs sm:text-sm leading-relaxed text-emerald-50">
            <li class="flex items-start gap-2.5">
              <span class="text-white text-base leading-none font-bold">•</span>
              <span><strong>prosuditi utjecaj filozofskih teorija 18. i 19. stoljeća</strong> na razvoj kulturnih gibanja i ljudskog stvaralaštva</span>
            </li>
            <li class="flex items-start gap-2.5">
              <span class="text-white text-base leading-none font-bold">•</span>
              <span><strong>ocijeniti utjecaj prosvjetiteljstva</strong> na razvoj ekonomskih teorija te gospodarski razvoj Europe i hrvatskih zemalja</span>
            </li>
            <li class="flex items-start gap-2.5">
              <span class="text-white text-base leading-none font-bold">•</span>
              <span><strong>objasniti političke odnose, ratne sukobe u Europi u 18. stoljeću</strong> i ulogu Vojne krajine u habsburškim ratovima 18. stoljeća</span>
            </li>
            <li class="flex items-start gap-2.5">
              <span class="text-white text-base leading-none font-bold">•</span>
              <span><strong>objasniti društveni razvoj i društvene promjene</strong> u Habsburškoj Monarhiji u 18. stoljeću</span>
            </li>
            <li class="flex items-start gap-2.5">
              <span class="text-white text-base leading-none font-bold">•</span>
              <span><strong>povezati gospodarske promjene</strong> u doba prosvijećenog apsolutizma na prostorima hrvatskih zemalja s kontekstom gospodarskog razvoja Habsburške Monarhije</span>
            </li>
            <li class="flex items-start gap-2.5">
              <span class="text-white text-base leading-none font-bold">•</span>
              <span><strong>odrediti teritorijalni, politički i vojni ustroj</strong> hrvatskih zemalja pod austrougarskom vlašću.</span>
            </li>
          </ul>
        </div>

        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b pb-3.5 border-slate-700/30">
          <div>
            <span class="text-[10px] sm:text-xs font-mono-num font-bold uppercase tracking-widest text-[#60aa75] bg-[#60aa75]/15 px-2.5 py-1 rounded-full border border-[#60aa75]/30">
              KURIKULUMSKI STANDARDI · GIMNAZIJA (3. RAZRED)
            </span>
            <h3 class="text-lg sm:text-xl font-serif-title font-bold text-white mt-1.5 flex items-center gap-2">
              <span>📚</span> Detaljna razrada nastavnih ishoda (Alfa, str. 12–21)
            </h3>
          </div>
          <span class="text-xs text-muted font-mono-num">Kurikulum MZO</span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs sm:text-sm text-muted">
          <div class="flex items-start gap-2.5 p-3 bg-card-inner rounded-xl border">
            <span class="text-[#60aa75] font-bold shrink-0 font-mono-num">1.</span>
            <span><strong>Razvoj države:</strong> Objasniti kako su ratovanje, porezi, trgovina i demografske promjene pridonijeli razvoju ranonovovjekovne države.</span>
          </div>
          <div class="flex items-start gap-2.5 p-3 bg-card-inner rounded-xl border">
            <span class="text-[#60aa75] font-bold shrink-0 font-mono-num">2.</span>
            <span><strong>Apsolutizam i suverenitet:</strong> Usporediti apsolutizam i teorije koje opravdavaju ili ograničavaju suverenitet vladara.</span>
          </div>
          <div class="flex items-start gap-2.5 p-3 bg-card-inner rounded-xl border">
            <span class="text-[#60aa75] font-bold shrink-0 font-mono-num">3.</span>
            <span><strong>Filozofska misao:</strong> Razlikovati empirizam, racionalizam i temeljne ideje prosvjetiteljstva te argumentirano prosuditi njihove dosege.</span>
          </div>
          <div class="flex items-start gap-2.5 p-3 bg-card-inner rounded-xl border">
            <span class="text-[#60aa75] font-bold shrink-0 font-mono-num">4.</span>
            <span><strong>Habsburške reforme:</strong> Povezati reforme Marije Terezije i Josipa II. s društvenim i gospodarskim promjenama u hrvatskim zemljama.</span>
          </div>
          <div class="flex items-start gap-2.5 p-3 bg-card-inner rounded-xl border">
            <span class="text-[#60aa75] font-bold shrink-0 font-mono-num">5.</span>
            <span><strong>Ekonomske teorije:</strong> Usporediti merkantilizam, kameralizam, fiziokratizam i ekonomske ideje Adama Smitha.</span>
          </div>
          <div class="flex items-start gap-2.5 p-3 bg-card-inner rounded-xl border">
            <span class="text-[#60aa75] font-bold shrink-0 font-mono-num">6.</span>
            <span><strong>Hrvatski mislioci i praksa:</strong> Protumačiti značenje Nikole Vitova Gučetića i Ivana Kapistrana Adamovića Čepinskoga.</span>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-3 text-xs pt-1">
          <div class="p-3.5 bg-card-inner rounded-xl border space-y-1.5">
            <strong class="text-[#60aa75] block font-bold">Povezanost s nacionalnim kurikulumom:</strong>
            <p class="text-muted leading-relaxed">
              U središtu je ishod <strong>POV SŠ B.3.1.</strong> (gospodarske promjene od 18. do početka 20. stoljeća). U obradi pojedinih sadržaja razvijaju se i dijelovi ishoda <strong>A.3.1.</strong>, <strong>E.3.1.</strong>, <strong>D.3.1.</strong> te <strong>C.3.1.</strong>
            </p>
          </div>

          <div class="p-3.5 bg-card-inner rounded-xl border space-y-1.5">
            <strong class="text-[#60aa75] block font-bold">Kako pokazati znanje na gimnazijskoj razini?</strong>
            <div class="space-y-1 text-muted">
              <div><strong class="text-[#60aa75] font-mono-num">Činjenice:</strong> <em>„Vestfalski mir zaključen je 1648.”</em></div>
              <div><strong class="text-[#60aa75] font-mono-num">Objašnjenje:</strong> <em>„Skuplje ratovanje povećalo je potrebu za redovitim porezima i činovnicima.”</em></div>
              <div><strong class="text-[#60aa75] font-mono-num">Argumentacija:</strong> <em>„Reforme školstva mogle su povećati pismenost, ali i olakšati državi nadzor nad podanicima.”</em></div>
            </div>
          </div>
        </div>
      </section>

    </main>

    <!-- FOOTER -->
    <footer class="text-center text-[11px] text-muted py-4 border-t border-slate-700/30 space-y-1">
      <p>Povijesni Dokle? · Nastavni sustav za 3. razred gimnazije prema kurikulumu (Alfa)</p>
      <p>Zaštita privatnosti: Rezultati se svaka 24h šalju profesoru na ocjenjivanje i trajno brišu s poslužitelja.</p>
    </footer>

  </div>

  <!-- MODALI -->
  <div id="loginModal" class="fixed inset-0 bg-slate-950/85 backdrop-blur-sm z-50 flex items-center justify-center p-3 sm:p-4 hidden">
    <div class="bg-surface rounded-3xl max-w-md w-full p-6 sm:p-8 shadow-2xl space-y-4 max-h-[95dvh] overflow-y-auto border-2 border-[#60aa75]/40">
      <div class="text-center space-y-2">
        <div class="w-12 h-12 mx-auto rounded-2xl bg-[#60aa75]/20 border border-[#60aa75]/40 flex items-center justify-center text-2xl text-[#60aa75]">
          👤
        </div>
        <h3 class="text-xl font-serif-title font-bold text-white">Prijava za kviz</h3>
        <p class="text-xs text-muted">
          Upišite svoje ime ili pseudonim za sudjelovanje u igri i bodovanje.
        </p>
      </div>

      <form id="registerForm" onsubmit="handleRegisterSubmit(event)" class="space-y-4 text-xs">
        <div>
          <label class="block font-bold text-[#60aa75] mb-1.5 text-sm flex items-center justify-between">
            <span>Ime ili pseudonim:</span>
            <span class="text-[10px] text-muted font-normal">npr. Marko ili Povjesničar3</span>
          </label>
          <input type="text" id="inputPlayerName" maxlength="30" required
                 placeholder="Upiši svoje ime ili nadimak..."
                 inputmode="text" autocomplete="nickname"
                 class="dokle-modal-input" />
        </div>

        <div>
          <label class="block font-semibold text-muted mb-1 text-xs">
            Razred (opcionalno):
          </label>
          <input type="text" id="inputClass" placeholder="npr. 3.a"
                 inputmode="text"
                 class="w-full px-3.5 py-2.5 bg-card-inner border border-slate-700/50 rounded-xl text-white text-xs focus:border-[#60aa75] focus:outline-none min-h-[42px]" />
        </div>

        <!-- STROGO UPOZORENJE NA VULGARNOST -->
        <div class="p-3 bg-red-950/50 border border-red-500/40 rounded-xl text-xs text-red-300 leading-snug space-y-1">
          <div class="font-bold flex items-center gap-1.5 text-red-200">
            <span>⚠️</span> <span>STROGO UPOZORENJE NA VULGARNOST:</span>
          </div>
          <p class="text-[11px] text-red-300/90 leading-relaxed">
            Zabranjeni su vulgarni, uvredljivi, pogrdni izrazi i govor mržnje. Sustav posjeduje automatski sigurnosni filtar koji takva imena automatski odbija i blokira.
          </p>
        </div>

        <div id="profanityErrorBox" class="hidden p-3 bg-red-600/20 border-2 border-red-500 rounded-xl text-xs text-red-200 font-bold text-center leading-relaxed">
          🚫 Uneseno ime sadrži neprimjeren ili uvredljiv izraz. Molimo odaberite pristojno ime ili nadimak.
        </div>

        <div class="flex gap-2.5 pt-1">
          <button type="button" onclick="closeLoginModal()" class="w-1/3 py-3 bg-card-inner hover:bg-slate-800 rounded-xl font-bold transition min-h-[46px] border text-muted hover:text-white">
            Odustani
          </button>
          <button type="submit" id="regSubmitBtn" class="w-2/3 py-3 bg-[#478b5c] hover:bg-[#3d774f] text-white font-black rounded-xl text-sm transition shadow-lg shadow-[#478b5c]/30 min-h-[46px] flex items-center justify-center gap-2">
            <span>Započni igru</span>
            <span>➔</span>
          </button>
        </div>
      </form>
    </div>
  </div>

  <div id="teacherModal" class="fixed inset-0 bg-slate-950/85 backdrop-blur-sm z-50 flex items-center justify-center p-3 sm:p-4 hidden">
    <div class="bg-surface rounded-3xl max-w-2xl w-full p-5 sm:p-7 shadow-2xl space-y-5 max-h-[90dvh] overflow-y-auto border">
      <div class="flex items-center justify-between border-b pb-3 border-slate-700/30">
        <div>
          <h3 class="text-lg sm:text-xl font-serif-title font-bold text-white">⚙️ Nastavnički upravljački portal</h3>
          <p class="text-xs text-muted">Nadzor baze podataka, profila i 24h brisanja</p>
        </div>
        <button onclick="closeTeacherModal()" class="text-muted hover:text-white text-xl p-1">✕</button>
      </div>

      <div id="teacherAuthSection" class="space-y-3">
        <p class="text-xs text-muted">
          Pristup evidenciji ocjena zaštićen je nastavničkom lozinkom:
        </p>
        <div class="flex gap-2">
          <input type="password" id="teacherPassInput" placeholder="Lozinka profesora..."
                 class="flex-1 px-3.5 py-2.5 bg-card-inner border rounded-xl text-xs text-white focus:outline-none focus:border-[#60aa75] min-h-[44px]" />
          <button onclick="verifyTeacherPass()" class="px-4 py-2.5 bg-[#478b5c] hover:bg-[#3d774f] text-white font-bold rounded-xl text-xs transition min-h-[44px]">
            Otključaj
          </button>
        </div>
      </div>

      <div id="teacherPanelSection" class="hidden space-y-4 text-xs">
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5 text-center">
          <div class="bg-card-inner p-2.5 rounded-xl border">
            <span class="text-muted block text-[10px]">Profili učenika</span>
            <strong class="text-base text-[#60aa75] font-mono-num" id="statUserCount">0 / 70</strong>
          </div>
          <div class="bg-card-inner p-2.5 rounded-xl border">
            <span class="text-muted block text-[10px]">Aktivnih rezultata</span>
            <strong class="text-base text-emerald-400 font-mono-num" id="statResultCount">0</strong>
          </div>
          <div class="bg-card-inner p-2.5 rounded-xl border">
            <span class="text-muted block text-[10px]">Poslanih mailova</span>
            <strong class="text-base text-blue-400 font-mono-num" id="statEmailCount">0</strong>
          </div>
          <div class="bg-card-inner p-2.5 rounded-xl border">
            <span class="text-muted block text-[10px]">Slanje na mail</span>
            <strong class="text-[10px] text-yellow-300 truncate block mt-0.5">eh.matija39@gmail.com</strong>
          </div>
        </div>

        <div class="bg-surface border-2 border-[#60aa75]/50 rounded-2xl p-3.5 space-y-2">
          <strong class="text-[#60aa75] text-xs sm:text-sm block">⚡ Ručno slanje i trajno brisanje rezultata</strong>
          <p class="text-muted text-[11px] leading-relaxed">
            Svi zabilježeni rezultati šalju se na vaš e-mail <strong>eh.matija39@gmail.com</strong> i nakon toga se <em>trajno brišu</em> iz baze.
          </p>
          <button onclick="triggerFlushAndWipe()" id="flushWipeBtn" class="w-full sm:w-auto px-4 py-2.5 bg-red-600 hover:bg-red-500 text-white font-bold rounded-xl text-xs transition shadow-lg shadow-red-600/30 min-h-[44px]">
            Pošalji na eh.matija39@gmail.com i obriši sada
          </button>
        </div>

        <div class="space-y-2">
          <div class="flex items-center justify-between">
            <span class="font-bold text-white">Evidentirani učenici:</span>
            <button onclick="exportTeacherCsv()" class="text-[#60aa75] hover:underline">Preuzmi CSV za e-Dnevnik</button>
          </div>
          <div class="border rounded-xl overflow-hidden max-h-44 overflow-y-auto" id="teacherStudentsList">
            <p class="text-muted p-3 text-center">Nema učenika.</p>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- JAVASCRIPT LOGIKA -->
  <script>
    const RAW_DATA = __GAMES_JSON__;

    function normalizeGames(data) {
      if (Array.isArray(data) && data.length > 0 && data[0].questions) {
        return data;
      }
      const grouped = {};
      for (const item of data) {
        const gId = item.game || 1;
        if (!grouped[gId]) {
          grouped[gId] = {
            gameId: gId,
            gameTitle_hr: item.gameTitle_hr || `Igra ${gId}`,
            gameTitle_en: item.gameTitle_en || `Game ${gId}`,
            note_hr: item.note_hr || '',
            note_en: item.note_en || '',
            questions: []
          };
        }
        grouped[gId].questions.push(item);
      }
      return Object.values(grouped);
    }

    const GAMES = normalizeGames(RAW_DATA);

    const HISTORICAL_CITIES = [
      { name: 'Zagreb', x: 560, y: 420, km: 0, desc_hr: 'Polazište. Prijestolnica Banske Hrvatske, sjedište Hrvatskoga sabora i banske vlasti.', desc_en: 'Starting point. Capital of Civil Croatia, seat of the Croatian Diet and Ban.' },
      { name: 'Varaždin', x: 567, y: 407, km: 350, desc_hr: 'Sjedište Hrvatskoga kraljevinskog vijeća do velikog požara 1776. godine.', desc_en: 'Seat of the Croatian Royal Council until the great fire of 1776.' },
      { name: 'Osijek', x: 614, y: 427, km: 700, desc_hr: 'Barokna Tvrđa, važno trgovačko središte na Dravi i posjedi Adama Čepinskoga.', desc_en: 'Baroque Fortress, key trade center on the Drava, and estate of Adam of Cepin.' },
      { name: 'Beč', x: 567, y: 358, km: 1100, desc_hr: 'Prijestolnica Habsburške Monarhije. Reforme Marije Terezije i Josipa II.', desc_en: 'Capital of Habsburg Monarchy. Reforms of Maria Theresa and Joseph II.' },
      { name: 'Prag', x: 529, y: 309, km: 1550, desc_hr: 'Kraljevski grad Češke krune, stoljetno Karlovo sveučilište i intelektualno vrelište.', desc_en: 'Royal city of Bohemian Crown, centuries-old Charles University.' },
      { name: 'Berlin', x: 508, y: 246, km: 2100, desc_hr: 'Dvor Fridrika II. Velikoga u Sanssouciju, pruski prosvijećeni apsolutizam.', desc_en: 'Court of Frederick II the Great at Sanssouci, Prussian enlightened absolutism.' },
      { name: 'Amsterdam', x: 338, y: 250, km: 2750, desc_hr: 'Središte europskog bankarstva, slobodne trgovine i tiskara prosvjetiteljskih djela.', desc_en: 'European hub of banking, free trade, and printing of enlightened treatises.' },
      { name: 'Pariz', x: 287, y: 341, km: 3500, desc_hr: 'Prijestolnica prosvjetiteljstva, saloni, Diderotova Enciklopedija, Voltaire i Rousseau.', desc_en: 'Capital of the Enlightenment, literary salons, Diderot\'s Encyclopedia, Voltaire, Rousseau.' },
      { name: 'London', x: 238, y: 272, km: 4400, desc_hr: 'Parlamentarizam, Kraljevsko društvo (Royal Society), misao Johna Lockea i Newtona.', desc_en: 'Parliamentary rule, Royal Society, philosophy of John Locke and Isaac Newton.' },
      { name: 'Edinburgh', x: 176, y: 157, km: 5400, desc_hr: 'Škotsko prosvjetiteljstvo, David Hume i Adam Smith (Bogatstvo naroda 1776.).', desc_en: 'Scottish Enlightenment, David Hume, and Adam Smith (Wealth of Nations 1776).' },
      { name: 'Lisabon', x: 57, y: 604, km: 6800, desc_hr: 'Reforme markiza de Pombala, obnova grada nakon potresa 1755. i modernizacija države.', desc_en: 'Reforms of the Marquis of Pombal and urban reconstruction after the 1755 earthquake.' },
      { name: 'Petrograd', x: 847, y: 54, km: 8500, desc_hr: 'Prozor u Europu Petra Velikog i prijestolnica carice Katarine II. Velike.', desc_en: 'Peter the Great\'s window to Europe and imperial court of Catherine II the Great.' }
    ];

    // SPOMEN-RUTA SJEĆANJA NA VUKOVAR I ŠKABRNJU (DOMOVINSKI RAT)
    const VUKOVAR_MEMORIAL_CITIES = [
      { name: 'Zagreb', x: 560, y: 420, km: 0, desc_hr: 'Prijestolnica, Sabor i Vlada RH, polazište Kolone sjećanja.', desc_en: 'Capital of Croatia, Parliament, starting point.' },
      { name: 'Karlovac (Turanj)', x: 550, y: 428, km: 700, desc_hr: 'Turanj – vrata Karlovca, ključna točka herojske obrane na Korani i Kupi 1991.', desc_en: 'Turanj – heroic defense on the Korana and Kupa rivers.' },
      { name: 'Gospić & Velebit', x: 540, y: 445, km: 1600, desc_hr: 'Ličko ratište. Herojska obrana grada pod stalnim granatiranjem i oslobađanje vojarni.', desc_en: 'Lika frontline and Velebit mountain defense.' },
      { name: 'Škabrnja & Nadin', x: 535, y: 458, km: 2600, desc_hr: '18. studenoga 1991. Zločin i herojski otpor na Ambaru i Ražovljevoj glavici.', desc_en: 'Nov 18, 1991. Tragedy and heroic defense at Ambar and Razovljeva glavica.' },
      { name: 'Zadar', x: 528, y: 455, km: 3600, desc_hr: 'Grad pod teškom opsadom i pomorskom blokadom bez struje i pitke vode u jesen 1991.', desc_en: 'City under siege and naval blockade in autumn 1991.' },
      { name: 'Knin', x: 548, y: 462, km: 4800, desc_hr: 'Srednjovjekovni kraljevski grad, simbol oslobođenja u operaciji Oluja u kolovozu 1995.', desc_en: 'Symbol of liberation in Operation Storm in August 1995.' },
      { name: 'Slavonski Brod', x: 595, y: 432, km: 6000, desc_hr: 'Strateški prijelaz preko Save, grad pod stalnim zračnim i topničkim udarima.', desc_en: 'Strategic Sava crossing under artillery bombardment.' },
      { name: 'Vinkovci', x: 620, y: 428, km: 7200, desc_hr: 'Neosvojivi bedem istočne Slavonije i željezničko čvorište obrane Podunavlja.', desc_en: 'Impregnable bulwark of eastern Slavonia.' },
      { name: 'Osijek', x: 614, y: 420, km: 8200, desc_hr: '„Osijek – nepokoreni grad”. Zaustavljanje oklopnih prodora na južnim prilazima.', desc_en: 'Osijek – unconquered city on the Drava.' },
      { name: 'Bogdanovci & Kukuruzni put', x: 625, y: 425, km: 9200, desc_hr: 'Herojsko selo i Kukuruzni put – jedina arterija opskrbe opkoljenog Vukovara.', desc_en: 'Heroic village and Corn Path – lifeline of Vukovar.' },
      { name: 'Vukovar (Vodotoranj & Ovčara)', x: 630, y: 424, km: 10500, desc_hr: 'GRAD HEROJ. 87 dana nadljudskog otpora 204. brigade, simbol slobode i pobjede.', desc_en: 'HERO CITY. 87 days of resistance of 204th brigade, symbol of freedom.' }
    ];

    function getActiveCities() {
      const game = GAMES[currentGameIndex];
      if (game && game.module === 'vukovar_skabrnja') {
        return VUKOVAR_MEMORIAL_CITIES;
      }
      return HISTORICAL_CITIES;
    }

    let currentLanguage = 'hr';
    let currentUser = null;
    let currentGameIndex = 0;
    let currentQuestionIndex = 0;
    let timerInterval = null;
    let remainingSeconds = 25;
    let totalScoreKm = 0;
    let correctCount = 0;
    let roundAnswers = [];
    let audioEnabled = true;
    let audioCtx = null;
    let pendingRegisterEmail = '';
    let isMapFolded = false;
    let isStudyViewActive = false;
    let pendingGameIdx = null;

    // DOKLE.EU BODOVANJE & NATJECATELJSKI FAKTORI
    let currentStreak = 0;
    let maxStreak = 0;
    let totalSpeedBonusKm = 0;
    let totalOrthoBonusKm = 0;
    let userCooldowns = [];
    let currentLbFilter = 'all';

    const API_BASE = window.location.origin.startsWith('http') ? window.location.origin : 'http://localhost:3000';

    const I18N = {
      hr: {
        headerSubtitle: 'Doba prosvjetiteljstva u Europi i Hrvatskoj (16.–18. st.)',
        lobbyTitle: 'Odaberi nastavnu igru',
        lobbyDesc: '8 otvorenih kategorija · 25 sekundi po pitanju. Rjeđi i specifičniji odgovori donose veću kilometražu!',
        lbHeading: 'Najbolji rezultati',
        lbSub: 'Top putnici',
        questionHint: 'Upiši pojam, mislioca, vladara, djelo ili državu...',
        submit: 'POTVRDI',
        next: 'SLJEDEĆE PITANJE ➔',
        timeOutTitle: 'VRIJEME JE ISTEKLO! (0 km)',
        timeOutDesc: '25 sekundi je prošlo bez unosa.',
        correctRare: '🌟 GENIJALAN ODGOVOR! Iznimno rijedak povijesni pojam (+{km} km)!',
        correctCommon: '✔️ TOČAN ODGOVOR! Uspješno prepoznat pojam (+{km} km).',
        incorrect: '❌ ODGOVOR NIJE PREPOZNAT (0 km).',
        finalDestReached: 'Dosegnuto povijesno odredište:'
      },
      en: {
        headerSubtitle: 'Age of Enlightenment in Europe & Croatia (16th–18th C.)',
        lobbyTitle: 'Select History Quiz Game',
        lobbyDesc: '8 open categories · 25 seconds per question. Rarer answers yield higher mileage!',
        lbHeading: 'Leaderboard',
        lbSub: 'Top travelers',
        questionHint: 'Type a thinker, ruler, treatise, reform, or state...',
        submit: 'SUBMIT',
        next: 'NEXT QUESTION ➔',
        timeOutTitle: 'TIME EXPIRED! (0 km)',
        timeOutDesc: '25 seconds elapsed without submission.',
        correctRare: '🌟 BRILLIANT! Exceptionally rare entity (+{km} km)!',
        correctCommon: '✔️ CORRECT! Well-known accepted answer (+{km} km).',
        incorrect: '❌ NOT RECOGNIZED (0 km).',
        finalDestReached: 'Historical destination reached:'
      }
    };

    // ==========================================
    // TEMA: DARK / LIGHT MODE
    // ==========================================
    function initTheme() {
      const saved = localStorage.getItem('dokle_theme') || 'dark';
      setTheme(saved);
    }

    function toggleTheme() {
      const isDark = document.documentElement.classList.contains('theme-dark');
      setTheme(isDark ? 'light' : 'dark');
    }

    function setTheme(mode) {
      if (mode === 'light') {
        document.documentElement.classList.remove('theme-dark');
        document.documentElement.classList.add('theme-light');
        document.getElementById('themeIcon').textContent = '🌙';
        document.querySelector('meta[name="theme-color"]').setAttribute('content', '#f4f8f5');
      } else {
        document.documentElement.classList.remove('theme-light');
        document.documentElement.classList.add('theme-dark');
        document.getElementById('themeIcon').textContent = '☀️';
        document.querySelector('meta[name="theme-color"]').setAttribute('content', '#0f2417');
      }
      localStorage.setItem('dokle_theme', mode);
    }

    // ==========================================
    // POVIJESNA SINTEZA ZVUKA (WEB AUDIO API)
    // ==========================================
    function initAudio() {
      if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      }
      if (audioCtx && audioCtx.state === 'suspended') {
        audioCtx.resume();
      }
    }

    window.addEventListener('touchstart', function unlockAudioMobile() {
      initAudio();
      window.removeEventListener('touchstart', unlockAudioMobile);
    }, { passive: true, once: true });

    // 1. ZVUK PUCANJA TOPA (Autentični ranonovovjekovni top s barutom)
    function playCannonBlast() {
      if (!audioEnabled) return;
      initAudio();
      const now = audioCtx.currentTime;

      // A) Sub-bass udarni val (eksplozija u cijevi: 140Hz -> 30Hz)
      const subOsc = audioCtx.createOscillator();
      const subGain = audioCtx.createGain();
      subOsc.type = 'triangle';
      subOsc.frequency.setValueAtTime(140, now);
      subOsc.frequency.exponentialRampToValueAtTime(30, now + 0.35);

      subGain.gain.setValueAtTime(0.85, now);
      subGain.gain.exponentialRampToValueAtTime(0.001, now + 1.1);

      subOsc.connect(subGain);
      subGain.connect(audioCtx.destination);
      subOsc.start(now);
      subOsc.stop(now + 1.2);

      // B) Šum baruta i odjek (low-pass sweep)
      const bufferSize = Math.floor(audioCtx.sampleRate * 1.4);
      const noiseBuffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
      const output = noiseBuffer.getChannelData(0);
      for (let i = 0; i < bufferSize; i++) {
        output[i] = Math.random() * 2 - 1;
      }

      const whiteNoise = audioCtx.createBufferSource();
      whiteNoise.buffer = noiseBuffer;

      const filter = audioCtx.createBiquadFilter();
      filter.type = 'lowpass';
      filter.frequency.setValueAtTime(950, now);
      filter.frequency.exponentialRampToValueAtTime(50, now + 1.3);

      const noiseGain = audioCtx.createGain();
      noiseGain.gain.setValueAtTime(0.9, now);
      noiseGain.gain.exponentialRampToValueAtTime(0.001, now + 1.35);

      whiteNoise.connect(filter);
      filter.connect(noiseGain);
      noiseGain.connect(audioCtx.destination);

      whiteNoise.start(now);
      whiteNoise.stop(now + 1.4);
    }

    // 2. ZVUK SUDARA MAČEVA / SABLJI (Za netočan odgovor)
    function playSwordClash() {
      if (!audioEnabled) return;
      initAudio();
      const now = audioCtx.currentTime;

      // Dvostruki metalni zveket sablji
      [2200, 2800].forEach((freq) => {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, now);
        osc.frequency.exponentialRampToValueAtTime(freq * 0.8, now + 0.35);
        gain.gain.setValueAtTime(0.3, now);
        gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.4);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start(now);
        osc.stop(now + 0.45);
      });

      // Zvuk trenja oštrica
      const bufSize = Math.floor(audioCtx.sampleRate * 0.12);
      const buf = audioCtx.createBuffer(1, bufSize, audioCtx.sampleRate);
      const data = buf.getChannelData(0);
      for (let i = 0; i < bufSize; i++) data[i] = Math.random() * 2 - 1;

      const scrape = audioCtx.createBufferSource();
      scrape.buffer = buf;
      const filter = audioCtx.createBiquadFilter();
      filter.type = 'bandpass';
      filter.frequency.setValueAtTime(3200, now);
      filter.Q.setValueAtTime(4, now);

      const scrapeGain = audioCtx.createGain();
      scrapeGain.gain.setValueAtTime(0.35, now);
      scrapeGain.gain.exponentialRampToValueAtTime(0.001, now + 0.12);

      scrape.connect(filter);
      filter.connect(scrapeGain);
      scrapeGain.connect(audioCtx.destination);
      scrape.start(now);
    }

    // 3. KRALJEVSKA SALVA I FANFARA (Za rijetke odgovore > 1200 km)
        // 5. TRIJUMFALNI MARŠ (Za kraj igre i ostvaren cilj)
    function playVictoryMarch() {
      if (!audioEnabled) return;
      initAudio();
      const fanfareNotes = [
        { f: 523.25, d: 0.16, delay: 0 },     // C5
        { f: 659.25, d: 0.16, delay: 0.16 },  // E5
        { f: 783.99, d: 0.22, delay: 0.32 },  // G5
        { f: 1046.50, d: 0.55, delay: 0.54 }  // C6
      ];
      fanfareNotes.forEach(note => {
        setTimeout(() => {
          if (!audioCtx) return;
          const osc = audioCtx.createOscillator();
          const gain = audioCtx.createGain();
          osc.type = 'triangle';
          osc.frequency.setValueAtTime(note.f, audioCtx.currentTime);
          gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
          gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + note.d);
          osc.connect(gain);
          gain.connect(audioCtx.destination);
          osc.start();
          osc.stop(audioCtx.currentTime + note.d + 0.05);
        }, note.delay * 1000);
      });
    }

    function playRareCannonSalvo() {
      if (!audioEnabled) return;
      playCannonBlast();
      // Drugi top nakon 180ms za dramatični plotun
      setTimeout(() => playCannonBlast(), 180);

      // Trijumfalna barokna fanfara
      [523.25, 659.25, 783.99, 1046.50].forEach((f, idx) => {
        setTimeout(() => {
          initAudio();
          const osc = audioCtx.createOscillator();
          const gain = audioCtx.createGain();
          osc.type = 'triangle';
          osc.frequency.setValueAtTime(f, audioCtx.currentTime);
          gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
          gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.3);
          osc.connect(gain);
          gain.connect(audioCtx.destination);
          osc.start();
          osc.stop(audioCtx.currentTime + 0.32);
        }, 300 + idx * 100);
      });
    }

    // 4. KUCANJE MEHANIZMA SATA (Zadnjih 5 sekundi)
    function playClockworkTick() {
      if (!audioEnabled) return;
      initAudio();
      const now = audioCtx.currentTime;
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = 'square';
      osc.frequency.setValueAtTime(1100, now);
      gain.gain.setValueAtTime(0.04, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.04);
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start(now);
      osc.stop(now + 0.05);
    }

    function triggerHaptic(type = 'success') {
      if (!navigator.vibrate) return;
      try {
        if (type === 'rare') {
          navigator.vibrate([50, 70, 90]);
        } else if (type === 'success') {
          navigator.vibrate(45);
        } else if (type === 'fail') {
          navigator.vibrate([70, 40, 70]);
        } else if (type === 'tick') {
          navigator.vibrate(15);
        }
      } catch (e) {}
    }

    function toggleAudio() {
      audioEnabled = !audioEnabled;
      document.getElementById('soundIcon').textContent = audioEnabled ? '🔊' : '🔇';
      document.getElementById('soundLabel').textContent = audioEnabled ? 'Zvuk' : 'Mute';
    }

    function toggleMapFold() {
      const vp = document.getElementById('mapViewport');
      const icon = document.getElementById('mapFoldIcon');
      const label = document.getElementById('mapFoldLabel');
      isMapFolded = !isMapFolded;
      if (isMapFolded) {
        vp.style.height = '0px';
        vp.style.opacity = '0';
        vp.style.margin = '0';
        if (icon) icon.textContent = '▼';
        if (label) label.textContent = 'Prikaži kartu';
      } else {
        vp.style.height = '';
        vp.style.opacity = '1';
        vp.style.margin = '';
        if (icon) icon.textContent = '▲';
        if (label) label.textContent = 'Sakrij kartu';
      }
    }

    function handleImgError(img, type) {
      if (!img) return;
      // 1. Ako thumbnail ne radi, pokušaj s direktnim punim URL-om
      const fallbackUrl = img.getAttribute('data-fallback');
      if (fallbackUrl && img.src !== fallbackUrl) {
        img.src = fallbackUrl;
        return;
      }

      // 2. Ako je mreža nedostupna / offline, prikaži stilizirani tematski poster
      img.onerror = null;
      img.style.display = 'none';

      const parent = img.parentElement;
      if (parent && !parent.querySelector('.img-fallback-badge')) {
        const badge = document.createElement('div');
        const isVukovar = type === 'vukovar' || type === 'skabrnja' || type === 'cross';
        const isTerezija = type === 'terezija';
        const isBook = type === 'textbook';

        badge.className = 'img-fallback-badge w-full h-full min-h-[140px] rounded-xl flex flex-col items-center justify-center p-3 sm:p-4 text-center border ' + 
          (isVukovar 
            ? 'bg-amber-950/40 border-amber-500/40 text-amber-200' 
            : 'bg-[#1e4028]/60 border-[#60aa75]/40 text-[#a3d4b2]');

        let icon = '🏛️';
        let title = 'Doba prosvjetiteljstva';
        let sub = 'Znanost, razum i enciklopedizam (18. st.)';

        if (type === 'vukovar') {
          icon = '🏰';
          title = 'Vukovarski vodotoranj';
          sub = 'Simbol hrabrosti, obrane i hrvatske pobjede 1991.';
        } else if (type === 'skabrnja') {
          icon = '🕯️';
          title = 'Spomenik u Škabrnji';
          sub = 'Sjećanje na žrtve 18. studenoga 1991.';
        } else if (type === 'cross') {
          icon = '✝️';
          title = 'Bijeli križ u Vukovaru';
          sub = 'Spomenik na ušću Vuke u Dunav';
        } else if (isTerezija) {
          icon = '👑';
          title = 'Carica Marija Terezija';
          sub = 'Habsburške reforme, školstvo i prosvijećeni apsolutizam';
        } else if (isBook) {
          icon = '📖';
          title = 'Udžbenik Povijest 3 (Alfa)';
          sub = 'Doba prosvjetiteljstva u Europi i Hrvatskoj';
        }

        badge.innerHTML = `
          <span class="text-3xl sm:text-4xl mb-1">${icon}</span>
          <strong class="font-serif-title text-xs sm:text-sm tracking-wide block">${title}</strong>
          <span class="text-[10px] text-muted opacity-80 mt-0.5 block">${sub}</span>
        `;
        parent.insertBefore(badge, img);
      }
    }

    function clearAnswerInput() {
      const input = document.getElementById('answerInput');
      if (input) {
        input.value = '';
        input.focus();
        const clearBtn = document.getElementById('clearAnswerBtn');
        if (clearBtn) clearBtn.classList.add('hidden');
      }
    }

    function toggleMainView() {
      if (isStudyViewActive) {
        switchToGameLobby();
      } else {
        switchToStudyView();
      }
    }

    function switchToStudyView() {
      isStudyViewActive = true;
      document.getElementById('lobbySection').classList.add('hidden');
      document.getElementById('gameSection').classList.add('hidden');
      document.getElementById('resultsSection').classList.add('hidden');
      document.getElementById('studySection').classList.remove('hidden');

      document.getElementById('viewToggleIcon').textContent = '🎮';
      document.getElementById('viewToggleLabel').textContent = 'Kviz';
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function switchToGameLobby() {
      isStudyViewActive = false;
      document.getElementById('studySection').classList.add('hidden');
      document.getElementById('gameSection').classList.add('hidden');
      document.getElementById('resultsSection').classList.add('hidden');
      document.getElementById('lobbySection').classList.remove('hidden');

      document.getElementById('viewToggleIcon').textContent = '📖';
      document.getElementById('viewToggleLabel').textContent = 'Skripta';
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    // ==========================================
    // INICIJALIZACIJA
    // ==========================================
    window.addEventListener('DOMContentLoaded', () => {
      initTheme();
      loadSavedUser();
      updateModuleBannerUI();
      renderLobby();
      fetchLeaderboard();
      updateMapPosition(0);
      if (currentUser && currentUser.id) {
        fetchUserCooldowns();
      }
    });

    function loadSavedUser() {
      try {
        const stored = localStorage.getItem('dokle_current_user');
        if (stored) {
          currentUser = JSON.parse(stored);
          updateUserBadgeUI();
        }
      } catch (e) {}
    }

    function updateUserBadgeUI() {
      const badge = document.getElementById('userBadge');
      const loginBtn = document.getElementById('loginBtn');
      const name = currentUser ? (currentUser.name || currentUser.first_name || 'Učenik') : '';
      if (currentUser && name) {
        badge.classList.remove('hidden');
        badge.classList.add('flex');
        document.getElementById('userDisplayName').textContent = name;
        loginBtn.classList.add('hidden');
      } else {
        badge.classList.add('hidden');
        badge.classList.remove('flex');
        loginBtn.classList.remove('hidden');
      }
    }

    async function fetchUserCooldowns() {
      if (!currentUser || !currentUser.id) return;
      try {
        const res = await fetch(`${API_BASE}/api/user/cooldowns?userId=${currentUser.id}`);
        const data = await res.json();
        if (data.success && Array.isArray(data.cooldowns)) {
          userCooldowns = data.cooldowns;
          renderLobby();
        }
      } catch (e) {
        console.warn('Lokalni rad za cooldown.');
      }
    }

    function formatCooldownTime(ms) {
      if (!ms || ms <= 0) return '0 min';
      const totalHours = Math.floor(ms / (3600 * 1000));
      const minutes = Math.floor((ms % (3600 * 1000)) / (60 * 1000));
      if (totalHours >= 24) {
        const days = Math.floor(totalHours / 24);
        const remH = totalHours % 24;
        return `${days}d ${remH}h`;
      }
      return `${totalHours}h ${minutes}m`;
    }

    let currentLobbySection = 'all';

    function returnToHome() {
      clearInterval(timerInterval);
      document.getElementById('studySection').classList.add('hidden');
      document.getElementById('gameSection').classList.add('hidden');
      document.getElementById('resultsSection').classList.add('hidden');
      document.getElementById('lobbySection').classList.remove('hidden');
      window.scrollTo({ top: 0, behavior: 'smooth' });
      setLobbySection('all');
    }

    function confirmExitGame() {
      if (confirm('Želite li prekinuti igru i vratiti se na početni izbor kvizova?')) {
        returnToHome();
      }
    }

    function setLobbySection(sec) {
      currentLobbySection = sec;
      updateModuleBannerUI();
      renderLobby();
      const banner = document.getElementById('moduleStatusBanner');
      if (banner && sec !== 'all') {
        banner.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
    }

    function updateModuleBannerUI() {
      const banner = document.getElementById('moduleStatusBanner');
      if (!banner) return;

      if (currentLobbySection === 'enlightenment') {
        banner.className = 'p-4 rounded-2xl border-2 border-[#60aa75]/60 bg-[#60aa75]/10 shadow-lg flex flex-col sm:flex-row sm:items-center justify-between gap-3 transition-all';
        banner.innerHTML = `
          <div class="flex items-center gap-3 min-w-0">
            <span class="text-3xl shrink-0">🏛️</span>
            <div class="min-w-0">
              <div class="text-[11px] uppercase font-mono-num font-bold text-[#60aa75] tracking-wider truncate">ODABRANI MODUL: REDOVNA NASTAVA</div>
              <h4 class="text-base sm:text-lg font-serif-title font-bold text-white truncate">Doba prosvjetiteljstva u Europi i Hrvatskoj (Kvizovi 1–4)</h4>
              <p class="text-[11px] text-muted line-clamp-1 sm:line-clamp-none">Apsolutizam, prosvjetiteljske ideje, habsburške reforme i gospodarstvo (Alfa, str. 12–21)</p>
            </div>
          </div>
          <div class="flex items-center gap-2 shrink-0">
            <button onclick="setLobbySection('vukovar')" class="px-4 py-2 bg-gradient-to-r from-amber-700 to-amber-600 hover:from-amber-600 hover:to-amber-500 text-white font-bold rounded-xl text-xs transition shadow-md flex items-center gap-1.5 active:scale-95">
              <span>🕯️ Prebaci na Vukovar i Škabrnju</span>
              <span>➔</span>
            </button>
            <button onclick="setLobbySection('all')" class="px-3 py-2 bg-card-inner hover:bg-slate-800 rounded-xl text-xs text-muted hover:text-white border transition">
              🏠 Sve igre
            </button>
          </div>
        `;
      } else if (currentLobbySection === 'vukovar') {
        banner.className = 'p-4 rounded-2xl border-2 border-amber-500/60 bg-amber-950/30 shadow-lg flex flex-col sm:flex-row sm:items-center justify-between gap-3 transition-all';
        banner.innerHTML = `
          <div class="flex items-center gap-3 min-w-0">
            <span class="text-3xl shrink-0">🕯️</span>
            <div class="min-w-0">
              <div class="text-[11px] uppercase font-mono-num font-bold text-amber-400 tracking-wider truncate">ODABRANI MODUL: 18. STUDENOGA</div>
              <h4 class="text-base sm:text-lg font-serif-title font-bold text-white truncate">Dan sjećanja na žrtve Vukovara i Škabrnje (Kvizovi 5–8)</h4>
              <p class="text-[11px] text-amber-200/80 line-clamp-1 sm:line-clamp-none">Herojska obrana Vukovara, stradanje Škabrnje, Domovinski rat i kultura sjećanja</p>
            </div>
          </div>
          <div class="flex items-center gap-2 shrink-0">
            <button onclick="setLobbySection('enlightenment')" class="px-4 py-2 bg-[#478b5c] hover:bg-[#3d774f] text-white font-bold rounded-xl text-xs transition shadow-md flex items-center gap-1.5 active:scale-95">
              <span>🏛️ Vrati se na Redovnu nastavu</span>
              <span>➔</span>
            </button>
            <button onclick="setLobbySection('all')" class="px-3 py-2 bg-card-inner hover:bg-slate-800 rounded-xl text-xs text-muted hover:text-white border transition">
              🏠 Sve igre
            </button>
          </div>
        `;
      } else {
        banner.className = 'p-3.5 sm:p-4 rounded-2xl border border-slate-700/50 bg-surface shadow-md flex flex-col sm:flex-row sm:items-center justify-between gap-3 transition-all';
        banner.innerHTML = `
          <div class="flex items-center gap-3 min-w-0">
            <span class="text-2xl shrink-0">📋</span>
            <div class="min-w-0">
              <div class="text-[11px] uppercase font-mono-num font-bold text-[#60aa75] tracking-wider truncate">SVI DOSTUPNI KVIZOVI</div>
              <h4 class="text-sm sm:text-base font-serif-title font-bold text-white truncate">Prikazano svih 8 nastavnih i memorijalnih igara</h4>
              <p class="text-[11px] text-muted line-clamp-1 sm:line-clamp-none">Odaberite željeni kviz iz popisa niže ili filtrirajte po modulu na vrhu</p>
            </div>
          </div>
          <div class="flex items-center gap-2 shrink-0">
            <button onclick="setLobbySection('enlightenment')" class="px-3 py-1.5 bg-[#60aa75]/20 hover:bg-[#60aa75]/30 text-[#60aa75] border border-[#60aa75]/40 rounded-xl text-xs font-bold transition">
              🏛️ Samo Prosvjetiteljstvo
            </button>
            <button onclick="setLobbySection('vukovar')" class="px-3 py-1.5 bg-amber-950/40 hover:bg-amber-900/50 text-amber-300 border border-amber-500/40 rounded-xl text-xs font-bold transition">
              🕯️ Samo Vukovar
            </button>
          </div>
        `;
      }
    }

    function filterStudyScript(filter) {
      document.querySelectorAll('.study-tab-btn').forEach(b => {
        b.classList.remove('bg-[#60aa75]', 'text-white');
        b.classList.add('bg-card-inner', 'text-muted', 'border');
      });
      const activeBtn = filter === 'all' ? document.getElementById('studyTabAll') :
                        filter === 'enlightenment' ? document.getElementById('studyTabEnl') :
                        document.getElementById('studyTabVuk');
      if (activeBtn) {
        activeBtn.classList.remove('bg-card-inner', 'text-muted', 'border');
        activeBtn.classList.add('bg-[#60aa75]', 'text-white');
      }

      // Show/hide lesson accordions
      const details = document.querySelectorAll('#studySection details');
      details.forEach((d, idx) => {
        if (filter === 'all') {
          d.classList.remove('hidden');
        } else if (filter === 'enlightenment') {
          if (idx < 5) d.classList.remove('hidden');
          else d.classList.add('hidden');
        } else if (filter === 'vukovar') {
          if (idx >= 5) d.classList.remove('hidden');
          else d.classList.add('hidden');
        }
      });
    }

    function renderLobby() {
      const grid = document.getElementById('gamesGrid');
      grid.innerHTML = '';

      const filteredGames = GAMES.map((g, idx) => ({ ...g, globalIdx: idx })).filter(g => {
        if (currentLobbySection === 'all') return true;
        if (currentLobbySection === 'enlightenment') return g.module !== 'vukovar_skabrnja';
        if (currentLobbySection === 'vukovar') return g.module === 'vukovar_skabrnja';
        return true;
      });

      filteredGames.forEach(game => {
        const idx = game.globalIdx;
        const isEn = currentLanguage === 'en';
        const gameNum = idx + 1;
        const cooldown = userCooldowns.find(c => c.game_id === gameNum && c.is_locked);
        const isLocked = Boolean(cooldown);

        const card = document.createElement('div');
        card.className = `bg-surface rounded-2xl p-4 sm:p-5 shadow-xl transition-all flex flex-col justify-between space-y-3 border ${isLocked ? 'border-amber-500/40 bg-card-inner opacity-90' : 'hover:border-[#60aa75]'}`;
        
        card.innerHTML = `
          <div class="space-y-1.5">
            <div class="flex items-center justify-between gap-1 flex-wrap">
              <span class="text-[10px] sm:text-xs font-mono-num font-bold text-[#60aa75] bg-[#60aa75]/15 px-2.5 py-0.5 rounded-full border border-[#60aa75]/30">
                ${isEn ? 'Game ' + gameNum : 'Igra ' + gameNum} · ${game.questions.length} ${isEn ? 'Q' : 'pit.'}
              </span>
              ${isLocked 
                ? `<span class="text-[10px] font-mono-num font-bold text-amber-300 bg-amber-950/70 border border-amber-500/50 px-2 py-0.5 rounded-full flex items-center gap-1">🔒 ${isEn ? 'Locked 96h' : 'Zaključano 96h'}</span>` 
                : `<span class="text-[10px] sm:text-xs text-muted font-mono-num">⏱️ 25s · Dokle bodovanje</span>`
              }
            </div>
            <h3 class="text-base sm:text-lg font-bold font-serif-title text-white">
              ${isEn ? (game.gameTitle_en || game.gameTitle_hr) : game.gameTitle_hr}
            </h3>
            <p class="text-xs text-muted leading-relaxed line-clamp-2 sm:line-clamp-none">
              ${isEn ? (game.note_en || game.note_hr) : (game.note_hr || '')}
            </p>
            ${isLocked ? `
              <div class="p-2 bg-amber-950/40 border border-amber-500/30 rounded-xl text-[11px] text-amber-200 leading-snug">
                ⏳ <strong>Odigrano:</strong> Ovaj kviz možete ponovno riješiti tek za <strong>${formatCooldownTime(cooldown.remaining_ms)}</strong>. Vaš rezultat je zabilježen na rang listi!
              </div>
            ` : ''}
          </div>

          ${isLocked ? `
            <button onclick="alert('⏳ Natjecateljsko pravilo: Svaki se kviz može riješiti samo jednom u 96 sati (4 dana) radi ravnopravnosti natjecanja. Preostalo vrijeme do otključavanja: ' + '${formatCooldownTime(cooldown.remaining_ms)}')" 
                    class="w-full py-3 bg-slate-800 text-slate-400 font-bold rounded-xl text-xs sm:text-sm cursor-not-allowed border border-slate-700/80 flex items-center justify-center gap-1.5 min-h-[44px]">
              <span>🔒 ZAKLJUČANO (${formatCooldownTime(cooldown.remaining_ms)})</span>
            </button>
          ` : `
            <button onclick="startGame(${idx})" class="w-full py-3 bg-[#478b5c] hover:bg-[#3d774f] text-white font-black rounded-xl text-xs sm:text-sm transition shadow-lg shadow-[#478b5c]/30 flex items-center justify-center gap-1.5 active:scale-95 min-h-[44px]">
              <span>${isEn ? 'START QUIZ' : 'ZAPOČNI IGRU'}</span>
              <span>➔</span>
            </button>
          `}
        `;
        grid.appendChild(card);
      });
    }

    function toggleLanguage() {
      currentLanguage = currentLanguage === 'hr' ? 'en' : 'hr';
      document.getElementById('langFlag').textContent = currentLanguage === 'hr' ? '🇭🇷' : '🇬🇧';
      document.getElementById('langLabel').textContent = currentLanguage.toUpperCase();
      document.getElementById('headerSubtitle').textContent = I18N[currentLanguage].headerSubtitle;
      document.getElementById('lobbyTitle').textContent = I18N[currentLanguage].lobbyTitle;
      document.getElementById('lobbyDesc').textContent = I18N[currentLanguage].lobbyDesc;
      document.getElementById('lbHeading').textContent = I18N[currentLanguage].lbHeading;
      document.getElementById('lbSub').textContent = I18N[currentLanguage].lbSub;
      renderLobby();
      if (!document.getElementById('gameSection').classList.contains('hidden')) {
        renderCurrentQuestion();
      }
    }

    // ==========================================
    // TOK IGRE
    // ==========================================
    function startGame(gameIdx) {
      if (!currentUser) {
        pendingGameIdx = gameIdx;
        openLoginModal();
        return;
      }

      // PROVJERA 96-SATNOG COOLDOWNA
      const targetGameNum = gameIdx + 1;
      const cooldown = userCooldowns.find(c => c.game_id === targetGameNum && c.is_locked);
      if (cooldown) {
        alert(`🔒 Ovaj kviz ste već odigrali!

Prema pravilima natjecanja, svaki pojedini kviz se može riješiti samo JEDNOM u 96 sati (4 dana).

Otključavanje za: ${formatCooldownTime(cooldown.remaining_ms)}.`);
        return;
      }

      initAudio();
      currentGameIndex = Math.min(Math.max(0, gameIdx), GAMES.length - 1);
      currentQuestionIndex = 0;
      totalScoreKm = 0;
      correctCount = 0;
      currentStreak = 0;
      maxStreak = 0;
      totalSpeedBonusKm = 0;
      totalOrthoBonusKm = 0;
      roundAnswers = [];

      document.getElementById('studySection').classList.add('hidden');
      document.getElementById('lobbySection').classList.add('hidden');
      document.getElementById('resultsSection').classList.add('hidden');
      document.getElementById('gameSection').classList.remove('hidden');

      renderCurrentQuestion();
    }

    function renderCurrentQuestion() {
      clearInterval(timerInterval);
      const isEn = currentLanguage === 'en';
      const game = GAMES[currentGameIndex];
      
      if (!game || !game.questions || !game.questions[currentQuestionIndex]) {
        console.error('Greška: pitanje nije pronađeno za indeks:', currentGameIndex, currentQuestionIndex);
        return;
      }

      const q = game.questions[currentQuestionIndex];

      document.getElementById('gameCatBadge').textContent = `${isEn ? 'Game' : 'Igra'} ${currentGameIndex + 1} · ${isEn ? 'Question' : 'Pitanje'} ${currentQuestionIndex + 1} / ${game.questions.length}`;
      document.getElementById('gameActiveTitle').textContent = isEn ? (game.gameTitle_en || game.gameTitle_hr) : game.gameTitle_hr;

      const qText = isEn 
        ? (q.question_en || q.q_en || q.question_hr) 
        : (q.question_hr || q.q_hr || q.question);

      document.getElementById('questionText').textContent = qText;
      document.getElementById('questionHint').textContent = I18N[currentLanguage].questionHint;

      const input = document.getElementById('answerInput');
      input.value = '';
      input.disabled = false;
      const clearBtn = document.getElementById('clearAnswerBtn');
      if (clearBtn) clearBtn.classList.add('hidden');

      document.getElementById('submitBtn').disabled = false;
      document.getElementById('feedbackBanner').classList.add('hidden');

      // Na mobilnim ekranima centriraj karticu pitanja u vidno polje
      if (window.innerWidth < 768) {
        const qCard = document.getElementById('questionCard');
        if (qCard) {
          qCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }

      input.focus();

      startTimer();
    }

    function startTimer() {
      remainingSeconds = 25;
      updateTimerUI();

      timerInterval = setInterval(() => {
        remainingSeconds--;
        updateTimerUI();

        if (remainingSeconds <= 5 && remainingSeconds > 0) {
          playClockworkTick();
          triggerHaptic('tick');
          document.getElementById('timerContainer').classList.add('timer-critical');
        } else {
          document.getElementById('timerContainer').classList.remove('timer-critical');
        }

        if (remainingSeconds <= 0) {
          clearInterval(timerInterval);
          handleTimeOut();
        }
      }, 1000);
    }

    function updateTimerUI() {
      const timerSec = document.getElementById('timerSeconds');
      const progressBar = document.getElementById('timerProgressBar');
      timerSec.textContent = remainingSeconds;
      const pct = (remainingSeconds / 25) * 100;
      progressBar.style.width = pct + '%';

      if (remainingSeconds <= 5) {
        timerSec.classList.remove('text-[#60aa75]');
        timerSec.classList.add('text-red-400');
        progressBar.classList.remove('from-[#2d633d]', 'to-[#60aa75]');
        progressBar.classList.add('from-red-500', 'to-rose-600');
      } else {
        timerSec.classList.add('text-[#60aa75]');
        timerSec.classList.remove('text-red-400');
        progressBar.classList.add('from-[#2d633d]', 'to-[#60aa75]');
        progressBar.classList.remove('from-red-500', 'to-rose-600');
      }
    }

    function handleAnswerSubmit(e) {
      if (e) e.preventDefault();
      clearInterval(timerInterval);

      const input = document.getElementById('answerInput');
      const rawAnswer = input.value.trim();
      input.disabled = true;
      document.getElementById('submitBtn').disabled = true;

      const game = GAMES[currentGameIndex];
      const q = game.questions[currentQuestionIndex];
      const match = findBestMatch(rawAnswer, q.answers);

      if (match) {
        handleSuccessAnswer(rawAnswer, match, q);
      } else {
        handleFailAnswer(rawAnswer, q);
      }
    }

    function findBestMatch(rawInput, answersList) {
      if (!rawInput || !answersList) return null;
      const clean = normalizeText(rawInput);
      if (!clean) return null;

      // 1. Direct exact normalized match with canonical or any alias
      for (const ans of answersList) {
        if (normalizeText(ans.c_hr) === clean || normalizeText(ans.c_en) === clean) {
          return ans;
        }
        if (ans.a && Array.isArray(ans.a)) {
          for (const alias of ans.a) {
            if (normalizeText(alias) === clean) {
              return ans;
            }
          }
        }
      }

      // 2. Prefix stripping (dr, doktor, general, pukovnik, kralj, car, operacija, bitka, grad, selo)
      const prefixes = ['dr', 'doktor', 'general', 'pukovnik', 'bojnik', 'kralj', 'car', 'operacija', 'bitkaza', 'grad', 'selo', 'ulica', 'polozaj'];
      let stripped = clean;
      for (const p of prefixes) {
        if (clean.startsWith(p) && clean.length > p.length + 2) {
          stripped = clean.slice(p.length);
          break;
        }
      }

      if (stripped !== clean && stripped.length >= 3) {
        for (const ans of answersList) {
          if (normalizeText(ans.c_hr) === stripped || normalizeText(ans.c_en) === stripped) {
            return ans;
          }
          if (ans.a && Array.isArray(ans.a)) {
            for (const alias of ans.a) {
              if (normalizeText(alias) === stripped) {
                return ans;
              }
            }
          }
        }
      }

      // 3. Croatian plural / sound alternation tolerance
      // e.g. doktori -> doktor; lijecnici -> lijecnik (ci -> k); branitelji -> branitelj; puske -> puska
      const pluralVariants = [];
      if (clean.endsWith('ci') && clean.length > 4) {
        pluralVariants.push(clean.slice(0, -2) + 'k');
      }
      if (clean.endsWith('i') && clean.length > 3) {
        pluralVariants.push(clean.slice(0, -1));
      }
      if (clean.endsWith('e') && clean.length > 3) {
        pluralVariants.push(clean.slice(0, -1) + 'a');
        pluralVariants.push(clean.slice(0, -1));
      }
      for (const pv of pluralVariants) {
        for (const ans of answersList) {
          if (normalizeText(ans.c_hr) === pv || (ans.a && ans.a.some(al => normalizeText(al) === pv))) {
            return ans;
          }
        }
      }

      // 4. Fuzzy Levenshtein match for typos (1 typo for >= 5 letters, 2 typos for >= 8 letters)
      for (const ans of answersList) {
        const targets = [normalizeText(ans.c_hr)];
        if (ans.a && Array.isArray(ans.a)) {
          ans.a.forEach(al => targets.push(normalizeText(al)));
        }
        for (const tgt of targets) {
          const maxLen = Math.max(clean.length, tgt.length);
          if (maxLen >= 8 && levenshteinDist(clean, tgt) <= 2) {
            return ans;
          }
          if (maxLen >= 5 && levenshteinDist(clean, tgt) <= 1) {
            return ans;
          }
        }
      }

      return null;
    }

    function levenshteinDist(s1, s2) {
      if (s1.length < s2.length) return levenshteinDist(s2, s1);
      if (s2.length === 0) return s1.length;
      let prev = Array.from({ length: s2.length + 1 }, (_, i) => i);
      for (let i = 0; i < s1.length; i++) {
        const curr = [i + 1];
        for (let j = 0; j < s2.length; j++) {
          curr.push(Math.min(prev[j + 1] + 1, curr[j] + 1, prev[j] + (s1[i] !== s2[j] ? 1 : 0)));
        }
        prev = curr;
      }
      return prev[prev.length - 1];
    }

    function normalizeText(str) {
      if (!str) return '';
      return str.toLowerCase()
        .replace(/[čć]/g, 'c')
        .replace(/[ž]/g, 'z')
        .replace(/[š]/g, 's')
        .replace(/[đ]/g, 'dj')
        .replace(/[^a-z0-9]/g, '');
    }

    function handleSuccessAnswer(playerInput, matchedAnswer, questionObj) {
      const isEn = currentLanguage === 'en';
      const baseKm = matchedAnswer.km || 200;

      // 1. DOKLE BRZINSKI BONUS (Preostalo vrijeme od 25s)
      const remSec = Math.max(0, remainingSeconds);
      let speedBonus = remSec * 15;
      let speedLabel = '';
      if (remSec >= 20) {
        speedBonus += 350;
        speedLabel = '⚡ Munjeviti refleks (< 5s)';
      } else if (remSec >= 15) {
        speedBonus += 200;
        speedLabel = '⚡ Brzi odgovor (< 10s)';
      } else if (remSec >= 10) {
        speedBonus += 100;
        speedLabel = '⚡ Dobar tempo';
      } else {
        speedLabel = '⚡ Preostalo vrijeme';
      }

      // 2. DOKLE BONUS ZA TOČNOST NAPISANOGA (Besprijekorno sricanje vs. sinonim)
      const cleanInput = normalizeText(playerInput);
      const isExactCanonical = (cleanInput === normalizeText(matchedAnswer.c_hr) || cleanInput === normalizeText(matchedAnswer.c_en));
      const orthoBonus = isExactCanonical ? 150 : 0;

      // 3. COMBO NIZ (Consecutive Streak Multiplier)
      currentStreak++;
      if (currentStreak > maxStreak) maxStreak = currentStreak;
      const streakMultiplier = 1 + Math.min(0.20, (currentStreak - 1) * 0.05);

      // UKUPNI KILOMETRI ZA OVO PITANJE
      const questionTotalKm = Math.round((baseKm + speedBonus + orthoBonus) * streakMultiplier);

      totalScoreKm += questionTotalKm;
      totalSpeedBonusKm += speedBonus;
      totalOrthoBonusKm += orthoBonus;
      correctCount++;

      animateOdometer(totalScoreKm);
      updateMapPosition(totalScoreKm);

      const isRare = baseKm >= 1200;

      // ZVUČNI EFEKTI: TOP ILI SALVA
      if (isRare) {
        playRareCannonSalvo();
        triggerHaptic('rare');
      } else {
        playCannonBlast();
        triggerHaptic('success');
      }

      if (isRare && typeof confetti === 'function') {
        confetti({
          particleCount: 80,
          spread: 65,
          origin: { y: 0.65 },
          colors: ['#60aa75', '#ffd700', '#2d633d', '#ffffff']
        });
      }

      const qText = isEn 
        ? (questionObj.question_en || questionObj.q_en || questionObj.question_hr) 
        : (questionObj.question_hr || questionObj.q_hr || questionObj.question);

      roundAnswers.push({
        question: qText,
        playerAnswer: playerInput,
        matchedCanonical: isEn ? (matchedAnswer.c_en || matchedAnswer.c_hr) : matchedAnswer.c_hr,
        baseKm: baseKm,
        speedBonus: speedBonus,
        orthoBonus: orthoBonus,
        streakMultiplier: streakMultiplier,
        totalQuestionKm: questionTotalKm,
        km: questionTotalKm,
        isCorrect: true
      });

      const feedback = document.getElementById('feedbackBanner');
      feedback.className = `rounded-2xl p-4 sm:p-5 transition-all ${isRare ? 'bg-[#60aa75]/30 border-2 border-[#60aa75] rare-glow' : 'bg-[#60aa75]/20 border border-[#60aa75]/60'}`;
      
      feedback.innerHTML = `
        <div class="space-y-3">
          <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 border-b border-slate-700/30 pb-2.5">
            <div>
              <strong class="text-sm sm:text-base text-[#60aa75] block font-bold">
                ${isRare ? '🌟 GENIJALAN RIJEDAK ODGOVOR!' : '✔️ TOČAN ODGOVOR!'} (+${questionTotalKm.toLocaleString('hr-HR')} km)
              </strong>
              <p class="text-[11px] sm:text-xs text-muted">
                Prihvaćen pojam: <strong>${isEn ? (matchedAnswer.c_en || matchedAnswer.c_hr) : matchedAnswer.c_hr}</strong> (${matchedAnswer.r || 'Rijetkost'})
              </p>
            </div>
            <button onclick="nextQuestion()" class="w-full sm:w-auto px-6 py-2.5 bg-[#478b5c] hover:bg-[#3d774f] text-white font-bold rounded-xl text-xs transition shrink-0 min-h-[40px] shadow-lg shadow-[#478b5c]/30">
              ${I18N[currentLanguage].next}
            </button>
          </div>

          <!-- Raščlamba Dokle.eu bodova -->
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 text-[11px] font-mono-num">
            <div class="bg-card-inner p-2 rounded-xl border border-slate-700/30">
              <span class="text-muted block text-[10px]">📍 Osnovna rijetkost:</span>
              <strong class="text-white">+${baseKm.toLocaleString('hr-HR')} km</strong>
            </div>
            <div class="bg-card-inner p-2 rounded-xl border border-slate-700/30 text-amber-300">
              <span class="text-muted block text-[10px]">${speedLabel}:</span>
              <strong>+${speedBonus} km (${remSec}s)</strong>
            </div>
            <div class="bg-card-inner p-2 rounded-xl border border-slate-700/30 ${orthoBonus > 0 ? 'text-emerald-300' : 'text-slate-400'}">
              <span class="text-muted block text-[10px]">✍️ Točnost sricanja:</span>
              <strong>${orthoBonus > 0 ? '+150 km (Besprijekorno)' : 'Usvojen sinonim'}</strong>
            </div>
            <div class="bg-card-inner p-2 rounded-xl border border-slate-700/30 text-purple-300">
              <span class="text-muted block text-[10px]">🔥 Niz zaredom:</span>
              <strong>${Math.round(streakMultiplier * 100)}% (${currentStreak}x u nizu)</strong>
            </div>
          </div>

          ${questionObj.bonusFact ? `<p class="text-[10px] sm:text-[11px] text-[#60aa75] italic font-semibold pt-0.5">💡 Metodička činjenica: ${questionObj.bonusFact}</p>` : ''}
        </div>
      `;
      feedback.classList.remove('hidden');
    }

    function handleFailAnswer(playerInput, questionObj) {
      const isEn = currentLanguage === 'en';
      currentStreak = 0; // Prekid niza
      
      // ZVUČNI EFEKT: SUDAR SABLJI
      playSwordClash();
      triggerHaptic('fail');

      document.getElementById('answerInput').classList.add('shake-anim');
      setTimeout(() => document.getElementById('answerInput').classList.remove('shake-anim'), 400);

      const qText = isEn 
        ? (questionObj.question_en || questionObj.q_en || questionObj.question_hr) 
        : (questionObj.question_hr || questionObj.q_hr || questionObj.question);

      roundAnswers.push({
        question: qText,
        playerAnswer: playerInput || (isEn ? '[No answer]' : '[Bez odgovora]'),
        matchedCanonical: null,
        km: 0,
        isCorrect: false
      });

      const feedback = document.getElementById('feedbackBanner');
      feedback.className = 'rounded-xl p-3.5 sm:p-4 bg-red-950/40 border border-red-500/50';
      feedback.innerHTML = `
        <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
          <div class="space-y-1 min-w-0">
            <strong class="text-xs sm:text-sm text-red-400 block font-bold">${I18N[currentLanguage].incorrect}</strong>
            <p class="text-[11px] sm:text-xs text-muted">
              Primjeri rješenja: <em>${questionObj.answers ? questionObj.answers.slice(0, 3).map(a => isEn ? (a.c_en || a.c_hr) : a.c_hr).join(', ') : ''}...</em>
            </p>
          </div>
          <button onclick="nextQuestion()" class="w-full sm:w-auto px-5 py-2.5 bg-surface hover:border-[#60aa75] font-bold rounded-xl text-xs transition shrink-0 border min-h-[40px]">
            ${I18N[currentLanguage].next}
          </button>
        </div>
      `;
      feedback.classList.remove('hidden');
    }

    function handleTimeOut() {
      const isEn = currentLanguage === 'en';
      currentStreak = 0; // Prekid niza
      playSwordClash();
      triggerHaptic('fail');

      const game = GAMES[currentGameIndex];
      const q = game.questions[currentQuestionIndex];
      const qText = isEn 
        ? (q.question_en || q.q_en || q.question_hr) 
        : (q.question_hr || q.q_hr || q.question);

      roundAnswers.push({
        question: qText,
        playerAnswer: isEn ? '[Time Expired]' : '[Vrijeme isteklo]',
        matchedCanonical: null,
        km: 0,
        isCorrect: false
      });

      const feedback = document.getElementById('feedbackBanner');
      feedback.className = 'rounded-xl p-3.5 sm:p-4 bg-red-950/40 border border-red-500/50';
      feedback.innerHTML = `
        <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
          <div>
            <strong class="text-xs sm:text-sm text-red-400 block font-bold">${I18N[currentLanguage].timeOutTitle}</strong>
            <p class="text-[11px] sm:text-xs text-muted">${I18N[currentLanguage].timeOutDesc}</p>
          </div>
          <button onclick="nextQuestion()" class="w-full sm:w-auto px-5 py-2.5 bg-surface hover:border-[#60aa75] font-bold rounded-xl text-xs transition shrink-0 border min-h-[40px]">
            ${I18N[currentLanguage].next}
          </button>
        </div>
      `;
      feedback.classList.remove('hidden');
    }

    function nextQuestion() {
      currentQuestionIndex++;
      const game = GAMES[currentGameIndex];
      if (game && currentQuestionIndex < game.questions.length) {
        renderCurrentQuestion();
      } else {
        finishGame();
      }
    }

    function updateMapPosition(totalKm) {
      document.getElementById('mapOdometer').textContent = totalKm.toLocaleString('hr-HR') + ' km';

      const cities = getActiveCities();
      let targetCity = cities[0];
      for (const city of cities) {
        if (totalKm >= city.km) {
          targetCity = city;
        }
      }

      document.getElementById('currentMilestoneName').textContent = targetCity.name;
      const pin = document.getElementById('travelerPin');
      if (pin) {
        pin.setAttribute('transform', `translate(${targetCity.x}, ${targetCity.y})`);
      }

      const activeLine = document.getElementById('activeRouteLine');
      if (activeLine) {
        const progress = Math.min(1, totalKm / 8500);
        const offset = 2500 - (progress * 2500);
        activeLine.style.strokeDashoffset = offset;
      }

      showCityInfo(targetCity.name);
    }

    function showCityInfo(cityName) {
      const cities = getActiveCities();
      const city = cities.find(c => c.name === cityName) || HISTORICAL_CITIES.find(c => c.name === cityName);
      if (!city) return;

      const isEn = currentLanguage === 'en';
      const badge = document.getElementById('cityInfoBadge');
      document.getElementById('badgeCityTitle').textContent = `📍 ${city.name}`;
      document.getElementById('badgeCityKm').textContent = `${city.km} km`;
      document.getElementById('badgeCityDesc').textContent = isEn ? city.desc_en : city.desc_hr;
      badge.classList.remove('hidden');
    }

    function animateOdometer(targetKm) {
      const el = document.getElementById('liveKmCounter');
      let start = parseInt(el.textContent.replace(/[^0-9]/g, '')) || 0;
      const diff = targetKm - start;
      const steps = 18;
      let currentStep = 0;

      const timer = setInterval(() => {
        currentStep++;
        const currentVal = Math.round(start + (diff * (currentStep / steps)));
        el.innerHTML = `${currentVal.toLocaleString('hr-HR')} <span class="text-[10px] font-normal text-muted">km</span>`;
        if (currentStep >= steps) clearInterval(timer);
      }, 25);
    }

    function finishGame() {
      playVictoryMarch();

      clearInterval(timerInterval);
      document.getElementById('gameSection').classList.add('hidden');
      document.getElementById('resultsSection').classList.remove('hidden');

      const isEn = currentLanguage === 'en';
      const game = GAMES[currentGameIndex];

      // GRAND SLAM BONUS ZA SVIH 8 TOČNIH ODGOVORA
      if (correctCount === game.questions.length) {
        totalScoreKm += 1500;
        animateOdometer(totalScoreKm);
      }

      const rankTitle = getRankTitle(totalScoreKm);
      const cities = getActiveCities();
      const destCity = cities.slice().reverse().find(c => totalScoreKm >= c.km) || cities[0];

      document.getElementById('resTotalKm').textContent = totalScoreKm.toLocaleString('hr-HR') + ' km';
      document.getElementById('resAccuracy').textContent = `${correctCount} / ${game.questions.length} (${Math.round((correctCount / game.questions.length) * 100)}%)`;
      document.getElementById('resFinalDest').textContent = destCity.name;

      const list = document.getElementById('answersDetailList');
      list.innerHTML = '';
      roundAnswers.forEach((ans, idx) => {
        const item = document.createElement('div');
        item.className = 'py-2 flex items-center justify-between gap-2 text-xs';
        item.innerHTML = `
          <div class="min-w-0 truncate">
            <span class="text-muted font-mono-num mr-1">${idx + 1}.</span>
            <strong class="text-white">${ans.playerAnswer}</strong>
            ${ans.matchedCanonical ? `<span class="text-muted hidden xs:inline"> (➔ ${ans.matchedCanonical})</span>` : ''}
          </div>
          <span class="font-mono-num font-bold shrink-0 ${ans.isCorrect ? 'text-[#60aa75]' : 'text-red-400'}">
            ${ans.isCorrect ? '+' + ans.km.toLocaleString('hr-HR') + ' km' : '0 km'}
          </span>
        `;
        list.appendChild(item);
      });

      saveResultToServer(destCity.name, rankTitle);
    }

    function getRankTitle(km) {
      if (km >= 7500) return 'Vrhunski carski savjetnik prosvjetiteljstva';
      if (km >= 5000) return 'Dopisni član Kraljevske akademije znanosti';
      if (km >= 3000) return 'Enciklopedist i salonski mislilac';
      if (km >= 1500) return 'Kraljevski povjerenik reformi';
      return 'Student ranomodernih političkih teorija';
    }

    async function saveResultToServer(dest, rankTitle) {
      if (!currentUser) return;
      const game = GAMES[currentGameIndex];

      const payload = {
        userId: currentUser.id,
        gameId: currentGameIndex + 1,
        gameTitle: currentLanguage === 'en' ? (game.gameTitle_en || game.gameTitle_hr) : game.gameTitle_hr,
        language: currentLanguage,
        totalKm: totalScoreKm,
        correctCount: correctCount,
        totalQuestions: game.questions.length,
        speedBonusKm: totalSpeedBonusKm,
        orthoBonusKm: totalOrthoBonusKm,
        maxStreak: maxStreak,
        rankTitle: rankTitle,
        destination: dest,
        details: roundAnswers
      };

      try {
        const res = await fetch(`${API_BASE}/api/results`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (data.success) {
          await fetchUserCooldowns();
          fetchLeaderboard();
        }
      } catch (err) {
        console.warn('Lokalni rad.', err);
      }
    }

    function backToLobby() {
      document.getElementById('resultsSection').classList.add('hidden');
      document.getElementById('gameSection').classList.add('hidden');
      document.getElementById('studySection').classList.add('hidden');
      document.getElementById('lobbySection').classList.remove('hidden');
      updateModuleBannerUI();
      renderLobby();
      fetchLeaderboard();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function replayCurrentGame() {
      startGame(currentGameIndex);
    }

    // ==========================================
    // PRIJAVA I OTP
    // ==========================================
    function openLoginModal() {
      document.getElementById('loginModal').classList.remove('hidden');
    }

    function closeLoginModal() {
      document.getElementById('loginModal').classList.add('hidden');
    }

    // STROGI KLIJENTSKI FILTAR VULGARNOSTI
    const CLIENT_PROFANITY_ROOTS = [
      'jeb', 'jebo', 'jebat', 'jebem', 'jebi', 'jebiga', 'jebote', 'jebate', 'jebanje', 'jebac', 'jebavac',
      'kurac', 'kurca', 'kurcina', 'kurce', 'kurcu', 'kurcev', 'karindj', 'karat',
      'picka', 'pička', 'picu', 'piču', 'picke', 'pičke', 'pizda', 'pizde', 'pizdo', 'pizdetina', 'pizdarija',
      'govno', 'govna', 'govnar', 'govnjar', 'govnarija', 'govnence',
      'seronja', 'sranje', 'posran', 'posrati', 'poserem', 'usrani', 'kenjam', 'kenjator', 'kenjac',
      'drkadzija', 'drkadžija', 'drkati', 'drkam', 'drkanje',
      'drolja', 'droljo', 'droljetina', 'kurva', 'kurvetina', 'kurvetino', 'kucka', 'kučka',
      'supak', 'šupak', 'supcina', 'šupčina', 'cmar', 'čmar',
      'peder', 'pederu', 'pedercina', 'pederčina', 'pedofil', 'lezba', 'lezbijka',
      'cigan', 'cigani', 'cigo', 'balija', 'cetnik', 'četnik', 'ustasa', 'ustaša',
      'hitler', 'nacist', 'fasist', 'fašist', 'siegheil', 'svastika',
      'debil', 'idiot', 'retard', 'moron',
      'fuck', 'fucker', 'fucking', 'shit', 'bitch', 'dick', 'pussy', 'asshole', 'cunt', 'whore', 'bastard', 'nigger', 'nigga'
    ];

    function isClientProfane(name) {
      if (!name || typeof name !== 'string') return true;
      const raw = name.trim().toLowerCase();
      if (raw.length < 2 || raw.length > 35) return true;

      const leetMap = {
        '0': 'o', '1': 'i', '3': 'e', '4': 'a', '5': 's', '7': 't', '8': 'b',
        '@': 'a', '$': 's', 'v': 'u', 'w': 'v'
      };
      let leetStr = '';
      for (const ch of raw) {
        leetStr += leetMap[ch] || ch;
      }

      const clean1 = raw.replace(/[^a-zčćžšđ]/g, '');
      const clean2 = leetStr.replace(/[^a-zčćžšđ]/g, '');
      const dedup1 = clean1.replace(/(.)\1+/g, '$1');
      const dedup2 = clean2.replace(/(.)\1+/g, '$1');

      const candidates = [clean1, clean2, dedup1, dedup2, raw.replace(/\s+/g, ''), leetStr.replace(/\s+/g, '')];

      for (const cand of candidates) {
        if (!cand) continue;
        const candNorm = cand
          .replace(/[čć]/g, 'c')
          .replace(/[ž]/g, 'z')
          .replace(/[š]/g, 's')
          .replace(/[đ]/g, 'dj');

        for (const bad of CLIENT_PROFANITY_ROOTS) {
          const badNorm = bad
            .replace(/[čć]/g, 'c')
            .replace(/[ž]/g, 'z')
            .replace(/[š]/g, 's')
            .replace(/[đ]/g, 'dj');

          if (candNorm.includes(badNorm)) {
            return true;
          }
        }
      }
      return false;
    }

    async function handleRegisterSubmit(e) {
      e.preventDefault();
      const nameInput = document.getElementById('inputPlayerName');
      const name = nameInput.value.trim();
      const classInput = document.getElementById('inputClass');
      const className = (classInput ? classInput.value : '').trim();
      const errBox = document.getElementById('profanityErrorBox');

      if (errBox) errBox.classList.add('hidden');
      nameInput.classList.remove('border-red-500', 'animate-pulse');

      if (!name || name.length < 2) {
        alert('Molimo upišite ime ili pseudonim od barem 2 znaka.');
        nameInput.focus();
        return;
      }

      // STROGA KLIJENTSKA PROVJERA VULGARNOSTI
      if (isClientProfane(name)) {
        if (errBox) errBox.classList.remove('hidden');
        nameInput.classList.add('border-red-500', 'animate-pulse');
        nameInput.focus();
        return;
      }

      const btn = document.getElementById('regSubmitBtn');
      btn.disabled = true;
      btn.textContent = 'Prijavljujem...';

      try {
        const res = await fetch(`${API_BASE}/api/auth/register`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name, className })
        });
        const data = await res.json();

        if (data.success) {
          currentUser = data.user || { id: 1, first_name: name, class_name: className };
          localStorage.setItem('dokle_current_user', JSON.stringify(currentUser));
          updateUserBadgeUI();
          closeLoginModal();
          await fetchUserCooldowns();
          if (pendingGameIdx !== null) {
            const g = pendingGameIdx;
            pendingGameIdx = null;
            startGame(g);
          }
        } else {
          if (errBox && (data.message_hr || '').includes('neprimjeren')) {
            errBox.textContent = '🚫 ' + data.message_hr;
            errBox.classList.remove('hidden');
          } else {
            alert(data.message_hr || data.message_en || 'Greška pri prijavi.');
          }
        }
      } catch (err) {
        // Lokalni offline rad / Netlify fallback
        currentUser = { id: 1, first_name: name, class_name: className };
        localStorage.setItem('dokle_current_user', JSON.stringify(currentUser));
        updateUserBadgeUI();
        closeLoginModal();
        if (pendingGameIdx !== null) {
          const g = pendingGameIdx;
          pendingGameIdx = null;
          startGame(g);
        }
      } finally {
        btn.disabled = false;
        btn.textContent = 'Započni igru ➔';
      }
    }

    function handleLogout() {
      if (confirm('Želite li se odjaviti i prijaviti pod drugim učenikom/imenom?')) {
        currentUser = null;
        localStorage.removeItem('dokle_current_user');
        updateUserBadgeUI();
        userCooldowns = [];
        renderLobby();
      }
    }

    function openOtpModal() {}
    function handleOtpSubmit() {}

    function openTeacherModal() {
      document.getElementById('teacherModal').classList.remove('hidden');
    }

    function closeTeacherModal() {
      document.getElementById('teacherModal').classList.add('hidden');
    }

    let authenticatedTeacherKey = '';

    async function verifyTeacherPass() {
      const pass = document.getElementById('teacherPassInput').value.trim();
      if (!pass) return;

      try {
        const res = await fetch(`${API_BASE}/api/admin/stats`, {
          headers: { 'X-Admin-Password': pass }
        });
        const data = await res.json();
        if (data.success) {
          authenticatedTeacherKey = pass;
          document.getElementById('teacherAuthSection').classList.add('hidden');
          document.getElementById('teacherPanelSection').classList.remove('hidden');
          renderTeacherDashboard(data);
        } else {
          alert('Pogrešna lozinka profesora.');
        }
      } catch (e) {
        alert('Poslužitelj nije dostupan.');
      }
    }

    function renderTeacherDashboard(data) {
      document.getElementById('statUserCount').textContent = `${data.stats.userCount} / ${data.stats.maxUsers}`;
      document.getElementById('statResultCount').textContent = data.stats.resultsCount;
      document.getElementById('statEmailCount').textContent = data.stats.emailCount;

      const list = document.getElementById('teacherStudentsList');
      if (data.students && data.students.length > 0) {
        list.innerHTML = data.students.map(s => `
          <div class="p-2.5 bg-card-inner flex items-center justify-between border-b text-[11px]">
            <div class="min-w-0 truncate">
              <strong class="text-white">${s.first_name} ${s.last_name || ''}</strong>
              <span class="text-muted text-[10px]">(${s.class_name || '-'})</span>
            </div>
            <div class="flex items-center gap-2 font-mono-num shrink-0">
              <span class="text-[#60aa75] font-bold">${s.best_km ? s.best_km.toLocaleString('hr-HR') + ' km' : '0 km'}</span>
              <span class="${s.is_verified ? 'text-[#60aa75]' : 'text-amber-500'}">${s.is_verified ? '✔️' : '⏳'}</span>
            </div>
          </div>
        `).join('');
      } else {
        list.innerHTML = '<p class="text-muted p-3 text-center">Nema učenika.</p>';
      }
    }

    async function triggerFlushAndWipe() {
      if (!confirm('Jeste li sigurni da želite odmah poslati izvješće na eh.matija39@gmail.com i trajno obrisati rezultate iz baze?')) return;
      const btn = document.getElementById('flushWipeBtn');
      btn.disabled = true;
      btn.textContent = 'Šaljem i brišem bazu...';

      try {
        const res = await fetch(`${API_BASE}/api/admin/flush-and-wipe`, {
          method: 'POST',
          headers: { 'X-Admin-Password': authenticatedTeacherKey }
        });
        const data = await res.json();
        if (data.success) {
          alert(`Uspješno! ${data.count} rezultata poslano je na eh.matija39@gmail.com i trajno obrisano iz baze.`);
          verifyTeacherPass();
        } else {
          alert('Greška: ' + (data.error || 'Nije uspjelo.'));
        }
      } catch (e) {
        alert('Pogreška pri spajanju s poslužiteljem.');
      } finally {
        btn.disabled = false;
        btn.textContent = 'Pošalji na eh.matija39@gmail.com i obriši sada';
      }
    }

    function exportTeacherCsv() {
      window.location.href = `${API_BASE}/api/teacher/export-csv`;
    }

    function changeLbFilter(tab) {
      currentLbFilter = tab;
      document.querySelectorAll('#lbFilterTabs .lb-tab-btn').forEach(btn => {
        btn.classList.remove('bg-[#60aa75]', 'text-white');
        btn.classList.add('bg-card-inner', 'text-muted', 'border');
      });
      event.target.classList.remove('bg-card-inner', 'text-muted', 'border');
      event.target.classList.add('bg-[#60aa75]', 'text-white');
      fetchLeaderboard();
    }

    async function fetchLeaderboard() {
      const tbody = document.getElementById('leaderboardTbody');
      const podium = document.getElementById('lbPodium');
      const url = currentLbFilter === 'all' 
        ? `${API_BASE}/api/leaderboard` 
        : `${API_BASE}/api/leaderboard?game_id=${currentLbFilter}`;

      try {
        const res = await fetch(url);
        const data = await res.json();
        if (data.success && Array.isArray(data.results) && data.results.length > 0) {
          const list = data.results;

          // Prikaz podija za top 3
          const top3 = list.slice(0, 3);
          const podiumColors = [
            'border-amber-400 bg-amber-950/30 text-amber-300', // 1. Zlato
            'border-slate-300 bg-slate-900/40 text-slate-200',  // 2. Srebro
            'border-amber-700 bg-amber-950/20 text-amber-500'   // 3. Bronca
          ];
          const podiumTitles = ['🥇 1. Mjesto', '🥈 2. Mjesto', '🥉 3. Mjesto'];

          podium.innerHTML = top3.map((r, i) => `
            <div class="rounded-2xl p-3 border-2 ${podiumColors[i]} flex flex-col justify-between space-y-1.5 shadow-lg">
              <div class="flex items-center justify-between text-xs font-mono-num font-bold">
                <span>${podiumTitles[i]}</span>
                <span class="text-[10px] opacity-80">${r.game_title || 'Igra'}</span>
              </div>
              <div>
                <strong class="text-sm sm:text-base text-white block truncate">${r.first_name} ${r.class_name ? `(${r.class_name})` : ''}</strong>
                <span class="text-[11px] text-muted truncate block">📍 ${r.destination}</span>
              </div>
              <div class="flex items-center justify-between border-t border-slate-700/30 pt-1.5 font-mono-num text-xs">
                <span class="font-bold text-[#60aa75]">${r.total_km.toLocaleString('hr-HR')} km</span>
                <span class="text-muted text-[10px]">${r.correct_count}/${r.total_questions} (${r.accuracy_pct}%)</span>
              </div>
            </div>
          `).join('');

          // Prikaz tablice
          tbody.innerHTML = list.map((r, i) => `
            <tr class="hover:bg-slate-800/40 transition">
              <td class="p-2.5 sm:px-3 text-center font-mono-num font-bold">
                <span class="inline-block w-6 h-6 rounded-full ${i < 3 ? 'bg-amber-500/20 text-amber-400 border border-amber-500/40' : 'bg-card-inner text-muted'} text-[11px] leading-6">
                  ${r.badge || (i + 1)}
                </span>
              </td>
              <td class="p-2.5 sm:px-3">
                <strong class="text-white block truncate text-xs">${r.first_name}</strong>
                <span class="text-[10px] text-muted">${r.class_name || 'Razred nije naveden'}</span>
              </td>
              <td class="p-2.5 sm:px-3 text-muted text-[11px] font-mono-num truncate max-w-[100px]">${r.game_title || 'Igra'}</td>
              <td class="p-2.5 sm:px-3 text-right font-mono-num font-bold text-[#60aa75] text-xs">${r.total_km.toLocaleString('hr-HR')} km</td>
              <td class="p-2.5 sm:px-3 text-center font-mono-num text-[11px]">${r.correct_count}/${r.total_questions}</td>
              <td class="p-2.5 sm:px-3 text-right font-mono-num text-[11px] text-muted hidden sm:table-cell">${r.destination}</td>
            </tr>
          `).join('');
        } else {
          podium.innerHTML = '';
          tbody.innerHTML = `<tr><td colspan="6" class="p-4 text-center text-muted">Budi prvi natjecatelj u današnjem 24-satnom krugu!</td></tr>`;
        }
      } catch (e) {
        podium.innerHTML = '';
        tbody.innerHTML = `<tr><td colspan="6" class="p-4 text-center text-muted">Lokalni način rada spreman. Pokrenite poslužitelj za mrežno natjecanje.</td></tr>`;
      }
    }
  </script>
</body>
</html>
'''

final_html = HTML_CONTENT.replace('__GAMES_JSON__', games_json)

# Workspace (glavna stranica i index.html za Netlify/Render)
workspace_path = r'c:\Users\cehma\Downloads\Logika\Povijesni_Dokle_Prosvjetiteljstvo.html'
with open(workspace_path, 'w', encoding='utf-8') as f:
    f.write(final_html)

index_path = r'c:\Users\cehma\Downloads\Logika\index.html'
with open(index_path, 'w', encoding='utf-8') as f:
    f.write(final_html)

# Artefakt
artifact_path = r'C:\Users\cehma\.gemini\antigravity\brain\0b254044-cb3b-452e-9426-3a40cf647a70\povijesni_dokle.html'
with open(artifact_path, 'w', encoding='utf-8') as f:
    f.write(final_html)

print('Uspješno generirana zelena tema udžbenika s topom i sabljama!')
