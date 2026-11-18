@echo off
title Povijesni Dokle? - Sigurni Skolski Posluzitelj
chcp 65001 > nul
echo ========================================================
echo    POVIJESNI DOKLE? - Baza podataka i posluzitelj
echo    Doba prosvjetiteljstva u Europi i Hrvatskoj (Alfa)
echo ========================================================
echo.
echo [SIGURNOST]
echo  - Ogranicenje: max 70 profila ucenika
echo  - E-mail verifikacija OTP kodom
echo  - Slanje rezultata svaka 24h na: eh.matija39@gmail.com
echo  - Trajno brisanje rezultata iz baze nakon slanja
echo  - Nastavnicka lozinka: Profesor2026!
echo.
echo Pokrecem osigurani SQLite server...
echo.
node server.js
pause
