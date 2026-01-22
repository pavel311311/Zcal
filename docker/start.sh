#!/bin/bash
# Docker 启动和修复脚本 - 一键解决所有问题

set -e

echo "==============================================="
echo "PCB 阻抗计算器 Docker 启动"
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

# 进入项目根目录
cd "$(dirname "$0")/.."

# 解析命令行参数
CLEAN_BUILD=false
QUICK_START=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --clean)
            CLEAN_BUILD=true
            shift
            ;;
        --quick)
            QUICK_START=true
            shift
            ;;
        --help|-h)
            echo "用法: $0 [选项]"
            echo "选项:"
            echo "  --clean   完全清理后重新构建"
            echo "  --quick   快速启动（跳过缓存清理和本地构建验证）"
            echo "  --help    显示此帮助信息"
            exit 0
            ;;
        *)
            echo "未知选项: $1"
            echo "使用 --help 查看帮助"
            exit 1
            ;;
    esac
done

# 进入docker目录
cd docker

echo "� 停止现有服务..."
docker-compose down --remove-orphans

if [ "$CLEAN_BUILD" = true ]; then
    echo "🧹 完全清理（镜像、卷、缓存）..."
    docker-compose down --rmi all --volumes --remove-orphans
    docker system prune -f
fi

if [ "$QUICK_START" = false ]; then
    echo "📦 清理前端缓存..."
    cd ../src/frontend
    rm -rf dist/ node_modules/.vite/ 2>/dev/null || true

    echo "📦 检查依赖..."
    if [ ! -d "node_modules" ] || [ ! -f "package-lock.json" ]; then
        echo "📦 安装依赖..."
        npm ci
    fi

    echo "🔨 本地构建验证..."
    npm run build

    echo "📁 验证构建产物..."
    if [ ! -f "dist/index.html" ]; then
        echo "❌ 构建失败：index.html 不存在"
        exit 1
    fi

    if [ ! -d "dist/assets" ]; then
        echo "❌ 构建失败：assets 目录不存在"
        exit 1
    fi

    ASSET_COUNT=$(find dist/assets -type f | wc -l)
    echo "✅ 构建成功：assets 目录包含 $ASSET_COUNT 个文件"

    # 检查index.html中的资源引用
    if grep -q '/assets/' dist/index.html; then
        echo "✅ 资源路径配置正确"
    else
        echo "⚠️ 警告：index.html 中可能缺少资源引用"
    fi

    cd ../../docker
fi

echo "🔨 构建 Docker 镜像..."
if [ "$CLEAN_BUILD" = true ]; then
    docker-compose build --no-cache
else
    docker-compose build
fi

echo "🚀 启动服务..."
docker-compose up -d

echo "⏳ 等待服务启动..."
sleep 15

echo "📊 检查服务状态..."
docker-compose ps

echo "🏥 健康检查..."
# 后端健康检查
if curl -f -s http://localhost:5000/health > /dev/null; then
    echo "✅ 后端服务正常"
else
    echo "❌ 后端健康检查失败"
fi

# 前端健康检查
if curl -f -s http://localhost:3000/health > /dev/null; then
    echo "✅ 前端服务正常"
else
    echo "❌ 前端健康检查失败"
fi

echo "🌐 测试前端页面..."
if curl -f -s http://localhost:3000/ > /dev/null; then
    echo "✅ 前端页面访问正常"
    
    # 测试静态资源
    echo "🔍 测试静态资源..."
    ASSETS=$(curl -s http://localhost:3000/ | grep -o '/assets/[^"]*' | head -3)
    ASSET_OK=0
    ASSET_TOTAL=0
    
    for asset in $ASSETS; do
        ASSET_TOTAL=$((ASSET_TOTAL + 1))
        if curl -f -s "http://localhost:3000$asset" > /dev/null; then
            ASSET_OK=$((ASSET_OK + 1))
        fi
    done
    
    if [ $ASSET_TOTAL -gt 0 ]; then
        echo "✅ 静态资源测试: $ASSET_OK/$ASSET_TOTAL 个文件正常"
    fi
else
    echo "❌ 前端页面访问失败"
    echo "🔍 检查容器日志:"
    docker-compose logs frontend | tail -10
fi

echo ""
echo "✅ 启动完成！"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📍 前端应用: http://localhost:3000"
echo "📍 后端API: http://localhost:5000"
echo "📍 API健康检查: http://localhost:5000/health"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "💡 查看日志: docker-compose logs -f"
echo "💡 停止服务: docker-compose down"
echo "💡 完全重建: $0 --clean"
echo "💡 快速启动: $0 --quick"
echo ""