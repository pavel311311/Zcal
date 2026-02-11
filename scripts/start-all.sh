#!/bin/bash

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CMD="${1:-start}"
VENV_PATH="$PROJECT_ROOT/.venv"
BACKEND_DIR="$PROJECT_ROOT/src/backend"
FRONTEND_DIR="$PROJECT_ROOT/src/frontend"
PID_FILE="/tmp/zcal.pids"
FLASK_PORT="${FLASK_PORT:-5001}"

start() {
    echo "==============================================="
    echo "启动 PCB 阻抗计算器 (前后端服务)"
    echo "==============================================="

    if [ ! -d "$VENV_PATH" ]; then
        echo "❌ 未找到虚拟环境，正在创建..."
        python3 -m venv "$VENV_PATH"
        if [ $? -ne 0 ]; then
            echo "❌ 虚拟环境创建失败"
            exit 1
        fi
    fi

    echo "📦 激活虚拟环境..."
    source "$VENV_PATH/bin/activate"

    echo "📦 检查后端依赖..."
    REQUIREMENTS_FILE="$BACKEND_DIR/requirements.txt"
    if [ -f "$REQUIREMENTS_FILE" ]; then
        pip install -q -r "$REQUIREMENTS_FILE" || {
            echo "❌ 后端依赖安装失败"
            exit 1
        }
    fi

    echo "📦 检查前端依赖..."
    if [ -d "$FRONTEND_DIR" ]; then
        NPM_LOCK="$FRONTEND_DIR/package-lock.json"
        cd "$FRONTEND_DIR"
        if [ ! -f "$NPM_LOCK" ]; then
            npm install
        else
            npm ci --audit=false --fund=false 2>/dev/null || true
        fi
        cd "$PROJECT_ROOT"
    fi

    echo "🚀 启动后端服务..."
    source "$VENV_PATH/bin/activate"
    cd "$BACKEND_DIR"
    export CORS_ORIGINS="*"
    export FLASK_ENV="production"
    export FLASK_PORT="$FLASK_PORT"
    echo '================================' > /tmp/backend.log
    echo 'Flask 后端服务运行中...' >> /tmp/backend.log
    echo "127.0.0.1:$FLASK_PORT" >> /tmp/backend.log
    echo 'CORS_ORIGINS=*' >> /tmp/backend.log
    echo '按 Ctrl+C 停止' >> /tmp/backend.log
    echo '================================' >> /tmp/backend.log
    nohup python3 run.py >> /tmp/backend.log 2>&1 &
    BACKEND_PID=$!
    echo "后端 PID: $BACKEND_PID"

    echo "🚀 启动前端服务..."
    cd "$FRONTEND_DIR"
    export VITE_API_URL="http://127.0.0.1:$FLASK_PORT/api"
    echo '================================' > /tmp/frontend.log
    echo 'Vite 前端服务运行中...' >> /tmp/frontend.log
    echo '按 Ctrl+C 停止' >> /tmp/frontend.log
    echo '================================' >> /tmp/frontend.log
    nohup npm run dev >> /tmp/frontend.log 2>&1 &
    FRONTEND_PID=$!
    echo "前端 PID: $FRONTEND_PID"

    echo "BACKEND_PID=$BACKEND_PID" > "$PID_FILE"
    echo "FRONTEND_PID=$FRONTEND_PID" >> "$PID_FILE"
    echo "FLASK_PORT=$FLASK_PORT" >> "$PID_FILE"

    echo ""
    echo "✅ 已启动所有服务！"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📍 后端服务: http://127.0.0.1:$FLASK_PORT"
    echo "📍 前端服务: http://127.0.0.1:3000"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "💡 日志文件: /tmp/backend.log 和 /tmp/frontend.log"
    echo ""
}

stop() {
    echo "🛑 正在停止服务..."
    if [ -f "$PID_FILE" ]; then
        . "$PID_FILE"
        [ -n "$BACKEND_PID" ] && kill "$BACKEND_PID" 2>/dev/null || true
        [ -n "$FRONTEND_PID" ] && kill "$FRONTEND_PID" 2>/dev/null || true
        rm -f "$PID_FILE"
    fi
    for p in $(lsof -tiTCP:"${FLASK_PORT}" -sTCP:LISTEN); do kill "$p" 2>/dev/null || true; done
    for p in $(lsof -tiTCP:3000 -sTCP:LISTEN); do kill "$p" 2>/dev/null || true; done
    pkill -f "python3 run.py" 2>/dev/null || true
    pkill -f "vite" 2>/dev/null || true
    pkill -f "node.*vite" 2>/dev/null || true
    echo "✅ 服务已停止"
}

status() {
    echo "📊 服务状态:"
    echo "- 后端端口: $FLASK_PORT"
    lsof -iTCP:"${FLASK_PORT}" -sTCP:LISTEN -P || true
    echo "- 前端端口: 3000"
    lsof -iTCP:3000 -sTCP:LISTEN -P || true
    [ -f "$PID_FILE" ] && echo "🔖 PID 文件: $(cat "$PID_FILE")" || echo "🔖 无 PID 文件"
}

case "$CMD" in
  start) start ;;
  stop) stop ;;
  status) status ;;
  *) echo "用法: $0 {start|stop|status}"; exit 1 ;;
esac
