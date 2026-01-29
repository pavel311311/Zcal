"""宽边耦合带状线 (Broadside Striplines) 模型"""
import math
from typing import Dict, Any
from .basic import BasicModel

class BroadsideStriplines(BasicModel):
    # 核心标识
    TYPE = "broadside_striplines"
    DISPLAY_NAME = "宽边耦合带状线 (Broadside Striplines)"
    LABEL = "broadside_striplines"
    
    # 模型参数
    PARAM_DEFINITIONS = [
        {'key': 'width', 'label': '线宽 (mm)', 'placeholder': '0.2', 'step': 0.01},
        {'key': 'spacing', 'label': '线间距 (mm)', 'placeholder': '0.4', 'step': 0.01},
        {'key': 'height', 'label': '介质厚度 (mm)', 'placeholder': '1.6', 'step': 0.01},
        {'key': 'thickness', 'label': '铜厚 (mm)', 'placeholder': '0.035', 'step': 0.001},
        {'key': 'dielectric', 'label': '介电常数', 'placeholder': '4.3', 'step': 0.01},
        {"key": "loss_tangent", "label": "损耗角正切", "placeholder": "0", "step": 0.001}
    ]

    def calculate(self) -> None:
        """宽边耦合带状线阻抗计算"""
        # 解包参数
        w = self.params["width"]
        s = self.params["spacing"]
        h = self.params["height"]
        t = self.params["thickness"]
        er = self.params["dielectric"]
        loss_tangent = self.params["loss_tangent"]

        # 铜厚修正有效线宽
        w_eff = self._copper_width_correction(w, t, h)
        
        # 宽边耦合带状线阻抗计算（简化）
        # 差分阻抗计算
        z0_diff = 120 / math.sqrt(er) * math.log(2 * (h + s) / (0.67 * math.pi * (w_eff + t)))
        
        # 单端阻抗
        z0_se = z0_diff / 2

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
            "loss_db_per_mm": round(loss_db_per_mm, 4) if loss_tangent > 0 else 0
        })
