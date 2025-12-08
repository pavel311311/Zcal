"""
表单定义 API 路由
"""
from flask import Blueprint, jsonify
from app.models.form_definitions import get_definitions, get_calculation_types

form_bp = Blueprint('form', __name__, url_prefix='')


@form_bp.route('/form_fields', methods=['GET'])
def get_form_fields(model='microstrip'):
    """返回所有计算类型的表单字段定义"""
    defs = get_definitions(model)
    return jsonify(defs), 200


@form_bp.route('/calculation_types', methods=['GET'])
def get_calculation_types_endpoint():
    """返回所有可用的计算类型"""
    types = get_calculation_types()
    return jsonify(types), 200
