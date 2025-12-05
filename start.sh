#!/bin/bash
# 项目启动脚本 - Linux/Mac

echo "=========================================="
echo "PCB 阻抗计算器 - 启动脚本"
echo "=========================================="

# 检查是否安装了Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose 未安装，请先安装 Docker Compose"
    exit 1
fi

echo "🚀 使用 Docker Compose 启动服务..."
docker-compose up -d

echo ""
echo "✅ 服务启动完成！"
echo ""
echo "📍 访问地址："
echo "   - 前端应用: http://localhost:3000"
echo "   - 后端API: http://localhost:5000/api"
echo "   - 健康检查: http://localhost:5000/health"
echo ""
echo "📋 查看日志："
echo "   docker-compose logs -f"
echo ""
echo "🛑 停止服务："
echo "   docker-compose down"
