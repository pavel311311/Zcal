# Docker 一键修复脚本
$ErrorActionPreference = "Stop"

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "Docker 静态资源问题一键修复" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Cyan

# 进入 docker 目录
Set-Location $PSScriptRoot

Write-Host "🛑 停止现有服务..." -ForegroundColor Yellow
docker-compose down --volumes --remove-orphans

Write-Host "🧹 清理旧镜像和缓存..." -ForegroundColor Yellow
docker-compose down --rmi all
docker system prune -f

Write-Host "📦 清理前端缓存..." -ForegroundColor Cyan
Set-Location "../src/frontend"
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "node_modules/.vite") { Remove-Item -Recurse -Force "node_modules/.vite" }

Write-Host "📦 重新安装依赖..." -ForegroundColor Cyan
npm ci

Write-Host "🔨 本地构建测试..." -ForegroundColor Cyan
npm run build

Write-Host "📁 检查构建产物..." -ForegroundColor Cyan
if (Test-Path "dist/index.html") {
    Write-Host "✅ index.html 存在" -ForegroundColor Green
} else {
    Write-Host "❌ index.html 不存在" -ForegroundColor Red
    exit 1
}

if (Test-Path "dist/assets") {
    $assetCount = (Get-ChildItem "dist/assets" | Measure-Object).Count
    Write-Host "✅ assets 目录存在，包含 $assetCount 个文件" -ForegroundColor Green
} else {
    Write-Host "❌ assets 目录不存在" -ForegroundColor Red
    exit 1
}

Write-Host "🔍 检查 index.html 内容..." -ForegroundColor Cyan
$indexContent = Get-Content "dist/index.html" -Raw
if ($indexContent -match '/assets/') {
    Write-Host "✅ 资源路径正确" -ForegroundColor Green
} else {
    Write-Host "❌ 资源路径可能有问题" -ForegroundColor Red
}

Write-Host "🐳 重新构建 Docker 镜像..." -ForegroundColor Cyan
Set-Location "../../docker"
docker-compose build --no-cache

Write-Host "🚀 启动服务..." -ForegroundColor Green
docker-compose up -d

Write-Host "⏳ 等待服务启动..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

Write-Host "📊 检查服务状态..." -ForegroundColor Cyan
docker-compose ps

Write-Host "🏥 健康检查..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3000/health" -UseBasicParsing -TimeoutSec 10
    Write-Host "✅ 前端健康检查通过" -ForegroundColor Green
} catch {
    Write-Host "❌ 前端健康检查失败: $($_.Exception.Message)" -ForegroundColor Red
}

try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000/health" -UseBasicParsing -TimeoutSec 10
    Write-Host "✅ 后端健康检查通过" -ForegroundColor Green
} catch {
    Write-Host "❌ 后端健康检查失败: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "🌐 测试前端页面..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3000/" -UseBasicParsing -TimeoutSec 10
    Write-Host "✅ 前端页面访问成功 (状态码: $($response.StatusCode))" -ForegroundColor Green
    
    # 检查返回的HTML中是否包含正确的资源引用
    if ($response.Content -match '/assets/') {
        Write-Host "✅ 页面包含正确的资源引用" -ForegroundColor Green
    } else {
        Write-Host "⚠️ 页面可能缺少资源引用" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ 前端页面访问失败: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "📋 检查容器内文件..." -ForegroundColor Cyan
try {
    $htmlFiles = docker exec pcb-calculator-frontend find /usr/share/nginx/html -name "*.html" 2>$null
    $jsFiles = docker exec pcb-calculator-frontend find /usr/share/nginx/html -name "*.js" 2>$null
    $cssFiles = docker exec pcb-calculator-frontend find /usr/share/nginx/html -name "*.css" 2>$null
    
    Write-Host "HTML 文件: $($htmlFiles.Count)" -ForegroundColor Yellow
    Write-Host "JS 文件: $($jsFiles.Count)" -ForegroundColor Yellow  
    Write-Host "CSS 文件: $($cssFiles.Count)" -ForegroundColor Yellow
} catch {
    Write-Host "⚠️ 无法检查容器内文件" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "✅ 修复完成！" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "📍 前端地址: http://localhost:3000" -ForegroundColor Yellow
Write-Host "📍 后端地址: http://localhost:5000" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "💡 如果仍有问题，请查看 TROUBLESHOOTING.md" -ForegroundColor Cyan
Write-Host "💡 查看日志: docker-compose logs -f" -ForegroundColor Cyan
Write-Host ""