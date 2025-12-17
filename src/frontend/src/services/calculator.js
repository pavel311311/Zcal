/**
 * 计算器服务 - 处理阻抗计算的核心业务逻辑
 */
import { getCalculationTypes, calculateImpedance, getFormFields, getMaterials } from "../api";

export class Calculator {
    constructor() {
        // 不再将store存储为实例属性，而是在需要时直接获取
    }

    /**
     * 加载计算模型类型
     * @returns {Promise<Array>} 模型类型数组
     */
    async loadModelTypes() {
        try {
            const response = await getCalculationTypes();
            console.log("Loaded calculation types:", response.data);
            return response.data;
        } catch (error) {
            console.error('加载模型类型失败：', error);
            const errorMsg = error.response?.data?.message || '加载计算模型类型失败';
            throw new Error(`${errorMsg}，请检查网络连接或稍后重试`);
        }
    }

    /**
     * 加载模型表单字段
     * @param {string} model - 模型名称
     * @returns {Promise<Array>} 表单字段数组
     */
    async loadFormFields(model) {
        if (!model) {
            console.warn('未指定模型名称，无法加载表单字段');
            return [];
        }
        try {
            const response = await getFormFields(model);
            // 给每个字段初始化value，避免undefined导致校验失败
            return response.data.map(field => ({
                ...field,
                value: field.value ?? field.defaultValue // 优先用已有值→默认值
            }));
        } catch (error) {
            console.error('加载表单字段失败：', error);
            const errorMsg = error.response?.data?.message || `加载${model}模型的表单字段失败`;
            throw new Error(`${errorMsg}，请确保模型名称正确或稍后重试`);
        }
    }

    /**
     * 提交计算请求
     * @param {Array} modelForm - 模型表单字段数组
     * @param {string} selectedModel - 选中的计算模型
     * @returns {Promise<Object>} 计算结果
     */
    async submitCalculation(modelForm, selectedModel) {
        // 参数验证
        if (!Array.isArray(modelForm)) {
            throw new Error('模型表单数据格式错误');
        }

        if (!selectedModel) {
            throw new Error('请先选择计算模型');
        }

        // 表单字段完整性检查
        const invalidFields = modelForm.filter(field => 
            field.required && (field.value === null || field.value === undefined || field.value === '')
        );
        
        if (invalidFields.length > 0) {
            const fieldNames = invalidFields.map(field => field.label).join('、');
            throw new Error(`请填写必填参数：${fieldNames}`);
        }

        try {
            // 将 modelForm 数组转为键值对对象
            const requestData = modelForm.reduce((obj, field) => {
                if (field.key) {
                    obj[field.key] = Number(field.value) // 确保是数值类型
                }
                return obj
            }, {})

            console.log('🚀 请求数据：', requestData)
            const response = await calculateImpedance(selectedModel, requestData)
            
            return response.data;
        } catch (error) {
            console.error('计算错误:', error);
            // 提取更友好的错误信息
            let errorMsg;
            if (error.response?.status === 400) {
                // 请求参数错误
                errorMsg = error.response.data?.message || '参数有误，请检查输入值是否合法';
            } else if (error.response?.status === 500) {
                // 服务器错误
                errorMsg = '服务器计算失败，请稍后重试';
            } else if (error.message?.includes('Network Error')) {
                errorMsg = '网络连接失败，请检查网络设置';
            } else {
                errorMsg = error.response?.data?.message || '计算失败，请检查参数或稍后重试';
            }
            throw new Error(errorMsg);
        }
    }

    /**
     * 验证表单是否有效
     * @param {Array} modelForm - 模型表单字段数组
     * @param {string} selectedModel - 选中的计算模型
     * @returns {boolean} 表单是否有效
     */
    isFormValid(modelForm, selectedModel) {
        // 1. 模型是否选中
        if (!selectedModel) {
            console.debug('表单无效：未选择模型');
            return false;
        }

        // 2. 表单字段是否为空
        if (!Array.isArray(modelForm) || modelForm.length === 0) {
            console.debug('表单无效：表单字段为空');
            return false;
        }

        // 3. 模型表单字段校验：有值则校验数值有效性，无值则用后端默认值兜底
        const isModelValid = modelForm.every(field => {
            // 优先取输入值 → 后端默认值 → 无
            const finalValue = field.value ?? field.defaultValue
            // 校验：finalValue存在且为有效数值
            const isValid = finalValue !== undefined && finalValue !== null && !isNaN(Number(finalValue))
            if (!isValid) {
                console.debug(`字段${field.label}无效：${finalValue}`);
            }
            return isValid
        })
        
        return isModelValid
    }

    /**
     * 加载材料数据
     * @returns {Promise<Object>} 材料数据对象
     */
    async loadMaterials() {
        try {
            const response = await getMaterials()
            return response.data
        } catch (error) {
            console.error('加载材料数据失败：', error);
            throw new Error('加载材料数据失败，请稍后重试');
        }
    }
}