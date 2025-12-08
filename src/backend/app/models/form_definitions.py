"""
表单字段定义 - 后端统一存放计算类型对应的表单字段
"""

# 计算类型定义
CALCULATION_TYPES = {
    'microstrip': {'name': '微带线 (Microstrip)', 'label': 'microstrip'},
    'stripline': {'name': '带状线 (Stripline)', 'label': 'stripline'},
    'differential': {'name': '差分对 (Differential)', 'label': 'differential'},
    'coaxial': {'name': '同轴线 (Coaxial)', 'label': 'coaxial'},
    'gssg': {'name': 'GSSG 差分对', 'label': 'gssg'},
    'embedded_microstrip': {'name': '嵌入式微带线', 'label': 'embedded_microstrip'},
    'offset_stripline': {'name': '偏移带状线', 'label': 'offset_stripline'},
    'gcpw': {'name': '接地共面波导 (GCPW)', 'label': 'gcpw'},
    'cpwg': {'name': 'CPWG 结构', 'label': 'cpwg'},
    'broadside_coupled': {'name': '宽边耦合带状线', 'label': 'broadside_coupled'},
}

FORM_DEFINITIONS = {
    'microstrip': [
        {'key': 'width', 'label': '线宽 (mm)', 'placeholder': '0.2', 'step': 0.01},
        {'key': 'height', 'label': '介质厚度 (mm)', 'placeholder': '1.6', 'step': 0.01},
        {'key': 'thickness', 'label': '铜厚 (mm)', 'placeholder': '0.035', 'step': 0.001},
        {'key': 'dielectric', 'label': '介电常数', 'placeholder': '4.3', 'step': 0.01}
    ],
    'stripline': [
        {'key': 'width', 'label': '线宽 (mm)', 'placeholder': '0.2', 'step': 0.01},
        {'key': 'height', 'label': '介质总厚度 (mm)', 'placeholder': '1.6', 'step': 0.01},
        {'key': 'thickness', 'label': '铜厚 (mm)', 'placeholder': '0.035', 'step': 0.001},
        {'key': 'dielectric', 'label': '介电常数', 'placeholder': '4.3', 'step': 0.01}
    ],
    'differential': [
        {'key': 'width', 'label': '线宽 (mm)', 'placeholder': '0.2', 'step': 0.01},
        {'key': 'spacing', 'label': '线间距 (mm)', 'placeholder': '0.2', 'step': 0.01},
        {'key': 'height', 'label': '介质厚度 (mm)', 'placeholder': '1.6', 'step': 0.01},
        {'key': 'thickness', 'label': '铜厚 (mm)', 'placeholder': '0.035', 'step': 0.001},
        {'key': 'dielectric', 'label': '介电常数', 'placeholder': '4.3', 'step': 0.01}
    ],
    'coaxial': [
        {'key': 'inner_diameter', 'label': '内导体直径 (mm)', 'placeholder': '0.5', 'step': 0.01},
        {'key': 'outer_diameter', 'label': '外导体内径 (mm)', 'placeholder': '2.0', 'step': 0.01},
        {'key': 'dielectric', 'label': '介电常数', 'placeholder': '1.0', 'step': 0.01}
    ],
    'gssg': [
        {'key': 'width', 'label': '信号线宽 (mm)', 'placeholder': '0.2', 'step': 0.01},
        {'key': 'spacing', 'label': '信号线间距 (mm)', 'placeholder': '0.2', 'step': 0.01},
        {'key': 'ground_spacing', 'label': '信号到地距离 (mm)', 'placeholder': '0.5', 'step': 0.01},
        {'key': 'height', 'label': '介质厚度 (mm)', 'placeholder': '1.6', 'step': 0.01},
        {'key': 'thickness', 'label': '铜厚 (mm)', 'placeholder': '0.035', 'step': 0.001},
        {'key': 'dielectric', 'label': '介电常数', 'placeholder': '4.3', 'step': 0.01}
    ],
    'embedded_microstrip': [
        {'key': 'width', 'label': '线宽 (mm)', 'placeholder': '0.2', 'step': 0.01},
        {'key': 'upper_height', 'label': '上层介质厚度 (mm)', 'placeholder': '0.5', 'step': 0.01},
        {'key': 'lower_height', 'label': '下层介质厚度 (mm)', 'placeholder': '1.1', 'step': 0.01},
        {'key': 'thickness', 'label': '铜厚 (mm)', 'placeholder': '0.035', 'step': 0.001},
        {'key': 'upper_dielectric', 'label': '上层介电常数', 'placeholder': '4.3', 'step': 0.01},
        {'key': 'lower_dielectric', 'label': '下层介电常数', 'placeholder': '4.3', 'step': 0.01}
    ],
    'offset_stripline': [
        {'key': 'width', 'label': '线宽 (mm)', 'placeholder': '0.2', 'step': 0.01},
        {'key': 'total_height', 'label': '总介质厚度 (mm)', 'placeholder': '1.6', 'step': 0.01},
        {'key': 'bottom_distance', 'label': '到下层接地距离 (mm)', 'placeholder': '0.8', 'step': 0.01},
        {'key': 'thickness', 'label': '铜厚 (mm)', 'placeholder': '0.035', 'step': 0.001},
        {'key': 'dielectric', 'label': '介电常数', 'placeholder': '4.3', 'step': 0.01}
    ],
    'gcpw': [
        {'key': 'width', 'label': '信号线宽 (mm)', 'placeholder': '0.2', 'step': 0.01},
        {'key': 'gap', 'label': '到地线间距 (mm)', 'placeholder': '0.2', 'step': 0.01},
        {'key': 'height', 'label': '介质厚度 (mm)', 'placeholder': '1.6', 'step': 0.01},
        {'key': 'thickness', 'label': '铜厚 (mm)', 'placeholder': '0.035', 'step': 0.001},
        {'key': 'dielectric', 'label': '介电常数', 'placeholder': '4.3', 'step': 0.01}
    ],
    'cpwg': [
        {'key': 'width', 'label': '信号线宽 (mm)', 'placeholder': '0.2', 'step': 0.01},
        {'key': 'gap', 'label': '线间间距 (mm)', 'placeholder': '0.2', 'step': 0.01},
        {'key': 'height', 'label': '介质厚度 (mm)', 'placeholder': '1.6', 'step': 0.01},
        {'key': 'thickness', 'label': '铜厚 (mm)', 'placeholder': '0.035', 'step': 0.001},
        {'key': 'dielectric', 'label': '介电常数', 'placeholder': '4.3', 'step': 0.01}
    ],
    'broadside_coupled': [
        {'key': 'width', 'label': '线宽 (mm)', 'placeholder': '0.2', 'step': 0.01},
        {'key': 'height', 'label': '介质厚度 (mm)', 'placeholder': '1.6', 'step': 0.01},
        {'key': 'vertical_spacing', 'label': '垂直间距 (mm)', 'placeholder': '0.2', 'step': 0.01},
        {'key': 'thickness', 'label': '铜厚 (mm)', 'placeholder': '0.035', 'step': 0.001},
        {'key': 'dielectric', 'label': '介电常数', 'placeholder': '4.3', 'step': 0.01}
    ]
}


def get_definitions(model):
    """返回完整的表单定义字典"""
    return FORM_DEFINITIONS[model] 


def get_calculation_types():
    """返回所有计算类型"""
    return CALCULATION_TYPES
