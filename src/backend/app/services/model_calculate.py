from .models import MODEL_MAP


def calculate(calc_type, params):
    # 验证模型类型
    if calc_type not in MODEL_MAP:
        return {
            "status": "error",
            "message": f"不支持的计算类型: {calc_type}"
        }

    # 实例化模型 + 计算
    model_class = MODEL_MAP[calc_type]
    model = model_class(params)
    result = model.get_result()
     
    return result