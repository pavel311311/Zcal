#!/bin/bash

# RFZ-calculate 项目服务管理脚本
# 用于配置树莓派开机自启动服务

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 配置变量
PROJECT_DIR="/home/pi/code/lala/RFZ-calculate"
SERVICE_NAME="rfz-calculate"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
START_SCRIPT="${PROJECT_DIR}/scripts/start.sh"
STOP_SCRIPT="${PROJECT_DIR}/scripts/stop.sh"

# 检查是否以root权限运行
check_root() {
    if [ "$EUID" -ne 0 ]; then
        echo -e "${RED}错误: 请使用 sudo 运行此脚本${NC}"
        echo "示例: sudo bash $0"
        exit 1
    fi
}

# 检查必要文件是否存在
check_files() {
    if [ ! -f "$START_SCRIPT" ]; then
        echo -e "${RED}错误: 找不到启动脚本 $START_SCRIPT${NC}"
        exit 1
    fi
    
    if [ ! -f "$STOP_SCRIPT" ]; then
        echo -e "${RED}错误: 找不到停止脚本 $STOP_SCRIPT${NC}"
        exit 1
    fi
    
    if [ ! -f "$PROJECT_DIR/src/app.py" ]; then
        echo -e "${RED}错误: 找不到Flask应用文件 $PROJECT_DIR/src/app.py${NC}"
        exit 1
    fi
}

# 创建systemd服务文件
create_service() {
    echo -e "${BLUE}正在创建 systemd 服务文件...${NC}"
    
    cat > "$SERVICE_FILE" << SERVICEEOF
[Unit]
Description=RFZ-calculate Flask Application Service
After=network-online.target
Wants=network-online.target

[Service]
Type=exec
User=pi
Group=pi
WorkingDirectory=$PROJECT_DIR
ExecStart=$START_SCRIPT
ExecStop=$STOP_SCRIPT
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal
Environment=FLASK_ENV=production
Environment=PYTHONPATH=$PROJECT_DIR/src

[Install]
WantedBy=multi-user.target
SERVICEEOF

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ 服务文件创建成功${NC}"
    else
        echo -e "${RED}✗ 服务文件创建失败${NC}"
        exit 1
    fi
}

# 安装服务
install_service() {
    echo -e "${YELLOW}开始安装 RFZ-calculate 项目开机自启动服务...${NC}"
    echo ""
    
    # 检查文件
    check_files
    
    # 创建服务文件
    create_service
    
    # 确保启动脚本可执行
    chmod +x "$START_SCRIPT"
    chmod +x "$STOP_SCRIPT"
    
    # 创建日志目录
    mkdir -p "$PROJECT_DIR/logs"
    chown pi:pi "$PROJECT_DIR/logs"
    
    # 重新加载systemd配置
    echo -e "${BLUE}重新加载 systemd 配置...${NC}"
    systemctl daemon-reload
    
    # 启用服务
    echo -e "${BLUE}启用开机自启动...${NC}"
    systemctl enable "$SERVICE_NAME"
    
    if [ $? -eq 0 ]; then
        echo ""
        echo -e "${GREEN}🎉 服务安装成功！${NC}"
        echo ""
        echo -e "${BLUE}服务状态:${NC}"
        systemctl status "$SERVICE_NAME" --no-pager -l
        echo ""
        echo -e "${YELLOW}可用命令:${NC}"
        echo "  启动服务: sudo systemctl start $SERVICE_NAME"
        echo "  停止服务: sudo systemctl stop $SERVICE_NAME"
        echo "  重启服务: sudo systemctl restart $SERVICE_NAME"
        echo "  查看状态: sudo systemctl status $SERVICE_NAME"
        echo "  查看日志: sudo journalctl -u $SERVICE_NAME -f"
        echo "  查看应用日志: tail -f $PROJECT_DIR/scripts/app.log"
        echo ""
        
        # 询问是否立即启动服务
        read -p "是否现在启动服务? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            systemctl start "$SERVICE_NAME"
            echo -e "${GREEN}✓ 服务已启动${NC}"
            echo -e "${BLUE}Flask应用应该在 http://localhost:5000 运行${NC}"
        fi
    else
        echo -e "${RED}✗ 服务安装失败${NC}"
        exit 1
    fi
}

# 卸载服务
uninstall_service() {
    echo -e "${YELLOW}开始卸载 RFZ-calculate 项目开机自启动服务...${NC}"
    echo ""
    
    # 检查服务是否存在
    if [ ! -f "$SERVICE_FILE" ]; then
        echo -e "${YELLOW}服务文件不存在，可能已经卸载${NC}"
        return 0
    fi
    
    # 停止服务
    echo -e "${BLUE}停止服务...${NC}"
    systemctl stop "$SERVICE_NAME" 2>/dev/null
    
    # 禁用服务
    echo -e "${BLUE}禁用开机自启动...${NC}"
    systemctl disable "$SERVICE_NAME" 2>/dev/null
    
    # 删除服务文件
    echo -e "${BLUE}删除服务文件...${NC}"
    rm -f "$SERVICE_FILE"
    
    # 重新加载systemd配置
    echo -e "${BLUE}重新加载 systemd 配置...${NC}"
    systemctl daemon-reload
    
    echo ""
    echo -e "${GREEN}🗑️ 服务卸载完成！${NC}"
}

# 查看服务状态
show_status() {
    if [ -f "$SERVICE_FILE" ]; then
        echo -e "${BLUE}服务状态:${NC}"
        systemctl status "$SERVICE_NAME" --no-pager -l
        echo ""
        echo -e "${BLUE}最近系统日志:${NC}"
        journalctl -u "$SERVICE_NAME" --no-pager -n 20
        echo ""
        if [ -f "$PROJECT_DIR/scripts/app.log" ]; then
            echo -e "${BLUE}最近应用日志:${NC}"
            tail -n 20 "$PROJECT_DIR/scripts/app.log"
        fi
    else
        echo -e "${YELLOW}服务未安装${NC}"
    fi
}

# 显示帮助信息
show_help() {
    echo -e "${BLUE}RFZ-calculate 项目服务管理脚本${NC}"
    echo ""
    echo -e "${YELLOW}用法:${NC}"
    echo "  sudo bash $0 [选项]"
    echo ""
    echo -e "${YELLOW}选项:${NC}"
    echo "  install   - 安装开机自启动服务"
    echo "  uninstall - 卸载开机自启动服务"
    echo "  status    - 查看服务状态和日志"
    echo "  help      - 显示此帮助信息"
    echo ""
    echo -e "${YELLOW}示例:${NC}"
    echo "  sudo bash $0 install     # 安装服务"
    echo "  sudo bash $0 uninstall   # 卸载服务"
    echo "  sudo bash $0 status      # 查看状态"
    echo ""
    echo -e "${YELLOW}注意:${NC}"
    echo "  - 服务启动后，Flask应用将在 http://localhost:5000 运行"
    echo "  - 应用日志存储在: $PROJECT_DIR/scripts/app.log"
    echo "  - 系统日志可通过: sudo journalctl -u $SERVICE_NAME -f 查看"
}

# 主函数
main() {
    case "$1" in
        "install")
            check_root
            install_service
            ;;
        "uninstall")
            check_root
            uninstall_service
            ;;
        "status")
            show_status
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        "")
            echo -e "${YELLOW}请指定操作选项。使用 'help' 查看帮助信息。${NC}"
            echo ""
            show_help
            ;;
        *)
            echo -e "${RED}错误: 未知选项 '$1'${NC}"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# 运行主函数
main "$@"