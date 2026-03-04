@echo off
chcp 65001 >nul
title JMComic QQ Bot - 浮浮酱
color 0A

echo ============================================================
echo   JMComic QQ Bot 启动脚本
echo   作者：浮浮酱 ฅ'ω'ฅ
echo ============================================================
echo.

echo [提示] 请确保 NapCat 已经启动并登录 QQ
echo.
pause

echo.
echo [1/2] 检查环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到 Python！
    pause
    exit /b 1
)
echo ✅ Python 环境正常
echo.

echo [2/2] 启动机器人...
echo ============================================================
echo.
python bot.py

pause
