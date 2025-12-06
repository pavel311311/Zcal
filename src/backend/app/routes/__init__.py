"""
API路由模块
"""
from app.routes.calculator import calculator_bp
from app.routes.material import material_bp

__all__ = ['calculator_bp', 'material_bp']
