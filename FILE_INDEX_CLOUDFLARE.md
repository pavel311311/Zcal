# 📑 Cloudflare部署 - 文件索引

## 🎯 快速导航

### 🚀 我想立即开始部署
👉 查看：`CLOUDFLARE_QUICK_START.md`  
⏱️ 耗时：5分钟

### 📖 我想了解详细步骤
👉 查看：`docs/CLOUDFLARE_DEPLOYMENT_GUIDE.md`  
⏱️ 耗时：20分钟

### 🏗️ 我想理解项目架构
👉 查看：`CLOUDFLARE_DEPLOYMENT_SUMMARY.md`  
⏱️ 耗时：10分钟

### ✅ 部署后我需要验证
👉 查看：`DEPLOYMENT_CHECKLIST.md`  
⏱️ 耗时：30分钟

### 📚 我想看完整总结
👉 查看：`CLOUDFLARE_README.md`  
⏱️ 耗时：15分钟

---

## 📂 文件组织结构

### 核心配置文件
```
根目录/
├── wrangler.toml                     ← Workers配置（需修改）
├── wrangler-pages.toml               ← Pages配置
│
src/backend/
├── worker.js                         ← Workers入口（完整代码）
├── package.json                      ← 依赖配置（已更新）
├── .env.example                      ← 环境变量模板
└── api/
    ├── calculator.js                 ← 计算API（完整代码）
    ├── form.js                       ← 表单API（完整代码）
    └── material.js                   ← 材料库API（完整代码）

src/frontend/
├── vite.config.js                    ← 构建配置（已优化）
├── package.json                      ← 依赖配置（已更新）
├── .env.cloudflare                   ← 环境变量
└── src/config/
    └── env.js                        ← 环境管理（完整代码）
```

### 部署自动化
```
scripts/
├── deploy-cloudflare.ps1             ← Windows脚本（完整代码）
└── deploy-cloudflare.sh              ← Linux/macOS脚本（完整代码）

.github/workflows/
└── deploy-cloudflare.yml             ← GitHub Actions（完整代码）
```

### 完整文档
```
docs/
└── CLOUDFLARE_DEPLOYMENT_GUIDE.md    ← 完整部署指南（380行）

根目录/
├── CLOUDFLARE_README.md              ← 总览文档
├── CLOUDFLARE_QUICK_START.md         ← 快速参考
├── CLOUDFLARE_DEPLOYMENT_SUMMARY.md  ← 架构总结
├── DEPLOYMENT_CHECKLIST.md           ← 验证清单
├── DEPLOYMENT_COMPLETE.md            ← 完成确认
└── FILE_INDEX.md                     ← 本文件
```

---

## 📊 文件统计

| 类别 | 文件数 | 代码行数 | 说明 |
|------|--------|--------|------|
| 配置 | 4 | 150 | wrangler、环境变量等 |
| 后端代码 | 4 | 620 | Worker + 3个API |
| 前端代码 | 2 | 80 | 配置管理 |
| 脚本 | 2 | 180 | 自动化部署 |
| CI/CD | 1 | 70 | GitHub Actions |
| 文档 | 6 | 1500+ | 完整指南和参考 |
| **总计** | **19** | **2600+** | 完整部署方案 |

---

## 🎯 使用场景速查

### 场景1：第一次部署

**步骤：**
1. 阅读 `CLOUDFLARE_QUICK_START.md`（5分钟）
2. 安装工具：`npm install -g wrangler`
3. 登录：`wrangler login`
4. 运行：`.\scripts\deploy-cloudflare.ps1`
5. 验证部署（使用 `DEPLOYMENT_CHECKLIST.md`）

**预计时间：** 30分钟

---

### 场景2：需要自定义配置

**查看文件：**
- `wrangler.toml` - 修改account_id、route、zone_id
- `wrangler-pages.toml` - 修改build_command
- `src/backend/.env.example` - 参考环境变量

**相关文档：**
- `docs/CLOUDFLARE_DEPLOYMENT_GUIDE.md` - 配置说明一节

**预计时间：** 15分钟

---

### 场景3：修改计算逻辑

**需要修改的文件：**
- `src/backend/api/calculator.js` - 修改计算函数
- `src/backend/api/form.js` - 更新表单定义

**部署命令：**
```bash
cd src/backend
wrangler deploy
```

**预计时间：** 10分钟

---

### 场景4：配置GitHub自动部署

**步骤：**
1. 在GitHub仓库设置 Secrets：
   - `CLOUDFLARE_ACCOUNT_ID`
   - `CLOUDFLARE_API_TOKEN`
2. 工作流文件已准备：`.github/workflows/deploy-cloudflare.yml`
3. 推送到main分支自动部署

**相关文档：**
- `CLOUDFLARE_QUICK_START.md` - GitHub Actions一节
- `docs/CLOUDFLARE_DEPLOYMENT_GUIDE.md` - 自动化部署一节

**预计时间：** 10分钟

---

### 场景5：部署后验证

**使用清单：** `DEPLOYMENT_CHECKLIST.md`

**验证步骤：**
- [ ] 检查前置条件
- [ ] 验证配置文件
- [ ] 本地测试
- [ ] 部署验证
- [ ] 功能测试

**预计时间：** 30分钟

---

## 🔍 代码文件速查

### 后端API - `src/backend/`

| 文件 | 行数 | 功能 |
|------|------|------|
| `worker.js` | 370 | Workers主入口、CORS、路由 |
| `api/calculator.js` | 80 | 4种阻抗计算 |
| `api/form.js` | 78 | 表单定义API |
| `api/material.js` | 92 | 材料库API |

**调用关系：**
```
worker.js (路由)
├── /api/calculate → calculator.js
├── /api/form/:type → form.js
├── /api/forms → form.js
├── /api/material/:name → material.js
└── /api/materials → material.js
```

---

### 前端集成 - `src/frontend/`

| 文件 | 行数 | 功能 |
|------|------|------|
| `vite.config.js` | 40 | 构建配置、代码分割 |
| `src/config/env.js` | 21 | 环境变量管理 |
| `.env.cloudflare` | 5 | 环境变量值 |

**使用方式：**
```javascript
// 在前端代码中使用
import { getApiUrl } from '@/config/env'
const url = getApiUrl('/calculate')
```

---

### 部署脚本 - `scripts/`

| 文件 | 平台 | 功能 |
|------|------|------|
| `deploy-cloudflare.ps1` | Windows | 全自动部署 |
| `deploy-cloudflare.sh` | Linux/macOS | 全自动部署 |

**使用方式：**
```powershell
# Windows
.\scripts\deploy-cloudflare.ps1 -AccountId "xxx" -ApiToken "xxx" -Domain "example.com"

# Linux/macOS
bash scripts/deploy-cloudflare.sh
```

---

## 📋 部署流程图

```
开始
  │
  ├→ 安装工具 (npm, wrangler)
  │
  ├→ 获取Cloudflare凭证
  │  ├─ Account ID
  │  ├─ API Token
  │  └─ Zone ID (可选)
  │
  ├→ 修改配置文件
  │  ├─ wrangler.toml
  │  └─ src/frontend/.env.cloudflare
  │
  ├→ 本地测试
  │  ├─ 后端: wrangler dev
  │  └─ 前端: npm run dev
  │
  ├→ 运行部署脚本
  │  └─ .\scripts\deploy-cloudflare.ps1
  │     (或 bash scripts/deploy-cloudflare.sh)
  │
  ├→ 验证部署
  │  ├─ 检查Workers健康状态
  │  ├─ 检查Pages可访问性
  │  └─ 测试API和功能
  │
  ├→ 配置DNS (可选)
  │  └─ CNAME记录到Cloudflare
  │
  └→ 完成！
```

---

## 🎓 学习资源

### 官方文档
- Cloudflare Workers: https://developers.cloudflare.com/workers
- Cloudflare Pages: https://developers.cloudflare.com/pages
- Wrangler CLI: https://developers.cloudflare.com/workers/cli-wrangler

### 本项目文档
- 📖 完整部署指南：`docs/CLOUDFLARE_DEPLOYMENT_GUIDE.md`
- ⚡ 快速开始：`CLOUDFLARE_QUICK_START.md`
- 🏗️ 架构总结：`CLOUDFLARE_DEPLOYMENT_SUMMARY.md`
- ✅ 验证清单：`DEPLOYMENT_CHECKLIST.md`

### 示例代码
- 后端API：`src/backend/worker.js` 和 `src/backend/api/`
- 前端配置：`src/frontend/src/config/env.js`

---

## 🆘 故障排查速查

| 问题 | 查看位置 |
|------|--------|
| 部署失败 | `CLOUDFLARE_QUICK_START.md` - 常见问题一节 |
| API无法访问 | `docs/CLOUDFLARE_DEPLOYMENT_GUIDE.md` - 常见问题Q2 |
| 前端无法调用API | `docs/CLOUDFLARE_DEPLOYMENT_GUIDE.md` - 常见问题Q3 |
| 如何获取Account ID | `docs/CLOUDFLARE_DEPLOYMENT_GUIDE.md` - 常见问题Q1 |
| 如何配置自定义域名 | `docs/CLOUDFLARE_DEPLOYMENT_GUIDE.md` - 常见问题Q5 |

---

## 📞 获取帮助

### 问题排查步骤

1. **查看相关文档**
   - 快速问题：`CLOUDFLARE_QUICK_START.md`
   - 具体问题：`docs/CLOUDFLARE_DEPLOYMENT_GUIDE.md`

2. **使用验证清单**
   - `DEPLOYMENT_CHECKLIST.md`

3. **查看源代码**
   - 后端：`src/backend/worker.js`
   - 前端：`src/frontend/vite.config.js`
   - 脚本：`scripts/`

4. **官方资源**
   - Cloudflare文档：https://developers.cloudflare.com
   - GitHub Issues：https://github.com/pavel311311/Zcal/issues

---

## ✨ 快速链接

| 内容 | 链接 |
|------|------|
| 快速开始 | `CLOUDFLARE_QUICK_START.md` |
| 详细指南 | `docs/CLOUDFLARE_DEPLOYMENT_GUIDE.md` |
| 总体概览 | `CLOUDFLARE_README.md` |
| 验证清单 | `DEPLOYMENT_CHECKLIST.md` |
| 架构总结 | `CLOUDFLARE_DEPLOYMENT_SUMMARY.md` |

---

## 🎉 开始部署！

```powershell
# Windows用户
cd c:\Users\Brent\Desktop\code\Zcal
.\scripts\deploy-cloudflare.ps1

# macOS/Linux用户
cd ~/projects/Zcal
bash scripts/deploy-cloudflare.sh
```

或先阅读：`CLOUDFLARE_QUICK_START.md`

---

*最后更新: 2025年12月6日*  
*版本: 1.0*  
*作者: GitHub Copilot*
