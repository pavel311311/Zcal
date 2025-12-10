"""
计算器API路由
"""
from flask import Blueprint, request, jsonify
from app.services.models import MODEL_MAP

calculator_bp = Blueprint('calculator', __name__, url_prefix='')

@calculator_bp.route('/calculate', methods=['POST'])
def calculate_impedance():
    """
    阻抗计算接口
    POST /api/calculate
    请求体示例：
    {
        "type": "microstrip",
        "params": {"width": 0.2, "height": 1.6, "thickness": 0.035, "dielectric": 4.3}
    }
    """
    try:
        # 1. 解析请求
        data = request.get_json()
        calc_type = data.get('type')
        params = data.get('params', {})

        # 2. 验证模型类型
        if calc_type not in MODEL_MAP:
            return jsonify({
                "status": "error",
                "message": f"不支持的计算类型: {calc_type}"
            }), 400

        # 3. 实例化模型 + 计算
        model_class = MODEL_MAP[calc_type]
        model = model_class(params)
        result = model.get_result()

        # 4. 返回结果
        return jsonify(result), 200 if result["status"] == "success" else 400

    except KeyError as e:
        return jsonify({'status': 'error', 'message': f'缺少参数: {str(e)}'}), 400
    except ValueError as e:
        return jsonify({'status': 'error', 'message': f'参数错误: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'计算错误: {str(e)}'}), 500
