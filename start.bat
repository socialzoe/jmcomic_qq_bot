@echo off
chcp 65001 >nul
echo ========================================
echo   JMComic QQ Bot 启动脚本
echo   作者：浮浮酱 ฅ'ω'ฅ
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未安装Python！
    echo 请先安装Python 3.9+
    pause
    exit /b 1
)
echo ✅ Python环境正常

echo.
echo [2/3] 检查依赖...
python -c "import nonebot" >nul 2>&1
if errorlevel 1 (
    echo ⚠️ 缺少依赖，正在安装...
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    if errorlevel 1 (
        echo ❌ 依赖安装失败！
        pause
        exit /b 1
    )
)
echo ✅ 依赖已安装

echo.
echo [3/3] 启动机器人...
echo ========================================
echo.

python bot.py

pause
