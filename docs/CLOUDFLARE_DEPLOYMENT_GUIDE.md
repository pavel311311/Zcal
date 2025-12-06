# Cloudflare Pages 完整部署指南

## 📋 目录
1. [前置要求](#前置要求)
2. [快速开始](#快速开始)
3. [详细步骤](#详细步骤)
4. [配置说明](#配置说明)
5. [常见问题](#常见问题)
6. [后续管理](#后续管理)

## 前置要求

### 必需账户和工具
- ✅ Cloudflare账户（https://dash.cloudflare.com）
- ✅ 域名（可以是免费域名，需加入Cloudflare）
- ✅ Node.js 16+ 和 npm
- ✅ Git
- ✅ Wrangler CLI

### 安装Wrangler
```bash
npm install -g wrangler
# 或使用yarn
yarn global add wrangler
```

### 验证安装
```bash
wrangler --version
node --version
npm --version
```

---

## 快速开始

### Windows用户
```powershell
cd c:\Users\Brent\Desktop\code\Zcal
.\scripts\deploy-cloudflare.ps1
```

### macOS/Linux用户
```bash
cd ~/projects/Zcal
chmod +x scripts/deploy-cloudflare.sh
bash scripts/deploy-cloudflare.sh
```

---

## 详细步骤

### 步骤1：登录Cloudflare

```bash
# 使用Wrangler登录
wrangler login
# 这会打开浏览器进行OAuth认证
```

### 步骤2：获取必要信息

在Cloudflare仪表板获取：
- **Account ID**: 访问 https://dash.cloudflare.com → 右下角 "API令牌" → 复制"账户ID"
- **API Token**: 创建新的API令牌，权限包括：
  - Zone:Read
  - Zone:Edit
  - Account:Read
  - Workers:Write
  - Pages:Write

### 步骤3：配置环境变量

编辑 `wrangler.toml`:
```toml
account_id = "your_account_id_here"
zone_id = "your_zone_id_here"

[env.production]
routes = [
  { pattern = "api.example.com/api/*", zone_name = "example.com" }
]
vars = { ENVIRONMENT = "production", API_BASE_URL = "https://api.example.com" }
```

### 步骤4：构建项目

```bash
# 前端
cd src/frontend
npm install
npm run build
cd ../..

# 后端（如果需要）
cd src/backend
npm install
cd ../..
```

### 步骤5：部署后端到Workers

```bash
cd src/backend
wrangler deploy
# 输出会显示部署的URL
```

### 步骤6：部署前端到Pages

```bash
cd src/frontend

# 首次部署需要创建项目
wrangler pages create pcb-impedance-calculator

# 部署dist目录
wrangler pages publish dist/ --project-name=pcb-impedance-calculator
```

---

## 配置说明

### wrangler.toml - Workers配置

```toml
# 项目元数据
name = "pcb-impedance-calculator"
type = "javascript"
account_id = "your_account_id"  # 从Cloudflare获取
workers_dev = true              # 启用workers.dev子域名

# 路由配置
route = "api.example.com/*"
zone_id = "your_zone_id"

# KV存储（用于缓存）
[[kv_namespaces]]
binding = "CACHE"
id = "kv_namespace_id"

# 环境变量
[env.production]
vars = { 
  ENVIRONMENT = "production",
  API_BASE_URL = "https://api.example.com"
}
```

### wrangler-pages.toml - Pages配置

```toml
# 构建命令和输出目录
build_command = "cd src/frontend && npm install && npm run build"
build_output_directory = "src/frontend/dist"

# Node.js版本
[env]
NODE_VERSION = "18"

# 环境变量
[env.production]
VITE_API_URL = "https://api.example.com"
```

### vite.config.js - 前端构建优化

```javascript
export default defineConfig({
  build: {
    outDir: 'dist',
    sourcemap: false,        // 生产环境关闭source map
    rollupOptions: {
      output: {
        manualChunks: {      // 代码分割优化
          'vue': ['vue'],
          'vendor': ['axios', 'pinia']
        }
      }
    }
  }
})
```

---

## 常见问题

### Q1: 如何获取Account ID?
**A:** 
1. 登录 https://dash.cloudflare.com
2. 选择任何域名
3. 右下角点击 "API令牌"
4. 复制"Account ID"或"Zone ID"

### Q2: API部署后无法访问?
**A:**
1. 检查 `wrangler.toml` 中的 `route` 配置
2. 确保DNS记录正确指向Cloudflare
3. 检查SSL/TLS设置为"完全"或以上

### Q3: 前后端通信失败?
**A:**
1. 确保后端API已成功部署
2. 检查 `src/frontend/src/config/env.js` 中的 API URL
3. 检查CORS设置（见 `worker.js`）
4. 使用浏览器开发工具查看请求

### Q4: 如何更新部署?
**A:**
```bash
# 修改代码后重新部署
npm run build              # 构建
wrangler deploy            # 部署Workers
wrangler pages publish dist/ # 部署Pages
```

### Q5: 如何设置自定义域名?
**A:**
1. 在Cloudflare仪表板 → 域名 → DNS
2. 添加CNAME记录或使用Pages设置
3. 等待DNS传播（通常5-30分钟）

---

## 后续管理

### 监控和日志

```bash
# 查看Workers日志
wrangler tail

# 查看构建状态
wrangler pages projects list
```

### 性能优化

1. **启用缓存**
   ```toml
   [[kv_namespaces]]
   binding = "CACHE"
   ```

2. **启用CDN缓存**
   - Cloudflare仪表板 → 缓存 → 缓存规则

3. **启用Gzip压缩**
   - Cloudflare仪表板 → 速度 → 优化

### 安全设置

1. **启用WAF规则**
   - Cloudflare仪表板 → 安全 → WAF规则

2. **设置速率限制**
   - Cloudflare仪表板 → 安全 → 速率限制

3. **启用Bot管理**
   - Cloudflare仪表板 → 安全 → Bot管理

### 自定义域名DNS

```
# 添加DNS记录到Cloudflare
Type: CNAME
Name: api
Target: your-worker-name.workers.dev

Type: CNAME
Name: @
Target: pcb-impedance-calculator.pages.dev
```

---

## 成本估算

| 服务 | 免费额度 | 价格 |
|------|--------|------|
| Workers | 100,000 请求/天 | $0.5/百万请求 |
| Pages | 无限构建和请求 | 免费 |
| KV存储 | 1GB | $0.5/GB |
| Domains | 免费域名 | $10/年+ |

---

## 获取帮助

- Cloudflare文档: https://developers.cloudflare.com
- Wrangler文档: https://developers.cloudflare.com/workers/cli-wrangler
- Workers示例: https://github.com/cloudflare/workers-sdk
- Pages文档: https://developers.cloudflare.com/pages

---

*最后更新: 2025年12月6日*
