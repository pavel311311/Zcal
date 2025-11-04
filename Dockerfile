# 使用 Python 3.9 slim 镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=src/app.py \
    FLASK_ENV=production

# 安装系统依赖
# ###树莓派4B 不知道是不是翻墙的原因，更新系统经常卡死，算了，屏蔽了先。
#RUN apt-get update && apt-get install -y \
#    gcc \
#    curl \
#    && rm -rf /var/lib/apt/lists/*

# 复制 requirements.txt 并安装 Python 依赖（路径相对于构建上下文）
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件（从构建上下文根目录复制全部到 /app）
COPY . .

# 创建必要的目录
RUN mkdir -p /app/logs

# 创建非 root 用户
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# 暴露端口
EXPOSE 5000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# 启动应用
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "src.app:app"]
