<#
.SYNOPSIS
    停止由 `start_all.ps1` 启动的服务（通过 PID 文件）。

USAGE
    .\stop_all.ps1
#>

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$pidFile = Join-Path $root 'start_all.pids'

if (-not (Test-Path $pidFile)) {
    Write-Host "PID 文件未找到： $pidFile" -ForegroundColor Yellow
    Write-Host "可能没有使用 start_all.ps1 启动，或者进程已退出。"
    exit 0
}

try {
    $data = Get-Content -Path $pidFile -Raw | ConvertFrom-Json
}
catch {
    Write-Host "无法读取 PID 文件： $_" -ForegroundColor Red
    exit 1
}

if ($data.backend) {
    Write-Host "Stopping backend (PID=$($data.backend))..."
    Stop-Process -Id $data.backend -ErrorAction SilentlyContinue -Force
}

if ($data.frontend) {
    Write-Host "Stopping frontend (PID=$($data.frontend))..."
    Stop-Process -Id $data.frontend -ErrorAction SilentlyContinue -Force
}

Remove-Item -Path $pidFile -ErrorAction SilentlyContinue
Write-Host "Stopped processes and removed PID file."
