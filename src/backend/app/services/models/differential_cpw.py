"""差分共面波导 (Differential CPW) 模型"""
import math
from typing import Dict, Any
from .basic import BasicModel

# 导入scikit-rf库
from skrf.media import cpw
from skrf import Frequency

class DifferentialCPW(BasicModel):
    # 核心标识
    TYPE = "differential_cpw"
    DISPLAY_NAME = "差分共面波导 (Differential CPW)"
    LABEL = "differential_cpw"
    
    # 结果定义
    RESULT_DEFINITIONS = [
        {'key': 'impedance', 'label': '差分阻抗', 'unit': 'Ω', 'precision': 2},
        {'key': 'single_ended_impedance', 'label': '单端阻抗', 'unit': 'Ω', 'precision': 2},
        {'key': 'er_eff', 'label': '有效介电常数', 'unit': '', 'precision': 3},
        {'key': 'coupling_coefficient', 'label': '耦合系数', 'unit': '', 'precision': 4},
        {'key': 'loss_db_per_mm', 'label': '损耗', 'unit': 'dB/mm', 'precision': 4}
    ]
    
    # 模型参数
    PARAM_DEFINITIONS = [
        {'key': 'frequency', 'label': '频率 (GHz)', 'placeholder': '1', 'step': 0.1},
        {'key': 'width', 'label': '线宽 (mm)', 'placeholder': '0.2', 'step': 0.01},
        {'key': 'gap', 'label': '缝隙宽度 (mm)', 'placeholder': '0.2', 'step': 0.01},
        {'key': 'spacing', 'label': '线间距 (mm)', 'placeholder': '0.4', 'step': 0.01},
        {'key': 'thickness', 'label': '铜厚 (mm)', 'placeholder': '0.035', 'step': 0.001},
        {'key': 'dielectric', 'label': '介电常数', 'placeholder': '4.3', 'step': 0.01},
        {"key": "loss_tangent", "label": "损耗角正切", "placeholder": "0", "step": 0.001}
    ]

    def calculate(self) -> None:
        """差分共面波导阻抗计算 - 使用scikit-rf库"""
        # 解包参数并转换为米
        w = self.params["width"] / 1000  # 转换为米
        g = self.params["gap"] / 1000  # 转换为米
        t = self.params["thickness"] / 1000  # 转换为米
        er = self.params["dielectric"]
        loss_tangent = self.params["loss_tangent"]

        # 创建频率对象
        freq_ghz = self.params.get('frequency', 1)
        freq_hz = freq_ghz * 1e9  # 转换为Hz
        freq = Frequency(freq_hz, freq_hz, 1, unit='hz')

        # 注意：scikit-rf没有专门的差分共面波导类
        # 对于差分共面波导，我们使用近似方法计算
        # 这里使用CPW类并调整参数来近似计算差分共面波导
        cpw_obj = cpw.CPW(
            frequency=freq,
            w=w,
            s=g,  # scikit-rf中使用s表示缝隙宽度
            t=t,
            ep_r=er,
            tand=loss_tangent
        )

        # 获取计算结果
        z0_se = float(cpw_obj.z0[0].real)  # 单端阻抗
        z0_diff = z0_se * 2  # 差分阻抗
        er_eff = float(cpw_obj.ep_reff_f[0].real)
        coupling_coefficient = w / (w + 2 * g)
        
        # 计算损耗
        alpha = float(cpw_obj.gamma[0].real)  # 衰减常数 (Np/m)
        loss_db_per_mm = alpha * 8.686 / 1000  # 转换为 dB/mm

        # 组装结果
        self.result["impedance"] = round(z0_diff, 2)
        self.result["single_ended_impedance"] = round(z0_se, 2)
        self.result["er_eff"] = round(er_eff, 3)
        self.result["coupling_coefficient"] = round(coupling_coefficient, 4)
        self.result["loss_db_per_mm"] = round(loss_db_per_mm, 4) if loss_tangent > 0 else 0
