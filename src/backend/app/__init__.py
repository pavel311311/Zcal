"""
PCB阻抗计算器 - 后端API主文件
"""
from flask import Flask, jsonify
from flask_cors import CORS
from .routes import calculator_bp, material_bp, form_bp, types_bp


def create_app():
    """创建Flask应用工厂函数"""
    app = Flask(__name__)
    
    # 配置
    app.config['JSON_AS_ASCII'] = False
    
    # 启用CORS支持跨域请求
    CORS(app, resources={
        r"/api/*": {
            "origins": ["*"],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })
    
    # 注册蓝图
    app.register_blueprint(calculator_bp, url_prefix='/api')
    app.register_blueprint(material_bp, url_prefix='/api')
    app.register_blueprint(form_bp, url_prefix='/api')
    app.register_blueprint(types_bp, url_prefix='/api')
    
    # 健康检查路由
    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy'}), 200
    
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