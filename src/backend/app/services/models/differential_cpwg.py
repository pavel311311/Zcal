"""差分共面波导接地 (Differential CPWG) 模型"""
import math
import numpy as np
from typing import Dict, Any
from .basic import BasicModel

# 导入scikit-rf库
from skrf.media import cpw
from skrf import Frequency

class DifferentialCPWG(BasicModel):
    # 核心标识
    TYPE = "differential_cpwg"
    DISPLAY_NAME = "差分共面波导接地 (Differential CPWG)"
    LABEL = "differential_cpwg"
    
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
        {'key': 'ground_width', 'label': '地平面宽度 (mm)', 'placeholder': '1.0', 'step': 0.01},
        {'key': 'thickness', 'label': '铜厚 (mm)', 'placeholder': '0.035', 'step': 0.001},
        {'key': 'dielectric_thickness', 'label': '介质厚度 (mm)', 'placeholder': '0.254', 'step': 0.001},
        {'key': 'dielectric', 'label': '介电常数', 'placeholder': '4.3', 'step': 0.01},
        {"key": "loss_tangent", "label": "损耗角正切", "placeholder": "0", "step": 0.001}
    ]

    def calculate(self) -> None:
        """差分共面波导接地阻抗计算 - 使用scikit-rf库"""
        # 解包参数并转换为米
        w = self.params["width"] / 1000  # 转换为米
        g = self.params["gap"] / 1000  # 转换为米
        spacing = self.params["spacing"] / 1000  # 转换为米
        t = self.params["thickness"] / 1000  # 转换为米
        h = self.params["dielectric_thickness"] / 1000  # 转换为米
        er = self.params["dielectric"]
        loss_tangent = self.params["loss_tangent"]

        # 创建频率对象
        freq_ghz = self.params.get('frequency', 1)
        freq = Frequency(freq_ghz, freq_ghz, 1, unit='ghz')

        # 使用CPW类计算单端阻抗
        cpw_obj = cpw.CPW(
            frequency=freq,
            w=w,
            s=g,  # scikit-rf中使用s表示缝隙宽度
            h=h,
            t=t,
            ep_r=er,
            tand=loss_tangent,
            has_ground=True
        )

        # 获取计算结果
        z0_se = float(cpw_obj.z0[0].real)  # 单端阻抗
        
        # 计算耦合修正因子 (Coupling Factor)
        # 参考单端到差分的转换经验公式
        # 差分阻抗通常在 2 * Z0 * (1 - 0.48 * exp(-0.96 * g/h)) 左右波动
        coupling_reduction = 1 - 0.48 * np.exp(-0.96 * (spacing / h))
        z0_diff = 2 * z0_se * coupling_reduction
        
        er_eff = float(cpw_obj.ep_reff_f[0].real)
        coupling_coefficient = spacing / (spacing + 2 * w)
        
        # 计算损耗
        alpha = float(cpw_obj.gamma[0].real)  # 衰减常数 (Np/m)
        loss_db_per_mm = alpha * 8.686 / 1000  # 转换为 dB/mm

        # 组装结果（交由 BasicModel.get_result() 统一格式化）
        self.result["impedance"] = z0_diff
        self.result["single_ended_impedance"] = z0_se
        self.result["er_eff"] = er_eff
        self.result["coupling_coefficient"] = coupling_coefficient
        self.result["loss_db_per_mm"] = loss_db_per_mm if loss_tangent > 0 else 0
