#!/bin/bash

# 定义scripts目录路径
SCRIPTS_DIR="/home/pi/code/lala/RFZ-calculate/scripts"

# 杀死Flask应用进程
if [ -f "$SCRIPTS_DIR/app.pid" ]; then
    kill $(cat "$SCRIPTS_DIR/app.pid") 2>/dev/null
    rm "$SCRIPTS_DIR/app.pid"
    echo "已停止Flask应用进程"
fi

# 杀死gunicorn主进程
if [ -f "$SCRIPTS_DIR/gunicorn.pid" ]; then
    kill $(cat "$SCRIPTS_DIR/gunicorn.pid") 2>/dev/null
    rm "$SCRIPTS_DIR/gunicorn.pid"
    echo "已停止gunicorn主进程"
fi

# 强制杀死所有python3 app.py进程（防止残留）
ps aux | grep "python3 app.py" | grep -v grep | awk '{print $2}' | xargs -r kill -9

# 强制杀死所有gunicorn相关进程（防止残留）
ps aux | grep "gunicorn.*app:app" | grep -v grep | awk '{print $2}' | xargs -r kill -9

# 强制杀死所有Flask相关进程（防止残留）
ps aux | grep "flask" | grep -v grep | awk '{print $2}' | xargs -r kill -9

echo "RFZ-calculate project stopped"