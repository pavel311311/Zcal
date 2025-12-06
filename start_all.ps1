<#
.SYNOPSIS
    一键在两个新的 PowerShell 窗口中启动后端和前端服务，并记录进程 ID。

.NOTES
    - 在仓库根目录运行（右键运行或在 PowerShell 中执行）：
        .\start_all.ps1
    - 需要已安装 Python、Node.js/npm。推荐使用仓库根目录的 `.venv` 虚拟环境（如果存在）。
    - 会把 PID 保存到 `start_all.pids` 文件，`stop_all.ps1` 使用它来停止服务。
#>

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$pidFile = Join-Path $root 'start_all.pids'

Write-Host "Repository root: $root"

# locate venv activate script if exists
$venvActivate = Join-Path $root '.venv\Scripts\Activate.ps1'
if (-not (Test-Path $venvActivate)) {
    $venvActivate = Join-Path $root 'venv\Scripts\Activate.ps1'
}

# Backend command: activate venv if available then run backend
if (Test-Path $venvActivate) {
    $backendCommand = "& '$venvActivate'; Set-Location -Path '$root\backend'; python run.py"
}
else {
    $backendCommand = "Set-Location -Path '$root\backend'; python run.py"
}

# Frontend command
$frontendCommand = "Set-Location -Path '$root\frontend'; npm run dev"

Write-Host 'Starting backend in new pwsh window...'
$backendProc = Start-Process -FilePath 'pwsh' -ArgumentList '-NoExit','-Command',$backendCommand -PassThru

Write-Host 'Starting frontend in new pwsh window...'
$frontendProc = Start-Process -FilePath 'pwsh' -ArgumentList '-NoExit','-Command',$frontendCommand -PassThru

# Save PIDs to file
$pidObj = @{ backend = $backendProc.Id; frontend = $frontendProc.Id }
$pidObj | ConvertTo-Json | Out-File -FilePath $pidFile -Encoding UTF8

Write-Host "Started backend (PID=$($backendProc.Id)) and frontend (PID=$($frontendProc.Id))."
Write-Host "PIDs saved to $pidFile"
Write-Host "Backend: http://localhost:5000  Frontend: http://localhost:3000"
