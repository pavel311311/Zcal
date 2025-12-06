# 一键启动/停止 前后端服务（Windows PowerShell）

此文档说明如何使用仓库根目录提供的 `start_all.ps1` 与 `stop_all.ps1`，在 Windows（PowerShell/PowerShell Core）上一键启动或停止本地开发用的前后端服务。

前置条件：
- 已安装 Python（并建议使用项目根目录的 `.venv` 虚拟环境）
- 已安装 Node.js 与 npm
- 在首次运行前，建议先在 `frontend/` 目录运行 `npm install`

快速使用：

1. 启动服务

在仓库根目录打开 PowerShell（或 PowerShell Core）并运行：

```powershell
# 可直接双击或在 PowerShell 中运行
.\start_all.ps1
```

脚本会在两个新的 PowerShell 窗口中分别启动：
- 后端：`python backend/run.py`（若存在 `.venv`，脚本会自动激活）
- 前端：`npm run dev`（在 `frontend/` 目录）

脚本会把两个进程的 PID 保存到仓库根目录的 `start_all.pids` 文件，方便后续停止。

2. 停止服务

在仓库根目录运行：

```powershell
.\stop_all.ps1
```

该脚本会读取 `start_all.pids` 并尝试停止对应的进程，随后删除 PID 文件。

故障排查：
- 如果前端没有启动，确认已在 `frontend/` 运行 `npm install` 并且 `npm run dev` 在本机可用。
- 如果后端无法启动，确认 Python 与依赖已安装（可在仓库根目录创建并激活 `.venv`，然后安装 `backend/requirements.txt`）。
- 如果 `start_all.pids` 文件不存在或内容无效，`stop_all.ps1` 会提示并安全退出。

备注：
- 本脚本为开发方便设计，会在新窗口中启动命令以便查看日志。若需要在后台运行（无新窗口），可自行修改脚本使用 PowerShell 作业或其他守护进程方案。

