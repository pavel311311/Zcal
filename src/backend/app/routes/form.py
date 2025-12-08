"""
表单定义 API 路由
"""
from pyexpat import model
from flask import Blueprint, jsonify
from app.models.form_definitions import get_definitions, get_calculation_types

form_bp = Blueprint('form', __name__, url_prefix='')


@form_bp.route('/form_fields/<string:model>', methods=['GET'])  # 声明string类型的model路径参数
def get_form_fields(model):
    """返回指定模型的表单字段定义"""

    # 校验model参数有效性（可选，避免无效参数）
    if not model:
        return jsonify({"error": "model参数不能为空"}), 400
    try:
        defs = get_definitions(model)  # 调用你的业务函数
        return jsonify(defs), 200
    except Exception as e:
        return jsonify({"error": f"获取字段定义失败：{str(e)}"}), 500


@form_bp.route('/calculation_types', methods=['GET'])
def get_calculation_types_endpoint():
    """返回所有可用的计算类型"""
    types = get_calculation_types()
    return jsonify(types), 200
