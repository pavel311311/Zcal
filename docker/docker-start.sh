#!/bin/bash

# Docker 容器启动脚本
# 确保跨设备访问无问题

set -e

echo "==============================================="
echo "启动 PCB 阻抗计算器 (Docker 容器)"
echo "==============================================="

# 设置环境变量 - 关键：允许所有来源的CORS访问
export CORS_ORIGINS="*"
export FLASK_ENV="production"
export FLASK_PORT="5000"

echo "🔧 环境配置:"
echo "   CORS_ORIGINS: $CORS_ORIGINS"
echo "   FLASK_ENV: $FLASK_ENV"
echo "   FLASK_PORT: $FLASK_PORT"

# 激活Python虚拟环境
source /app/.venv/bin/activate

echo "🚀 启动后端服务..."
cd /app/src/backend
python run.py &
BACKEND_PID=$!
echo "   后端 PID: $BACKEND_PID"

# 等待后端启动
echo "⏳ 等待后端服务启动..."
sleep 5

# 测试后端是否启动成功
if curl -f http://localhost:5000/api/health > /dev/null 2>&1; then
    echo "✅ 后端服务启动成功"
else
    echo "❌ 后端服务启动失败"
    exit 1
fi

echo "🚀 启动前端服务..."
cd /app/src/frontend
serve -s dist -l 3000 &
FRONTEND_PID=$!
echo "   前端 PID: $FRONTEND_PID"

echo ""
echo "✅ 服务启动完成!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📍 前端服务: http://localhost:3000"
echo "📍 后端服务: http://localhost:5000"
echo "📍 API健康检查: http://localhost:5000/api/health"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "💡 容器支持跨设备访问，CORS已配置为允许所有来源"
echo ""

# 优雅关闭处理
cleanup() {
    echo "🛑 正在停止服务..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    wait $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    echo "✅ 服务已停止"
    exit 0
}

trap cleanup SIGTERM SIGINT

# 保持容器运行
wait