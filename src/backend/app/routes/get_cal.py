"""
计算器API路由
"""
from flask import Blueprint, request, jsonify
from app.services import calculate

calculator_bp = Blueprint('calculator', __name__, url_prefix='')

@calculator_bp.route('/calculate', methods=['POST'])
def calculate_impedance():
    try:
        # 1. 解析请求
        data = request.get_json()
        calc_type = data.get('type')
        params = data.get('params', {})

        result = calculate(calc_type, params)

        # 4. 返回结果
        return jsonify(result), 200 if result["status"] == "success" else 400

    except KeyError as e:
        return jsonify({'status': 'error', 'message': f'缺少参数: {str(e)}'}), 400
    except ValueError as e:
        return jsonify({'status': 'error', 'message': f'参数错误: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'计算错误: {str(e)}'}), 500
