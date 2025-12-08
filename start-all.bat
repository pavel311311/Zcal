@echo off
REM 一键启动前后端服务脚本 (批处理版本)
REM 在不同的命令行窗口中启动后端和前端

setlocal enabledelayedexpansion
cd /d "%~dp0"

echo.
echo ===============================================
echo 启动 PCB 阻抗计算器 ^(前后端服务^)
echo ===============================================
echo.

REM 检查虚拟环境
if not exist ".venv" (
    echo 正在创建虚拟环境...
    python -m venv .venv
    if errorlevel 1 (
        echo ❌ 虚拿环境创建失败
        pause
        exit /b 1
    )
)

REM 激活虚拟环境
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ 虚拟环境激活失败
    pause
    exit /b 1
)

REM 安装后端依赖
echo 📦 检查后端依赖...
if exist "src\backend\requirements.txt" (
    pip install -q -r src\backend\requirements.txt
    if errorlevel 1 (
        echo ❌ 后端依赖安装失败
        pause
        exit /b 1
    )
)

REM 安装前端依赖
echo 📦 检查前端依赖...
if exist "src\frontend\package.json" (
    cd src\frontend
    if not exist "package-lock.json" (
        echo 首次安装前端依赖...
        call npm install
    ) else (
        call npm ci --audit=false --fund=false >nul 2>&1
    )
    cd ..\..
)

REM 启动后端服务
echo.
echo 🚀 启动后端服务...
echo.
start "Backend - Flask" cmd /k "call .venv\Scripts\activate.bat && cd src\backend && python run.py"

REM 等待1秒
timeout /t 1 /nobreak >nul

REM 启动前端服务
echo 🚀 启动前端服务...
echo.
start "Frontend - Vite" cmd /k "cd src\frontend && npm run dev"

REM 显示信息
echo.
echo ================================================
echo ✅ 已启动所有服务！
echo ================================================
echo.
echo 📍 后端服务: http://127.0.0.1:5000
echo 📍 前端服务: http://127.0.0.1:5173 (或其他端口)
echo.
echo 💡 提示: 两个服务均在独立窗口运行
echo        按 Ctrl+C 停止对应服务
echo.
pause
