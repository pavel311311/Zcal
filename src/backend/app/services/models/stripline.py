class Stripline:
        # 核心标识（与原有TYPE一致）
    TYPE = "stripline"
    # 前端显示名称
    DISPLAY_NAME = "带状线 (Stripline)"
    # 前端标签（兼容原有逻辑）
    LABEL = "stripline"
    # 【表单字段定义】完全对应原FORM_DEFINITIONS中的microstrip项
    PARAM_DEFINITIONS = [
        {'key': 'width', 'label': '线宽 (mm)', 'placeholder': '0.2', 'step': 0.01},
        {'key': 'height', 'label': '介质厚度 (mm)', 'placeholder': '1.6', 'step': 0.01},
        {'key': 'thickness', 'label': '铜厚 (mm)', 'placeholder': '0.035', 'step': 0.001},
        {'key': 'dielectric', 'label': '介电常数', 'placeholder': '4.3', 'step': 0.01},
        {"key": "loss_tangent", "label": "损耗角正切", "placeholder": "0", "step": 0.001}

    ]
