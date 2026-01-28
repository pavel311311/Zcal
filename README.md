# Zcal 项目

## 项目简介
Zcal 是一个日历应用，包含前端和后端服务。

## 快速开始

### 方法一：使用本地构建

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd Zcal
   ```

2. **构建并启动服务**
   ```bash
   cd docker
   docker-compose up -d --build
   ```

### 方法二：使用 Docker Hub 镜像

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd Zcal
   ```

2. **设置环境变量（可选）**
   ```bash
   # 默认为 pavel314，如需使用其他用户名请设置
   # export DOCKER_HUB_USERNAME=<other-docker-hub-username>
   ```

3. **拉取镜像并启动服务**
   ```bash
   docker-compose up -d
   ```

## 服务访问

- 前端服务：`http://localhost`
- 后端服务：`http://localhost:5000`

## 环境变量

### 后端服务
- `FLASK_ENV`：运行环境（默认为 production）
- `FLASK_PORT`：服务端口（默认为 5000）
- `CORS_ORIGINS`：允许的跨域来源（默认为 *）

## 健康检查

服务启动后，可以通过以下命令检查服务状态：

```bash
docker-compose ps
```

## 停止服务

```bash
docker-compose down
```

## Docker Hub 镜像

项目的 Docker 镜像会通过 GitHub Actions 自动构建并推送到 Docker Hub：

- 后端镜像：`pavel314/zcal-backend:latest`
- 前端镜像：`pavel314/zcal-frontend:latest`

**支持的架构**：
- linux/amd64 (x86_64)
- linux/arm64 (ARM64，适用于树莓派等设备)