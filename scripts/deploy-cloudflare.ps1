# Cloudflare 部署脚本 (PowerShell版)
# 用于在Windows上构建和部署项目到Cloudflare

param(
    [string]$AccountId,
    [string]$ApiToken,
    [string]$Domain
)

Write-Host "🚀 Zcal项目 Cloudflare部署" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# 检查必要工具
Write-Host "🔍 检查必要工具..." -ForegroundColor Yellow

$tools = @('node', 'npm', 'git')
foreach ($tool in $tools) {
    if (!(Get-Command $tool -ErrorAction SilentlyContinue)) {
        Write-Host "❌ 未找到 $tool" -ForegroundColor Red
        exit 1
    }
}

# 检查和安装wrangler
if (!(Get-Command wrangler -ErrorAction SilentlyContinue)) {
    Write-Host "📥 安装wrangler..." -ForegroundColor Yellow
    npm install -g wrangler
}

# 交互式输入
if (-not $AccountId) {
    $AccountId = Read-Host "请输入Cloudflare账户ID"
}
if (-not $ApiToken) {
    $ApiToken = Read-Host "请输入Cloudflare API Token" -AsSecureString
    $ApiToken = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToCoTaskMemUnicode($ApiToken))
}
if (-not $Domain) {
    $Domain = Read-Host "请输入域名(例如 example.com)"
}

# 设置环境变量
Write-Host "📝 配置Cloudflare环境变量..." -ForegroundColor Yellow
$env:CLOUDFLARE_ACCOUNT_ID = $AccountId
$env:CLOUDFLARE_API_TOKEN = $ApiToken

# 更新wrangler.toml
Write-Host "⚙️  更新配置文件..." -ForegroundColor Yellow
(Get-Content wrangler.toml) -replace 'account_id = ""', "account_id = `"$AccountId`"" | Set-Content wrangler.toml
(Get-Content wrangler.toml) -replace 'https://example.com', "https://$Domain" | Set-Content wrangler.toml
(Get-Content wrangler.toml) -replace 'api.example.com', "api.$Domain" | Set-Content wrangler.toml

# 1. 构建后端
Write-Host "`n📦 构建后端Worker..." -ForegroundColor Yellow
Push-Location "src/backend"
npm install 2>&1 | Out-Null
Pop-Location

# 2. 构建前端
Write-Host "📦 构建前端..." -ForegroundColor Yellow
Push-Location "src/frontend"
npm install 2>&1 | Out-Null
npm run build 2>&1 | Out-Null
Pop-Location

# 3. 部署后端
Write-Host "`n🚀 部署后端到Cloudflare Workers..." -ForegroundColor Yellow
Push-Location "src/backend"
wrangler deploy
$BackendDeployed = $?
Pop-Location

# 4. 部署前端
Write-Host "`n🚀 部署前端到Cloudflare Pages..." -ForegroundColor Yellow
Write-Host "请执行以下命令手动部署前端:" -ForegroundColor Cyan
Write-Host "cd src\frontend" -ForegroundColor Green
Write-Host "wrangler pages deploy dist/ --project-name=pcb-impedance-calculator" -ForegroundColor Green

Write-Host "`n✅ 部署脚本完成！" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host "后端API: https://api.$Domain" -ForegroundColor Cyan
Write-Host "前端: https://$Domain" -ForegroundColor Cyan
Write-Host "`n📋 下一步：在Cloudflare仪表板配置DNS和SSL/TLS设置" -ForegroundColor Yellow
