#!/bin/bash

# Docker部署测试脚本

echo "==============================================="
echo "PCB 阻抗计算器 - Docker 部署测试"
echo "==============================================="

# 检查Docker环境
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose 未安装"
    exit 1
fi

echo "✅ Docker 环境检查通过"

# 构建并启动服务
echo "🔨 构建并启动服务..."
docker-compose up --build -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 30

# 测试后端
echo "🔍 测试后端服务..."
if curl -f http://localhost:5000/api/health > /dev/null 2>&1; then
    echo "✅ 后端服务正常"
else
    echo "❌ 后端服务异常"
    exit 1
fi

# 测试前端
echo "🔍 测试前端服务..."
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ 前端服务正常"
else
    echo "❌ 前端服务异常"
    exit 1
fi

# 测试CORS
echo "🔍 测试CORS配置..."
CORS_HEADER=$(curl -H "Origin: http://192.168.1.100:3000" -s -I http://localhost:5000/api/health | grep -i "access-control-allow-origin")
if [[ $CORS_HEADER == *"*"* ]]; then
    echo "✅ CORS配置正确"
else
    echo "❌ CORS配置异常"
fi

echo ""
echo "🎉 部署测试完成！"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📍 前端: http://localhost:3000"
echo "📍 后端: http://localhost:5000"
echo "📍 日志: docker-compose logs -f"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"