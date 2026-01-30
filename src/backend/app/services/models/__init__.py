"""导出所有传输线模型"""
from .microstrip import Microstrip
from .stripline import Stripline
from .differential_microstrip import DifferentialMicrostrip
from .coaxial import Coaxial
from .cpw import CPW
from .cpwg import CPWG
from .asymmetric_stripline import AsymmetricStripline
from .broadside_striplines import BroadsideStriplines
from .differential_striplines import DifferentialStriplines
from .differential_cpw import DifferentialCPW
from .differential_cpwg import DifferentialCPWG


# 模型映射（路由层用）
MODEL_MAP = {
    "microstrip": Microstrip,
    "stripline": Stripline,
    "differential_microstrip": DifferentialMicrostrip,
    "coaxial": Coaxial,
    "cpw": CPW,
    "cpwg": CPWG,
    "asymmetric_stripline": AsymmetricStripline,
    "broadside_striplines": BroadsideStriplines,
    "differential_striplines": DifferentialStriplines,
    "differential_cpw": DifferentialCPW,
    "differential_cpwg": DifferentialCPWG
}

__all__ = [
    "MODEL_MAP",
    "Microstrip",
    "Stripline",
    "DifferentialMicrostrip",
    "Coaxial",
    "CPW",
    "CPWG",
    "AsymmetricStripline",
    "BroadsideStriplines",
    "DifferentialStriplines",
    "DifferentialCPW",
    "DifferentialCPWG"
]