"""差分带状线 (Differential Striplines) 模型"""
import math
from typing import Dict, Any
from .basic import BasicModel

# 导入scikit-rf库
import skrf as rf
from skrf.media import mline

class DifferentialStriplines(BasicModel):
    # 核心标识
    TYPE = "differential_striplines"
    DISPLAY_NAME = "差分带状线 (Differential Striplines)"
    LABEL = "differential_striplines"
    
    # 模型参数
    PARAM_DEFINITIONS = [
        {'key': 'width', 'label': '线宽 (mm)', 'placeholder': '0.2', 'step': 0.01},
        {'key': 'spacing', 'label': '线间距 (mm)', 'placeholder': '0.2', 'step': 0.01},
        {'key': 'height', 'label': '介质厚度 (mm)', 'placeholder': '1.6', 'step': 0.01},
        {'key': 'thickness', 'label': '铜厚 (mm)', 'placeholder': '0.035', 'step': 0.001},
        {'key': 'dielectric', 'label': '介电常数', 'placeholder': '4.3', 'step': 0.01},
        {"key": "loss_tangent", "label": "损耗角正切", "placeholder": "0", "step": 0.001}
    ]

    def calculate(self) -> None:
        """差分带状线阻抗计算 - 使用scikit-rf库"""
        # 解包参数并转换为米
        w = self.params["width"] / 1000  # 转换为米
        s = self.params["spacing"] / 1000  # 转换为米
        h = self.params["height"] / 1000  # 转换为米
        t = self.params["thickness"] / 1000  # 转换为米
        er = self.params["dielectric"]
        loss_tangent = self.params["loss_tangent"]

        # 创建频率对象
        freq = self._create_frequency()

        # 注意：scikit-rf没有专门的差分带状线类
        # 对于差分带状线，我们使用近似方法计算
        # 这里使用MLine类并调整参数来近似计算差分带状线
        mline_obj = mline.MLine(
            frequency=freq,
            w=w,
            h=h / 2,  # 差分带状线的有效高度是介质厚度的一半
            t=t,
            ep_r=er,
            tand=loss_tangent
        )

        # 获取计算结果
        z0_se = float(mline_obj.z0[0].real)  # 单端阻抗
        # 差分阻抗计算（近似）
        # 注意：实际的差分阻抗需要考虑耦合效应，这里使用简化的方法
        z0_diff = z0_se * 2  # 近似计算差分阻抗
        er_eff = er  # 差分带状线的有效介电常数等于基板介电常数
        # 确保w_eff是实数
        w_eff = mline_obj.w_eff
        effective_width = float(w_eff.real) if hasattr(w_eff, 'real') else float(w_eff)
        # 耦合系数计算
        k = s / (s + 2 * effective_width)
        k_prime = math.sqrt(1 - k**2)
        # 使用椭圆积分计算耦合因子
        from scipy.special import ellipk
        if k < 0.7:
            coupling_factor = ellipk(k) / ellipk(k_prime)
        else:
            coupling_factor = math.pi / math.log(2 * (1 + math.sqrt(k_prime)) / (1 - math.sqrt(k_prime)))
        
        # 计算损耗
        alpha = float(mline_obj.gamma[0].real)  # 衰减常数 (Np/m)
        loss_db_per_mm = alpha * 8.686 / 1000  # 转换为 dB/mm

        # 组装结果
        self.result.update({
            "impedance": round(z0_diff, 2),
            "single_ended_impedance": round(z0_se, 2),
            "er_eff": er_eff,
            "effective_width": round(effective_width * 1000, 4),  # 转换回毫米
            "coupling_coefficient": round(coupling_factor, 4),
            "loss_db_per_mm": round(loss_db_per_mm, 4) if loss_tangent > 0 else 0
        })
