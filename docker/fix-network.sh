#!/bin/bash

# PCB计算器 Docker 网络问题修复脚本

echo "🔧 PCB计算器 Docker 网络问题修复脚本"
echo "=================================="

# 获取服务器IP地址
SERVER_IP=$(hostname -I | awk '{print $1}')
echo "📍 检测到服务器IP: $SERVER_IP"

# 检查是否存在.env文件
FRONTEND_ENV="src/frontend/.env"
BACKEND_ENV="src/backend/.env"

echo "📝 配置环境文件..."

# 创建前端环境文件
if [ ! -f "$FRONTEND_ENV" ]; then
    cp src/frontend/.env.example "$FRONTEND_ENV"
    echo "✅ 创建前端环境文件: $FRONTEND_ENV"
fi

# 创建后端环境文件
if [ ! -f "$BACKEND_ENV" ]; then
    cp src/backend/.env.example "$BACKEND_ENV"
    echo "✅ 创建后端环境文件: $BACKEND_ENV"
fi

# 提供配置选项
echo ""
echo "🚀 请选择部署方式:"
echo "1) Docker容器间通信 (推荐)"
echo "2) 使用服务器IP地址: $SERVER_IP"
echo "3) 自定义IP地址"

read -p "请输入选择 (1-3): " choice

case $choice in
    1)
        echo "🐳 配置Docker容器间通信..."
        # docker-compose.yml已经配置为使用backend服务名
        echo "✅ 使用容器服务名 'backend' 进行通信"
        ;;
    2)
        echo "🌐 配置服务器IP通信..."
        sed -i "s|VITE_API_URL=.*|VITE_API_URL=http://$SERVER_IP:5000/api|" "$FRONTEND_ENV"
        echo "✅ 前端API地址设置为: http://$SERVER_IP:5000/api"
        ;;
    3)
        read -p "请输入自定义IP地址: " CUSTOM_IP
        sed -i "s|VITE_API_URL=.*|VITE_API_URL=http://$CUSTOM_IP:5000/api|" "$FRONTEND_ENV"
        echo "✅ 前端API地址设置为: http://$CUSTOM_IP:5000/api"
        ;;
    *)
        echo "❌ 无效选择，使用默认配置"
        ;;
esac

echo ""
echo "🔄 重启Docker服务..."

# 停止现有服务
docker-compose down

# 重新构建并启动
docker-compose up --build -d

echo ""
echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
echo "📊 检查服务状态:"
docker-compose ps

echo ""
echo "🧪 测试API连接:"

# 测试后端API
if curl -s http://localhost:5000/health > /dev/null; then
    echo "✅ 后端API连接正常"
else
    echo "❌ 后端API连接失败"
fi

# 测试前端
if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ 前端服务正常"
else
    echo "❌ 前端服务异常"
fi

echo ""
echo "📋 访问信息:"
echo "前端地址: http://localhost:3000"
echo "前端地址: http://$SERVER_IP:3000"
echo "后端API: http://localhost:5000/api"
echo "后端API: http://$SERVER_IP:5000/api"

echo ""
echo "📚 如果仍有问题，请查看:"
echo "- 部署文档: docker/DEPLOYMENT.md"
echo "- 容器日志: docker-compose logs"
echo "- 故障排除: docker/TROUBLESHOOTING.md"

echo ""
echo "🎉 修复脚本执行完成！"