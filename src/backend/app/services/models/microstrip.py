"""微带线模型"""
import math
from .base_transmission_line import BaseTransmissionLine

class Microstrip(BaseTransmissionLine):
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

    def calculate(self):
        """微带线阻抗计算"""
        # 解包参数
        w = self.params["width"]
        h = self.params["height"]
        t = self.params["thickness"]
        er = self.params["dielectric"]
        loss_tangent = self.params["loss_tangent"]

        # 有效介电常数
        er_eff = (er + 1) / 2 + (er - 1) / 2 * (1 + 12 * h / w) ** (-0.5)
        # 铜厚修正有效线宽
        w_eff = self._copper_width_correction(w, t, h)

        # 阻抗计算（分场景）
        if w_eff / h < 1:
            z0 = 60 / math.sqrt(er_eff) * math.log(8 * h / w_eff + w_eff / (4 * h))
        else:
            z0 = 120 * math.pi / math.sqrt(er_eff) / (w_eff / h + 1.393 + 0.667 * math.log(w_eff / h + 1.444))

        # 组装结果
        self.result.update({
            "impedance": round(z0, 2),
            "er_eff": round(er_eff, 3),
            "effective_width": round(w_eff, 4)  # 补充有效线宽结果
        })