# Docker 部署指南

## 网络连接问题解决方案

### 问题描述
在Linux服务器上使用Docker部署时，前端无法连接到后端API，出现"网络连接失败"错误。

### 根本原因
1. **容器网络隔离**：Docker容器中的`localhost`指向容器内部，不是宿主机
2. **硬编码URL**：前端配置使用了`http://localhost:5000/api`，在容器间通信时失效
3. **IP地址变化**：不同服务器的IP地址不同，需要动态配置

### 解决方案

#### 1. 使用Docker服务名通信（推荐）
在`docker-compose.yml`中，前端容器通过服务名`backend`访问后端：
```yaml
environment:
  - VITE_API_URL=http://backend:5000/api
```

#### 2. 使用服务器IP地址
如果需要外部访问，创建`.env`文件：
```bash
# 在 src/frontend/ 目录下创建 .env 文件
VITE_API_URL=http://YOUR_SERVER_IP:5000/api
```

#### 3. 自动检测环境（已实现）
前端代码已更新为自动检测运行环境：
- Docker环境：使用容器间通信
- 生产环境：使用服务器IP
- 开发环境：使用localhost

## 部署步骤

### 1. 准备环境文件
```bash
# 复制环境配置文件
cp src/frontend/.env.example src/frontend/.env
cp src/backend/.env.example src/backend/.env

# 根据实际情况修改配置
# 如果使用服务器IP，修改 src/frontend/.env：
# VITE_API_URL=http://YOUR_SERVER_IP:5000/api
```

### 2. 构建和启动服务
```bash
cd docker
docker-compose up --build -d
```

### 3. 验证部署
```bash
# 检查容器状态
docker-compose ps

# 查看日志
docker-compose logs frontend
docker-compose logs backend

# 测试API连接
curl http://localhost:5000/api/materials
curl http://YOUR_SERVER_IP:5000/api/materials
```

## 常见问题排查

### 1. 前端无法连接后端
**症状**：浏览器控制台显示"网络连接失败"

**排查步骤**：
```bash
# 1. 检查容器是否正常运行
docker-compose ps

# 2. 检查后端健康状态
curl http://localhost:5000/health

# 3. 检查网络连通性
docker-compose exec frontend ping backend

# 4. 查看前端日志
docker-compose logs frontend
```

**解决方案**：
- 确保`VITE_API_URL`配置正确
- 检查防火墙设置
- 验证端口是否被占用

### 2. CORS错误
**症状**：浏览器显示跨域请求被阻止

**解决方案**：
- 后端已配置允许所有来源
- 如需限制，修改`src/backend/app/__init__.py`中的CORS配置

### 3. 端口冲突
**症状**：容器启动失败，提示端口被占用

**解决方案**：
```bash
# 查看端口占用
netstat -tulpn | grep :3000
netstat -tulpn | grep :5000

# 修改docker-compose.yml中的端口映射
ports:
  - "8080:3000"  # 前端改为8080端口
  - "8000:5000"  # 后端改为8000端口
```

## 生产环境建议

### 1. 使用反向代理
推荐使用Nginx作为反向代理：
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:3000;
    }
    
    location /api {
        proxy_pass http://localhost:5000;
    }
}
```

### 2. 环境变量配置
```bash
# 生产环境变量
export VITE_API_URL=https://your-domain.com/api
export FLASK_ENV=production
```

### 3. 安全配置
- 限制CORS来源为实际域名
- 使用HTTPS
- 配置防火墙规则
- 定期更新依赖包

## 监控和日志

### 查看实时日志
```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f frontend
docker-compose logs -f backend
```

### 健康检查
```bash
# 后端健康检查
curl http://localhost:5000/health

# 前端访问测试
curl http://localhost:3000
```