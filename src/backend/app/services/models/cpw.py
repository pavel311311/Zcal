"""共面波导 (CPW) 模型"""
import math
from typing import Dict, Any
from .basic import BasicModel

# 导入scikit-rf库
import skrf as rf
from skrf.media import cpw

class CPW(BasicModel):
    # 核心标识
    TYPE = "cpw"
    DISPLAY_NAME = "共面波导 (CPW)"
    LABEL = "cpw"
    
    # 模型参数
    PARAM_DEFINITIONS = [
        {'key': 'width', 'label': '线宽 (mm)', 'placeholder': '0.2', 'step': 0.01},
        {'key': 'gap', 'label': '缝隙宽度 (mm)', 'placeholder': '0.2', 'step': 0.01},
        {'key': 'thickness', 'label': '铜厚 (mm)', 'placeholder': '0.035', 'step': 0.001},
        {'key': 'dielectric', 'label': '介电常数', 'placeholder': '4.3', 'step': 0.01},
        {"key": "loss_tangent", "label": "损耗角正切", "placeholder": "0", "step": 0.001}
    ]

    def calculate(self) -> None:
        """共面波导阻抗计算 - 使用scikit-rf库"""
        # 解包参数并转换为米
        w = self.params["width"] / 1000  # 转换为米
        g = self.params["gap"] / 1000  # 转换为米
        t = self.params["thickness"] / 1000  # 转换为米
        er = self.params["dielectric"]
        loss_tangent = self.params["loss_tangent"]

        # 创建频率对象
        freq = self._create_frequency()

        # 使用scikit-rf的CPW类计算
        cpw_obj = cpw.CPW(
            frequency=freq,
            w=w,
            s=g,  # scikit-rf中使用s表示缝隙宽度
            t=t,
            ep_r=er,
            tand=loss_tangent
        )

        # 获取计算结果
        impedance = float(cpw_obj.z0[0].real)
        er_eff = float(cpw_obj.ep_reff_f[0].real)
        coupling_coefficient = w / (w + 2 * g)
        
        # 计算损耗
        alpha = float(cpw_obj.gamma[0].real)  # 衰减常数 (Np/m)
        loss_db_per_mm = alpha * 8.686 / 1000  # 转换为 dB/mm

        # 组装结果
        self.result.update({
            "impedance": round(impedance, 2),
            "er_eff": round(er_eff, 3),
            "coupling_coefficient": round(coupling_coefficient, 4),
            "loss_db_per_mm": round(loss_db_per_mm, 4) if loss_tangent > 0 else 0
        })
