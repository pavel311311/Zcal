FROM node:18-alpine

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production
ENV CORS_ORIGINS=*

# 安装Python和系统依赖
RUN apk add --no-cache \
    python3 \
    py3-pip \
    python3-dev \
    build-base \
    && ln -sf python3 /usr/bin/python

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY . .

# 创建Python虚拟环境并安装后端依赖
RUN python3 -m venv /app/.venv \
    && /app/.venv/bin/pip install --no-cache-dir -r src/backend/requirements.txt

# 安装前端依赖并构建
RUN cd src/frontend \
    && npm ci \
    && npm run build \
    && npm install -g serve

# 复制启动脚本并设置权限
COPY docker/docker-start.sh /app/docker-start.sh
RUN chmod +x /app/docker-start.sh

# 暴露端口
EXPOSE 3000 5000

# 启动服务
CMD ["/app/docker-start.sh"]