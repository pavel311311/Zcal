"""
后端应用主入口
"""
import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    # 设置CORS允许的来源（开发环境使用 * 允许所有）
    os.environ.setdefault('CORS_ORIGINS', '*')
    
    app.run(
        debug=os.getenv('FLASK_ENV') == 'development',
        host='0.0.0.0',
        port=int(os.getenv('FLASK_PORT', 5000))
    )

