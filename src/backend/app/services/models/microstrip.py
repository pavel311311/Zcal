"""微带线模型"""
import math
from typing import Dict, Any
from .basic import BasicModel

class Microstrip(BasicModel):
    # 核心标识
    TYPE = "microstrip"
    DISPLAY_NAME = "微带线 (Microstrip)"
    LABEL = "microstrip"
    
    # 模型参数
    PARAM_DEFINITIONS = [
        {'key': 'width', 'label': '线宽 (mm)', 'placeholder': '0.2', 'step': 0.01},
        {'key': 'height', 'label': '介质厚度 (mm)', 'placeholder': '1.6', 'step': 0.01},
        {'key': 'thickness', 'label': '铜厚 (mm)', 'placeholder': '0.035', 'step': 0.001},
        {'key': 'dielectric', 'label': '介电常数', 'placeholder': '4.3', 'step': 0.01},
        {"key": "loss_tangent", "label": "损耗角正切", "placeholder": "0", "step": 0.001}
    ]

    def calculate(self) -> None:
        """微带线阻抗计算"""
        # 解包参数
        w = self.params["width"]
        h = self.params["height"]
        t = self.params["thickness"]
        er = self.params["dielectric"]
        loss_tangent = self.params["loss_tangent"]

        # 有效介电常数计算
        er_eff = (er + 1) / 2 + (er - 1) / 2 * (1 + 12 * h / w) ** (-0.5)
        
        # 铜厚修正有效线宽
        w_eff = self._copper_width_correction(w, t, h)

        # 阻抗计算（分场景优化）
        if w_eff / h < 1:
            # 窄线条件
            z0 = 60 / math.sqrt(er_eff) * math.log(8 * h / w_eff + w_eff / (4 * h))
        else:
            # 宽线条件
            z0 = 120 * math.pi / math.sqrt(er_eff) / (w_eff / h + 1.393 + 0.667 * math.log(w_eff / h + 1.444))

        # 损耗计算（如果有损耗角正切）
        loss_db_per_mm = 0
        if loss_tangent > 0:
            # 介质损耗计算 (简化公式)
            freq_ghz = 1.0  # 假设1GHz频率
            loss_db_per_mm = 27.3 * freq_ghz * math.sqrt(er_eff) * loss_tangent / z0

        # 组装结果
        self.result.update({
            "impedance": round(z0, 2),
            "er_eff": round(er_eff, 3),
            "effective_width": round(w_eff, 4),
            "loss_db_per_mm": round(loss_db_per_mm, 4) if loss_tangent > 0 else 0
        })