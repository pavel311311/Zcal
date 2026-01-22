# PCB 阻抗计算器 Docker 启动脚本 (Windows PowerShell)
# 整合了启动、修复、诊断、网络配置功能

param(
    [switch]$Clean,       # 完全清理重建
    [switch]$Quick,       # 快速启动
    [switch]$FixNetwork,  # 修复网络配置
    [switch]$Help         # 显示帮助
)

$ErrorActionPreference = "Stop"

if ($Help) {
    Write-Host "PCB 阻抗计算器 Docker 启动脚本" -ForegroundColor Green
    Write-Host ""
    Write-Host "用法: .\start.ps1 [选项]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "选项:" -ForegroundColor Cyan
    Write-Host "  -Clean       完全清理后重新构建" -ForegroundColor White
    Write-Host "  -Quick       快速启动（跳过缓存清理和验证）" -ForegroundColor White
    Write-Host "  -FixNetwork  修复网络配置问题" -ForegroundColor White
    Write-Host "  -Help        显示此帮助信息" -ForegroundColor White
    Write-Host ""
    Write-Host "示例:" -ForegroundColor Cyan
    Write-Host "  .\start.ps1              # 标准启动" -ForegroundColor White
    Write-Host "  .\start.ps1 -Clean       # 完全重建" -ForegroundColor White
    Write-Host "  .\start.ps1 -Quick       # 快速启动" -ForegroundColor White
    Write-Host "  .\start.ps1 -FixNetwork  # 修复网络配置" -ForegroundColor White
    exit 0
}

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "PCB 阻抗计算器 Docker 启动" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Cyan

# 检查 Docker 是否运行
try {
    docker info | Out-Null
} catch {
    Write-Host "❌ Docker 未运行，请先启动 Docker Desktop" -ForegroundColor Red
    exit 1
}

# 检查 docker-compose 是否可用
if (-not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    Write-Host "❌ docker-compose 未安装" -ForegroundColor Red
    exit 1
}

# 网络配置检测和修复
if ($FixNetwork) {
    Write-Host "🔧 网络配置检测和修复..." -ForegroundColor Yellow
    
    # 获取本机IP地址
    $ServerIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -notlike "127.*" -and $_.IPAddress -notlike "169.*"} | Select-Object -First 1).IPAddress
    if (-not $ServerIP) { $ServerIP = "localhost" }
    Write-Host "📍 检测到服务器IP: $ServerIP" -ForegroundColor Green
    
    # 检查环境文件
    $FrontendEnv = "../src/frontend/.env"
    $BackendEnv = "../src/backend/.env"
    
    # 创建前端环境文件
    if (-not (Test-Path $FrontendEnv)) {
        Copy-Item "../src/frontend/.env.example" $FrontendEnv
        Write-Host "✅ 创建前端环境文件: $FrontendEnv" -ForegroundColor Green
    }
    
    # 创建后端环境文件
    if (-not (Test-Path $BackendEnv)) {
        Copy-Item "../src/backend/.env.example" $BackendEnv
        Write-Host "✅ 创建后端环境文件: $BackendEnv" -ForegroundColor Green
    }
    
    Write-Host ""
    Write-Host "🚀 网络配置选项:" -ForegroundColor Cyan
    Write-Host "1) Docker容器间通信 (推荐)"
    Write-Host "2) 使用服务器IP地址: $ServerIP"
    Write-Host "3) 自定义IP地址"
    
    $choice = Read-Host "请输入选择 (1-3)"
    
    switch ($choice) {
        "1" {
            Write-Host "🐳 配置Docker容器间通信..." -ForegroundColor Blue
            Write-Host "✅ 使用容器服务名 'backend' 进行通信" -ForegroundColor Green
        }
        "2" {
            Write-Host "🌐 配置服务器IP通信..." -ForegroundColor Blue
            $content = Get-Content $FrontendEnv
            $content = $content -replace "VITE_API_URL=.*", "VITE_API_URL=http://$ServerIP:5000/api"
            Set-Content $FrontendEnv $content
            Write-Host "✅ 前端API地址设置为: http://$ServerIP:5000/api" -ForegroundColor Green
        }
        "3" {
            $CustomIP = Read-Host "请输入自定义IP地址"
            $content = Get-Content $FrontendEnv
            $content = $content -replace "VITE_API_URL=.*", "VITE_API_URL=http://$CustomIP:5000/api"
            Set-Content $FrontendEnv $content
            Write-Host "✅ 前端API地址设置为: http://$CustomIP:5000/api" -ForegroundColor Green
        }
        default {
            Write-Host "❌ 无效选择，使用默认配置" -ForegroundColor Red
        }
    }
    Write-Host ""
}

# 进入 docker 目录
Set-Location $PSScriptRoot

Write-Host "🛑 停止现有服务..." -ForegroundColor Yellow
docker-compose down --remove-orphans

if ($Clean) {
    Write-Host "🧹 完全清理（镜像、卷、缓存）..." -ForegroundColor Yellow
    docker-compose down --rmi all --volumes --remove-orphans
    docker system prune -f
}

if (-not $Quick) {
    Write-Host "📦 清理前端缓存..." -ForegroundColor Cyan
    Set-Location "../src/frontend"
    
    if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" -ErrorAction SilentlyContinue }
    if (Test-Path "node_modules/.vite") { Remove-Item -Recurse -Force "node_modules/.vite" -ErrorAction SilentlyContinue }

    Write-Host "📦 检查依赖..." -ForegroundColor Cyan
    if (-not (Test-Path "node_modules") -or -not (Test-Path "package-lock.json")) {
        Write-Host "📦 安装依赖..." -ForegroundColor Cyan
        npm ci
    }

    Write-Host "🔨 本地构建验证..." -ForegroundColor Cyan
    npm run build

    Write-Host "📁 验证构建产物..." -ForegroundColor Cyan
    if (-not (Test-Path "dist/index.html")) {
        Write-Host "❌ 构建失败：index.html 不存在" -ForegroundColor Red
        exit 1
    }

    if (-not (Test-Path "dist/assets")) {
        Write-Host "❌ 构建失败：assets 目录不存在" -ForegroundColor Red
        exit 1
    }

    $assetCount = (Get-ChildItem "dist/assets" -File | Measure-Object).Count
    Write-Host "✅ 构建成功：assets 目录包含 $assetCount 个文件" -ForegroundColor Green

    # 检查index.html中的资源引用
    $indexContent = Get-Content "dist/index.html" -Raw
    if ($indexContent -match '/assets/') {
        Write-Host "✅ 资源路径配置正确" -ForegroundColor Green
    } else {
        Write-Host "⚠️ 警告：index.html 中可能缺少资源引用" -ForegroundColor Yellow
    }

    Set-Location "../../docker"
}

Write-Host "🔨 构建 Docker 镜像..." -ForegroundColor Cyan
if ($Clean) {
    docker-compose build --no-cache
} else {
    docker-compose build
}

Write-Host "🚀 启动服务..." -ForegroundColor Green
docker-compose up -d

Write-Host "⏳ 等待服务启动..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

Write-Host "📊 检查服务状态..." -ForegroundColor Cyan
docker-compose ps

Write-Host "🏥 健康检查..." -ForegroundColor Cyan

# 后端健康检查
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000/health" -UseBasicParsing -TimeoutSec 10
    Write-Host "✅ 后端服务正常" -ForegroundColor Green
} catch {
    Write-Host "❌ 后端健康检查失败" -ForegroundColor Red
    Write-Host "🔍 后端日志:" -ForegroundColor Yellow
    docker-compose logs backend | Select-Object -Last 5
}

# 前端页面检查
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3000/" -UseBasicParsing -TimeoutSec 10
    Write-Host "✅ 前端页面访问正常 (状态码: $($response.StatusCode))" -ForegroundColor Green
    
    # 测试静态资源
    Write-Host "🔍 测试静态资源..." -ForegroundColor Cyan
    $assets = [regex]::Matches($response.Content, '/assets/[^"]*') | ForEach-Object { $_.Value } | Select-Object -First 3
    $assetOk = 0
    $assetTotal = $assets.Count
    
    foreach ($asset in $assets) {
        try {
            $assetResponse = Invoke-WebRequest -Uri "http://localhost:3000$asset" -UseBasicParsing -TimeoutSec 5
            $assetOk++
        } catch {
            # 静默处理失败的资源
        }
    }
    
    if ($assetTotal -gt 0) {
        Write-Host "✅ 静态资源测试: $assetOk/$assetTotal 个文件正常" -ForegroundColor Green
    }
    
    # 测试API连接
    Write-Host "🔍 测试API连接..." -ForegroundColor Cyan
    try {
        $apiResponse = Invoke-WebRequest -Uri "http://localhost:5000/api/materials" -UseBasicParsing -TimeoutSec 10
        Write-Host "✅ API连接正常" -ForegroundColor Green
    } catch {
        Write-Host "❌ API连接失败 - 可能是网络配置问题" -ForegroundColor Red
        Write-Host "💡 尝试运行: .\start.ps1 -FixNetwork" -ForegroundColor Yellow
    }
    
} catch {
    Write-Host "❌ 前端页面访问失败: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "🔍 检查容器日志:" -ForegroundColor Yellow
    docker-compose logs frontend | Select-Object -Last 10
}

Write-Host ""
Write-Host "✅ 启动完成！" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "📍 前端应用: http://localhost:3000" -ForegroundColor Yellow
Write-Host "📍 后端API: http://localhost:5000" -ForegroundColor Yellow
Write-Host "📍 API健康检查: http://localhost:5000/health" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "💡 查看日志: docker-compose logs -f" -ForegroundColor Cyan
Write-Host "💡 停止服务: docker-compose down" -ForegroundColor Cyan
Write-Host "💡 完全重建: .\start.ps1 -Clean" -ForegroundColor Cyan
Write-Host "💡 快速启动: .\start.ps1 -Quick" -ForegroundColor Cyan
Write-Host "💡 修复网络: .\start.ps1 -FixNetwork" -ForegroundColor Cyan
Write-Host ""