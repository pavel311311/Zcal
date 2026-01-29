"""导出所有传输线模型"""
from .microstrip import Microstrip
from .stripline import Stripline
from .differential import Differential
from .coaxial import Coaxial
from .cpw import CPW
from .cpwg import CPWG
from .asymmetric_stripline import AsymmetricStripline
from .broadside_striplines import BroadsideStriplines
from .differential_striplines import DifferentialStriplines


# 模型映射（路由层用）
MODEL_MAP = {
    "microstrip": Microstrip,
    "stripline": Stripline,
    "differential": Differential,
    "coaxial": Coaxial,
    "cpw": CPW,
    "cpwg": CPWG,
    "asymmetric_stripline": AsymmetricStripline,
    "broadside_striplines": BroadsideStriplines,
    "differential_striplines": DifferentialStriplines
}

__all__ = [
    "MODEL_MAP",
    "Microstrip",
    "Stripline",
    "Differential",
    "Coaxial",
    "CPW",
    "CPWG",
    "AsymmetricStripline",
    "BroadsideStriplines",
    "DifferentialStriplines"
]