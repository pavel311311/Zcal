#!/bin/bash

# RFZ-calculate 快速安装脚本
# 用于一键安装和配置 RFZ-calculate 项目

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

PROJECT_DIR="/home/pi/code/lala/RFZ-calculate"
SCRIPTS_DIR="$PROJECT_DIR/scripts"

echo -e "${BLUE}RFZ-calculate 项目快速安装脚本${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""

# 检查项目目录是否存在
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}错误: 项目目录不存在 $PROJECT_DIR${NC}"
    echo "请确保项目已正确克隆到指定位置"
    exit 1
fi

# 进入项目目录
cd "$PROJECT_DIR"

echo -e "${YELLOW}1. 检查 Python 环境...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}错误: Python3 未安装${NC}"
    echo "请安装 Python3: sudo apt update && sudo apt install python3 python3-pip"
    exit 1
fi
echo -e "${GREEN}✓ Python3 已安装${NC}"

echo -e "${YELLOW}2. 创建虚拟环境（可选）...${NC}"
if [ ! -d ".venv" ]; then
    read -p "是否创建 Python 虚拟环境? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python3 -m venv .venv
        echo -e "${GREEN}✓ 虚拟环境已创建${NC}"
    fi
fi

echo -e "${YELLOW}3. 安装 Python 依赖...${NC}"
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo -e "${BLUE}已激活虚拟环境${NC}"
fi

pip3 install -r requirements.txt
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Python 依赖安装完成${NC}"
else
    echo -e "${RED}✗ Python 依赖安装失败${NC}"
    exit 1
fi

echo -e "${YELLOW}4. 设置脚本权限...${NC}"
chmod +x "$SCRIPTS_DIR/start.sh"
chmod +x "$SCRIPTS_DIR/stop.sh"
chmod +x "$SCRIPTS_DIR/service_manager.sh"
echo -e "${GREEN}✓ 脚本权限设置完成${NC}"

echo -e "${YELLOW}5. 创建必要目录...${NC}"
mkdir -p "$SCRIPTS_DIR"
mkdir -p "$PROJECT_DIR/logs"
echo -e "${GREEN}✓ 目录结构创建完成${NC}"

echo -e "${YELLOW}6. 测试应用启动...${NC}"
cd "$PROJECT_DIR/src"
timeout 10 python3 -c "
import app
try:
    # 测试导入和基本功能
    calc = app.PCBImpedanceCalculator()
    print('应用模块加载成功')
except Exception as e:
    print(f'应用测试失败: {e}')
    exit(1)
"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ 应用测试通过${NC}"
else
    echo -e "${RED}✗ 应用测试失败${NC}"
    echo "请检查依赖是否正确安装"
fi

echo ""
echo -e "${GREEN}🎉 RFZ-calculate 安装完成！${NC}"
echo ""
echo -e "${YELLOW}后续步骤:${NC}"
echo "1. 手动测试应用:"
echo "   $SCRIPTS_DIR/start.sh"
echo ""
echo "2. 配置开机自启动:"
echo "   sudo $SCRIPTS_DIR/service_manager.sh install"
echo ""
echo "3. 访问应用:"
echo "   http://localhost:5000"
echo "   http://[树莓派IP]:5000"
echo ""

# 询问是否立即启动应用
read -p "是否现在启动应用进行测试? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    "$SCRIPTS_DIR/start.sh" &
    SETUP_PID=$!
    
    echo "应用启动中，请稍候..."
    sleep 5
    
    # 检查应用是否正常启动
    if curl -s http://localhost:5000 > /dev/null 2>&1; then
        echo -e "${GREEN}✓ 应用启动成功！访问: http://localhost:5000${NC}"
    else
        echo -e "${YELLOW}应用可能仍在启动中，请稍后访问 http://localhost:5000${NC}"
    fi
    
    echo ""
    echo "要停止应用，请运行:"
    echo "$SCRIPTS_DIR/stop.sh"
fi