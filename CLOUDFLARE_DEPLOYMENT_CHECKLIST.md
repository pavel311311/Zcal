# Cloudflare部署前检查清单

## ✅ 环境准备

- [ ] Node.js 16+ 已安装
  ```powershell
  node --version
  ```

- [ ] npm 已安装
  ```powershell
  npm --version
  ```

- [ ] Git 已安装
  ```powershell
  git --version
  ```

- [ ] Wrangler CLI 已安装
  ```powershell
  npm install -g wrangler
  wrangler --version
  ```

## ✅ Cloudflare账户准备

- [ ] Cloudflare账户已创建 (https://dash.cloudflare.com)
- [ ] 域名已添加到Cloudflare
- [ ] 已获取 Account ID
  - 位置: https://dash.cloudflare.com → 右下角 "API令牌"
  - 保存位置: `wrangler.toml` 第3行
  
- [ ] 已创建 API Token
  - 权限包含: Zone:Read, Zone:Edit, Account:Read, Workers:Write, Pages:Write
  - 已妥善保存 (✅ 绝不要提交到git!)

- [ ] 已获取 Zone ID
  - 位置: 域名概览页面 → 右侧边栏
  - 保存位置: `wrangler.toml` 第6行

## ✅ 代码检查

- [ ] 已检查 `wrangler.toml` 配置
  - [ ] Account ID 已填入
  - [ ] Zone ID 已填入
  - [ ] 路由规则正确

- [ ] 已检查 `.env.cloudflare` 文件
  - [ ] API_BASE_URL 已设置
  - [ ] CORS_ORIGIN 已设置

- [ ] 前端代码检查
  - [ ] `src/frontend/src/config/env.js` 存在
  - [ ] API URL配置正确

- [ ] 后端代码检查
  - [ ] `src/backend/worker.js` 存在
  - [ ] API处理函数完整

## ✅ 本地测试

- [ ] 前端本地构建成功
  ```powershell
  cd src/frontend
  npm install
  npm run build
  ```

- [ ] 后端本地测试成功
  ```powershell
  cd src/backend
  npm install
  wrangler dev
  ```

- [ ] 前端调用后端API测试成功

## ✅ 安全检查

- [ ] `.gitignore` 包含:
  - [ ] `.env`
  - [ ] `.env.local`
  - [ ] `.env.*.local`
  - [ ] `node_modules/`
  - [ ] `dist/`

- [ ] 没有提交敏感信息到git
  - [ ] 没有API Token
  - [ ] 没有Account ID (可以公开)
  - [ ] 没有私钥

- [ ] GitHub Secrets已设置（如果使用CI/CD）
  - [ ] CLOUDFLARE_ACCOUNT_ID
  - [ ] CLOUDFLARE_API_TOKEN

## ✅ DNS配置（可选，首次需要）

- [ ] 添加DNS记录到Cloudflare
  ```
  类型: CNAME
  名称: api
  目标: pcb-impedance-calculator.workers.dev
  
  类型: CNAME
  名称: www
  目标: pcb-impedance-calculator.pages.dev
  ```

- [ ] 等待DNS传播 (通常5-30分钟)

## ✅ 部署步骤

### 自动化部署（推荐）
- [ ] 运行部署脚本
  ```powershell
  .\scripts\deploy-cloudflare.ps1
  ```

### 手动部署
- [ ] 登录Cloudflare
  ```powershell
  wrangler login
  ```

- [ ] 构建前端
  ```powershell
  cd src/frontend
  npm run build
  ```

- [ ] 部署后端
  ```powershell
  cd src/backend
  wrangler deploy
  ```

- [ ] 部署前端
  ```powershell
  cd src/frontend
  wrangler pages publish dist/ --project-name=pcb-impedance-calculator
  ```

## ✅ 部署后验证

- [ ] 后端Workers已部署
  - [ ] 访问 `https://pcb-impedance-calculator.workers.dev/api/health` 返回 `{"status":"ok"}`

- [ ] 前端Pages已部署
  - [ ] 访问 `https://pcb-impedance-calculator.pages.dev` 显示应用

- [ ] 前后端通信正常
  - [ ] 打开应用，选择计算类型
  - [ ] 输入参数，点击计算
  - [ ] 获得正确结果

- [ ] 自定义域名正常（如果配置了）
  - [ ] 前端访问: `https://example.com`
  - [ ] 后端访问: `https://api.example.com`

## ✅ 监控和维护

- [ ] 启用Cloudflare分析
  - [ ] 在仪表板查看流量
  - [ ] 监控错误率

- [ ] 设置告警（可选）
  - [ ] Workers错误告警
  - [ ] Pages构建失败告警

- [ ] 配置日志
  - [ ] 启用 `wrangler tail` 查看实时日志
  - [ ] 保存关键错误日志

## ✅ 文档检查

- [ ] 已阅读 `CLOUDFLARE_DEPLOYMENT_SUMMARY.md`
- [ ] 已阅读 `CLOUDFLARE_QUICK_START.md`
- [ ] 已阅读 `docs/CLOUDFLARE_DEPLOYMENT_GUIDE.md`
- [ ] 已保存重要链接

---

## 🆘 问题排查

如果遇到问题，按以下顺序检查：

1. **检查日志**
   ```powershell
   wrangler tail
   ```

2. **检查配置**
   - [ ] `wrangler.toml` 语法正确
   - [ ] 环境变量正确
   - [ ] DNS配置正确

3. **重新登录**
   ```powershell
   wrangler logout
   wrangler login
   ```

4. **清除缓存**
   ```powershell
   rm -r node_modules
   npm install
   ```

5. **查看官方文档**
   - https://developers.cloudflare.com/workers
   - https://developers.cloudflare.com/pages

---

## 📞 需要帮助？

- GitHub Issues: https://github.com/pavel311311/Zcal/issues
- Cloudflare社区: https://community.cloudflare.com
- Stack Overflow: https://stackoverflow.com/questions/tagged/cloudflare

---

**部署前最后一步: 打印此清单，逐项检查✅**

*检查完成日期: ________________*
*检查人: ________________*
*备注: ________________________________________________*
