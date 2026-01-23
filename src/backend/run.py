"""
后端应用主入口
"""
import os
import sys

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

app = create_app()

if __name__ == '__main__':
    # 设置CORS允许所有来源（开发环境）
    os.environ.setdefault('CORS_ORIGINS', '*')
    
    app.run(
        debug=os.getenv('FLASK_ENV') == 'development',
        host='0.0.0.0',
        port=int(os.getenv('FLASK_PORT', 5000))
    )
