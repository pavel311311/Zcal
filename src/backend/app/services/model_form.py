"""
表单字段定义 - 后端统一存放计算类型对应的表单字段
"""
from app.services.models import MODEL_MAP
#调用MODEL_MAP中的各个模型类来动态生成表单定义和计算类型映射


# --------------------------生成模型类型 --------------------------
def get_calculation_types():
    """从模型类动态生成 CALCULATION_TYPES"""
    calculation_types = []
    for model_type, model_class in MODEL_MAP.items():
        calculation_types.append({
            'type': model_type,
            'name': model_class.DISPLAY_NAME,
            'label': model_class.LABEL
        })
    return calculation_types

#------------------------------生成模型配置参数-----------------------------
# 定义默认模型（兜底用）
DEFAULT_MODEL = 'microstrip'
def get_form_definitions(model):
    """
    从模型类动态生成表单定义，并根据计算类型标识返回对应字段列表（含完整兜底逻辑）
    :param model: 计算类型标识（字符串）
    :return: 对应模型的表单字段列表，无效/空值时返回默认模型的字段
    """
    # 第一步：动态生成所有模型的表单定义字典
    form_definitions = {}
    for model_type, model_class in MODEL_MAP.items():
        form_definitions[model_type] = model_class.PARAM_DEFINITIONS
    
    # 第二步：参数校验与兜底处理
    # 1. 非字符串类型转换，空值直接置为默认
    if not isinstance(model, str):
        model = str(model) if model is not None else DEFAULT_MODEL
    # 2. 去除首尾空格，空字符串置为默认
    model = model.strip() or DEFAULT_MODEL
    # 3. 模型不存在时返回默认模型定义
    return form_definitions.get(model, form_definitions[DEFAULT_MODEL])


