"""传输线基类 - 封装公共逻辑"""
import math
from typing import Dict, List, Any, Optional

# 导入scikit-rf库
import skrf as rf
from skrf import Frequency

class BasicModel:
    # 模型标识（子类必须重写）
    TYPE: Optional[str] = None
    DISPLAY_NAME: Optional[str] = None
    LABEL: Optional[str] = None
    # 【核心】表单字段定义（包含placeholder作为默认值）
    PARAM_DEFINITIONS: List[Dict[str, Any]] = []

    def __init__(self, params: Dict[str, Any]):
        """初始化：参数验证 + 赋值"""
        self.params = self._validate_and_format_params(params)
        self.result: Dict[str, Any] = {"status": "success"}

    def _validate_and_format_params(self, params: Dict[str, Any]) -> Dict[str, float]:
        """参数验证与格式转换（公共方法）：从placeholder提取默认值"""
        if not self.PARAM_DEFINITIONS:
            raise ValueError(f"模型 {self.__class__.__name__} 未定义参数字段")
            
        validated = {}
        
        # 遍历一次完成所有操作：默认值提取、参数验证与格式转换
        for param_def in self.PARAM_DEFINITIONS:
            key = param_def["key"]
            placeholder = param_def.get("placeholder")
            
            if placeholder is None:
                raise ValueError(f"参数 {key} 未定义默认值（placeholder）")
            
            # 获取参数（优先传参，其次用placeholder默认值）
            value = params.get(key, placeholder)
            
            # 转换为浮点数
            try:
                validated[key] = float(value)
            except (ValueError, TypeError):
                raise ValueError(f"参数 {key} 必须是数字，当前值: {value}")
            
            # 参数范围验证
            self._validate_param_range(key, validated[key])
        
        return validated

    def _validate_param_range(self, key: str, value: float) -> None:
        """参数范围验证"""
        # 频率必须大于0
        if key == "frequency" and value <= 0:
            raise ValueError(f"频率必须大于0，当前值: {value}")
        
        # 介电常数必须≥1
        if key.startswith("dielectric") and value < 1:
            raise ValueError(f"介电常数 {key} 必须≥1，当前值: {value}")
        
        # 损耗角正切范围验证 (0-1)
        if key == "loss_tangent" and (value < 0 or value > 1):
            raise ValueError(f"损耗角正切必须在0-1之间，当前值: {value}")
        
        # 物理尺寸不能为负数
        if key in ["width", "height", "thickness", "spacing", "gap"] and value < 0:
            raise ValueError(f"物理尺寸 {key} 不能为负数，当前值: {value}")
        
        # 厚度不能为0
        if key in ["height", "thickness"] and value <= 0:
            raise ValueError(f"厚度参数 {key} 必须大于0，当前值: {value}")



    def calculate(self) -> Dict[str, Any]:
        """核心计算方法（子类必须重写）"""
        raise NotImplementedError(f"子类 {self.__class__.__name__} 必须实现calculate方法")

    def get_result(self) -> Dict[str, Any]:
        """获取计算结果（统一返回格式）"""
        try:
            self.calculate()
            return self.result
        except Exception as e:
            return {"status": "error", "message": str(e)}
    


    def _create_frequency(self) -> Frequency:
        """创建频率对象，用于scikit-rf库"""
        # 使用用户输入的频率参数
        freq_ghz = self.params.get('frequency', 1)
        freq_hz = freq_ghz * 1e9  # 转换为Hz
        return Frequency(freq_hz, freq_hz, 1, unit='hz')