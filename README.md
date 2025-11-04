# PCB阻抗计算器

一个功能强大的PCB传输线阻抗计算Web应用，支持多种传输线类型的阻抗计算。

## 🚀 功能特点

- **多种传输线类型支持**：
  - 微带线 (Microstrip)
  - 带状线 (Stripline)  
  - 差分对 (Differential Pair)
  - 同轴线 (Coaxial)

- **预设材料库**：
  - FR4 (标准和高频)
  - Rogers 4003C/4350B
  - Isola 370HR
  - Teflon/PTFE
  - Polyimide

- **精确计算**：
  - 考虑铜厚修正
  - 有效介电常数计算
  - 耦合系数分析
  - 损耗角正切支持

- **现代化界面**：
  - 响应式设计
  - 直观的图形展示
  - 实时计算结果
  - 移动设备友好

## 📋 快速启动

### Windows系统

#### 方法一：使用PowerShell脚本（推荐）
```powershell
# 在项目目录中运行
.\start.ps1
```

#### 方法二：使用批处理文件
```cmd
# 双击运行或在命令行中执行
start.bat
```

### Linux/Mac系统
```bash
# 添加执行权限并运行
chmod +x start.sh
./start.sh
```

### 手动安装步骤

#### 1. 创建虚拟环境
```bash
python -m venv venv
```

#### 2. 激活虚拟环境
Windows:
```cmd
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

#### 3. 安装依赖
```bash
pip install -r requirements.txt
```

#### 4. 运行应用
```bash
cd src
python app.py
```

## 🐳 Docker 部署

```bash
# 使用 Docker Compose 部署
docker-compose up -d

# 或使用部署脚本
./deploy.sh prod
```

### 3. 访问应用

打开浏览器访问：`http://localhost:5000`

## 🔧 使用指南

### 微带线计算
- **适用场景**：外层走线，单面接地
- **主要参数**：线宽(W)、介质厚度(H)、铜厚(T)、介电常数(εr)
- **计算结果**：特征阻抗、有效介电常数

### 带状线计算  
- **适用场景**：内层走线，双面接地
- **主要参数**：线宽(W)、介质总厚度(H)、铜厚(T)、介电常数(εr)
- **计算结果**：特征阻抗

### 差分对计算
- **适用场景**：高速数字信号，抗干扰
- **主要参数**：线宽(W)、线间距(S)、介质厚度(H)、铜厚(T)、介电常数(εr)
- **计算结果**：差分阻抗、单端阻抗、耦合系数

### 同轴线计算
- **适用场景**：高频应用，射频信号
- **主要参数**：内导体直径(d)、外导体内径(D)、介电常数(εr)
- **计算结果**：特征阻抗

## 📊 技术参数

### 支持的单位
- **长度**：毫米 (mm)
- **阻抗**：欧姆 (Ω)
- **介电常数**：无量纲
- **损耗角正切**：无量纲

### 计算精度
- 阻抗精度：±1%（在有效参数范围内）
- 支持参数范围：
  - 线宽：0.05mm - 50mm
  - 介质厚度：0.1mm - 10mm
  - 介电常数：1.0 - 20.0

## 🧮 计算公式

### 微带线阻抗
```
Z₀ = (60/√εᵣₑff) × ln(8h/wₑff + wₑff/4h)  当 wₑff/h < 1
Z₀ = (120π/√εᵣₑff) / (wₑff/h + 1.393 + 0.667×ln(wₑff/h + 1.444))  当 wₑff/h ≥ 1
```

### 带状线阻抗
```
Z₀ = (60/√εᵣ) × ln(4h/(0.67π(wₑff-t)))  当 wₑff/h ≤ 0.35
Z₀ = 94.15/(√εᵣ × (wₑff/h + 0.92))  当 wₑff/h > 0.35
```

### 差分对阻抗
```
Z_diff = 2 × Z₀_se × (1 - k)
其中 k 为耦合系数，Z₀_se 为单端阻抗
```

### 同轴线阻抗
```
Z₀ = (60/√εᵣ) × ln(D/d)
```

## 🌐 API接口

### 计算阻抗
```http
POST /api/calculate
Content-Type: application/json

{
  "type": "microstrip",
  "params": {
    "width": 0.2,
    "height": 0.2,
    "thickness": 0.035,
    "dielectric": 4.3
  }
}
```

### 获取材料信息
```http
GET /api/materials
```

## 📚 常用材料参数

| 材料 | 介电常数 | 损耗角正切 | 应用场景 |
|------|----------|------------|----------|
| FR4 (标准) | 4.3 | 0.02 | 通用PCB |
| FR4 (高频) | 4.1 | 0.015 | 高频应用 |
| Rogers 4003C | 3.38 | 0.0027 | 高频/微波 |
| Rogers 4350B | 3.48 | 0.0037 | 高速数字 |
| Isola 370HR | 4.04 | 0.019 | 高速应用 |
| Teflon/PTFE | 2.1 | 0.0002 | 超高频 |
| Polyimide | 3.4 | 0.008 | 柔性板 |

## 🔍 设计建议

### 50Ω单端信号
- USB 2.0/3.0
- 时钟信号
- 单端控制信号

### 100Ω差分信号  
- USB 2.0/3.0差分对
- 以太网信号
- LVDS信号

### 75Ω同轴线
- 视频信号
- 射频信号

### 90Ω差分信号
- HDMI信号
- DisplayPort信号

## 🛠️ 项目结构

```
PCB_board_Res/
├── app.py              # Flask应用主文件
├── requirements.txt    # Python依赖
├── README.md          # 项目说明
├── templates/         # HTML模板
│   └── index.html     # 主页面
└── static/           # 静态资源文件夹
```

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进这个项目！

### 开发环境设置
1. Clone项目到本地
2. 安装依赖：`pip install -r requirements.txt`
3. 运行开发服务器：`python app.py`

### 提交规范
- 添加新功能前请先提交Issue讨论
- 代码需要通过基本测试
- 提交信息请使用中文，描述清楚修改内容

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- GitHub Issues
- 邮箱：[your-email@example.com]

---

**享受PCB设计的乐趣！** 🎯