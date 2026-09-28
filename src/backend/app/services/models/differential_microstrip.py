"""差分对模型"""
import math
import numpy as np
from typing import Dict, Any
from .basic import BasicModel, as_scalar

# 导入scikit-rf库
from skrf.media import mline
from skrf import Frequency

class DifferentialMicrostrip(BasicModel):
    # 核心标识
    TYPE = "differential_microstrip"
    DISPLAY_NAME = "差分微带线 (Differential Microstrip)"
    LABEL = "differential_microstrip"
    
    # 结果定义
    RESULT_DEFINITIONS = [
        {'key': 'impedance', 'label': '差分阻抗', 'unit': 'Ω', 'precision': 2},
        {'key': 'single_ended_impedance', 'label': '单端阻抗', 'unit': 'Ω', 'precision': 2},
        {'key': 'er_eff', 'label': '有效介电常数', 'unit': '', 'precision': 3},
        {'key': 'effective_width', 'label': '有效宽度', 'unit': 'mm', 'precision': 4},
        {'key': 'coupling_coefficient', 'label': '耦合系数', 'unit': '', 'precision': 4},
        {'key': 'loss_db_per_mm', 'label': '损耗', 'unit': 'dB/mm', 'precision': 4}
    ]
    
    # 模型参数
    PARAM_DEFINITIONS = [
        {'key': 'frequency', 'label': '频率 F (GHz)', 'placeholder': '1', 'step': 0.1},
        {'key': 'width', 'label': '线宽 W (mm)', 'placeholder': '0.2', 'step': 0.01},
        {'key': 'spacing', 'label': '线间距 S (mm)', 'placeholder': '0.2', 'step': 0.01},
        {'key': 'height', 'label': '介质厚度 H (mm)', 'placeholder': '1.6', 'step': 0.01},
        {'key': 'thickness', 'label': '铜厚 T (mm)', 'placeholder': '0.035', 'step': 0.001},
        {'key': 'dielectric', 'label': '介电常数 ε_r', 'placeholder': '4.3', 'step': 0.01},
        {"key": "loss_tangent", "label": "损耗角正切 tanδ", "placeholder": "0", "step": 0.001}
    ]

    def calculate(self) -> Dict[str, Any]:
        """差分对阻抗计算 - 使用scikit-rf库"""
        # 解包参数并转换为米
        w = self.params["width"] / 1000  # 转换为米
        s = self.params["spacing"] / 1000  # 转换为米
        h = self.params["height"] / 1000  # 转换为米
        t = self.params["thickness"] / 1000  # 转换为米
        er = self.params["dielectric"]
        loss_tangent = self.params["loss_tangent"]

        # 创建频率对象
        freq_ghz = self.params.get('frequency', 1)
        freq = Frequency(freq_ghz, freq_ghz, 1, unit='ghz')

        # 使用 MLine 类计算单端阻抗
        ms = mline.MLine(
            frequency=freq,
            w=w,
            h=h,
            t=t,
            ep_r=er,
            tand=loss_tangent
        )

        # 获取计算结果（使用 as_scalar 安全提取，避免 numpy 数组转换 TypeError）
        z0_se = as_scalar(ms.z0[0].real)  # 单端（偶模近似）特征阻抗
        er_eff = as_scalar(ms.ep_reff_f[0].real)

        # ---- 差分/奇模耦合（经验近似, empirical approximation）----
        # 依据边耦合微带线奇模经验趋势：
        #   间距 s 增大 -> 耦合减弱 -> 奇模阻抗 Z_odd 上升 -> 差分阻抗上升
        #   当 s -> 无穷大, Z_odd -> Z0（单端）; 当 s -> 0, 耦合最强 Z_odd 下降。
        # 采用指数衰减的耦合强度模型（系数经 50Ω 差分对样本标定）。
        g = s / h
        coupling_strength = math.exp(-0.5 * g)          # 0<k<=1，s 越大越趋近 0
        f_coupling = 1 - 0.3 * coupling_strength         # 耦合越弱越趋近 1

        z_odd = z0_se * f_coupling
        z0_diff = 2 * z_odd

        # 计算有效宽度
        effective_width = as_scalar(ms.w_eff)

        # 计算耦合系数
        # 当线间距增大时，耦合系数减小
        coupling_coefficient = (2 * effective_width) / (s + 2 * effective_width)

        # 计算损耗
        alpha = as_scalar(ms.gamma[0].real)  # 衰减常数 (Np/m)
        loss_db_per_mm = alpha * 8.686 / 1000  # 转换为 dB/mm

        # 组装结果（交由 BasicModel.get_result() 统一格式化）
        self.result["impedance"] = z0_diff
        self.result["single_ended_impedance"] = z0_se
        self.result["er_eff"] = er_eff
        self.result["effective_width"] = effective_width * 1000  # 转换回毫米
        self.result["coupling_coefficient"] = coupling_coefficient
        self.result["loss_db_per_mm"] = loss_db_per_mm if loss_tangent > 0 else 0
        
        return self.result
