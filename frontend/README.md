# PCB 阻抗计算器 - 前端 (Vue 3)

这是PCB阻抗计算器的前端应用，采用Vue 3 + Vite构建。

## 项目结构

```
frontend/
├── src/
│   ├── components/          # Vue组件
│   │   ├── CalculatorForm.vue    # 计算表单组件
│   │   └── ResultDisplay.vue     # 结果显示组件
│   ├── views/              # 视图页面
│   ├── api/                # API服务
│   │   └── index.js        # 后端API客户端
│   ├── styles/             # 全局样式
│   │   └── global.css      # 全局样式文件
│   ├── utils/              # 工具函数
│   ├── App.vue             # 根组件
│   └── main.js             # 应用入口
├── public/                 # 静态资源
├── index.html              # HTML模板
├── package.json            # 项目依赖配置
├── vite.config.js          # Vite配置
└── README.md               # 项目说明

```

## 快速开始

### 安装依赖

```bash
npm install
```

### 开发模式运行

```bash
npm run dev
```

应用将在 `http://localhost:3000` 启动，API代理到 `http://localhost:5000`

### 生产构建

```bash
npm run build
```

生成的文件将输出到 `dist` 目录

### 预览构建结果

```bash
npm run preview
```

## 技术栈

- **Vue 3**: 前端框架
- **Vite**: 构建工具
- **Axios**: HTTP客户端
- **CSS3**: 样式

## 功能特性

- ✅ 多种传输线阻抗计算
- ✅ 材料库支持
- ✅ 实时参数验证
- ✅ 详细的计算结果显示
- ✅ 结果导出功能
- ✅ 响应式设计

## 环境变量

在 `.env` 文件中配置：

```
VITE_API_URL=http://localhost:5000/api
```

## 主要组件说明

### CalculatorForm.vue
- 计算类型选择
- 动态表单字段生成
- 材料库集成
- 参数验证和提交

### ResultDisplay.vue
- 计算结果展示
- 多种阻抗值显示
- 介电特性显示
- 结果导出功能

## API集成

前端通过 Axios 客户端调用后端API：

```javascript
// 计算阻抗
POST /api/calculate
{
  "type": "microstrip",
  "params": {...}
}

// 获取材料库
GET /api/materials
```

## 开发指南

1. 所有组件放在 `src/components` 目录
2. API调用放在 `src/api` 目录
3. 全局样式放在 `src/styles` 目录
4. 使用 `<script setup>` 语法编写组件

## 部署

### Docker 部署

```bash
docker build -t pcb-calculator-frontend .
docker run -p 3000:3000 pcb-calculator-frontend
```

### Nginx 配置

```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://backend:5000/api/;
    }
}
```

## 浏览器支持

- Chrome (最新版)
- Firefox (最新版)
- Safari (最新版)
- Edge (最新版)

## 许可证

MIT
