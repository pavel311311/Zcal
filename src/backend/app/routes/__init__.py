"""
API路由模块
"""
from .get_cal import calculator_bp
from .get_material import material_bp
from .get_models_form import form_bp
from .get_model_types import types_bp

__all__ = ['calculator_bp', 'material_bp', 'form_bp', 'types_bp']