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

2. **设置环境变量**
   ```bash
   # 替换为实际的 Docker Hub 用户名
   export DOCKER_HUB_USERNAME=<your-docker-hub-username>
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

- 后端镜像：`${DOCKER_HUB_USERNAME}/zcal-backend:latest`
- 前端镜像：`${DOCKER_HUB_USERNAME}/zcal-frontend:latest`