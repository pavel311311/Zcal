from .models import MODEL_MAP


def calculate(calc_type, params):
    """
    执行阻抗计算
    
    Args:
        calc_type: 模型类型标识符
        params: 计算参数字典
        
    Returns:
        计算结果字典
        
    Raises:
        ValueError: 不支持的计算类型或参数错误
    """
    # 验证模型类型，抛出异常让路由统一处理
    if calc_type not in MODEL_MAP:
        raise ValueError(f"不支持的计算类型: {calc_type}")

    # 实例化模型 + 计算（参数校验由 BasicModel.__init__ 负责）
    model_class = MODEL_MAP[calc_type]
    model = model_class(params)
    result = model.get_result()
     
    return result