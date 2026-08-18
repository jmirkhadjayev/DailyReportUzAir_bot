@echo off
chcp 65001 >nul
title Kundalik hisobot boti
cd /d "%~dp0"

if not exist ".env" (
    echo [!] .env fayli topilmadi.
    echo     .env.example faylini .env deb nusxalang va BOT_TOKEN ni yozing.
    pause
    exit /b 1
)

echo Bot ishga tushmoqda... To'xtatish uchun Ctrl+C bosing.
python bot.py
pause
