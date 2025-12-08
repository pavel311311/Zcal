# 一键启动前后端服务脚本
# 在不同的PowerShell窗口中启动后端和前端

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "启动 PCB 阻抗计算器 (前后端服务)" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Cyan

# 检查后端虚拟环境
$venvPath = Join-Path $ProjectRoot ".venv"
if (-not (Test-Path $venvPath)) {
    Write-Host "❌ 未找到虚拟环境，正在创建..." -ForegroundColor Yellow
    python -m venv $venvPath
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ 虚拟环境创建失败" -ForegroundColor Red
        exit 1
    }
}

# 激活虚拟环境并安装/更新依赖
Write-Host "📦 激活虚拟环境..." -ForegroundColor Cyan
& "$venvPath\Scripts\Activate.ps1"

Write-Host "📦 检查后端依赖..." -ForegroundColor Cyan
$backendDir = Join-Path $ProjectRoot "src\backend"
$requirementsFile = Join-Path $backendDir "requirements.txt"
if (Test-Path $requirementsFile) {
    pip install -q -r $requirementsFile
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ 后端依赖安装失败" -ForegroundColor Red
        exit 1
    }
}

# 检查前端依赖
$frontendDir = Join-Path $ProjectRoot "src\frontend"
Write-Host "📦 检查前端依赖..." -ForegroundColor Cyan
if (Test-Path $frontendDir) {
    $npmLock = Join-Path $frontendDir "package-lock.json"
    if (-not (Test-Path $npmLock)) {
        Write-Host "⚠️  package-lock.json 不存在，首次安装中..." -ForegroundColor Yellow
        Push-Location $frontendDir
        npm install
        Pop-Location
    } else {
        Push-Location $frontendDir
        npm ci --audit=false --fund=false 2>$null
        Pop-Location
    }
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️  前端依赖检查完成（继续启动）" -ForegroundColor Yellow
    }
}

# 启动后端服务 (在新窗口中)
Write-Host "🚀 启动后端服务..." -ForegroundColor Green
$backendScript = @"
`$ErrorActionPreference = 'Stop'
`$ProjectRoot = '$ProjectRoot'
`$venvPath = Join-Path `$ProjectRoot '.venv'
& "`$venvPath\Scripts\Activate.ps1"
cd (Join-Path `$ProjectRoot 'src\backend')
Write-Host '================================' -ForegroundColor Cyan
Write-Host 'Flask 后端服务运行中...' -ForegroundColor Green
Write-Host '127.0.0.1:5000' -ForegroundColor Yellow
Write-Host '按 Ctrl+C 停止' -ForegroundColor Yellow
Write-Host '================================' -ForegroundColor Cyan
python run.py
Read-Host '按 Enter 关闭窗口'
"@
Start-Process powershell -ArgumentList "-NoExit -Command $backendScript" -WindowStyle Normal

# 启动前端服务 (在新窗口中)
Write-Host "🚀 启动前端服务..." -ForegroundColor Green
$frontendScript = @"
`$ProjectRoot = '$ProjectRoot'
cd (Join-Path `$ProjectRoot 'src\frontend')
Write-Host '================================' -ForegroundColor Cyan
Write-Host 'Vite 前端服务运行中...' -ForegroundColor Green
Write-Host '按 Ctrl+C 停止' -ForegroundColor Yellow
Write-Host '================================' -ForegroundColor Cyan
npm run dev
Read-Host '按 Enter 关闭窗口'
"@
Start-Process powershell -ArgumentList "-NoExit -Command $frontendScript" -WindowStyle Normal

Write-Host ""
Write-Host "✅ 已启动所有服务！" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "📍 后端服务: http://127.0.0.1:5000" -ForegroundColor Yellow
Write-Host "📍 前端服务: http://127.0.0.1:5173 (或其他端口)" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "💡 提示: 两个服务均在独立窗口运行，按 Ctrl+C 停止对应服务" -ForegroundColor Cyan
Write-Host ""
