"""微带线模型"""
import math
from typing import Dict, Any
from .basic import BasicModel

# 导入scikit-rf库
import skrf as rf
from skrf.media import mline

class Microstrip(BasicModel):
    # 核心标识
    TYPE = "microstrip"
    DISPLAY_NAME = "微带线 (Microstrip)"
    LABEL = "microstrip"
    
    # 模型参数
    PARAM_DEFINITIONS = [
        {'key': 'frequency', 'label': '频率 (GHz)', 'placeholder': '1', 'step': 0.1},
        {'key': 'width', 'label': '线宽 (mm)', 'placeholder': '0.2', 'step': 0.01},
        {'key': 'height', 'label': '介质厚度 (mm)', 'placeholder': '1.6', 'step': 0.01},
        {'key': 'thickness', 'label': '铜厚 (mm)', 'placeholder': '0.035', 'step': 0.001},
        {'key': 'dielectric', 'label': '介电常数', 'placeholder': '4.3', 'step': 0.01},
        {"key": "loss_tangent", "label": "损耗角正切", "placeholder": "0", "step": 0.001}
    ]

    def calculate(self) -> None:
        """微带线阻抗计算 - 使用scikit-rf库"""
        # 解包参数并转换为米
        w = self.params["width"] / 1000  # 转换为米
        h = self.params["height"] / 1000  # 转换为米
        t = self.params["thickness"] / 1000  # 转换为米
        er = self.params["dielectric"]
        loss_tangent = self.params["loss_tangent"]

        # 创建频率对象
        freq = self._create_frequency()

        # 使用scikit-rf的MLine类计算
        mline_obj = mline.MLine(
            frequency=freq,
            w=w,
            h=h,
            t=t,
            ep_r=er,
            tand=loss_tangent
        )

        # 获取计算结果
        # 直接使用标量值，避免numpy数组
        impedance = float(mline_obj.z0[0].real)
        er_eff = float(mline_obj.ep_reff_f[0].real)
        # 确保w_eff是实数
        w_eff = mline_obj.w_eff
        effective_width = float(w_eff.real) if hasattr(w_eff, 'real') else float(w_eff)
        
        # 计算损耗
        alpha = float(mline_obj.gamma[0].real)  # 衰减常数 (Np/m)
        loss_db_per_mm = alpha * 8.686 / 1000  # 转换为 dB/mm

        # 组装结果
        self.result.update({
            "impedance": round(impedance, 2),
            "er_eff": round(er_eff, 3),
            "effective_width": round(effective_width * 1000, 4),  # 转换回毫米
            "loss_db_per_mm": round(loss_db_per_mm, 4) if loss_tangent > 0 else 0
        })