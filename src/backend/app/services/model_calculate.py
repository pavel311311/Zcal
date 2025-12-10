from .models import MODEL_MAP
#调用MODEL_MAP中的各个模型类来动态生成表单定义和计算类型映射

def calculate(calc_type, params):
            # 2. 验证模型类型
    if calc_type not in MODEL_MAP:
        return {
                "status": "error",
                "message": f"不支持的计算类型: {calc_type}"
        }, 400

    # 3. 实例化模型 + 计算
    model_class = MODEL_MAP[calc_type]
    model = model_class(params)
    result = model.get_result()
    return result