"""传输线基类 - 封装公共逻辑"""
import math

class BaseTransmissionLine:
    # 模型标识（子类必须重写）
    # 【核心】模型唯一标识（如'microstrip'）
    TYPE = None
    # 【核心】前端显示名称（如'微带线 (Microstrip)'）
    DISPLAY_NAME = None
    # 【核心】前端标签（与TYPE一致，兼容原有逻辑）
    LABEL = None
    # 【核心】表单字段定义（对应原FORM_DEFINITIONS的列表项）
    PARAM_DEFINITIONS = []
    # 默认参数（计算时兜底用）
    DEFAULT_PARAMS = {}

    def __init__(self, params: dict):
        """初始化：参数验证 + 赋值"""
        self.params = self._validate_and_format_params(params)
        self.result = {"status": "success"}

    def _validate_and_format_params(self, params: dict) -> dict:
        """参数验证与格式转换（公共方法）"""
        validated = {}
        for param_def in self.PARAM_DEFINITIONS:
            key = param_def["key"]
            # 获取参数（优先传参，其次默认值）
            value = params.get(key, self.DEFAULT_PARAMS.get(key))
            if value is None:
                raise ValueError(f"缺少必要参数: {key}")
            
            # 转换为浮点数
            try:
                validated[key] = float(value)
            except ValueError:
                raise ValueError(f"参数 {key} 必须是数字，当前值: {value}")
            
            # 非负验证（介电常数≥1）
            if key.startswith("dielectric") and validated[key] < 1:
                raise ValueError(f"介电常数 {key} 必须≥1")
            elif key not in ["loss_tangent"] and validated[key] < 0:
                raise ValueError(f"参数 {key} 不能为负数")
        return validated

    def _copper_width_correction(self, w: float, t: float, h: float) -> float:
        """铜厚修正（公共方法：计算有效线宽）"""
        if t <= 0 or h <= 0:
            return w
        return w + t * (1 + math.log(2 * h / t)) / math.pi

    def _elliptic_integral_K(self, k: float) -> float:
        """椭圆积分K(k)近似计算（公共方法）"""
        if k < 0.7:
            return math.pi / math.log(2 * (1 + math.sqrt(k)) / (1 - math.sqrt(k)))
        else:
            k_prime = math.sqrt(1 - k**2)
            return math.log(2 * (1 + math.sqrt(k_prime)) / (1 - math.sqrt(k_prime))) / math.pi

    def calculate(self) -> dict:
        """核心计算方法（子类必须重写）"""
        raise NotImplementedError("子类必须实现calculate方法")

    def get_result(self) -> dict:
        """获取计算结果（统一返回格式）"""
        try:
            self.calculate()
            return self.result
        except Exception as e:
            return {"status": "error", "message": str(e)}