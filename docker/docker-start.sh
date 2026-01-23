#!/bin/bash

# Docker 容器启动脚本
# 基于 scripts/start-all.sh 但适配容器环境

set -e
PROJECT_ROOT="/app"

echo "==============================================="
echo "启动 PCB 阻抗计算器 (Docker 容器)"
echo "==============================================="

# 创建Python虚拟环境
VENV_PATH="$PROJECT_ROOT/.venv"
echo "📦 创建Python虚拟环境..."
python3 -m venv "$VENV_PATH"
source "$VENV_PATH/bin/activate"

# 安装后端依赖
echo "📦 安装后端依赖..."
BACKEND_DIR="$PROJECT_ROOT/src/backend"
REQUIREMENTS_FILE="$BACKEND_DIR/requirements.txt"
if [ -f "$REQUIREMENTS_FILE" ]; then
    pip install --no-cache-dir -r "$REQUIREMENTS_FILE"
fi

# 安装前端依赖
echo "📦 安装前端依赖..."
FRONTEND_DIR="$PROJECT_ROOT/src/frontend"
cd "$FRONTEND_DIR"
npm ci --only=production
npm install -g serve

# 构建前端
echo "🔨 构建前端..."
npm run build

# 设置环境变量
export FLASK_ENV=production
export FLASK_PORT=5000
export CORS_ORIGINS=*

echo "🚀 启动服务..."

# 启动后端服务（后台运行）
cd "$BACKEND_DIR"
source "$VENV_PATH/bin/activate"
python run.py &
BACKEND_PID=$!

# 等待后端启动
sleep 5

# 启动前端服务
cd "$FRONTEND_DIR"
serve -s dist -l 3000 &
FRONTEND_PID=$!

echo "✅ 服务启动完成!"
echo "前端: http://localhost:3000"
echo "后端: http://localhost:5000"

# 保持容器运行
trap 'kill $BACKEND_PID $FRONTEND_PID; exit' SIGTERM SIGINT
wait