"""
材料库API路由
"""
from flask import Blueprint, jsonify

material_bp = Blueprint('material', __name__, url_prefix='')


@material_bp.route('/materials', methods=['GET'])
def get_materials():
    """
    获取常用PCB材料的介电常数
    GET /api/materials
    """
    materials = {
        'FR4': {'er': 4.3, 'loss_tangent': 0.02, 'name': 'FR4 (标准)'},
        'FR4_HF': {'er': 4.1, 'loss_tangent': 0.015, 'name': 'FR4 (高频)'},
        'Rogers4003C': {'er': 3.38, 'loss_tangent': 0.0027, 'name': 'Rogers 4003C'},
        'Rogers4350B': {'er': 3.48, 'loss_tangent': 0.0037, 'name': 'Rogers 4350B'},
        'Isola370HR': {'er': 4.04, 'loss_tangent': 0.019, 'name': 'Isola 370HR'},
        'Teflon': {'er': 2.1, 'loss_tangent': 0.0002, 'name': 'Teflon/PTFE'},
        'Polyimide': {'er': 3.4, 'loss_tangent': 0.008, 'name': 'Polyimide'},
    }
    return jsonify(materials), 200
