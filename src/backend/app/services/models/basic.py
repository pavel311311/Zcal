"""传输线基类 - 封装公共逻辑"""
import math
from typing import Dict, List, Any, Optional

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
        
        # 第一步：解析PARAM_DEFINITIONS中的placeholder作为默认值（转浮点数）
        param_defaults = {}
        for param_def in self.PARAM_DEFINITIONS:
            key = param_def["key"]
            placeholder = param_def.get("placeholder")
            if placeholder is None:
                raise ValueError(f"参数 {key} 未定义默认值（placeholder）")
            # 将placeholder字符串转为浮点数
            try:
                param_defaults[key] = float(placeholder)
            except (ValueError, TypeError):
                raise ValueError(f"参数 {key} 的默认值（placeholder）必须是数字，当前值: {placeholder}")
        
        # 第二步：参数验证与格式转换
        for param_def in self.PARAM_DEFINITIONS:
            key = param_def["key"]
            # 获取参数（优先传参，其次用placeholder默认值）
            value = params.get(key, param_defaults[key])
            
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

    def _copper_width_correction(self, w: float, t: float, h: float) -> float:
        """铜厚修正（公共方法：计算有效线宽）"""
        if t <= 0 or h <= 0:
            return w
        return w + t * (1 + math.log(2 * h / t)) / math.pi

    def _elliptic_integral_K(self, k: float) -> float:
        """椭圆积分K(k)近似计算（公共方法）"""
        if not (0 <= k <= 1):
            raise ValueError(f"椭圆积分参数k必须在[0,1]范围内，当前值: {k}")
            
        if k < 0.7:
            return math.pi / math.log(2 * (1 + math.sqrt(k)) / (1 - math.sqrt(k)))
        else:
            k_prime = math.sqrt(1 - k**2)
            return math.log(2 * (1 + math.sqrt(k_prime)) / (1 - math.sqrt(k_prime))) / math.pi

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