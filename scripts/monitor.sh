#!/bin/bash

# RFZ-calculate 应用状态监控脚本
# 用于检查应用运行状态和健康度

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

PROJECT_DIR="/home/pi/code/lala/RFZ-calculate"
SCRIPTS_DIR="$PROJECT_DIR/scripts"

echo -e "${BLUE}RFZ-calculate 应用状态监控${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# 检查进程状态
check_process() {
    echo -e "${YELLOW}进程状态检查:${NC}"
    
    # 检查 PID 文件
    if [ -f "$SCRIPTS_DIR/app.pid" ]; then
        APP_PID=$(cat "$SCRIPTS_DIR/app.pid")
        if ps -p $APP_PID > /dev/null 2>&1; then
            echo -e "${GREEN}✓ 应用进程运行中 (PID: $APP_PID)${NC}"
        else
            echo -e "${RED}✗ PID 文件存在但进程未运行${NC}"
        fi
    elif [ -f "$SCRIPTS_DIR/gunicorn.pid" ]; then
        GUNICORN_PID=$(cat "$SCRIPTS_DIR/gunicorn.pid")
        if ps -p $GUNICORN_PID > /dev/null 2>&1; then
            echo -e "${GREEN}✓ Gunicorn 主进程运行中 (PID: $GUNICORN_PID)${NC}"
            
            # 检查 worker 进程
            WORKER_COUNT=$(pgrep -P $GUNICORN_PID | wc -l)
            echo -e "${BLUE}  Worker 进程数: $WORKER_COUNT${NC}"
        else
            echo -e "${RED}✗ Gunicorn PID 文件存在但进程未运行${NC}"
        fi
    else
        echo -e "${RED}✗ 未找到 PID 文件${NC}"
    fi
    
    # 检查相关进程
    PYTHON_PROCESSES=$(ps aux | grep -E "python3.*app\.py" | grep -v grep | wc -l)
    GUNICORN_PROCESSES=$(ps aux | grep -E "gunicorn.*app:app" | grep -v grep | wc -l)
    
    echo -e "${BLUE}相关进程统计:${NC}"
    echo "  Python app.py 进程: $PYTHON_PROCESSES"
    echo "  Gunicorn 进程: $GUNICORN_PROCESSES"
    echo ""
}

# 检查网络连接
check_network() {
    echo -e "${YELLOW}网络连接检查:${NC}"
    
    # 检查端口监听
    if netstat -tlnp 2>/dev/null | grep :5000 > /dev/null; then
        PORT_INFO=$(netstat -tlnp 2>/dev/null | grep :5000)
        echo -e "${GREEN}✓ 端口 5000 正在监听${NC}"
        echo "  $PORT_INFO"
    else
        echo -e "${RED}✗ 端口 5000 未监听${NC}"
    fi
    
    # 测试 HTTP 连接
    if command -v curl &> /dev/null; then
        HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000 2>/dev/null)
        if [ "$HTTP_STATUS" = "200" ]; then
            echo -e "${GREEN}✓ HTTP 服务正常 (状态码: $HTTP_STATUS)${NC}"
        else
            echo -e "${RED}✗ HTTP 服务异常 (状态码: ${HTTP_STATUS:-无响应})${NC}"
        fi
    else
        echo -e "${YELLOW}! curl 未安装，无法测试 HTTP 连接${NC}"
    fi
    echo ""
}

# 检查日志文件
check_logs() {
    echo -e "${YELLOW}日志文件检查:${NC}"
    
    # 检查日志文件大小和最后修改时间
    for logfile in "app.log" "error.log" "access.log"; do
        LOGPATH="$SCRIPTS_DIR/$logfile"
        if [ -f "$LOGPATH" ]; then
            SIZE=$(du -h "$LOGPATH" | cut -f1)
            MODIFIED=$(stat -c %y "$LOGPATH" | cut -d. -f1)
            echo -e "${GREEN}✓ $logfile${NC} - 大小: $SIZE, 最后修改: $MODIFIED"
        fi
    done
    echo ""
}

# 检查资源使用
check_resources() {
    echo -e "${YELLOW}资源使用检查:${NC}"
    
    # 内存使用
    if command -v free &> /dev/null; then
        MEMORY_INFO=$(free -h | grep Mem)
        echo -e "${BLUE}内存使用:${NC} $MEMORY_INFO"
    fi
    
    # CPU 负载
    if [ -f /proc/loadavg ]; then
        LOAD_AVG=$(cat /proc/loadavg | cut -d' ' -f1-3)
        echo -e "${BLUE}CPU 负载:${NC} $LOAD_AVG"
    fi
    
    # 磁盘空间
    DISK_USAGE=$(df -h "$PROJECT_DIR" | tail -1)
    echo -e "${BLUE}磁盘使用:${NC} $DISK_USAGE"
    echo ""
}

# 显示最近的日志
show_recent_logs() {
    echo -e "${YELLOW}最近日志 (最后 5 行):${NC}"
    
    for logfile in "error.log" "app.log" "access.log"; do
        LOGPATH="$SCRIPTS_DIR/$logfile"
        if [ -f "$LOGPATH" ] && [ -s "$LOGPATH" ]; then
            echo -e "${BLUE}--- $logfile ---${NC}"
            tail -n 5 "$LOGPATH"
            echo ""
        fi
    done
}

# 主函数
main() {
    case "$1" in
        "process"|"proc")
            check_process
            ;;
        "network"|"net")
            check_network
            ;;
        "logs"|"log")
            check_logs
            show_recent_logs
            ;;
        "resources"|"res")
            check_resources
            ;;
        "all"|"")
            check_process
            check_network
            check_logs
            check_resources
            ;;
        "help"|"-h"|"--help")
            echo "用法: $0 [选项]"
            echo ""
            echo "选项:"
            echo "  all       - 完整状态检查 (默认)"
            echo "  process   - 仅检查进程状态"
            echo "  network   - 仅检查网络连接"
            echo "  logs      - 仅检查日志文件"
            echo "  resources - 仅检查资源使用"
            echo "  help      - 显示此帮助信息"
            ;;
        *)
            echo -e "${RED}未知选项: $1${NC}"
            echo "使用 '$0 help' 查看帮助信息"
            exit 1
            ;;
    esac
}

# 运行主函数
main "$@"