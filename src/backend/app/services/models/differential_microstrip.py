"""差分对模型"""
import math
from typing import Dict, Any
from .basic import BasicModel

class DifferentialMicrostrip(BasicModel):
    # 核心标识
    TYPE = "differential_microstrip"
    DISPLAY_NAME = "差分对微带 (Differential Microstrip)"
    LABEL = "differential_microstrip"
    
    # 模型参数
    PARAM_DEFINITIONS = [
        {'key': 'width', 'label': '线宽 (mm)', 'placeholder': '0.2', 'step': 0.01},
        {'key': 'spacing', 'label': '线间距 (mm)', 'placeholder': '0.2', 'step': 0.01},
        {'key': 'height', 'label': '介质厚度 (mm)', 'placeholder': '1.6', 'step': 0.01},
        {'key': 'thickness', 'label': '铜厚 (mm)', 'placeholder': '0.035', 'step': 0.001},
        {'key': 'dielectric', 'label': '介电常数', 'placeholder': '4.3', 'step': 0.01},
        {"key": "loss_tangent", "label": "损耗角正切", "placeholder": "0", "step": 0.001}
    ]

    def calculate(self) -> None:
        """差分对阻抗计算"""
        # 解包参数
        w = self.params["width"]
        s = self.params["spacing"]
        h = self.params["height"]
        t = self.params["thickness"]
        er = self.params["dielectric"]
        loss_tangent = self.params["loss_tangent"]

        # 有效介电常数
        er_eff = (er + 1) / 2 + (er - 1) / 2 * (1 + 12 * h / w) ** (-0.5)
        
        # 铜厚修正有效线宽
        w_eff = self._copper_width_correction(w, t, h)
        
        # 单端阻抗计算
        if w_eff / h < 1:
            z0_se = 60 / math.sqrt(er_eff) * math.log(8 * h / w_eff + w_eff / (4 * h))
        else:
            z0_se = 120 * math.pi / math.sqrt(er_eff) / (w_eff / h + 1.393 + 0.667 * math.log(w_eff / h + 1.444))
        
        # 耦合系数计算
        k = s / (s + 2 * w_eff)
        k_prime = math.sqrt(1 - k**2)
        
        # 差分阻抗计算
        if k < 0.7:
            coupling_factor = self._elliptic_integral_K(k) / self._elliptic_integral_K(k_prime)
        else:
            coupling_factor = math.pi / math.log(2 * (1 + math.sqrt(k_prime)) / (1 - math.sqrt(k_prime)))
        
        z0_diff = 2 * z0_se * (1 - 0.48 * math.exp(-0.96 * s / h))

        # 损耗计算
        loss_db_per_mm = 0
        if loss_tangent > 0:
            freq_ghz = 1.0  # 假设1GHz频率
            loss_db_per_mm = 27.3 * freq_ghz * math.sqrt(er_eff) * loss_tangent / z0_diff

        # 组装结果
        self.result.update({
            "impedance": round(z0_diff, 2),
            "single_ended_impedance": round(z0_se, 2),
            "er_eff": round(er_eff, 3),
            "effective_width": round(w_eff, 4),
            "coupling_coefficient": round(k, 4),
            "loss_db_per_mm": round(loss_db_per_mm, 4) if loss_tangent > 0 else 0
        })
