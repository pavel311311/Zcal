"""带状线模型"""
import math
from typing import Dict, Any
from .basic import BasicModel

# 导入scikit-rf库
from skrf.media import MLine
from skrf import Frequency

class Stripline(BasicModel):
    # 核心标识
    TYPE = "stripline"
    DISPLAY_NAME = "带状线 (Stripline)"
    LABEL = "stripline"
    # 结果定义
    RESULT_DEFINITIONS = [
        {'key': 'impedance', 'label': '特征阻抗', 'unit': 'Ω', 'precision': 2},
        {'key': 'er_eff', 'label': '有效介电常数', 'unit': '', 'precision': 3},
        {'key': 'effective_width', 'label': '有效宽度', 'unit': 'mm', 'precision': 4},
        {'key': 'loss_db_per_mm', 'label': '损耗', 'unit': 'dB/mm', 'precision': 4}
    ]
    # 模型参数
    PARAM_DEFINITIONS = [
        {'key': 'frequency', 'label': '频率 F (GHz)', 'placeholder': '1', 'step': 0.1},
        {'key': 'width', 'label': '线宽 W (mm)', 'placeholder': '0.2', 'step': 0.01},
        {'key': 'height', 'label': '介质厚度 H (mm)', 'placeholder': '1.6', 'step': 0.01},
        {'key': 'thickness', 'label': '铜厚 T (mm)', 'placeholder': '0.035', 'step': 0.001},
        {'key': 'dielectric', 'label': '介电常数 ε_r', 'placeholder': '4.3', 'step': 0.01},
        {"key": "loss_tangent", "label": "损耗角正切 tanδ", "placeholder": "0", "step": 0.001}
    ]

    def calculate(self) -> Dict[str, Any]:
        """带状线阻抗计算 - 结合scikit-rf库和准确的计算公式"""
        # 解包参数
        width = self.params["width"]  # mm
        height = self.params["height"]  # mm
        thickness = self.params["thickness"]  # mm
        er = self.params["dielectric"]
        loss_tangent = self.params["loss_tangent"]
        frequency = self.params.get('frequency', 1)  # GHz

        # 创建频率对象
        freq_ghz = frequency
        freq_hz = freq_ghz * 1e9  # 转换为Hz
        freq = Frequency(freq_hz, freq_hz, 1, unit='hz')

        # 转换为米
        w = width / 1000  # 转换为米
        h = height / 1000  # 转换为米
        t = thickness / 1000  # 转换为米

        # 计算有效宽度（考虑导体厚度的影响）
        # 对于带状线，导体厚度的影响是增加有效宽度
        delta_w = t / (2 * math.pi) * math.log(4 * math.e / (t * math.pi / (2 * h)))
        w_eff = w + delta_w
        effective_width = w_eff * 1000  # 转换回毫米

        # 计算带状线特征阻抗
        # 使用Hammerstad公式（适用于宽带状线）
        if w_eff / h > 0.35:
            # 宽带状线公式
            impedance = (60 / math.sqrt(er)) * math.log((1.9 * (2 * h + w_eff)) / (0.8 * w_eff + 2 * t))
        else:
            # 窄带状线公式
            k = (math.pi * w_eff) / (2 * h)
            k_prime = math.sqrt(1 - k**2)
            # 计算第一类完全椭圆积分
            # 这里使用近似值，实际应用中可能需要更精确的计算
            impedance = (60 / math.sqrt(er)) * (math.pi / (2 * math.log(2 * (1 + math.sqrt(k_prime)) / (1 - math.sqrt(k_prime)))))

        # 有效介电常数（带状线中等于基板介电常数）
        er_eff = er

        # 使用scikit-rf的MLine类计算损耗
        # 注意：这里使用MLine类来近似计算损耗，因为它考虑了频率和材料特性
        mline_obj = MLine(
            frequency=freq,
            w=w,
            h=h / 2,  # 带状线的有效高度是介质厚度的一半
            t=t,
            ep_r=er,
            tand=loss_tangent
        )

        # 计算损耗
        alpha = float(mline_obj.gamma[0].real)  # 衰减常数 (Np/m)
        loss_db_per_mm = alpha * 8.686 / 1000  # 转换为 dB/mm

        # 组装结果（交由 BasicModel.get_result() 统一格式化）
        self.result["impedance"] = impedance
        self.result["er_eff"] = er_eff
        self.result["effective_width"] = effective_width
        self.result["loss_db_per_mm"] = loss_db_per_mm if loss_tangent > 0 else 0
        
        return self.result
