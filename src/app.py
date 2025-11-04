from flask import Flask, render_template, request, jsonify
import math
import json

app = Flask(__name__)

class PCBImpedanceCalculator:
    """PCB阻抗计算器类"""
    
    @staticmethod
    def microstrip_impedance(w, h, t, er, loss_tangent=0):
        """
        微带线阻抗计算
        w: 线宽 (mm)
        h: 介质厚度 (mm) 
        t: 铜厚 (mm)
        er: 介电常数
        loss_tangent: 损耗角正切
        """
        try:
            # 有效介电常数
            er_eff = (er + 1) / 2 + (er - 1) / 2 * (1 + 12 * h / w) ** (-0.5)
            
            # 考虑铜厚的修正
            w_eff = w + t * (1 + math.log(2 * h / t)) / math.pi
            
            # 阻抗计算
            if w_eff / h < 1:
                z0 = 60 / math.sqrt(er_eff) * math.log(8 * h / w_eff + w_eff / (4 * h))
            else:
                z0 = 120 * math.pi / math.sqrt(er_eff) / (w_eff / h + 1.393 + 0.667 * math.log(w_eff / h + 1.444))
            
            return {
                'impedance': round(z0, 2),
                'er_eff': round(er_eff, 3),
                'status': 'success'
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @staticmethod
    def stripline_impedance(w, h, t, er):
        """
        带状线阻抗计算
        w: 线宽 (mm)
        h: 介质总厚度 (mm)
        t: 铜厚 (mm)
        er: 介电常数
        """
        try:
            # 考虑铜厚的修正
            w_eff = w + t * (1 + math.log(4 * math.pi * w / t)) / math.pi
            
            # 阻抗计算
            if w_eff / h <= 0.35:
                z0 = 60 / math.sqrt(er) * math.log(4 * h / (0.67 * math.pi * (w_eff - t)))
            else:
                z0 = 94.15 / math.sqrt(er) / (w_eff / h + 0.92)
            
            return {
                'impedance': round(z0, 2),
                'status': 'success'
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @staticmethod
    def differential_impedance(w, s, h, t, er):
        """
        差分对阻抗计算
        w: 线宽 (mm)
        s: 线间距 (mm)
        h: 介质厚度 (mm)
        t: 铜厚 (mm)
        er: 介电常数
        """
        try:
            # 参数验证
            if w <= 0 or s <= 0 or h <= 0 or t < 0 or er < 1:
                return {'status': 'error', 'message': '参数值无效'}
            
            # 单端阻抗
            single_end = PCBImpedanceCalculator.microstrip_impedance(w, h, t, er)
            if single_end['status'] != 'success':
                return single_end
                
            z0_se = single_end['impedance']
            er_eff = single_end['er_eff']
            
            # 改进的耦合系数计算
            # 使用更准确的差分对公式
            w_eff = w + t * (1 + math.log(2 * h / t)) / math.pi if t > 0 else w
            
            # 计算耦合系数 k
            # 使用 Wadell 的公式
            A = math.exp(-0.5 * math.pi * s / h)
            B = math.exp(-0.5 * math.pi * (s + w_eff) / h)
            
            if s / h >= 0.1:  # 避免数值计算问题
                k = (A - B) / (A + B)
            else:
                # 对于很小的间距，使用近似公式
                k = s / (s + 2 * w_eff)
            
            # 确保 k 在合理范围内
            k = max(0.01, min(0.99, k))
            
            # 奇模阻抗和偶模阻抗
            if k < 0.7:
                # 使用精确公式
                k_prime = math.sqrt(1 - k**2)
                K_k = math.pi / 2 / math.log(2 * (1 + math.sqrt(k)) / (1 - math.sqrt(k)))
                K_k_prime = math.pi / 2 / math.log(2 * (1 + math.sqrt(k_prime)) / (1 - math.sqrt(k_prime)))
                
                z0_odd = z0_se * math.sqrt(1 - k * K_k / K_k_prime)
                z0_even = z0_se * math.sqrt(1 + k * K_k / K_k_prime)
            else:
                # 使用简化公式避免数值问题
                z0_odd = z0_se / (1 + k)
                z0_even = z0_se * (1 + k)
            
            # 差分阻抗
            z_diff = 2 * z0_odd
            
            # 共模阻抗
            z_common = z0_even / 2
            
            return {
                'differential_impedance': round(z_diff, 2),
                'single_ended_impedance': round(z0_se, 2),
                'odd_mode_impedance': round(z0_odd, 2),
                'even_mode_impedance': round(z0_even, 2),
                'common_mode_impedance': round(z_common, 2),
                'coupling_coefficient': round(k, 4),
                'status': 'success'
            }
        except Exception as e:
            return {'status': 'error', 'message': f'差分对计算错误: {str(e)}'}

    @staticmethod
    def coaxial_impedance(inner_diameter, outer_diameter, er):
        """
        同轴线阻抗计算
        inner_diameter: 内导体直径 (mm)
        outer_diameter: 外导体内径 (mm)
        er: 介电常数
        """
        try:
            z0 = 60 / math.sqrt(er) * math.log(outer_diameter / inner_diameter)
            return {
                'impedance': round(z0, 2),
                'status': 'success'
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @staticmethod
    def gssg_impedance(w, s, g, h, t, er):
        """
        GSSG (Ground-Signal-Signal-Ground) 阻抗计算
        w: 信号线宽 (mm)
        s: 信号线间距 (mm)
        g: 信号线到地线的间距 (mm)
        h: 介质厚度 (mm)
        t: 铜厚 (mm)
        er: 介电常数
        """
        try:
            # 有效介电常数
            er_eff = (er + 1) / 2 + (er - 1) / 2 * (1 + 12 * h / w) ** (-0.5)
            
            # 考虑铜厚的有效线宽
            w_eff = w + t * (1 + math.log(2 * h / t)) / math.pi
            
            # 单端阻抗 (忽略耦合)
            z0_se = 120 * math.pi / math.sqrt(er_eff) / (w_eff / h + 1.393 + 0.667 * math.log(w_eff / h + 1.444))
            
            # 耦合因子计算
            k1 = s / (s + 2 * w)  # 信号间耦合
            k2 = (s + 2 * w) / (s + 2 * w + 2 * g)  # 到地线的耦合
            
            # 差分阻抗
            z_diff = 2 * z0_se * math.sqrt(1 - k1 * k2)
            
            # 共模阻抗
            z_common = z0_se * math.sqrt((1 + k1) / (1 - k1)) / 2
            
            return {
                'differential_impedance': round(z_diff, 2),
                'common_mode_impedance': round(z_common, 2),
                'single_ended_impedance': round(z0_se, 2),
                'coupling_factor': round(k1, 4),
                'ground_coupling': round(k2, 4),
                'er_eff': round(er_eff, 3),
                'status': 'success'
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @staticmethod
    def embedded_microstrip_impedance(w, h1, h2, t, er1, er2):
        """
        嵌入式微带线阻抗计算 (上下不同介质)
        w: 线宽 (mm)
        h1: 上层介质厚度 (mm)
        h2: 下层介质厚度 (mm)  
        t: 铜厚 (mm)
        er1: 上层介电常数
        er2: 下层介电常数
        """
        try:
            # 等效介电常数
            er_eff = (er1 * h1 + er2 * h2) / (h1 + h2)
            
            # 等效介质厚度
            h_eff = (h1 + h2) * er_eff / ((er1 * h1 + er2 * h2) / (h1 + h2))
            
            # 考虑铜厚
            w_eff = w + t * (1 + math.log(2 * h_eff / t)) / math.pi
            
            # 阻抗计算
            if w_eff / h_eff < 1:
                z0 = 60 / math.sqrt(er_eff) * math.log(8 * h_eff / w_eff + w_eff / (4 * h_eff))
            else:
                z0 = 120 * math.pi / math.sqrt(er_eff) / (w_eff / h_eff + 1.393 + 0.667 * math.log(w_eff / h_eff + 1.444))
            
            return {
                'impedance': round(z0, 2),
                'er_eff': round(er_eff, 3),
                'h_eff': round(h_eff, 3),
                'status': 'success'
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @staticmethod
    def offset_stripline_impedance(w, h, b, t, er):
        """
        偏移带状线阻抗计算
        w: 线宽 (mm)
        h: 总介质厚度 (mm)
        b: 信号线到下层接地层距离 (mm)
        t: 铜厚 (mm)
        er: 介电常数
        """
        try:
            # 到上层接地层的距离
            a = h - b
            
            # 考虑铜厚
            w_eff = w + t * (1 + math.log(4 * math.pi * min(a, b) / t)) / math.pi
            
            # 偏移修正系数
            if a != b:
                offset_factor = 1 + (abs(a - b) / min(a, b)) * 0.1
            else:
                offset_factor = 1
            
            # 基本带状线阻抗
            if w_eff / min(a, b) <= 0.35:
                z0_base = 60 / math.sqrt(er) * math.log(4 * min(a, b) / (0.67 * math.pi * (w_eff - t)))
            else:
                z0_base = 94.15 / math.sqrt(er) / (w_eff / min(a, b) + 0.92)
            
            z0 = z0_base * offset_factor
            
            return {
                'impedance': round(z0, 2),
                'offset_factor': round(offset_factor, 3),
                'upper_distance': round(a, 3),
                'lower_distance': round(b, 3),
                'status': 'success'
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @staticmethod
    def grounded_coplanar_waveguide_impedance(w, s, h, t, er):
        """
        接地共面波导 (GCPW) 阻抗计算 - 简化版本
        w: 信号线宽 (mm)
        s: 信号线到地线间距 (mm)
        h: 介质厚度 (mm)
        t: 铜厚 (mm)
        er: 介电常数
        """
        try:
            # 有效介电常数
            er_eff = (er + 1) / 2 + (er - 1) / 2 * (1 + 10 * h / (w + s)) ** (-0.5)
            
            # 几何参数
            k = w / (w + 2 * s)
            
            if k < 0.5:
                k_prime = math.sqrt(1 - k ** 2)
                K_ratio = math.pi / (2 * math.log(2 * (1 + math.sqrt(k_prime)) / (1 - math.sqrt(k_prime))))
            else:
                K_ratio = (2 / math.pi) * math.log(2 * (1 + math.sqrt(k)) / (1 - math.sqrt(k)))
            
            # 阻抗计算
            z0 = 30 * math.pi / math.sqrt(er_eff) / K_ratio
            
            return {
                'impedance': round(z0, 2),
                'er_eff': round(er_eff, 3),
                'k_parameter': round(k, 4),
                'status': 'success'
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @staticmethod
    def cpwg_impedance(w, s, h, t, er, g=None, gw=None):
        """
        CPWG (Coplanar Waveguide with Ground) 阻抗计算 - GSSG差分对结构
        GSSG = Ground-Signal-Signal-Ground (两个信号线的差分对)
        这是一种同时具备表层侧边接地和背面接地的差分传输线结构
        
        w: 单个信号线宽度 (mm)
        s: 两个信号线之间的间距 (mm)  
        h: 介质厚度 (mm)
        t: 金属厚度 (mm)
        er: 介电常数
        g: 信号线到地线的间距 (mm) - 新增参数
        gw: 地线宽度 (mm) - 新增参数
        
        基于GSSG差分对理论和IEEE标准，考虑完整的几何参数
        """
        try:
            # 输入参数验证和默认值设置
            if w <= 0 or s <= 0 or h <= 0 or t < 0 or er < 1:
                raise ValueError("输入参数必须为正值，且介电常数≥1")
            
            # 如果没有提供G和GW参数，使用默认值
            if g is None:
                g = w  # 默认信号到地间距等于信号线宽度
            if gw is None:
                gw = 3 * w  # 默认地线宽度为信号线宽度的3倍
                
            # 输入新参数验证
            if g <= 0 or gw <= 0:
                raise ValueError("信号到地间距G和地线宽度GW必须为正值")
            
            # 考虑金属厚度的几何修正
            w_eff = w + t * (1 + math.log(4 * h / t)) / math.pi if t > 0 else w
            
            # GSSG差分对完整几何参数
            # G-S-S-G结构：Ground-Signal-Signal-Ground
            # 总宽度：GW + G + W + S + W + G + GW
            
            # 1. 基于IEEE标准的CPWG差分对计算
            # 椭圆积分参数k的正确定义
            
            # 奇模参数 (差分驱动) - 两信号线反相
            # 奇模时，两信号线之间相当于有"虚拟地"
            a_odd = w_eff
            b_odd = w_eff + 2 * g + s  # 总宽度
            
            # 椭圆积分的k参数
            k_odd = a_odd / b_odd
            k_odd_prime = math.sqrt(1 - k_odd * k_odd)
            
            # 偶模参数 (共模驱动) - 两信号线同相
            # 偶模时，两信号线可看作一个宽导体
            a_even = w_eff + s  # 两信号线+间距总宽度
            b_even = w_eff + s + 2 * g  # 到外侧地线的总宽度
            
            k_even = a_even / b_even
            k_even_prime = math.sqrt(1 - k_even * k_even)
            
            # 2. 椭圆积分K(k)的计算
            def elliptic_integral_K(k):
                """计算完全椭圆积分K(k)"""
                if k < 0.7:
                    # 使用标准公式
                    return math.pi / math.log(2 * (1 + math.sqrt(k)) / (1 - math.sqrt(k)))
                else:
                    # k接近1时使用互补公式
                    k_prime = math.sqrt(1 - k * k)
                    return math.log(2 * (1 + math.sqrt(k_prime)) / (1 - math.sqrt(k_prime))) / math.pi
            
            K_odd = elliptic_integral_K(k_odd)
            K_even = elliptic_integral_K(k_even)
            
            # 3. 有效介电常数 - 基于填充因子
            # CPWG结构的填充因子
            q_odd = math.exp(-math.pi * K_odd * h / (2 * w_eff))
            q_even = math.exp(-math.pi * K_even * h / (2 * (w_eff + s)))
            
            # 有效介电常数
            er_eff_odd = (1 + er * q_odd) / (1 + q_odd)
            er_eff_even = (1 + er * q_even) / (1 + q_even)
            
            # 4. 奇偶模阻抗计算 - 标准CPWG公式
            Z_odd = (30 * math.pi / math.sqrt(er_eff_odd)) * (K_odd / math.pi)
            Z_even = (30 * math.pi / math.sqrt(er_eff_even)) * (K_even / math.pi)
            
            # 5. 差分阻抗和其他阻抗计算 - 标准公式
            Z_diff = 2 * Z_odd  # 差分阻抗 = 2 × 奇模阻抗
            Z_common = Z_even / 2  # 共模阻抗 = 偶模阻抗 / 2  
            Z_single = math.sqrt(Z_odd * Z_even)  # 单端阻抗 = √(奇模×偶模)
            
            # 6. 耦合系数 - 标准定义
            coupling_coefficient = (Z_even - Z_odd) / (Z_even + Z_odd)
            
            # 7. 几何参数的影响评估
            # 椭圆积分参数
            k_ratio_odd = k_odd
            k_ratio_even = k_even
            
            # 有效介电常数
            er_eff_final = (er_eff_odd + er_eff_even) / 2  # 平均值
            
            # 填充因子
            filling_factor = (q_odd + q_even) / 2
            
            # 8. 计算损耗
            if t > 0:
                # 导体损耗 (1GHz参考)
                Rs = math.sqrt(math.pi * 4e-7 * 1e9 / (58e6 * t * 1e-3))
                conductor_loss = Rs * (2 + w_eff / s) / (120 * math.sqrt(er_eff_final))
            else:
                conductor_loss = 0
            
            # 介质损耗
            tan_delta = 0.02  # 假设损耗角正切
            dielectric_loss = 27.3 * er * tan_delta * (er_eff_final - 1) / (er - 1) / math.sqrt(er_eff_final)
            
            return {
                'differential_impedance': round(Z_diff, 2),
                'single_ended_impedance': round(Z_single, 2), 
                'common_mode_impedance': round(Z_common, 2),
                'odd_mode_impedance': round(Z_odd, 2),
                'even_mode_impedance': round(Z_even, 2),
                'er_eff': round(er_eff_final, 3),
                'er_eff_odd': round(er_eff_odd, 3),
                'er_eff_even': round(er_eff_even, 3),
                'k_odd': round(k_odd, 4),
                'k_even': round(k_even, 4),
                'filling_factor': round(filling_factor, 4),
                'coupling_coefficient': round(coupling_coefficient, 4),
                'K_odd': round(K_odd, 4),
                'K_even': round(K_even, 4),
                'conductor_loss': round(conductor_loss, 4) if t > 0 else None,
                'dielectric_loss': round(dielectric_loss, 4),
                'signal_to_ground_gap': g,
                'ground_width': gw,
                'status': 'success'
            }
            
        except Exception as e:
            return {'status': 'error', 'message': f'CPWG计算错误: {str(e)}'}

    @staticmethod
    def broadside_coupled_stripline_impedance(w, h, s, t, er):
        """
        宽边耦合带状线阻抗计算
        w: 线宽 (mm)
        h: 介质厚度 (mm)
        s: 垂直间距 (mm)
        t: 铜厚 (mm)
        er: 介电常数
        """
        try:
            # 基本带状线阻抗
            w_eff = w + t * (1 + math.log(4 * math.pi * h / t)) / math.pi
            
            if w_eff / h <= 0.35:
                z0_base = 60 / math.sqrt(er) * math.log(4 * h / (0.67 * math.pi * (w_eff - t)))
            else:
                z0_base = 94.15 / math.sqrt(er) / (w_eff / h + 0.92)
            
            # 耦合修正
            coupling_factor = math.exp(-2 * math.pi * s / w) if s > 0 else 1
            
            # 差分和共模阻抗
            z_diff = z0_base * math.sqrt(1 - coupling_factor)
            z_common = z0_base * math.sqrt(1 + coupling_factor)
            
            return {
                'differential_impedance': round(z_diff, 2),
                'common_mode_impedance': round(z_common, 2),
                'single_ended_impedance': round(z0_base, 2),
                'coupling_factor': round(coupling_factor, 4),
                'status': 'success'
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    """打赏设置管理页面"""
    return render_template('admin.html')

@app.route('/api/calculate', methods=['POST'])
def calculate_impedance():
    try:
        data = request.get_json()
        calc_type = data.get('type')
        params = data.get('params', {})
        
        calculator = PCBImpedanceCalculator()
        
        if calc_type == 'microstrip':
            result = calculator.microstrip_impedance(
                w=float(params['width']),
                h=float(params['height']),
                t=float(params['thickness']),
                er=float(params['dielectric']),
                loss_tangent=float(params.get('loss_tangent', 0))
            )
        elif calc_type == 'stripline':
            result = calculator.stripline_impedance(
                w=float(params['width']),
                h=float(params['height']),
                t=float(params['thickness']),
                er=float(params['dielectric'])
            )
        elif calc_type == 'differential':
            result = calculator.differential_impedance(
                w=float(params['width']),
                s=float(params['spacing']),
                h=float(params['height']),
                t=float(params['thickness']),
                er=float(params['dielectric'])
            )
        elif calc_type == 'coaxial':
            result = calculator.coaxial_impedance(
                inner_diameter=float(params['inner_diameter']),
                outer_diameter=float(params['outer_diameter']),
                er=float(params['dielectric'])
            )
        elif calc_type == 'gssg':
            result = calculator.gssg_impedance(
                w=float(params['width']),
                s=float(params['spacing']),
                g=float(params['ground_spacing']),
                h=float(params['height']),
                t=float(params['thickness']),
                er=float(params['dielectric'])
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
                er=float(params['dielectric'])
            )
        elif calc_type == 'gcpw':
            result = calculator.grounded_coplanar_waveguide_impedance(
                w=float(params['width']),
                s=float(params['gap']),
                h=float(params['height']),
                t=float(params['thickness']),
                er=float(params['dielectric'])
            )
        elif calc_type == 'cpwg':
            result = calculator.cpwg_impedance(
                w=float(params['width']),
                s=float(params['gap']),
                h=float(params['height']),
                t=float(params['thickness']),
                er=float(params['dielectric']),
                g=float(params.get('signal_to_ground', params['width'])),  # 默认等于线宽
                gw=float(params.get('ground_width', 3 * float(params['width'])))  # 默认3倍线宽
            )
        elif calc_type == 'broadside_coupled':
            result = calculator.broadside_coupled_stripline_impedance(
                w=float(params['width']),
                h=float(params['height']),
                s=float(params['vertical_spacing']),
                t=float(params['thickness']),
                er=float(params['dielectric'])
            )
        else:
            result = {'status': 'error', 'message': '不支持的计算类型'}
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'计算错误: {str(e)}'})

@app.route('/api/materials')
def get_materials():
    """获取常用PCB材料的介电常数"""
    materials = {
        'FR4': {'er': 4.3, 'loss_tangent': 0.02, 'name': 'FR4 (标准)'},
        'FR4_HF': {'er': 4.1, 'loss_tangent': 0.015, 'name': 'FR4 (高频)'},
        'Rogers4003C': {'er': 3.38, 'loss_tangent': 0.0027, 'name': 'Rogers 4003C'},
        'Rogers4350B': {'er': 3.48, 'loss_tangent': 0.0037, 'name': 'Rogers 4350B'},
        'Isola370HR': {'er': 4.04, 'loss_tangent': 0.019, 'name': 'Isola 370HR'},
        'Teflon': {'er': 2.1, 'loss_tangent': 0.0002, 'name': 'Teflon/PTFE'},
        'Polyimide': {'er': 3.4, 'loss_tangent': 0.008, 'name': 'Polyimide'},
    }
    return jsonify(materials)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)