#!/bin/bash
# Docker 启动脚本

set -e

echo "==============================================="
echo "启动 阻抗计算器 Docker 服务"
echo "==============================================="

# 检查 Docker 是否运行
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker 未运行，请先启动 Docker"
    exit 1
fi

# 检查 docker-compose 是否可用
if ! command -v docker-compose > /dev/null 2>&1; then
    echo "❌ docker-compose 未安装"
    exit 1
fi

# 进入 docker 目录
cd "$(dirname "$0")"

# 停止现有容器
echo "🛑 停止现有容器..."
docker-compose down --remove-orphans

# 清理旧镜像（可选）
if [ "$1" = "--clean" ]; then
    echo "🧹 清理旧镜像..."
    docker-compose down --rmi all --volumes --remove-orphans
fi

# 构建并启动服务
echo "🔨 构建镜像..."
docker-compose build --no-cache

echo "🚀 启动服务..."
docker-compose up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
echo "📊 检查服务状态..."
docker-compose ps

# 检查健康状态
echo "🏥 检查健康状态..."
echo "后端健康检查:"
curl -f http://localhost:5000/health || echo "❌ 后端健康检查失败"

echo "前端健康检查:"
curl -f http://localhost:3000/health || echo "❌ 前端健康检查失败"

echo ""
echo "✅ 部署完成！"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📍 前端地址: http://localhost:3000"
echo "📍 后端地址: http://localhost:5000"
echo "📍 API文档: http://localhost:5000/api"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "💡 查看日志: docker-compose logs -f"
echo "💡 停止服务: docker-compose down"
echo ""