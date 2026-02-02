"""差分对模型"""
import math
from typing import Dict, Any
from .basic import BasicModel

# 导入scikit-rf库
from skrf.media import mline
from skrf import Frequency

class DifferentialMicrostrip(BasicModel):
    # 核心标识
    TYPE = "differential_microstrip"
    DISPLAY_NAME = "差分对微带 (Differential Microstrip)"
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
        {'key': 'frequency', 'label': '频率 (GHz)', 'placeholder': '1', 'step': 0.1},
        {'key': 'width', 'label': '线宽 (mm)', 'placeholder': '0.2', 'step': 0.01},
        {'key': 'spacing', 'label': '线间距 (mm)', 'placeholder': '0.2', 'step': 0.01},
        {'key': 'height', 'label': '介质厚度 (mm)', 'placeholder': '1.6', 'step': 0.01},
        {'key': 'thickness', 'label': '铜厚 (mm)', 'placeholder': '0.035', 'step': 0.001},
        {'key': 'dielectric', 'label': '介电常数', 'placeholder': '4.3', 'step': 0.01},
        {"key": "loss_tangent", "label": "损耗角正切", "placeholder": "0", "step": 0.001}
    ]

    def calculate(self) -> None:
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
        freq_hz = freq_ghz * 1e9  # 转换为Hz
        freq = Frequency(freq_hz, freq_hz, 1, unit='hz')

        # 注意：scikit-rf没有专门的差分微带线类
        # 对于差分微带线，我们使用近似方法计算
        # 这里使用MLine类并调整参数来近似计算差分微带线
        mline_obj = mline.MLine(
            frequency=freq,
            w=w,
            h=h,
            t=t,
            ep_r=er,
            tand=loss_tangent
        )

        # 获取计算结果
        z0_se = float(mline_obj.z0[0].real)  # 单端阻抗
        # 差分阻抗计算（近似）
        z0_diff = 2 * z0_se * (1 - 0.48 * math.exp(-0.96 * s / h))
        er_eff = float(mline_obj.ep_reff_f[0].real)
        # 确保w_eff是实数
        w_eff = mline_obj.w_eff
        effective_width = float(w_eff.real) if hasattr(w_eff, 'real') else float(w_eff)
        coupling_coefficient = s / (s + 2 * effective_width)
        
        # 计算损耗
        alpha = float(mline_obj.gamma[0].real)  # 衰减常数 (Np/m)
        loss_db_per_mm = alpha * 8.686 / 1000  # 转换为 dB/mm

        # 组装结果（交由 BasicModel.get_result() 统一格式化）
        self.result["impedance"] = z0_diff
        self.result["single_ended_impedance"] = z0_se
        self.result["er_eff"] = er_eff
        self.result["effective_width"] = effective_width * 1000  # 转换回毫米
        self.result["coupling_coefficient"] = coupling_coefficient
        self.result["loss_db_per_mm"] = loss_db_per_mm if loss_tangent > 0 else 0
