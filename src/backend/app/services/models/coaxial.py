"""同轴线模型"""
import math
from typing import Dict, Any
from .basic import BasicModel

class Coaxial(BasicModel):
    # 核心标识
    TYPE = "coaxial"
    DISPLAY_NAME = "同轴线 (Coaxial)"
    LABEL = "coaxial"
    
    # 模型参数
    PARAM_DEFINITIONS = [
        {'key': 'inner_diameter', 'label': '内导体直径 (mm)', 'placeholder': '0.5', 'step': 0.01},
        {'key': 'outer_diameter', 'label': '外导体直径 (mm)', 'placeholder': '1.6', 'step': 0.01},
        {'key': 'dielectric', 'label': '介电常数', 'placeholder': '2.1', 'step': 0.01},
        {"key": "loss_tangent", "label": "损耗角正切", "placeholder": "0", "step": 0.001}
    ]

    def calculate(self) -> None:
        """同轴线阻抗计算"""
        # 解包参数
        d_inner = self.params["inner_diameter"]
        d_outer = self.params["outer_diameter"]
        er = self.params["dielectric"]
        loss_tangent = self.params["loss_tangent"]

        # 参数验证
        if d_outer <= d_inner:
            raise ValueError("外导体直径必须大于内导体直径")

        # 同轴线阻抗计算
        z0 = 60 / math.sqrt(er) * math.log(d_outer / d_inner)

        # 损耗计算
        loss_db_per_mm = 0
        if loss_tangent > 0:
            freq_ghz = 1.0  # 假设1GHz频率
            loss_db_per_mm = 27.3 * freq_ghz * math.sqrt(er) * loss_tangent / z0

        # 组装结果
        self.result.update({
            "impedance": round(z0, 2),
            "er_eff": er,  # 同轴线的有效介电常数等于填充介质的介电常数
            "diameter_ratio": round(d_outer / d_inner, 4),
            "loss_db_per_mm": round(loss_db_per_mm, 4) if loss_tangent > 0 else 0
        })
