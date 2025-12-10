"""
API路由模块
"""
from app.routes.calculator import calculator_bp
from app.routes.material import material_bp
from app.routes.get_models_form import form_bp
from app.routes.get_model_types import types_bp

__all__ = ['calculator_bp', 'material_bp', 'form_bp', 'types_bp']