# 第一阶段：前端构建
FROM node:16-alpine AS frontend-build
WORKDIR /app/frontend
COPY src/frontend/ .
RUN npm install && npm run build

# 第二阶段：主镜像
FROM python:3.11-slim
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    nginx \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# 复制后端代码
COPY src/backend/ .
RUN pip install --upgrade pip
# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制前端构建产物
COPY --from=frontend-build /app/frontend/dist /var/www/html

# 配置Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# 配置Supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# 设置环境变量
ENV FLASK_ENV=production
ENV FLASK_PORT=5000
ENV CORS_ORIGINS=*

# 暴露端口
EXPOSE 80

# 启动Supervisor
CMD ["/usr/bin/supervisord"]