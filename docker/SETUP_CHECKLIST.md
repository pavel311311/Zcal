# Docker 设置检查清单

## ✅ 安装检查清单

### 1. 安装 Docker Desktop

**Windows:**
- 下载：https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe
- 安装后重启电脑
- 启动 Docker Desktop

**macOS:**
- 下载：https://desktop.docker.com/mac/main/amd64/Docker.dmg
- 拖拽到 Applications 文件夹
- 启动 Docker Desktop

**Linux (Ubuntu):**
```bash
# 卸载旧版本
sudo apt-get remove docker docker-engine docker.io containerd runc

# 安装依赖
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg lsb-release

# 添加Docker官方GPG密钥
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# 添加仓库
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 安装Docker
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# 启动Docker服务
sudo systemctl start docker
sudo systemctl enable docker

# 添加用户到docker组
sudo usermod -aG docker $USER
```

### 2. 验证安装

```bash
# 检查Docker版本
docker --version

# 检查Docker Compose版本
docker-compose --version

# 测试Docker运行
docker run hello-world
```

### 3. 配置检查

**Windows PowerShell 执行策略:**
```powershell
# 检查当前策略
Get-ExecutionPolicy

# 如果是Restricted，需要修改
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Linux 权限:**
```bash
# 确保用户在docker组中
groups $USER

# 如果没有docker组，重新登录或运行
newgrp docker
```

## 🔧 配置文件检查

### 检查项目结构
```
项目根目录/
├── docker/
│   ├── docker-compose.yml
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   ├── .env
│   └── start.ps1 / start.sh
├── src/
│   ├── backend/
│   │   ├── requirements.txt
│   │   ├── run.py
│   │   └── app/
│   └── frontend/
│       ├── package.json
│       ├── nginx.conf
│       └── src/
```

### 检查端口占用
```bash
# Windows
netstat -an | findstr :3000
netstat -an | findstr :5000

# Linux/macOS
lsof -i :3000
lsof -i :5000
```

## 🚀 启动步骤

### 方式一：自动脚本

**Windows:**
```powershell
cd docker
.\start.ps1
```

**Linux/macOS:**
```bash
cd docker
chmod +x start.sh
./start.sh
```

### 方式二：手动启动

```bash
cd docker

# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 查看状态
docker-compose ps
```

## 🐛 常见问题解决

### 问题1：Docker命令不识别
**解决方案：**
- Windows：重启电脑，确保Docker Desktop已启动
- Linux：检查Docker服务状态 `sudo systemctl status docker`
- 确保PATH环境变量包含Docker路径

### 问题2：权限被拒绝
**解决方案：**
```bash
# Linux
sudo usermod -aG docker $USER
newgrp docker

# Windows
# 以管理员身份运行PowerShell
```

### 问题3：端口被占用
**解决方案：**
```bash
# 修改docker-compose.yml中的端口映射
ports:
  - "8080:3000"  # 前端改为8080
  - "8000:5000"  # 后端改为8000
```

### 问题4：镜像构建失败
**解决方案：**
```bash
# 清理Docker缓存
docker system prune -a

# 重新构建
docker-compose build --no-cache
```

### 问题5：容器无法启动
**解决方案：**
```bash
# 查看详细日志
docker-compose logs

# 检查配置文件语法
docker-compose config
```

## 📋 部署前检查清单

- [ ] Docker Desktop 已安装并运行
- [ ] 端口 3000 和 5000 未被占用
- [ ] 项目文件结构完整
- [ ] 网络连接正常（用于下载依赖）
- [ ] 磁盘空间充足（至少2GB）

## 🔍 验证部署成功

部署完成后，检查以下地址：

- [ ] http://localhost:3000 - 前端应用正常显示
- [ ] http://localhost:5000 - 后端API根路径返回JSON
- [ ] http://localhost:5000/health - 健康检查返回healthy
- [ ] http://localhost:5000/api/calculation_types - API正常响应

## 📞 获取帮助

如果遇到问题：

1. 查看 `docker/README.md` 详细文档
2. 运行 `docker-compose logs` 查看错误日志
3. 检查 Docker Desktop 是否正常运行
4. 确认防火墙没有阻止端口访问