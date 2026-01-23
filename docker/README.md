# Docker 部署指南

## 文件说明

- `Dockerfile` - Docker镜像定义
- `docker-compose.yml` - Docker Compose配置  
- `docker-start.sh` - Docker容器专用启动脚本
- `.dockerignore` - 构建时忽略的文件

## 快速启动

### 使用 Docker Compose（推荐）

```bash
# 进入docker目录
cd docker

# 构建并启动服务
docker-compose up --build

# 后台运行
docker-compose up -d --build
```

### 使用 Docker 命令

```bash
# 构建镜像
docker build -f docker/Dockerfile -t pcb-calculator .

# 运行容器
docker run -d \
  --name pcb-calculator \
  -p 3000:3000 \
  -p 5000:5000 \
  pcb-calculator
```

## 访问服务

- 前端界面: http://localhost:3000
- 后端API: http://localhost:5000

## 管理命令

```bash
# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 清理
docker-compose down --volumes --rmi all
```

## 与本地开发的区别

- 本地开发使用 `scripts/start-all.sh` (Linux) 或 `start-all.ps1` (Windows)
- Docker部署使用 `docker/docker-start.sh` (容器环境优化)