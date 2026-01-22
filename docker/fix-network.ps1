# PCB计算器 Docker 网络问题修复脚本 (PowerShell版本)

Write-Host "🔧 PCB计算器 Docker 网络问题修复脚本" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan

# 获取本机IP地址
$ServerIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -notlike "127.*" -and $_.IPAddress -notlike "169.*"} | Select-Object -First 1).IPAddress
Write-Host "📍 检测到服务器IP: $ServerIP" -ForegroundColor Green

# 检查是否存在.env文件
$FrontendEnv = "src/frontend/.env"
$BackendEnv = "src/backend/.env"

Write-Host "📝 配置环境文件..." -ForegroundColor Yellow

# 创建前端环境文件
if (-not (Test-Path $FrontendEnv)) {
    Copy-Item "src/frontend/.env.example" $FrontendEnv
    Write-Host "✅ 创建前端环境文件: $FrontendEnv" -ForegroundColor Green
}

# 创建后端环境文件
if (-not (Test-Path $BackendEnv)) {
    Copy-Item "src/backend/.env.example" $BackendEnv
    Write-Host "✅ 创建后端环境文件: $BackendEnv" -ForegroundColor Green
}

# 提供配置选项
Write-Host ""
Write-Host "🚀 请选择部署方式:" -ForegroundColor Cyan
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
Write-Host "🔄 重启Docker服务..." -ForegroundColor Yellow

# 停止现有服务
docker-compose down

# 重新构建并启动
docker-compose up --build -d

Write-Host ""
Write-Host "⏳ 等待服务启动..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# 检查服务状态
Write-Host "📊 检查服务状态:" -ForegroundColor Cyan
docker-compose ps

Write-Host ""
Write-Host "🧪 测试API连接:" -ForegroundColor Cyan

# 测试后端API
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000/health" -TimeoutSec 5 -ErrorAction Stop
    Write-Host "✅ 后端API连接正常" -ForegroundColor Green
} catch {
    Write-Host "❌ 后端API连接失败" -ForegroundColor Red
}

# 测试前端
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3000" -TimeoutSec 5 -ErrorAction Stop
    Write-Host "✅ 前端服务正常" -ForegroundColor Green
} catch {
    Write-Host "❌ 前端服务异常" -ForegroundColor Red
}

Write-Host ""
Write-Host "📋 访问信息:" -ForegroundColor Cyan
Write-Host "前端地址: http://localhost:3000"
Write-Host "前端地址: http://$ServerIP:3000"
Write-Host "后端API: http://localhost:5000/api"
Write-Host "后端API: http://$ServerIP:5000/api"

Write-Host ""
Write-Host "📚 如果仍有问题，请查看:" -ForegroundColor Yellow
Write-Host "- 部署文档: docker/DEPLOYMENT.md"
Write-Host "- 容器日志: docker-compose logs"
Write-Host "- 故障排除: docker/TROUBLESHOOTING.md"

Write-Host ""
Write-Host "🎉 修复脚本执行完成！" -ForegroundColor Green