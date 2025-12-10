"""
表单字段定义 - 后端统一存放计算类型对应的表单字段
"""
from app.services.models import MODEL_MAP


# 定义默认模型（兜底用）
DEFAULT_MODEL = 'microstrip'

# -------------------------- 动态生成配置（替代原有硬编码） --------------------------
def _get_dynamic_calculation_types():
    """从模型类动态生成 CALCULATION_TYPES"""
    calculation_types = {}
    for model_type, model_class in MODEL_MAP.items():
        calculation_types[model_type] = {
            'name': model_class.DISPLAY_NAME,
            'label': model_class.LABEL
        }
    return calculation_types

def _get_dynamic_form_definitions():
    """从模型类动态生成 FORM_DEFINITIONS"""
    form_definitions = {}
    for model_type, model_class in MODEL_MAP.items():
        form_definitions[model_type] = model_class.PARAM_DEFINITIONS
    return form_definitions

# 动态生成（替代原有硬编码的CALCULATION_TYPES/FORM_DEFINITIONS）
CALCULATION_TYPES = _get_dynamic_calculation_types()
FORM_DEFINITIONS = _get_dynamic_form_definitions()

#----------------------------------------------------------------------------------------------

# 定义默认模型（兜底用）

def get_definitions(model):
    """
    返回完整的表单定义字典
    :param model: 计算类型标识（字符串）
    :return: 对应模型的表单字段列表，无效时返回默认模型的字段
    """
    # 1. 参数类型校验：确保是字符串（非字符串则转成字符串，空值置为默认）
    if not isinstance(model, str):
        model = str(model) if model is not None else DEFAULT_MODEL
    
    # 2. 去除首尾空格，空字符串置为默认
    model = model.strip() or DEFAULT_MODEL
    
    # 3. 兜底：如果model不在定义中，返回默认模型
    # return FORM_DEFINITIONS.get(model, FORM_DEFINITIONS[DEFAULT_MODEL])
    return FORM_DEFINITIONS.get(model, FORM_DEFINITIONS[DEFAULT_MODEL])


def get_calculation_types():
    """返回所有计算类型"""
    return CALCULATION_TYPES