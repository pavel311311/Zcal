# 🚀 Cloudflare部署快速参考

## 5分钟快速开始

### 前置检查清单
- [ ] 有Cloudflare账户（https://dash.cloudflare.com）
- [ ] 域名已添加到Cloudflare
- [ ] Node.js 16+ 已安装
- [ ] npm 已安装

### 命令速查表

```powershell
# 1️⃣  全自动部署（推荐）
.\scripts\deploy-cloudflare.ps1

# 2️⃣  获取账户信息
wrangler whoami

# 3️⃣  本地测试后端
cd src/backend
wrangler dev

# 4️⃣  本地测试前端
cd src/frontend
npm run dev

# 5️⃣  手动部署后端
cd src/backend
wrangler deploy

# 6️⃣  手动部署前端
cd src/frontend
wrangler pages publish dist/ --project-name=pcb-impedance-calculator

# 7️⃣  查看部署日志
wrangler tail

# 8️⃣  查看Pages项目
wrangler pages projects list
```

---

## 关键信息速查

### 我需要从Cloudflare获取什么？

1. **Account ID**
   - 位置: https://dash.cloudflare.com → 右下角 "API令牌"
   - 格式: 长字符串，如 `abc123def456`

2. **API Token**
   - 位置: https://dash.cloudflare.com → 右下角 "API令牌" → 创建令牌
   - 权限: Zone:Read, Zone:Edit, Account:Read, Workers:Write, Pages:Write

3. **Zone ID**
   - 位置: 选择域名 → 概览 → 右侧边栏
   - 格式: 长字符串

### 部署后的URL是什么？

| 组件 | URL示例 |
|------|--------|
| Workers (dev) | `https://pcb-impedance-calculator.workers.dev` |
| Workers (自定义) | `https://api.example.com` |
| Pages (dev) | `https://pcb-impedance-calculator.pages.dev` |
| Pages (自定义) | `https://example.com` |

### 文件修改位置

| 需要修改的地方 | 文件路径 |
|----------------|---------|
| 账户ID和Token | `wrangler.toml` 第3行 |
| API URL | `src/frontend/.env.cloudflare` |
| 后端逻辑 | `src/backend/api/*.js` |
| 前端页面 | `src/frontend/src/` |

---

## 常见问题速解

### ❓ 部署卡住了怎么办？
```powershell
# 检查网络连接
ping api.cloudflare.com

# 重新登录
wrangler login

# 增加日志级别
wrangler deploy --debug
```

### ❓ API无法访问怎么办？
- 检查 `wrangler.toml` 中的 `route` 和 `zone_id`
- 确保DNS记录已添加
- 使用 `wrangler tail` 查看日志

### ❓ 前端无法调用API怎么办？
- 检查 `src/frontend/src/config/env.js` 中的 API URL
- 检查跨域CORS设置（已在 `worker.js` 中配置）
- 在浏览器控制台查看具体错误

### ❓ 如何回滚部署？
```powershell
# 部署前一个版本（需要git）
git revert HEAD
git push

# 或者手动部署上一个版本
wrangler deploy --env production
```

---

## 环境变量配置

### 开发环境
```env
VITE_API_URL=http://localhost:8787/api
NODE_ENV=development
```

### 生产环境
```env
VITE_API_URL=https://api.example.com
NODE_ENV=production
```

---

## 成本预估（美元/月）

| 服务 | 月费用 |
|------|--------|
| Pages | $0 (免费) |
| Workers | $0-10 (按100万请求计) |
| KV存储 | $0-2 (按GB计) |
| **总计** | **$0-12** |

---

## 有用的链接

- 📖 完整部署指南: `docs/CLOUDFLARE_DEPLOYMENT_GUIDE.md`
- 📊 架构概览: `CLOUDFLARE_DEPLOYMENT_SUMMARY.md`
- 🔐 API文档: `src/backend/worker.js`
- 📝 配置文件: `wrangler.toml`

---

## 支持我们

如果有任何问题，请查看：
1. 完整的部署指南（本目录下）
2. Cloudflare官方文档: https://developers.cloudflare.com
3. GitHub Issues: https://github.com/pavel311311/Zcal/issues

---

*最后更新: 2025年12月6日*
