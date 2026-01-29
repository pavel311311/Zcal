"""差分带状线 (Differential Striplines) 模型"""
import math
from typing import Dict, Any
from .basic import BasicModel

class DifferentialStriplines(BasicModel):
    # 核心标识
    TYPE = "differential_striplines"
    DISPLAY_NAME = "差分带状线 (Differential Striplines)"
    LABEL = "differential_striplines"
    
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
        """差分带状线阻抗计算"""
        # 解包参数
        w = self.params["width"]
        s = self.params["spacing"]
        h = self.params["height"]
        t = self.params["thickness"]
        er = self.params["dielectric"]
        loss_tangent = self.params["loss_tangent"]

        # 铜厚修正有效线宽
        w_eff = self._copper_width_correction(w, t, h)
        
        # 差分带状线阻抗计算（简化）
        # 单端阻抗
        if w_eff / h <= 0.35:
            z0_se = 60 / math.sqrt(er) * math.log(4 * h / (0.67 * math.pi * (w_eff + t)))
        else:
            cf = 1 + (t / h) * (1 + math.log(2 * h / t))
            z0_se = 94.15 / math.sqrt(er) / (w_eff / h + cf)
        
        # 差分阻抗
        k = s / (s + 2 * w_eff)
        k_prime = math.sqrt(1 - k**2)
        coupling_factor = self._elliptic_integral_K(k) / self._elliptic_integral_K(k_prime)
        z0_diff = 2 * z0_se * (1 - coupling_factor)

        # 损耗计算
        loss_db_per_mm = 0
        if loss_tangent > 0:
            freq_ghz = 1.0  # 假设1GHz频率
            loss_db_per_mm = 27.3 * freq_ghz * math.sqrt(er) * loss_tangent / z0_diff

        # 组装结果
        self.result.update({
            "impedance": round(z0_diff, 2),
            "single_ended_impedance": round(z0_se, 2),
            "er_eff": er,  # 带状线的有效介电常数等于基板介电常数
            "effective_width": round(w_eff, 4),
            "coupling_coefficient": round(coupling_factor, 4),
            "loss_db_per_mm": round(loss_db_per_mm, 4) if loss_tangent > 0 else 0
        })
