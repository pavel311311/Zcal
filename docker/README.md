# Docker 部署指南

## 🚀 快速开始

### 方式一：使用启动脚本（推荐）

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
docker-compose up -d
```

## 📋 前置要求

- Docker 20.10+
- Docker Compose 2.0+
- 可用端口：3000（前端）、5000（后端）

## 🔧 配置说明

### 环境变量

编辑 `.env` 文件来修改配置：

```bash
# 端口配置
FRONTEND_PORT=3000
BACKEND_PORT=5000

# API地址
VITE_API_URL=http://localhost:5000/api
```

### 自定义端口

如果需要使用不同端口，修改 `docker-compose.yml`：

```yaml
services:
  frontend:
    ports:
      - "8080:3000"  # 使用8080端口访问前端
  backend:
    ports:
      - "8000:5000"  # 使用8000端口访问后端
```

## 🛠️ 常用命令

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 查看日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend
docker-compose logs -f frontend

# 重新构建镜像
docker-compose build --no-cache

# 完全清理（删除容器、镜像、卷）
docker-compose down --rmi all --volumes --remove-orphans
```

## 🏥 健康检查

服务启动后，可以通过以下地址检查健康状态：

- 后端健康检查：http://localhost:5000/health
- 前端健康检查：http://localhost:3000/health
- API根路径：http://localhost:5000/

## 📊 服务访问

- **前端应用**：http://localhost:3000
- **后端API**：http://localhost:5000/api
- **API文档**：http://localhost:5000/api

## 🐛 故障排除

### 端口被占用

```bash
# 查看端口占用
netstat -tulpn | grep :3000
netstat -tulpn | grep :5000

# 或使用 lsof (macOS/Linux)
lsof -i :3000
lsof -i :5000
```

### 容器启动失败

```bash
# 查看详细日志
docker-compose logs

# 检查容器状态
docker-compose ps

# 进入容器调试
docker-compose exec backend bash
docker-compose exec frontend sh
```

### 镜像构建失败

```bash
# 清理Docker缓存
docker system prune -a

# 重新构建
docker-compose build --no-cache
```

## 📁 文件结构

```
docker/
├── docker-compose.yml      # 主配置文件
├── Dockerfile.backend      # 后端镜像构建文件
├── Dockerfile.frontend     # 前端镜像构建文件
├── .env                    # 环境变量配置
├── start.sh               # Linux/macOS启动脚本
├── start.ps1              # Windows启动脚本
└── README.md              # 本文档
```

## 🔒 生产环境配置

生产环境建议修改以下配置：

1. **环境变量**：
```bash
FLASK_ENV=production
FLASK_DEBUG=0
```

2. **安全配置**：
```yaml
environment:
  - CORS_ORIGINS=https://yourdomain.com
```

3. **资源限制**：
```yaml
deploy:
  resources:
    limits:
      memory: 512M
      cpus: '0.5'
```

## 📈 监控和日志

### 查看实时日志
```bash
docker-compose logs -f --tail=100
```

### 监控资源使用
```bash
docker stats
```

### 导出日志
```bash
docker-compose logs > app.log 2>&1
```

## 🔄 更新部署

```bash
# 拉取最新代码
git pull

# 重新构建并启动
cd docker
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```