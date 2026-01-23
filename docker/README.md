# PCB阻抗计算器 Docker部署指南

## 快速部署

### 1. 前置要求
- Linux服务器（Ubuntu/CentOS/Debian等）
- Docker 20.10+
- Docker Compose 2.0+

### 2. 安装Docker（如未安装）
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# 重新登录或执行
newgrp docker
```

### 3. 部署应用
```bash
# 克隆项目到服务器
git clone <your-repo-url>
cd <project-name>

# 进入docker目录
cd docker

# 给部署脚本执行权限
chmod +x deploy.sh

# 执行部署
./deploy.sh
```

### 4. 访问应用
- **前端**: http://服务器IP
- **后端API**: http://服务器IP:5000

## 手动部署

如果自动脚本失败，可以手动执行：

```bash
cd docker

# 构建并启动
docker-compose up --build -d

# 查看状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

## 服务管理

```bash
# 查看运行状态
docker-compose ps

# 查看日志
docker-compose logs -f [service_name]

# 重启服务
docker-compose restart

# 停止服务
docker-compose down

# 完全清理（包括数据）
docker-compose down -v --rmi all
```

## 端口配置

默认端口配置：
- 前端: 80
- 后端: 5000

如需修改端口，编辑 `docker-compose.yml` 文件中的 `ports` 配置。

## 跨域配置

后端已配置允许所有来源的跨域请求（`CORS_ORIGINS=*`），确保不同IP的用户都能正常访问。

## 故障排除

### 1. 端口被占用
```bash
# 查看端口占用
sudo netstat -tlnp | grep :80
sudo netstat -tlnp | grep :5000

# 停止占用端口的服务或修改docker-compose.yml中的端口
```

### 2. 服务无法启动
```bash
# 查看详细日志
docker-compose logs backend
docker-compose logs frontend

# 检查镜像构建
docker-compose build --no-cache
```

### 3. 前端无法连接后端
- 检查后端服务是否正常运行
- 确认防火墙设置允许5000端口
- 检查CORS配置

## 生产环境优化

1. **使用反向代理**：建议使用Nginx作为反向代理
2. **HTTPS配置**：配置SSL证书
3. **资源限制**：在docker-compose.yml中添加资源限制
4. **日志管理**：配置日志轮转
5. **监控告警**：添加健康检查和监控

## 安全建议

1. 修改默认端口
2. 配置防火墙规则
3. 定期更新镜像
4. 使用非root用户运行容器