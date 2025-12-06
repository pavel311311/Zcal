# gunicorn 配置文件
# 保存为: /home/pi/code/lala/RFZ-calculate/gunicorn_config.py

import multiprocessing
import os

# 项目根目录
project_dir = "/home/pi/code/lala/RFZ-calculate"

# 服务器配置
bind = "0.0.0.0:5000"
workers = 2  # 树莓派使用2个worker进程比较合适
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 5

# 日志配置
logs_dir = os.path.join(project_dir, "scripts")
accesslog = os.path.join(logs_dir, "access.log")
errorlog = os.path.join(logs_dir, "error.log")
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# 进程管理
pidfile = os.path.join(logs_dir, "gunicorn.pid")
daemon = True
user = "pi"
group = "pi"

# 应用配置
chdir = os.path.join(project_dir, "src")
pythonpath = os.path.join(project_dir, "src")

# 性能优化
preload_app = True
max_requests = 1000
max_requests_jitter = 100

# 安全
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190