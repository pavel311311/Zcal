"""
表单定义 API 路由
"""
# from pyexpat import model
from flask import Blueprint, jsonify, request
from app.services import  get_calculation_types

types_bp = Blueprint('types', __name__, url_prefix='')


@types_bp.route('/calculation_types', methods=['GET'])
def get_calculation_types_endpoint():
    """返回所有可用的计算类型"""
    types = get_calculation_types()
    return jsonify(types), 200