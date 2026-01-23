# PCB 阻抗计算器 - Docker 部署

## 🚀 快速启动

```bash
cd docker
docker-compose up --build -d
```

## 📍 访问服务

- **前端**: http://localhost:3000
- **后端**: http://localhost:5000

## 🛠️ 管理命令

```bash
# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 重启服务
docker-compose restart
```

## 💡 说明

- 使用 `node:18-alpine` 基础镜像（轻量，约150MB）
- 自动配置CORS支持跨设备访问
- 包含健康检查和自动重启