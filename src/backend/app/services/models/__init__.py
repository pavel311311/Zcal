"""导出所有传输线模型"""
from .microstrip import Microstrip
from .stripline import Stripline
from .differential import Differential
from .coaxial import Coaxial


# 模型映射（路由层用）
MODEL_MAP = {
    "microstrip": Microstrip,
    "stripline": Stripline,
    "differential": Differential,
    "coaxial": Coaxial,
}

__all__ = [
    "MODEL_MAP",
    "Microstrip",
    "Stripline",
    "Differential",
    "Coaxial",
]