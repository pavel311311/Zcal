"""
PCB阻抗计算器 - 后端API主文件
"""
import os
from flask import Flask, jsonify
from flask_cors import CORS
from .routes import calculator_bp, material_bp, form_bp, types_bp, health_bp


def create_app():
    """创建Flask应用工厂函数"""
    app = Flask(__name__)
    
    # 配置
    app.config['JSON_AS_ASCII'] = False
    
    # 获取CORS允许的来源
    cors_origins = os.environ.get('CORS_ORIGINS', 'http://localhost:3000')
    
    # 如果设置为 '*' 或包含 '*'，则允许所有来源
    if cors_origins == '*' or '*' in cors_origins:
        origins_list = ["*"]
    else:
        # 将逗号分隔的字符串转换为列表
        origins_list = [origin.strip() for origin in cors_origins.split(',')]
    
    # 启用CORS支持跨域请求
    CORS(app, resources={
        r"/api/*": {
            "origins": origins_list,
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"],
            "supports_credentials": False  # 当使用 * 时必须为 False
        }
    })
    
    # 注册蓝图
    app.register_blueprint(calculator_bp, url_prefix='/api')
    app.register_blueprint(material_bp, url_prefix='/api')
    app.register_blueprint(form_bp, url_prefix='/api')
    app.register_blueprint(types_bp, url_prefix='/api')
    app.register_blueprint(health_bp)  # 健康检查不需要前缀
    
    # 根路径健康检查
    @app.route('/')
    def root():
        return jsonify({
            'service': 'PCB Impedance Calculator API',
            'status': 'running',
            'version': '1.0.0',
            'cors_origins': origins_list  # 显示当前CORS配置
        }), 200
    
    # 错误处理
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'status': 'error', 'message': '资源未找到'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'status': 'error', 'message': '服务器内部错误'}), 500
    
    return app


# if __name__ == '__main__':
#     app = create_app()
#     app.run(debug=True, host='0.0.0.0', port=5000)
__all__ = ['create_app']