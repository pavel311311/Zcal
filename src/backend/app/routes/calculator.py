"""
计算器API路由
"""
from flask import Blueprint, request, jsonify
from app.services.calculator import PCBImpedanceCalculator

calculator_bp = Blueprint('calculator', __name__, url_prefix='')


@calculator_bp.route('/calculate', methods=['POST'])
def calculate_impedance():
    """
    阻抗计算接口
    POST /api/calculate
    """
    try:
        data = request.get_json()
        calc_type = data.get('type')
        params = data.get('params', {})
    # '''
    # 这里要修改 了~！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
    # 新增了materials处理 
    #     # 如果提供了材料名称，则可以在这里根据需要调整参数
    #      # ''' 
    
    # ''''''
        calculator = PCBImpedanceCalculator()
        
        if calc_type == 'microstrip':
            result = calculator.microstrip_impedance(
                w=float(params['width']),
                h=float(params['height']),
                t=float(params['thickness']),
                er=float(params['dk']),
                loss_tangent=float(params.get('df', 0))
            )
        elif calc_type == 'stripline':
            result = calculator.stripline_impedance(
                w=float(params['width']),
                h=float(params['height']),
                t=float(params['thickness']),
                er=float(params['dk'])
            )
        elif calc_type == 'differential':
            result = calculator.differential_impedance(
                w=float(params['width']),
                s=float(params['spacing']),
                h=float(params['height']),
                t=float(params['thickness']),
                er=float(params['dk'])
            )
        elif calc_type == 'coaxial':
            result = calculator.coaxial_impedance(
                inner_diameter=float(params['inner_diameter']),
                outer_diameter=float(params['outer_diameter']),
                er=float(params['dk'])
            )
        elif calc_type == 'gssg':
            result = calculator.gssg_impedance(
                w=float(params['width']),
                s=float(params['spacing']),
                g=float(params['ground_spacing']),
                h=float(params['height']),
                t=float(params['thickness']),
                er=float(params['dk'])
            )
        elif calc_type == 'embedded_microstrip':
            result = calculator.embedded_microstrip_impedance(
                w=float(params['width']),
                h1=float(params['upper_height']),
                h2=float(params['lower_height']),
                t=float(params['thickness']),
                er1=float(params['upper_dielectric']),
                er2=float(params['lower_dielectric'])
            )
        elif calc_type == 'offset_stripline':
            result = calculator.offset_stripline_impedance(
                w=float(params['width']),
                h=float(params['total_height']),
                b=float(params['bottom_distance']),
                t=float(params['thickness']),
                er=float(params['dk'])
            )
        elif calc_type == 'gcpw':
            result = calculator.grounded_coplanar_waveguide_impedance(
                w=float(params['width']),
                s=float(params['gap']),
                h=float(params['height']),
                t=float(params['thickness']),
                er=float(params['dk'])
            )
        elif calc_type == 'cpwg':
            result = calculator.cpwg_impedance(
                w=float(params['width']),
                s=float(params['gap']),
                h=float(params['height']),
                t=float(params['thickness']),
                er=float(params['dk']),
                g=float(params.get('signal_to_ground', params['width'])),
                gw=float(params.get('ground_width', 3 * float(params['width'])))
            )
        elif calc_type == 'broadside_coupled':
            result = calculator.broadside_coupled_stripline_impedance(
                w=float(params['width']),
                h=float(params['height']),
                s=float(params['vertical_spacing']),
                t=float(params['thickness']),
                er=float(params['dk'])
            )
        else:
            result = {'status': 'error', 'message': '不支持的计算类型'}
        
        return jsonify(result), 200 if result.get('status') == 'success' else 400
    
    except KeyError as e:
        return jsonify({'status': 'error', 'message': f'缺少参数: {str(e)}'}), 400
    except ValueError as e:
        return jsonify({'status': 'error', 'message': f'参数类型错误: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'计算错误: {str(e)}'}), 500
