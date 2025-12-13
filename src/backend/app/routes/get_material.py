"""
材料库API路由
"""
from flask import Blueprint, jsonify
from app.services.model_materials import substrate_materials

material_bp = Blueprint('material', __name__, url_prefix='')


@material_bp.route('/materials', methods=['GET'])
def get_materials():
    """
    获取预定义的基板材料列表
    """
    return jsonify(substrate_materials), 200
