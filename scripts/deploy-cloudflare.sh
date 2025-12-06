#!/bin/bash

# Cloudflare部署脚本
# 用于构建和部署前后端到Cloudflare

set -e

echo "🚀 Zcal项目 Cloudflare部署"
echo "================================"

# 检查环境
if ! command -v wrangler &> /dev/null; then
    echo "❌ 未找到wrangler，正在安装..."
    npm install -g wrangler
fi

if ! command -v git &> /dev/null; then
    echo "❌ 未找到git"
    exit 1
fi

# 更新环境变量
echo "📝 配置Cloudflare环境变量"
read -p "请输入Cloudflare账户ID: " CF_ACCOUNT_ID
read -p "请输入Cloudflare API Token: " CF_API_TOKEN
read -p "请输入域名(例如 example.com): " DOMAIN

export CLOUDFLARE_ACCOUNT_ID=$CF_ACCOUNT_ID
export CLOUDFLARE_API_TOKEN=$CF_API_TOKEN

# 更新配置文件
sed -i "s/account_id = \"\"/account_id = \"$CF_ACCOUNT_ID\"/" wrangler.toml
sed -i "s|https://example.com|https://$DOMAIN|g" wrangler.toml
sed -i "s|api.example.com|api.$DOMAIN|g" wrangler.toml

# 1. 构建后端Worker
echo ""
echo "📦 构建后端Worker..."
cd src/backend
npm install
# 如果需要编译Python到JavaScript，可以使用pyodide或其他工具
# wrangler build
cd ../..

# 2. 构建前端
echo ""
echo "📦 构建前端..."
cd src/frontend
npm install
npm run build
cd ../..

# 3. 部署后端到Workers
echo ""
echo "🚀 部署后端到Cloudflare Workers..."
cd src/backend
wrangler deploy
cd ../..

# 4. 部署前端到Pages
echo ""
echo "🚀 部署前端到Cloudflare Pages..."
cd src/frontend
# 需要在Cloudflare Pages项目中配置
# wrangler pages deploy dist/
echo "请执行以下命令来部署前端:"
echo "wrangler pages publish dist/ --project-name=pcb-impedance-calculator"
cd ../..

echo ""
echo "✅ 部署脚本完成！"
echo "================================"
echo "后端API: https://api.$DOMAIN"
echo "前端: https://$DOMAIN"
echo ""
echo "下一步：在Cloudflare仪表板配置DNS和SSL/TLS设置"
