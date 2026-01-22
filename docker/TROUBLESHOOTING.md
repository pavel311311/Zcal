# Docker 静态资源问题排查指南

## 🚨 问题描述

Docker构建后，浏览器显示静态资源（JS/CSS文件）加载失败，通常表现为：
- 404错误：找不到 `/assets/index-xxx.js` 等文件
- MIME类型错误：资源被当作HTML加载
- 白屏或样式丢失

## 🔍 问题排查步骤

### 1. 检查构建产物

```bash
# 进入前端目录
cd src/frontend

# 本地构建测试
npm run build

# 检查dist目录结构
ls -la dist/
ls -la dist/assets/

# 查看index.html内容
cat dist/index.html
```

**期望结果：**
- `dist/assets/` 目录存在且包含JS/CSS文件
- `index.html` 中的资源路径正确（如 `/assets/index-xxx.js`）

### 2. 检查Docker容器内文件

```bash
# 构建并启动容器
cd docker
docker-compose up -d frontend

# 检查容器内文件
docker exec pcb-calculator-frontend ls -la /usr/share/nginx/html/
docker exec pcb-calculator-frontend ls -la /usr/share/nginx/html/assets/

# 检查index.html
docker exec pcb-calculator-frontend cat /usr/share/nginx/html/index.html
```

### 3. 检查Nginx配置

```bash
# 查看nginx配置
docker exec pcb-calculator-frontend cat /etc/nginx/conf.d/default.conf

# 检查nginx进程
docker exec pcb-calculator-frontend ps aux | grep nginx

# 查看nginx日志
docker logs pcb-calculator-frontend
```

### 4. 测试资源访问

```bash
# 测试主页
curl -I http://localhost:3000/

# 测试静态资源（替换为实际文件名）
curl -I http://localhost:3000/assets/index-xxx.js
curl -I http://localhost:3000/assets/index-xxx.css
```

## 🛠️ 常见问题及解决方案

### 问题1：assets目录不存在

**症状：** `ls: /usr/share/nginx/html/assets/: No such file or directory`

**原因：** Vite构建配置问题或Docker复制路径错误

**解决方案：**
```bash
# 1. 检查vite.config.js配置
# 确保包含：
# build: {
#   outDir: 'dist',
#   assetsDir: 'assets'
# }

# 2. 重新构建
cd src/frontend
rm -rf dist/
npm run build

# 3. 重新构建Docker镜像
cd ../../docker
docker-compose build --no-cache frontend
```

### 问题2：MIME类型错误

**症状：** 浏览器控制台显示 `MIME type ('text/html') is not executable`

**原因：** Nginx配置不正确，JS文件被当作HTML返回

**解决方案：**
```bash
# 使用简化的nginx配置
cp src/frontend/nginx.simple.conf src/frontend/nginx.conf

# 重新构建
docker-compose build --no-cache frontend
docker-compose up -d
```

### 问题3：404错误

**症状：** 浏览器显示 `GET http://localhost:3000/assets/xxx.js net::ERR_ABORTED 404`

**原因：** 文件路径不匹配或nginx路由配置问题

**解决方案：**
```bash
# 1. 检查文件是否存在
docker exec pcb-calculator-frontend find /usr/share/nginx/html -name "*.js"

# 2. 检查nginx配置中的root路径
docker exec pcb-calculator-frontend nginx -T

# 3. 重启nginx
docker exec pcb-calculator-frontend nginx -s reload
```

### 问题4：权限问题

**症状：** nginx日志显示权限被拒绝

**解决方案：**
```bash
# 在Dockerfile中添加权限设置
RUN chmod -R 755 /usr/share/nginx/html

# 重新构建镜像
docker-compose build --no-cache frontend
```

## 🚀 快速修复脚本

### Windows PowerShell
```powershell
cd docker
.\debug-build.ps1
```

### Linux/macOS
```bash
cd docker
chmod +x fix-assets.sh
./fix-assets.sh
```

## 🔧 手动修复步骤

### 1. 完全重建

```bash
# 停止所有容器
docker-compose down --volumes --remove-orphans

# 删除所有镜像
docker-compose down --rmi all

# 清理前端缓存
cd ../src/frontend
rm -rf dist/ node_modules/.vite/
npm ci

# 重新构建
cd ../../docker
docker-compose build --no-cache
docker-compose up -d
```

### 2. 验证修复

```bash
# 等待服务启动
sleep 10

# 检查服务状态
docker-compose ps

# 测试访问
curl http://localhost:3000/
```

## 📋 预防措施

### 1. 本地测试
在Docker构建前，先进行本地构建测试：
```bash
cd src/frontend
npm run build
npm run preview  # 测试构建产物
```

### 2. 配置检查
确保以下配置正确：
- `vite.config.js` 中的 `base: '/'`
- `nginx.conf` 中的 `root` 路径
- Docker构建上下文路径

### 3. 分步构建
使用分步构建来定位问题：
```bash
# 只构建前端
docker build -f Dockerfile.frontend -t test-frontend ../src/frontend

# 测试单个容器
docker run -p 3000:3000 test-frontend
```

## 📞 获取更多帮助

如果问题仍然存在：

1. 查看完整的Docker日志：`docker-compose logs`
2. 检查浏览器开发者工具的网络面板
3. 确认防火墙没有阻止端口访问
4. 尝试使用不同的端口：修改 `docker-compose.yml` 中的端口映射

## 🎯 成功标志

修复成功后，你应该看到：
- ✅ http://localhost:3000 正常显示页面
- ✅ 浏览器控制台无错误
- ✅ 所有静态资源正常加载
- ✅ 页面样式和交互正常