# PowerShell 启动脚本 - Windows

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "PCB 阻抗计算器 - 启动脚本" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# 检查是否安装了Docker
$dockerInstalled = $null
try {
    $dockerInstalled = docker --version 2>$null
}
catch {}

if ($null -eq $dockerInstalled) {
    Write-Host "❌ Docker 未安装，请先安装 Docker Desktop" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Docker 已安装" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 使用 Docker Compose 启动服务..." -ForegroundColor Yellow
docker-compose up -d

Write-Host ""
Write-Host "✅ 服务启动完成！" -ForegroundColor Green
Write-Host ""
Write-Host "📍 访问地址：" -ForegroundColor Cyan
Write-Host "   - 前端应用: http://localhost:3000" -ForegroundColor White
Write-Host "   - 后端API: http://localhost:5000/api" -ForegroundColor White
Write-Host "   - 健康检查: http://localhost:5000/health" -ForegroundColor White
Write-Host ""
Write-Host "📋 查看日志：" -ForegroundColor Cyan
Write-Host "   docker-compose logs -f" -ForegroundColor Gray
Write-Host ""
Write-Host "🛑 停止服务：" -ForegroundColor Cyan
Write-Host "   docker-compose down" -ForegroundColor Gray
Write-Host ""
