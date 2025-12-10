"""
表单定义 API 路由
"""
from pyexpat import model
from flask import Blueprint, jsonify, request
from app.services.form_definitions import get_definitions

form_bp = Blueprint('form', __name__, url_prefix='')


@form_bp.route('/form_fields', methods=['GET'])  # 去掉路径参数
def get_form_fields():
    """返回指定模型的表单字段定义"""
    # 从Query参数中获取model（而非路径参数）
    model = request.args.get('model', '')  # 关键：用request.args取?model=xxx
    
    # 校验model参数有效性
    if not model:
        return jsonify({"error": "model参数不能为空（请通过?model=xxx传递）"}), 400
    try:
        defs = get_definitions(model)
        return jsonify(defs), 200
    except Exception as e:
        return jsonify({"error": f"获取字段定义失败：{str(e)}"}), 500