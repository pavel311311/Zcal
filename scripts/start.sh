#!/bin/bash
# filepath: /home/pi/code/lala/RFZ-calculate/scripts/start.sh

# 定义scripts目录路径
SCRIPTS_DIR="/home/pi/code/lala/RFZ-calculate/scripts"
PROJECT_DIR="/home/pi/code/lala/RFZ-calculate"

# 创建日志目录（如果不存在）
mkdir -p "$SCRIPTS_DIR"

# 进入项目目录
cd "$PROJECT_DIR"

# 激活虚拟环境（如果存在）
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "已激活虚拟环境"
fi

# 检查gunicorn是否可用，优先使用gunicorn作为生产服务器
if command -v gunicorn &> /dev/null && [ -f "$PROJECT_DIR/gunicorn_config.py" ]; then
    echo "使用 gunicorn 配置启动应用..."
    cd "$PROJECT_DIR"
    gunicorn -c gunicorn_config.py app:app
    
    if [ -f "$SCRIPTS_DIR/gunicorn.pid" ]; then
        APP_PID=$(cat "$SCRIPTS_DIR/gunicorn.pid")
        echo "RFZ-calculate Flask应用已启动（gunicorn），PID: $APP_PID"
        # 创建兼容的app.pid文件
        echo $APP_PID > "$SCRIPTS_DIR/app.pid"
    else
        echo "启动失败，请检查日志文件 $SCRIPTS_DIR/error.log"
        exit 1
    fi
elif command -v gunicorn &> /dev/null; then
    echo "使用 gunicorn 默认配置启动应用..."
    cd "$PROJECT_DIR/src"
    gunicorn -w 2 -b 0.0.0.0:5000 app:app --daemon \
        --pid "$SCRIPTS_DIR/app.pid" \
        --log-file "$SCRIPTS_DIR/app.log" \
        --log-level info \
        --access-logfile "$SCRIPTS_DIR/access.log"
    
    if [ -f "$SCRIPTS_DIR/app.pid" ]; then
        APP_PID=$(cat "$SCRIPTS_DIR/app.pid")
        echo "RFZ-calculate Flask应用已启动（gunicorn），PID: $APP_PID"
    else
        echo "启动失败，请检查日志"
        exit 1
    fi
else
    echo "gunicorn 不可用，使用 Flask 开发服务器..."
    # 启动Flask应用
    cd "$PROJECT_DIR/src"
    /usr/bin/python3 app.py > "$SCRIPTS_DIR/app.log" 2>&1 &
    APP_PID=$!
    
    # 保存PID到scripts目录
    echo $APP_PID > "$SCRIPTS_DIR/app.pid"
    
    echo "RFZ-calculate Flask应用已启动（开发模式），PID: $APP_PID"
    
    # 等待进程
    wait $APP_PID
fi

echo "日志文件: $SCRIPTS_DIR/app.log"
echo "应用地址: http://0.0.0.0:5000"