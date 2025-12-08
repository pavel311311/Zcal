# 一键启动前后端服务脚本 (单窗口版本 - 后端和前端同时运行)
# 使用 Start-Job 在后台启动服务

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "启动 PCB 阻抗计算器 (前后端服务 - 单窗口版)" -ForegroundColor Green
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

# 激活虚拟环境并安装依赖
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
}

Write-Host ""
Write-Host "🚀 启动服务..." -ForegroundColor Green
Write-Host ""

# 启动后端服务 (后台Job)
$backendJob = Start-Job -ScriptBlock {
    param($ProjectRoot, $venvPath)
    & "$venvPath\Scripts\Activate.ps1"
    cd (Join-Path $ProjectRoot 'src\backend')
    python run.py
} -ArgumentList $ProjectRoot, $venvPath -Name "Backend"

Write-Host "✅ 后端服务已启动 (Job ID: $($backendJob.Id))" -ForegroundColor Green

Start-Sleep -Seconds 2

# 启动前端服务
$frontendJob = Start-Job -ScriptBlock {
    param($ProjectRoot)
    cd (Join-Path $ProjectRoot 'src\frontend')
    npm run dev
} -ArgumentList $ProjectRoot -Name "Frontend"

Write-Host "✅ 前端服务已启动 (Job ID: $($frontendJob.Id))" -ForegroundColor Green
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "📍 后端服务: http://127.0.0.1:5000" -ForegroundColor Yellow
Write-Host "📍 前端服务: http://127.0.0.1:5173 (或其他端口)" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 查看日志命令:" -ForegroundColor Cyan
Write-Host "  后端日志: Receive-Job -Job $($backendJob.Id) -Keep" -ForegroundColor Gray
Write-Host "  前端日志: Receive-Job -Job $($frontendJob.Id) -Keep" -ForegroundColor Gray
Write-Host ""
Write-Host "🛑 停止服务命令:" -ForegroundColor Cyan
Write-Host "  Stop-Job -Job $($backendJob.Id), $($frontendJob.Id)" -ForegroundColor Gray
Write-Host "  Remove-Job -Job $($backendJob.Id), $($frontendJob.Id)" -ForegroundColor Gray
Write-Host ""
Write-Host "💡 提示: 监视服务状态..." -ForegroundColor Cyan

# 监视服务
while ($true) {
    $backendState = (Get-Job -Id $backendJob.Id).State
    $frontendState = (Get-Job -Id $frontendJob.Id).State
    
    if ($backendState -eq "Failed" -or $backendState -eq "Stopped") {
        Write-Host "⚠️  后端服务已停止 (状态: $backendState)" -ForegroundColor Red
        break
    }
    if ($frontendState -eq "Failed" -or $frontendState -eq "Stopped") {
        Write-Host "⚠️  前端服务已停止 (状态: $frontendState)" -ForegroundColor Red
        break
    }
    
    Start-Sleep -Seconds 5
}

Write-Host ""
Write-Host "停止所有服务..." -ForegroundColor Yellow
Get-Job -Name "Backend", "Frontend" | Stop-Job
Get-Job -Name "Backend", "Frontend" | Remove-Job
Write-Host "✅ 已清理所有服务" -ForegroundColor Green
