# 开发指南 - PCB 阻抗计算器

## 快速参考

### 项目结构说明

```
前后端分离架构
│
├── 后端 (Backend) - Flask REST API
│   ├── 端口: 5000
│   ├── 框架: Flask 2.3
│   ├── 语言: Python 3.11
│   └── 启动: python run.py
│
└── 前端 (Frontend) - Vue 3 SPA
    ├── 端口: 3000
    ├── 框架: Vue 3 + Vite
    ├── 语言: JavaScript/ES6+
    └── 启动: npm run dev
```

## 后端开发指南

### 添加新的计算方法

1. **在 `backend/app/services/calculator.py` 中添加方法：**

```python
@staticmethod
def new_calculator_method(param1, param2, ...):
    """
    新计算方法说明
    param1: 参数1说明
    param2: 参数2说明
    """
    try:
        # 计算逻辑
        result = some_calculation(param1, param2)
        
        return {
            'result_field': round(result, 2),
            'status': 'success'
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
```

2. **在 `backend/app/routes/calculator.py` 中添加路由处理：**

```python
elif calc_type == 'new_type':
    result = calculator.new_calculator_method(
        param1=float(params['param1']),
        param2=float(params['param2'])
    )
```

### API 响应格式规范

**成功响应：**
```json
{
  "status": "success",
  "impedance": 50.25,
  "er_eff": 3.456,
  ...其他字段
}
```

**错误响应：**
```json
{
  "status": "error",
  "message": "错误描述信息"
}
```

### 测试后端 API

使用 curl 命令：
```bash
curl -X POST http://localhost:5000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "type": "microstrip",
    "params": {
      "width": 0.2,
      "height": 1.6,
      "thickness": 0.035,
      "dielectric": 4.3
    }
  }'
```

## 前端开发指南

### 添加新的计算类型

1. **在 `frontend/src/components/CalculatorForm.vue` 中的 `typeFields` 对象中添加：**

```javascript
new_type: [
  { key: 'param1', label: '参数1标签 (单位)', placeholder: '默认值', step: 0.01 },
  { key: 'param2', label: '参数2标签 (单位)', placeholder: '默认值', step: 0.01 },
  // ... 更多参数
]
```

2. **在表单 select 中添加选项：**

```html
<option value="new_type">新的计算类型描述</option>
```

3. **前端会自动生成表单字段和处理提交**

### Vue 3 组件结构

**CalculatorForm.vue：**
- 负责收集用户输入
- 验证输入参数
- 调用后端 API
- 发出计算结果事件

**ResultDisplay.vue：**
- 接收计算结果 props
- 格式化显示结果
- 提供导出功能

### 修改样式

编辑 `frontend/src/styles/global.css` 修改全局样式。

CSS 变量可在 `:root` 中修改：
```css
:root {
  --primary-color: #667eea;
  --secondary-color: #764ba2;
  --border-radius: 15px;
  --box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}
```

## 配置文件说明

### 后端配置

**`backend/.env`**
```
FLASK_ENV=development       # 运行环境
FLASK_DEBUG=True            # 调试模式
FLASK_PORT=5000             # 监听端口
```

### 前端配置

**`frontend/.env`**
```
VITE_API_URL=http://localhost:5000/api  # 后端 API 地址
```

**`frontend/vite.config.js`**
- 开发服务器代理配置
- 构建输出配置
- Source map 配置

## Docker 相关

### 构建镜像

```bash
# 构建所有镜像
docker-compose build

# 构建单个镜像
docker build -t pcb-backend ./backend
docker build -t pcb-frontend ./frontend
```

### 运行容器

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 重启服务
docker-compose restart
```

## 调试技巧

### 后端调试

1. 启用 Flask 调试模式（已在 `.env` 中配置）
2. 使用 `print()` 或 Python 日志模块
3. 使用 IDE 调试器设置断点

### 前端调试

1. 使用浏览器开发者工具 (F12)
2. 使用 Vue DevTools 浏览器扩展
3. 检查 Network 标签查看 API 请求

## 常见问题

### CORS 错误

如果出现跨域错误，检查：
1. 后端是否启用了 CORS
2. 前端 API URL 是否正确
3. 请求方法是否正确

### API 超时

如果计算超时：
1. 检查后端是否在运行
2. 检查防火墙设置
3. 增加 axios 超时时间（在 `api/index.js`）

### 前端连接不到后端

检查清单：
```bash
# 1. 后端是否运行
curl http://localhost:5000/health

# 2. 网络连通性
ping localhost

# 3. 检查防火墙
# 3. 检查前端 API URL 配置
```

## 编码规范

### Python 代码规范

- 使用 4 个空格缩进
- 遵守 PEP 8 规范
- 添加类型提示（可选）
- 添加适当的文档字符串

### JavaScript 代码规范

- 使用 2 个空格缩进
- 使用 ES6+ 语法
- 使用 Vue 3 Composition API
- 添加适当的注释

## 性能优化建议

1. **后端优化：**
   - 缓存材料库数据
   - 输入参数验证
   - 结果精度控制

2. **前端优化：**
   - 组件代码分割
   - 路由懒加载
   - 结果缓存

## 部署建议

### 生产环境

后端：
```bash
gunicorn -c gunicorn_config.py app:app
```

前端：
```bash
npm run build
# 使用 Nginx 或其他静态文件服务器
```

### 环境变量

生产环境应该在部署时设置正确的环境变量。

## 更新日志

### v1.0.0 (前后端分离初版)
- ✅ 完成前后端分离架构
- ✅ 实现 10 种传输线阻抗计算
- ✅ 集成材料库
- ✅ Docker 容器化
- ✅ 响应式前端设计

## 联系和支持

如有问题，请查看相应的 README 文件或检查日志文件。

---

**最后更新:** 2025年12月5日
