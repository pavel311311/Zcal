# RFZ-calculate 服务启动脚本

本目录包含用于管理 RFZ-calculate Flask 应用程序的服务脚本。

## 文件说明

### setup.sh
一键安装和配置脚本，包含：
- Python 环境检查
- 虚拟环境创建（可选）
- 依赖包安装
- 权限设置
- 应用测试
- 可选的立即启动

### start.sh
启动 RFZ-calculate Flask 应用程序的脚本。
- 自动激活 Python 虚拟环境（如果存在）
- 优先使用 gunicorn（生产环境）
- 降级到 Flask 开发服务器
- 记录进程 PID 用于后续管理
- 输出日志到相应的日志文件

### stop.sh
停止 RFZ-calculate Flask 应用程序的脚本。
- 优雅地停止应用进程
- 清理 gunicorn 和 Flask 残留进程
- 删除 PID 文件

### service_manager.sh
系统服务管理脚本，用于配置开机自启动。

### monitor.sh
应用状态监控脚本，包含：
- 进程状态检查
- 网络连接测试
- 日志文件分析
- 资源使用监控
- 健康状态报告

## 使用方法

### 一键安装（推荐）

```bash
# 运行安装脚本
bash /home/pi/code/lala/RFZ-calculate/scripts/setup.sh
```

安装脚本会自动完成：
- 环境检查
- 依赖安装
- 权限设置
- 应用测试

### 手动设置权限

如果需要手动设置，首次使用前需要设置脚本的可执行权限：

```bash
chmod +x /home/pi/code/lala/RFZ-calculate/scripts/*.sh
```

### 手动启动/停止应用

```bash
# 启动应用
/home/pi/code/lala/RFZ-calculate/scripts/start.sh

# 停止应用
/home/pi/code/lala/RFZ-calculate/scripts/stop.sh
```

### 配置开机自启动

```bash
# 安装开机自启动服务
sudo bash /home/pi/code/lala/RFZ-calculate/scripts/service_manager.sh install

# 卸载开机自启动服务
sudo bash /home/pi/code/lala/RFZ-calculate/scripts/service_manager.sh uninstall

# 查看服务状态
bash /home/pi/code/lala/RFZ-calculate/scripts/service_manager.sh status
```

### 系统服务控制

安装服务后，可以使用 systemctl 命令管理：

```bash
# 启动服务
sudo systemctl start rfz-calculate

# 停止服务
sudo systemctl stop rfz-calculate

# 重启服务
sudo systemctl restart rfz-calculate

# 查看服务状态
sudo systemctl status rfz-calculate

# 查看实时日志
sudo journalctl -u rfz-calculate -f

# 查看应用日志
tail -f /home/pi/code/lala/RFZ-calculate/scripts/app.log

# 查看应用状态监控
/home/pi/code/lala/RFZ-calculate/scripts/monitor.sh
```

## 应用访问

应用启动后，可以通过以下地址访问：
- 本地访问: http://localhost:5000
- 网络访问: http://[树莓派IP地址]:5000

## 日志文件

### gunicorn 模式（推荐）
- 应用错误日志: `/home/pi/code/lala/RFZ-calculate/scripts/error.log`
- 访问日志: `/home/pi/code/lala/RFZ-calculate/scripts/access.log`
- 进程ID文件: `/home/pi/code/lala/RFZ-calculate/scripts/gunicorn.pid`

### Flask 开发模式
- 应用日志: `/home/pi/code/lala/RFZ-calculate/scripts/app.log`
- 进程ID文件: `/home/pi/code/lala/RFZ-calculate/scripts/app.pid`

### 系统日志
- 系统日志: 通过 `sudo journalctl -u rfz-calculate` 查看

## 配置文件

### gunicorn_config.py
项目根目录下的 gunicorn 配置文件，包含：
- 性能优化配置
- 日志配置
- 进程管理配置
- 安全设置

如果存在此文件，启动脚本将优先使用 gunicorn 作为 WSGI 服务器。

## 注意事项

1. 确保 Python 3 已安装
2. 确保项目依赖已安装: `pip install -r requirements.txt`
3. 推荐安装 gunicorn 以获得更好的生产性能: `pip install gunicorn`
4. 如果使用虚拟环境，确保 `.venv` 目录存在
5. 服务以 `pi` 用户身份运行
6. 启动脚本会自动选择最适合的服务器：
   - 优先使用 gunicorn（生产环境）
   - 降级到 Flask 开发服务器

## 故障排除

如果服务无法启动，请检查：

1. Python 环境是否正确配置
2. 项目依赖是否已安装
3. 端口 5000 是否被其他应用占用
4. 查看日志文件获取详细错误信息

```bash
# 检查端口占用
sudo netstat -tlnp | grep :5000

# 查看详细日志 - gunicorn 模式
tail -f /home/pi/code/lala/RFZ-calculate/scripts/error.log
tail -f /home/pi/code/lala/RFZ-calculate/scripts/access.log

# 查看详细日志 - Flask 开发模式
tail -f /home/pi/code/lala/RFZ-calculate/scripts/app.log

# 查看系统服务日志
sudo journalctl -u rfz-calculate -f

# 检查进程状态
ps aux | grep -E "(gunicorn|python3.*app\.py)"

# 完整状态监控
/home/pi/code/lala/RFZ-calculate/scripts/monitor.sh

# 仅检查网络连接
/home/pi/code/lala/RFZ-calculate/scripts/monitor.sh network
```