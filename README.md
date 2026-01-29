# Zcal 项目

## 项目简介
Zcal 是一个阻抗计算工具，用于计算射频阻抗。
## 截图
![Zcal 截图](/docs/image2.png)

## 使用说明
1. 输入射频阻抗的实部和虚部。
2. 点击“计算”按钮。
3. 下方会显示计算结果。

## 直接访问网页服务：
<div align="center">

### [✔️ 🐸Zcal阻抗计算工具](https://gphlrjdsdibc.ap-southeast-1.clawcloudrun.com/)

</div>

## 安装说明
docker部署 
docker-compose 快速安装
1. 确保已安装 Docker 和 Docker Compose。
2. 克隆项目代码：
   ```bash
   git clone https://github.com/pavel311311/Zcal.git
   cd Zcal/docker
   ```
3. 拉取 Docker Hub 镜像：
   ```bash
   docker-compose pull
   ```
4. 启动服务：
   ```bash
   docker-compose up -d
   ```
访问web页面服务：`http://localhost:80`
