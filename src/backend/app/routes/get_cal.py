"""
计算器API路由
"""
import time
from flask import Blueprint, request, jsonify
from app.services import calculate
from app.utils.logger import setup_logger, log_request, log_response, log_error, log_calculation

# 设置日志器
logger = setup_logger("calculator_api")

calculator_bp = Blueprint('calculator', __name__, url_prefix='')

@calculator_bp.route('/calculate', methods=['POST'])
def calculate_impedance():
    start_time = time.time()
    endpoint = "POST /calculate"
    
    try:
        # 1. 解析请求
        data = request.get_json()
        if not data:
            raise ValueError("请求体不能为空")
            
        calc_type = data.get('type')
        params = data.get('params', {})
        
        if not calc_type:
            raise ValueError("计算类型不能为空")
        
        # 记录请求日志
        log_request(logger, {"type": calc_type, "params": params}, endpoint)
        
        # 2. 执行计算
        result = calculate(calc_type, params)
        
        # 3. 记录计算日志
        log_calculation(logger, calc_type, params, result)
        
        # 4. 计算耗时并记录响应日志
        duration = time.time() - start_time
        log_response(logger, result, endpoint, duration)
        
        # 5. 返回结果
        status_code = 200 if result.get("status") == "success" else 400
        return jsonify(result), status_code

    except (KeyError, ValueError) as e:
        error_msg = f'{"缺少参数" if isinstance(e, KeyError) else "参数错误"}: {str(e)}'
        log_error(logger, e, endpoint)
        return jsonify({'status': 'error', 'message': error_msg}), 400
        
    except Exception as e:
        error_msg = f'计算错误: {str(e)}'
        log_error(logger, e, endpoint)
        return jsonify({'status': 'error', 'message': error_msg}), 500
