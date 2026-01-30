"""同轴线模型"""
import math
from typing import Dict, Any
from .basic import BasicModel

# 导入scikit-rf库
import skrf as rf

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
        """同轴线阻抗计算 - 使用scikit-rf库"""
        # 解包参数并转换为米
        d_inner = self.params["inner_diameter"] / 1000  # 转换为米
        d_outer = self.params["outer_diameter"] / 1000  # 转换为米
        er = self.params["dielectric"]
        loss_tangent = self.params["loss_tangent"]

        # 参数验证
        if d_outer <= d_inner:
            raise ValueError("外导体直径必须大于内导体直径")

        # 创建频率对象
        freq = self._create_frequency()

        # 使用scikit-rf的Coaxial类计算
        coaxial = rf.media.Coaxial(
            frequency=freq,
            Dint=d_inner,
            Dout=d_outer,
            epsilon_r=er,
            tan_delta=loss_tangent
        )

        # 获取计算结果
        impedance = float(coaxial.z0[0].real)
        er_eff = er  # 同轴线的有效介电常数等于填充介质的介电常数
        diameter_ratio = d_outer / d_inner
        
        # 计算损耗
        alpha = float(coaxial.gamma[0].real)  # 衰减常数 (Np/m)
        loss_db_per_mm = alpha * 8.686 / 1000  # 转换为 dB/mm

        # 组装结果
        self.result.update({
            "impedance": round(impedance, 2),
            "er_eff": er_eff,
            "diameter_ratio": round(diameter_ratio, 4),
            "loss_db_per_mm": round(loss_db_per_mm, 4) if loss_tangent > 0 else 0
        })
