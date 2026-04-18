@echo off
chcp 65001 >nul
title Зеркальный Питомник 3.0
cd /d "%~dp0"

echo.
echo === ZelKalO 3.0 ===
echo.

python -m pip install -r requirements.txt --quiet

echo Zapusk...
echo.

python mirror_nursery_bot.py

pause
