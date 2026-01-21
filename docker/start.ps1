# Docker 启动脚本 (Windows PowerShell)

$ErrorActionPreference = "Stop"

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "启动 PCB 阻抗计算器 Docker 服务" -ForegroundColor Green
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

# 进入 docker 目录
Set-Location $PSScriptRoot

# 停止现有容器
Write-Host "🛑 停止现有容器..." -ForegroundColor Yellow
docker-compose down --remove-orphans

# 清理旧镜像（可选）
if ($args[0] -eq "--clean") {
    Write-Host "🧹 清理旧镜像..." -ForegroundColor Yellow
    docker-compose down --rmi all --volumes --remove-orphans
}

# 构建并启动服务
Write-Host "🔨 构建镜像..." -ForegroundColor Cyan
docker-compose build --no-cache

Write-Host "🚀 启动服务..." -ForegroundColor Green
docker-compose up -d

# 等待服务启动
Write-Host "⏳ 等待服务启动..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# 检查服务状态
Write-Host "📊 检查服务状态..." -ForegroundColor Cyan
docker-compose ps

# 检查健康状态
Write-Host "🏥 检查健康状态..." -ForegroundColor Cyan
Write-Host "后端健康检查:" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000/health" -UseBasicParsing
    Write-Host "✅ 后端服务正常" -ForegroundColor Green
} catch {
    Write-Host "❌ 后端健康检查失败" -ForegroundColor Red
}

Write-Host "前端健康检查:" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3000/health" -UseBasicParsing
    Write-Host "✅ 前端服务正常" -ForegroundColor Green
} catch {
    Write-Host "❌ 前端健康检查失败" -ForegroundColor Red
}

Write-Host ""
Write-Host "✅ 部署完成！" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "📍 前端地址: http://localhost:3000" -ForegroundColor Yellow
Write-Host "📍 后端地址: http://localhost:5000" -ForegroundColor Yellow
Write-Host "📍 API文档: http://localhost:5000/api" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "💡 查看日志: docker-compose logs -f" -ForegroundColor Cyan
Write-Host "💡 停止服务: docker-compose down" -ForegroundColor Cyan
Write-Host ""