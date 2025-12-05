# 项目文件索引

## 📋 核心入口文件

| 文件位置 | 用途 | 说明 |
|---------|------|------|
| `backend/run.py` | 后端启动 | Flask 应用主入口 |
| `frontend/src/main.js` | 前端启动 | Vue 应用主入口 |
| `frontend/index.html` | 前端 HTML | HTML 模板文件 |

## 🔙 后端文件结构

| 文件/目录 | 功能描述 |
|---------|---------|
| `backend/app/__init__.py` | Flask 应用工厂，配置 CORS |
| `backend/app/routes/calculator.py` | 阻抗计算 API 端点 |
| `backend/app/routes/material.py` | 材料库 API 端点 |
| `backend/app/services/calculator.py` | PCB 阻抗计算核心算法（所有计算方法） |
| `backend/requirements.txt` | Python 依赖列表 |
| `backend/Dockerfile` | Docker 镜像配置 |
| `backend/.env` | 环境变量配置 |
| `backend/README.md` | 后端说明文档 |

## 🎨 前端文件结构

| 文件/目录 | 功能描述 |
|---------|---------|
| `frontend/src/App.vue` | 根组件，整体布局 |
| `frontend/src/main.js` | Vue 应用入口 |
| `frontend/src/components/CalculatorForm.vue` | 计算表单组件 |
| `frontend/src/components/ResultDisplay.vue` | 结果显示组件 |
| `frontend/src/api/index.js` | Axios API 客户端配置 |
| `frontend/src/styles/global.css` | 全局样式 |
| `frontend/package.json` | Node.js 依赖配置 |
| `frontend/vite.config.js` | Vite 构建工具配置 |
| `frontend/Dockerfile` | Docker 镜像配置 |
| `frontend/.env` | 环境变量配置 |
| `frontend/README.md` | 前端说明文档 |

## 🐳 容器和编排

| 文件 | 用途 |
|-----|------|
| `docker-compose.yml` | Docker 编排配置（启动所有服务） |
| `backend/Dockerfile` | 后端镜像构建文件 |
| `frontend/Dockerfile` | 前端镜像构建文件 |

## 📚 文档文件

| 文件 | 内容 |
|-----|------|
| `README.md` | 项目主说明 |
| `MIGRATION_COMPLETE.md` | 改造完成说明 |
| `DEVELOPMENT_GUIDE.md` | 开发指南（如何扩展功能） |
| `MIGRATION_SUMMARY.py` | 改造总结和统计 |
| `backend/README.md` | 后端技术说明 |
| `frontend/README.md` | 前端技术说明 |

## 🚀 启动脚本

| 脚本 | 系统 | 用途 |
|-----|------|------|
| `start.sh` | Linux/Mac | 一键启动所有服务 |
| `start.ps1` | Windows | PowerShell 启动脚本 |

## 🔑 关键配置文件

| 文件 | 配置项 |
|-----|--------|
| `backend/.env` | Flask 环境变量 (FLASK_ENV, FLASK_DEBUG, FLASK_PORT) |
| `frontend/.env` | Vite 环境变量 (VITE_API_URL) |
| `frontend/vite.config.js` | Vite 构建配置，API 代理 |
| `backend/gunicorn_config.py` | Gunicorn 生产服务器配置 |

---

## 🔄 数据流程图

```
用户浏览器
    ↓
Vue 3 前端 (http://localhost:3000)
    ↓
Axios API 客户端
    ↓
Flask 后端 API (http://localhost:5000/api)
    ↓
PCB 阻抗计算器核心算法
    ↓
返回 JSON 结果
    ↓
Vue 组件展示结果
```

---

## 📊 API 端点快速参考

| 方法 | 端点 | 文件 | 说明 |
|------|------|------|------|
| POST | `/api/calculate` | `backend/app/routes/calculator.py` | 计算阻抗 |
| GET | `/api/materials` | `backend/app/routes/material.py` | 获取材料库 |
| GET | `/health` | `backend/app/__init__.py` | 健康检查 |

---

## 🔧 修改指南

### 添加新的计算类型

1. 在 `backend/app/services/calculator.py` 中添加新方法
2. 在 `backend/app/routes/calculator.py` 中添加路由处理
3. 在 `frontend/src/components/CalculatorForm.vue` 中的 `typeFields` 添加字段定义
4. 在 HTML select 中添加新选项

### 修改样式

- 编辑 `frontend/src/styles/global.css`
- 修改 CSS 变量在 `:root` 中

### 修改材料库

- 编辑 `backend/app/routes/material.py` 中的 `materials` 字典

---

## 📦 依赖管理

### 后端依赖
```bash
cd backend
pip install -r requirements.txt
```

主要依赖：
- Flask==2.3.3
- flask-cors==4.0.0
- gunicorn==21.2.0

### 前端依赖
```bash
cd frontend
npm install
```

主要依赖：
- vue@^3.3.4
- axios@^1.5.0
- vite@^4.4.9

---

## 🧪 测试快速命令

```bash
# 检查后端健康状态
curl http://localhost:5000/health

# 获取材料库
curl http://localhost:5000/api/materials

# 测试阻抗计算
curl -X POST http://localhost:5000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"type":"microstrip","params":{"width":0.2,"height":1.6,"thickness":0.035,"dielectric":4.3}}'
```

---

## 📍 重要文件位置总结

| 需求 | 编辑文件 |
|------|---------|
| 添加新计算方法 | `backend/app/services/calculator.py` |
| 添加新 API 端点 | `backend/app/routes/` 中的相应文件 |
| 修改 UI 布局 | `frontend/src/App.vue` |
| 修改表单字段 | `frontend/src/components/CalculatorForm.vue` |
| 修改结果展示 | `frontend/src/components/ResultDisplay.vue` |
| 修改样式 | `frontend/src/styles/global.css` |
| 修改材料库 | `backend/app/routes/material.py` |
| 修改环境配置 | `.env` 文件 |

---

## ✅ 改造完成清单

- [x] 后端结构改造
- [x] 前端框架切换到 Vue 3
- [x] API 客户端集成
- [x] CORS 支持配置
- [x] Docker 容器化
- [x] 文档编写
- [x] 启动脚本创建
- [x] 开发指南编写

---

**最后更新**：2025年12月5日  
**版本**：1.0.0 (前后端分离初版)  
**状态**：✅ 完成就绪
