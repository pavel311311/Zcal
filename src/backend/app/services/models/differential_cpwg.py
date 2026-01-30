"""差分共面波导接地 (Differential CPWG) 模型"""
import math
from typing import Dict, Any
from .basic import BasicModel

# 导入scikit-rf库
import skrf as rf

class DifferentialCPWG(BasicModel):
    # 核心标识
    TYPE = "differential_cpwg"
    DISPLAY_NAME = "差分共面波导接地 (Differential CPWG)"
    LABEL = "differential_cpwg"
    
    # 模型参数
    PARAM_DEFINITIONS = [
        {'key': 'width', 'label': '线宽 (mm)', 'placeholder': '0.2', 'step': 0.01},
        {'key': 'gap', 'label': '缝隙宽度 (mm)', 'placeholder': '0.2', 'step': 0.01},
        {'key': 'spacing', 'label': '线间距 (mm)', 'placeholder': '0.4', 'step': 0.01},
        {'key': 'height', 'label': '介质厚度 (mm)', 'placeholder': '1.6', 'step': 0.01},
        {'key': 'thickness', 'label': '铜厚 (mm)', 'placeholder': '0.035', 'step': 0.001},
        {'key': 'dielectric', 'label': '介电常数', 'placeholder': '4.3', 'step': 0.01},
        {"key": "loss_tangent", "label": "损耗角正切", "placeholder": "0", "step": 0.001}
    ]

    def calculate(self) -> None:
        """差分共面波导接地阻抗计算 - 使用scikit-rf库"""
        # 解包参数并转换为米
        w = self.params["width"] / 1000  # 转换为米
        g = self.params["gap"] / 1000  # 转换为米
        t = self.params["thickness"] / 1000  # 转换为米
        er = self.params["dielectric"]
        loss_tangent = self.params["loss_tangent"]

        # 创建频率对象
        freq = self._create_frequency()

        # 注意：scikit-rf没有专门的差分共面波导接地类
        # 对于差分共面波导接地，我们使用近似方法计算
        # 这里使用CPW类并调整参数来近似计算差分共面波导接地
        cpw = rf.media.CPW(
            frequency=freq,
            w=w,
            s=g,  # scikit-rf中使用s表示缝隙宽度
            t=t,
            ep_r=er,
            tand=loss_tangent,
            has_metal_backside=True  # 差分共面波导接地有金属背面
        )

        # 获取计算结果
        z0_se = float(cpw.z0_characteristic[0].real)  # 单端阻抗
        z0_diff = z0_se * 2  # 差分阻抗
        er_eff = float(cpw.ep_reff_f[0].real)
        coupling_coefficient = w / (w + 2 * g)
        
        # 计算损耗
        alpha = float(cpw.gamma[0].real)  # 衰减常数 (Np/m)
        loss_db_per_mm = alpha * 8.686 / 1000  # 转换为 dB/mm

        # 组装结果
        self.result.update({
            "impedance": round(z0_diff, 2),
            "single_ended_impedance": round(z0_se, 2),
            "er_eff": round(er_eff, 3),
            "coupling_coefficient": round(coupling_coefficient, 4),
            "loss_db_per_mm": round(loss_db_per_mm, 4) if loss_tangent > 0 else 0
        })
