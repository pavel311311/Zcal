# PCB 阻抗计算器 - 后端 (Flask)

这是PCB阻抗计算器的后端API应用，采用Flask框架和Python实现。

## 项目结构

```
backend/
├── app/
│   ├── __init__.py              # Flask应用工厂
│   ├── routes/                  # API路由
│   │   ├── __init__.py
│   │   ├── calculator.py        # 计算接口
│   │   └── material.py          # 材料库接口
│   ├── services/                # 业务逻辑
│   │   ├── __init__.py
│   │   └── calculator.py        # 阻抗计算核心算法
│   ├── models/                  # 数据模型
│   ├── utils/                   # 工具函数
│   └── config.py                # 应用配置
├── run.py                       # 应用入口
├── requirements.txt             # 依赖列表
├── README.md                    # 项目说明
└── .env                         # 环境变量
```

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 环境变量配置

创建 `.env` 文件：

```
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_PORT=5000
```

### 运行开发服务器

```bash
python run.py
```

服务将在 `http://localhost:5000` 启动

### 生产环境运行

```bash
gunicorn -c gunicorn_config.py app:app
```

## API 接口

### 1. 计算阻抗

**请求:**
```
POST /api/calculate
Content-Type: application/json

{
  "type": "microstrip",
  "params": {
    "width": 0.2,
    "height": 1.6,
    "thickness": 0.035,
    "dielectric": 4.3
  }
}
```

**支持的计算类型:**
- `microstrip` - 微带线
- `stripline` - 带状线
- `differential` - 差分对
- `coaxial` - 同轴线
- `gssg` - GSSG差分对
- `embedded_microstrip` - 嵌入式微带线
- `offset_stripline` - 偏移带状线
- `gcpw` - 接地共面波导
- `cpwg` - CPWG结构
- `broadside_coupled` - 宽边耦合带状线

**响应:**
```json
{
  "impedance": 50.23,
  "er_eff": 3.456,
  "status": "success"
}
```

### 2. 获取材料库

**请求:**
```
GET /api/materials
```

**响应:**
```json
{
  "FR4": {"er": 4.3, "loss_tangent": 0.02, "name": "FR4 (标准)"},
  "Rogers4003C": {"er": 3.38, "loss_tangent": 0.0027, "name": "Rogers 4003C"},
  ...
}
```

### 3. 健康检查

**请求:**
```
GET /health
```

**响应:**
```json
{"status": "healthy"}
```

## 核心算法

### PCBImpedanceCalculator 类

主要计算方法：

- `microstrip_impedance()` - 微带线阻抗
- `stripline_impedance()` - 带状线阻抗
- `differential_impedance()` - 差分对阻抗
- `coaxial_impedance()` - 同轴线阻抗
- `gssg_impedance()` - GSSG差分阻抗
- `embedded_microstrip_impedance()` - 嵌入式微带线
- `offset_stripline_impedance()` - 偏移带状线
- `grounded_coplanar_waveguide_impedance()` - GCPW阻抗
- `cpwg_impedance()` - CPWG阻抗（高级）
- `broadside_coupled_stripline_impedance()` - 宽边耦合

## 技术栈

- **Flask**: Web框架
- **Flask-CORS**: 跨域资源共享
- **Gunicorn**: WSGI服务器
- **Python 3.8+**: 编程语言

## 开发指南

### 添加新的计算方法

1. 在 `app/services/calculator.py` 中添加静态方法
2. 在 `app/routes/calculator.py` 中添加路由处理

### 项目规范

- 所有计算方法返回包含 `status` 字段的字典
- 成功返回 `{'status': 'success', ...}`
- 失败返回 `{'status': 'error', 'message': '...'}`

## 部署

### Docker 部署

```bash
docker build -t pcb-calculator-backend .
docker run -p 5000:5000 pcb-calculator-backend
```

### Docker Compose

```bash
docker-compose up -d
```

## 配置说明

### 环境变量

- `FLASK_ENV` - 运行环境 (development/production)
- `FLASK_DEBUG` - 调试模式
- `FLASK_PORT` - 监听端口

### CORS 配置

支持跨域请求，允许所有来源访问 `/api/*` 路由。

## 错误处理

所有错误响应格式：

```json
{
  "status": "error",
  "message": "错误描述"
}
```

## 性能优化

- 使用缓存来存储材料库数据
- 计算结果进行数值精度控制
- 输入参数验证和范围检查

## 许可证

MIT
