"""共面波导接地 (CPWG) 模型"""
import math
from typing import Dict, Any
from .basic import BasicModel

class CPWG(BasicModel):
    # 核心标识
    TYPE = "cpwg"
    DISPLAY_NAME = "共面波导接地 (CPWG)"
    LABEL = "cpwg"
    
    # 模型参数
    PARAM_DEFINITIONS = [
        {'key': 'width', 'label': '线宽 (mm)', 'placeholder': '0.2', 'step': 0.01},
        {'key': 'gap', 'label': '缝隙宽度 (mm)', 'placeholder': '0.2', 'step': 0.01},
        {'key': 'height', 'label': '介质厚度 (mm)', 'placeholder': '1.6', 'step': 0.01},
        {'key': 'thickness', 'label': '铜厚 (mm)', 'placeholder': '0.035', 'step': 0.001},
        {'key': 'dielectric', 'label': '介电常数', 'placeholder': '4.3', 'step': 0.01},
        {"key": "loss_tangent", "label": "损耗角正切", "placeholder": "0", "step": 0.001}
    ]

    def calculate(self) -> None:
        """共面波导接地阻抗计算"""
        # 解包参数
        w = self.params["width"]
        g = self.params["gap"]
        h = self.params["height"]
        t = self.params["thickness"]
        er = self.params["dielectric"]
        loss_tangent = self.params["loss_tangent"]

        # 有效介电常数（简化计算）
        er_eff = (er + 1) / 2
        
        # 耦合因子计算
        k = w / (w + 2 * g)
        k_prime = math.sqrt(1 - k**2)
        
        # 椭圆积分计算
        K_k = self._elliptic_integral_K(k)
        K_k_prime = self._elliptic_integral_K(k_prime)
        
        # 阻抗计算
        z0 = 60 / math.sqrt(er_eff) * (K_k_prime / K_k)

        # 损耗计算
        loss_db_per_mm = 0
        if loss_tangent > 0:
            freq_ghz = 1.0  # 假设1GHz频率
            loss_db_per_mm = 27.3 * freq_ghz * math.sqrt(er_eff) * loss_tangent / z0

        # 组装结果
        self.result.update({
            "impedance": round(z0, 2),
            "er_eff": round(er_eff, 3),
            "coupling_coefficient": round(k, 4),
            "loss_db_per_mm": round(loss_db_per_mm, 4) if loss_tangent > 0 else 0
        })
