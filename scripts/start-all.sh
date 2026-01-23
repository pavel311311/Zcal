#!/bin/bash

# 一键启动前后端服务脚本 (Linux 版本)
# 在后台启动后端和前端服务

set -e
# 获取项目根目录（scripts的上级目录）
PROJECT_ROOT=$(dirname "$(dirname "$(readlink -f "$0")")")

echo "==============================================="
echo "启动 PCB 阻抗计算器 (前后端服务)"
echo "==============================================="

# 检查后端虚拟环境
VENV_PATH="$PROJECT_ROOT/.venv"
if [ ! -d "$VENV_PATH" ]; then
    echo "❌ 未找到虚拟环境，正在创建..."
    python3 -m venv "$VENV_PATH"
    if [ $? -ne 0 ]; then
        echo "❌ 虚拟环境创建失败"
        exit 1
    fi
fi

# 激活虚拟环境并安装/更新依赖
echo "📦 激活虚拟环境..."
source "$VENV_PATH/bin/activate"

echo "📦 检查后端依赖..."
BACKEND_DIR="$PROJECT_ROOT/src/backend"
REQUIREMENTS_FILE="$BACKEND_DIR/requirements.txt"
if [ -f "$REQUIREMENTS_FILE" ]; then
    pip install -q -r "$REQUIREMENTS_FILE"
    if [ $? -ne 0 ]; then
        echo "❌ 后端依赖安装失败"
        exit 1
    fi
fi

# 检查前端依赖
FRONTEND_DIR="$PROJECT_ROOT/src/frontend"
echo "📦 检查前端依赖..."
if [ -d "$FRONTEND_DIR" ]; then
    NPM_LOCK="$FRONTEND_DIR/package-lock.json"
    cd "$FRONTEND_DIR"
    if [ ! -f "$NPM_LOCK" ]; then
        echo "⚠️  package-lock.json 不存在，首次安装中..."
        npm install
    else
        npm ci --audit=false --fund=false 2>/dev/null
    fi
    if [ $? -ne 0 ]; then
        echo "⚠️  前端依赖检查完成（继续启动）"
    fi
    cd "$PROJECT_ROOT"
fi

# 启动后端服务 (在后台)
echo "🚀 启动后端服务..."
source "$VENV_PATH/bin/activate"
cd "$BACKEND_DIR"

# 设置环境变量允许跨域访问
export CORS_ORIGINS="*"
export FLASK_ENV="production"

echo '================================' > /tmp/backend.log
echo 'Flask 后端服务运行中...' >> /tmp/backend.log
echo '127.0.0.1:5000' >> /tmp/backend.log
echo 'CORS_ORIGINS=*' >> /tmp/backend.log
echo '按 Ctrl+C 停止' >> /tmp/backend.log
echo '================================' >> /tmp/backend.log
nohup python3 run.py >> /tmp/backend.log 2>&1 &
BACKEND_PID=$!
echo "后端 PID: $BACKEND_PID"

# 启动前端服务 (在后台)
echo "🚀 启动前端服务..."
cd "$FRONTEND_DIR"
echo '================================' > /tmp/frontend.log
echo 'Vite 前端服务运行中...' >> /tmp/frontend.log
echo '按 Ctrl+C 停止' >> /tmp/frontend.log
echo '================================' >> /tmp/frontend.log
nohup npm run dev >> /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!
echo "前端 PID: $FRONTEND_PID"

echo ""
echo "✅ 已启动所有服务！"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📍 后端服务: http://127.0.0.1:5000"
echo "📍 前端服务: http://127.0.0.1:3000 (或其他端口)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "💡 提示: 服务在后台运行，使用 kill $BACKEND_PID 和 kill $FRONTEND_PID 停止服务"
echo "💡 日志文件: /tmp/backend.log 和 /tmp/frontend.log"
echo ""