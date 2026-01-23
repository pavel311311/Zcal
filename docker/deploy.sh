#!/bin/bash

# PCB阻抗计算器 Docker部署脚本

echo "🚀 开始部署PCB阻抗计算器..."

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

# 进入docker目录
cd "$(dirname "$0")"

# 停止现有容器
echo "🛑 停止现有容器..."
docker-compose down

# 清理旧镜像（可选）
echo "🧹 清理旧镜像..."
docker-compose down --rmi all --volumes --remove-orphans 2>/dev/null || true

# 构建并启动服务
echo "🔨 构建并启动服务..."
docker-compose up --build -d

# 检查服务状态
echo "⏳ 等待服务启动..."
sleep 10

# 检查后端健康状态
echo "🔍 检查后端服务..."
if curl -f http://localhost:5000/ > /dev/null 2>&1; then
    echo "✅ 后端服务运行正常"
else
    echo "❌ 后端服务启动失败"
    docker-compose logs backend
    exit 1
fi

# 检查前端健康状态
echo "🔍 检查前端服务..."
if curl -f http://localhost/health > /dev/null 2>&1; then
    echo "✅ 前端服务运行正常"
else
    echo "❌ 前端服务启动失败"
    docker-compose logs frontend
    exit 1
fi

echo ""
echo "🎉 部署完成！"
echo "📱 前端访问地址: http://localhost"
echo "🔧 后端API地址: http://localhost:5000"
echo ""
echo "📊 查看服务状态: docker-compose ps"
echo "📋 查看日志: docker-compose logs -f"
echo "🛑 停止服务: docker-compose down"