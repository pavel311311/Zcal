# 🥔🐸 Zcal 阻抗计算工具

> 在线版：[https://www.zcal.top/](https://www.zcal.top/)

![Zcal 截图](/docs/image2.png)

## 项目简介

Zcal 是一个面向 PCB / 射频工程师的**传输线阻抗计算工具**，提供 11 种常用传输线结构的特征阻抗、有效介电常数、损耗等参数的快速估算。前端基于 Vue 3 + Vite，后端基于 Python Flask + scikit-rf，集成 Nginx + Supervisor 单容器一键部署，并附带 SQLite 实现的轻量访问统计。

## ✨ 功能特性

- 🧮 **11 种传输线模型**：覆盖微带、带状、共面波导、同轴及其差分 / 非对称变体
- 🧱 **预置基板材料库**：FR4（标准/高频）、Rogers 4003C / 4350B、Isola 370HR、Teflon、Polyimide 等
- 📡 **频域参数**：有效介电常数 ε_eff、损耗角正切、损耗 dB/mm、耦合系数、不对称因子等
- 🧰 **动态表单**：每个模型的参数表由后端按 `MODEL_MAP` 动态生成，新增模型自动出现在前端
- 📊 **访问统计**：内置 SQLite + `POST /api/analytics/hit` 上报 + `GET /api/analytics/stats` 聚合
- 🐳 **Docker 一键部署**：多阶段构建，前端产物经 Nginx 反代到 Flask
- 🧪 **CI 自动化**：GitHub Actions 跑 pytest + npm run build 通过后再构建推送镜像到 Docker Hub

## 🧪 技术栈

| 层级       | 技术                                                                                |
| ---------- | ----------------------------------------------------------------------------------- |
| 前端       | Vue 3、Pinia、Vue Router、Axios、Vite 5                                             |
| 后端       | Python 3.11 / 3.13、Flask 3、Flask-CORS、python-dotenv、gunicorn                    |
| 电磁求解   | scikit-rf 1.9（`skrf.media.MLine / Coaxial / CPW` + 差分类经验修正）、scipy、numpy  |
| 反向代理   | Nginx 1.x                                                                           |
| 进程管理   | Supervisor                                                                          |
| 数据存储   | SQLite（访问统计 `analytics.db`）                                                   |
| 容器化     | Docker 多阶段构建（Node 20 构建前端 → Python 3.13 运行后端 + Nginx）                 |
| CI / CD    | GitHub Actions（pytest + npm run build + docker buildx 推送 Docker Hub）            |

## 📐 支持的传输线模型

Zcal 在 `src/backend/app/services/models/__init__.py` 的 `MODEL_MAP` 中注册了 **8 个**模型；另有 **3 个**模型类已实现但尚未注册到路由（`asymmetric_stripline`、`broadside_striplines`、`differential_striplines`），合计 **11 种**。

| #  | `type` 标识                  | 中文名                | 公式来源 / 精度说明                                                                                  | 备注             |
| -- | ---------------------------- | --------------------- | --------------------------------------------------------------------------------------------------- | ---------------- |
| 1  | `microstrip`                 | 微带线                | `skrf.media.mline.MLine`（Hammerstad 闭合式 + Wheeler 微扰修正，含频率色散与铜厚修正）              | 经典公式         |
| 2  | `stripline`                  | 带状线                | 宽带 / 窄带 Hammerstad 公式（窄带使用第一类椭圆积分近似）+ `skrf.media.MLine` 算损耗                  | 经典公式         |
| 3  | `coaxial`                    | 同轴线                | `skrf.media.Coaxial`（基于 `Z₀ = 60/√εᵣ · ln(D/d)`）                                                  | 经典公式         |
| 4  | `cpw`                        | 共面波导              | `skrf.media.cpw.CPW`（Ghione / Wenzel 修正）                                                          | 经典公式         |
| 5  | `cpwg`                       | 共面波导接地          | `skrf.media.cpw.CPW` + `has_metal_backside=True`                                                    | **经验近似**     |
| 6  | `differential_microstrip`    | 差分微带线            | `MLine` 算单端阻抗 + 奇模耦合修正 `f = 1 - 0.3·exp(-0.5·s/h)`，`Z_diff = 2·Z₀·f`                    | **经验近似**     |
| 7  | `differential_cpw`           | 差分共面波导          | `cpw.CPW` 算单端 + 经验耦合因子 `1 - 0.48·exp(-0.96·s/h)`                                           | **经验近似**     |
| 8  | `differential_cpwg`          | 差分共面波导接地      | `cpw.CPW(has_ground=True)` 算单端 + 经验耦合因子                                                     | **经验近似**     |
| 9  | `asymmetric_stripline`*      | 非对称带状线          | `MLine` 用 `(h₁+h₂)/2` 作等效高度 + 不对称因子 `h₁/(h₁+h₂)`                                          | **经验近似**     |
| 10 | `broadside_striplines`*      | 宽边耦合带状线        | `MLine(h=h/2)` + `Z_diff = 2·Z₀`（粗近似）                                                          | **经验近似**     |
| 11 | `differential_striplines`*   | 差分带状线            | `MLine(h=h/2)` + 椭圆积分 `K(k)/K(k')` 算耦合因子                                                    | **经验近似**     |

> 注：带 `*` 的 3 种模型已实现但**尚未注册到 `MODEL_MAP`**，目前不会出现在前端下拉框中；其它 8 种可直接通过 `/api/calculation_types` 与 `/api/form_fields` 调用。差分类、非对称、宽边耦合均依赖经验公式，仅供工程估算，量产请用专业场解（如 Ansys HFSS / Simbeor / Siwave）。

## 📂 目录结构

```
Zcal/
├── .github/
│   └── workflows/
│       └── docker-build-push.yml   # CI: pytest → npm build → docker buildx 推 Docker Hub
├── docs/                            # README 截图（image1/2/11.png）
├── src/
│   ├── backend/                     # Flask 后端
│   │   ├── app/
│   │   │   ├── __init__.py          # Flask 工厂 + CORS + 蓝图注册
│   │   │   ├── routes/              # API 蓝图（calculate/materials/form_fields/...）
│   │   │   ├── services/
│   │   │   │   ├── model_calculate.py
│   │   │   │   ├── model_form.py
│   │   │   │   ├── model_materials.py
│   │   │   │   └── models/          # 11 个传输线模型类 + MODEL_MAP
│   │   │   └── utils/logger.py
│   │   ├── requirements.txt
│   │   ├── run.py                   # 入口（python run.py 或 gunicorn）
│   │   └── .env.example
│   └── frontend/                    # Vue 3 前端
│       ├── src/                     # 视图、组件、Pinia store、API 客户端
│       ├── public/                  # 静态资源 + favicon
│       ├── .env.example             # VITE_API_URL 配置示例
│       ├── .env.production
│       ├── vite.config.js
│       └── package.json
├── tests/                           # pytest 回归基线（test_models_baseline.py）
├── Dockerfile                        # 多阶段构建（node 20 → python 3.13-slim）
├── docker-compose.yml                # 一键起容器，暴露 80 端口
├── nginx.conf                        # 前端静态 + /api 反代 Flask
├── supervisord.conf                  # 同时拉起 nginx + gunicorn
└── README.md                         # 你正在看的这个文件 🥔🐸
```

## 🚀 在线访问

<div align="center">

### [🐸 点击访问 https://www.zcal.top/](https://www.zcal.top/)

</div>

## 🛠️ 本地开发

### 1. 克隆仓库

```bash
git clone <your-repo-url> Zcal
cd Zcal
```

### 2. 后端（Flask + Python 3.11+）

```bash
cd src/backend

# 创建并激活虚拟环境
python3 -m venv .venv
source .venv/bin/activate           # Windows: .venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 复制环境变量（可选，默认端口 5000）
cp .env.example .env

# 启动开发服务器（FLASK_ENV=development 默认开启 debug）
python run.py
# 监听 http://localhost:5000
```

### 3. 前端（Vue 3 + Vite + Node 20）

```bash
cd src/frontend

# 配置后端地址（可选，默认就是 http://localhost:5000/api）
cp .env.example .env.local

# 安装依赖
npm install

# 启动开发服务器（自带 /api → http://localhost:5000 的代理）
npm run dev
# 访问 http://localhost:3000
```

### 4. 跑回归测试

```bash
# 在仓库根目录，需要先激活后端 venv
pytest tests -q
```

## 🐳 Docker 部署

仓库自带多阶段 `Dockerfile`（先 `node:20-alpine` 构前端，再 `python:3.13-slim` 跑 Flask + Nginx + Supervisor），以及 `docker-compose.yml` 一键拉起：

```bash
# 在仓库根目录
docker compose up -d --build

# 查看日志
docker compose logs -f zcal

# 销毁容器（数据卷 zcal_data 保留 SQLite 统计）
docker compose down
```

默认暴露宿主 `80` 端口，访问 [http://localhost/](http://localhost/) 即可。`/api/*` 走 Nginx 反代到容器内 `:5000` 的 Flask，`/health` 直接返回 `healthy`。

如需推送到自己的镜像仓库，可在 GitHub 仓库的 `Settings → Secrets` 配置 `DOCKER_HUB_USERNAME` 和 `DOCKER_HUB_TOKEN`，CI 会自动按 `main→latest` / `dev→dev` 推送。

## 🔌 API 接口

所有业务接口统一挂载在 `/api` 前缀下（健康检查除外）；CORS 默认 `http://localhost:3000`，可通过环境变量 `CORS_ORIGINS=*` 放开。

| 方法   | 路径                          | 说明                                                                       | 鉴权 |
| ------ | ----------------------------- | -------------------------------------------------------------------------- | ---- |
| `GET`  | `/health`                     | 健康检查，返回 `{status:"healthy", service, timestamp}`                     | 否   |
| `GET`  | `/api/health`                 | 同上，挂在 `/api` 前缀下供前端统一管理                                       | 否   |
| `GET`  | `/api/calculation_types`      | 返回所有可用计算类型（基于 `MODEL_MAP` 动态生成）                            | 否   |
| `GET`  | `/api/form_fields?model=xxx`  | 返回指定模型的表单字段定义（`PARAM_DEFINITIONS`），未传 `model` 时回退到 `microstrip` | 否   |
| `GET`  | `/api/materials`              | 返回预定义基板材料库（FR4 / Rogers / Isola / Teflon / Polyimide）             | 否   |
| `POST` | `/api/calculate`              | **核心**：执行阻抗计算，返回 `impedance / er_eff / loss_db_per_mm` 等         | 否   |
| `POST` | `/api/analytics/hit`          | 上报一次访问，写入 SQLite `visits` 表                                         | 否   |
| `GET`  | `/api/analytics/stats?date=YYYY-MM-DD` | 返回当日 PV / UV 与累计 PV / UV（不传 `date` 默认今天）             | 否   |

### `POST /api/calculate` 请求示例

```jsonc
// 微带线：线宽 0.2mm，介质 1.6mm FR4，铜厚 0.035mm，1GHz
{
  "type": "microstrip",
  "params": {
    "frequency": 1,
    "width": 0.2,
    "height": 1.6,
    "thickness": 0.035,
    "dielectric": 4.3,
    "loss_tangent": 0.02
  }
}
```

```jsonc
// 同轴线：Dout=1.6mm / Din=0.5mm，εr=2.1（≈50Ω 粗估）
{
  "type": "coaxial",
  "params": {
    "frequency": 1,
    "inner_diameter": 0.5,
    "outer_diameter": 1.6,
    "dielectric": 2.1,
    "loss_tangent": 0.0002
  }
}
```

```jsonc
// 差分共面波导：W=0.2 / G=0.2 / S=0.4，H=0.254mm FR4
{
  "type": "differential_cpw",
  "params": {
    "frequency": 5,
    "width": 0.2,
    "gap": 0.2,
    "spacing": 0.4,
    "thickness": 0.035,
    "dielectric_thickness": 0.254,
    "dielectric": 4.3,
    "loss_tangent": 0.02
  }
}
```

成功响应（`200`）：

```json
{
  "status": "success",
  "impedance": 140.38,
  "er_eff": 3.21,
  "loss_db_per_mm": 0.0014,
  "type": "microstrip"
}
```

失败响应（`400` / `500`）：

```json
{
  "status": "error",
  "message": "参数错误: 不支持的计算类型: foo"
}
```

### `POST /api/analytics/hit` 请求示例

```json
{
  "path": "/"
}
```

### `GET /api/analytics/stats` 响应示例

```json
{
  "date": "2026-09-28",
  "daily_visits": 42,
  "daily_unique_visitors": 17,
  "total_visits": 1337,
  "total_unique_visitors": 256
}
```

## ✅ 测试

后端在 `tests/` 下提供了基于 `pytest` 的**模型回归基线**（`test_models_baseline.py`），覆盖微带 / 带状 / 共面波导 / 同轴 / 差分微带 / 差分 CPW 等关键路径。

```bash
# 仓库根目录，先激活后端 venv 并安装 requirements.txt
pytest tests -q
```

CI 上每次 push / pull_request 都会自动跑这套测试，只有 backend 与 frontend build 全绿才会构建并推送 Docker 镜像。

## 📝 使用说明

1. 打开 [https://www.zcal.top/](https://www.zcal.top/)，选择传输线模型。
2. 按表单填写线宽、介质厚度、铜厚、介电常数、损耗角正切等参数。
3. 点击「计算」按钮，查看特征阻抗、有效介电常数、损耗等结果。

## 📄 许可证

本仓库**当前尚未包含 LICENSE 文件**。建议补充一份 MIT License 以便他人合法复用代码；本 PR 不直接生成 LICENSE，只在此处友情提醒一下 🐸。

## 🙏 致谢

- 电磁求解基于 [scikit-rf](https://scikit-rf.org/) 团队的工作。
- 部分差分类经验修正参考业界常见 Saturn PCB Toolkit / Siwave 公开资料。
- 🥔 土豆 & 🐸 青蛙，祝你阻抗匹配一次过！
