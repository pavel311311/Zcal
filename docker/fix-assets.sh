#!/bin/bash
# 修复Docker中的静态资源问题

set -e

echo "==============================================="
echo "修复 Docker 静态资源问题"
echo "==============================================="

# 进入项目根目录
cd "$(dirname "$0")/.."

echo "🔧 修复前端构建配置..."

# 1. 清理前端构建缓存
echo "🧹 清理构建缓存..."
cd src/frontend
rm -rf dist/ node_modules/.vite/

# 2. 重新安装依赖
echo "📦 重新安装依赖..."
npm ci

# 3. 本地构建测试
echo "🔨 本地构建测试..."
npm run build

# 4. 检查构建产物
echo "📁 检查构建产物..."
ls -la dist/
ls -la dist/assets/

# 5. 验证index.html中的资源路径
echo "🔍 检查index.html资源路径..."
cat dist/index.html

# 回到docker目录
cd ../../docker

# 6. 重新构建Docker镜像
echo "🐳 重新构建Docker镜像..."
docker-compose build --no-cache frontend

# 7. 启动服务
echo "🚀 启动服务..."
docker-compose up -d

# 8. 等待服务启动
echo "⏳ 等待服务启动..."
sleep 10

# 9. 检查服务状态
echo "📊 检查服务状态..."
docker-compose ps

# 10. 测试访问
echo "🌐 测试前端访问..."
curl -I http://localhost:3000/ || echo "❌ 前端访问失败"

echo "🌐 测试静态资源..."
# 获取index.html中的资源文件名
ASSETS=$(curl -s http://localhost:3000/ | grep -o '/assets/[^"]*' | head -3)
for asset in $ASSETS; do
    echo "测试资源: $asset"
    curl -I "http://localhost:3000$asset" || echo "❌ 资源访问失败: $asset"
done

echo ""
echo "✅ 修复完成！"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📍 前端地址: http://localhost:3000"
echo "📍 后端地址: http://localhost:5000"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""