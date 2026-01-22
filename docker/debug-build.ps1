# Docker 调试构建脚本
$ErrorActionPreference = "Stop"

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "Docker 调试构建" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Cyan

# 进入 docker 目录
Set-Location $PSScriptRoot

# 停止现有容器
Write-Host "🛑 停止现有容器..." -ForegroundColor Yellow
docker-compose down --remove-orphans

# 清理旧镜像
Write-Host "🧹 清理旧镜像..." -ForegroundColor Yellow
docker-compose down --rmi all --volumes --remove-orphans

# 单独构建前端镜像进行调试
Write-Host "🔨 构建前端镜像..." -ForegroundColor Cyan
docker build -f Dockerfile.frontend -t pcb-frontend-debug ../src/frontend

# 运行前端容器进行测试
Write-Host "🚀 启动前端容器..." -ForegroundColor Green
docker run -d --name pcb-frontend-test -p 3000:3000 pcb-frontend-debug

# 等待容器启动
Write-Host "⏳ 等待容器启动..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# 检查容器状态
Write-Host "📊 检查容器状态..." -ForegroundColor Cyan
docker ps | findstr pcb-frontend-test

# 检查容器内文件
Write-Host "📁 检查容器内文件..." -ForegroundColor Cyan
docker exec pcb-frontend-test ls -la /usr/share/nginx/html/
docker exec pcb-frontend-test ls -la /usr/share/nginx/html/assets/

# 检查nginx配置
Write-Host "⚙️ 检查nginx配置..." -ForegroundColor Cyan
docker exec pcb-frontend-test cat /etc/nginx/conf.d/default.conf

# 检查nginx日志
Write-Host "📋 检查nginx日志..." -ForegroundColor Cyan
docker logs pcb-frontend-test

# 测试访问
Write-Host "🌐 测试访问..." -ForegroundColor Green
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3000" -UseBasicParsing
    Write-Host "✅ 前端访问成功" -ForegroundColor Green
    Write-Host "响应状态: $($response.StatusCode)" -ForegroundColor Yellow
} catch {
    Write-Host "❌ 前端访问失败: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "🔍 调试信息:" -ForegroundColor Cyan
Write-Host "容器名称: pcb-frontend-test" -ForegroundColor Yellow
Write-Host "访问地址: http://localhost:3000" -ForegroundColor Yellow
Write-Host "停止容器: docker stop pcb-frontend-test" -ForegroundColor Yellow
Write-Host "删除容器: docker rm pcb-frontend-test" -ForegroundColor Yellow
Write-Host ""