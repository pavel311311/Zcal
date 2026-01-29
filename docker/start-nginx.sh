#!/bin/bash

# 设置默认API地址
DEFAULT_API_URL="http://backend:5000/api"

# 从环境变量获取API地址，如果没有设置则使用默认值
API_URL=${VITE_API_URL:-$DEFAULT_API_URL}

# 生成配置文件，将API地址注入到前端
cat > /usr/share/nginx/html/config.js << EOF
window.__APP_CONFIG__ = {
  API_URL: "$API_URL"
};
EOF

# 确保配置文件可读
chmod +r /usr/share/nginx/html/config.js

# 打印启动信息
echo "================================"
echo "前端服务启动配置"
echo "================================"
echo "API基础地址: $API_URL"
echo "================================"

# 启动Nginx
exec nginx -g "daemon off;"
