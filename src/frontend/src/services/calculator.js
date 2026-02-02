/**
 * 计算器服务 - 处理阻抗计算的核心业务逻辑
 */
import { getCalculationTypes, calculateImpedance, getFormFields, getMaterials } from "../api";

// 缓存已加载的数据
const cache = {
  modelTypes: null,
  formFields: new Map(),
  materials: null
};

export class Calculator {
    /**
     * 加载计算模型类型
     * @returns {Promise<Array>} 模型类型数组
     */
    async loadModelTypes() {
        if (cache.modelTypes) {
            return cache.modelTypes;
        }
        try {
            const response = await getCalculationTypes();
            cache.modelTypes = response;
            return response;
        } catch (error) {
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
            return [];
        }
        if (cache.formFields.has(model)) {
            return cache.formFields.get(model);
        }
        try {
            const response = await getFormFields(model);
            const processedFields = response.map(field => ({
                ...field,
                value: field.value ?? field.defaultValue
            }));
            cache.formFields.set(model, processedFields);
            return processedFields;
        } catch (error) {
            const errorMsg = error.response?.data?.message || `加载${model}模型的表单字段失败`;
            throw new Error(`${errorMsg}，请确保模型名称正确或稍后重试`);
        }
    }

    /**
     * 验证表单是否有效
     * @param {Array} modelForm - 模型表单字段数组
     * @param {string} selectedModel - 选中的计算模型
     * @returns {boolean} 表单是否有效
     */
    isFormValid(modelForm, selectedModel) {
        if (!selectedModel) {
            return false;
        }
        if (!Array.isArray(modelForm) || modelForm.length === 0) {
            return false;
        }

        // 3. 只要有模型和表单字段，就认为表单有效
        // 空值将在提交时使用 placeholder 作为默认值
        return true;
    }

    /**
     * 提交计算请求
     * @param {Array} modelForm - 模型表单字段数组
     * @param {string} selectedModel - 选中的计算模型
     * @returns {Promise<Object>} 计算结果
     */
    async submitCalculation(modelForm, selectedModel) {
        // 使用统一的表单验证
        if (!this.isFormValid(modelForm, selectedModel)) {
            throw new Error('表单数据无效，请检查所有参数');
        }

        try {
            // 将 modelForm 数组转为键值对对象
            // 如果字段值为空，使用 placeholder 作为默认值
            const requestData = modelForm.reduce((obj, field) => {
                if (field.key) {
                    let value = field.value;
                    if (value === null || value === undefined || value === '' || isNaN(Number(value))) {
                        value = field.placeholder || field.defaultValue || 0;
                    }
                    obj[field.key] = Number(value);
                }
                return obj;
            }, {});
            const response = await calculateImpedance(selectedModel, requestData);
            return response;
        } catch (error) {
            let errorMsg;
            if (error.response?.status === 400) {
                errorMsg = error.response.data?.message || '参数有误，请检查输入值是否合法';
            } else if (error.response?.status === 500) {
                errorMsg = '服务器计算失败，请稍后重试';
            } else if (error.message?.includes('Network Error')) {
                errorMsg = '网络连接失败，请检查网络设置';
            } else {
                errorMsg = error.response?.data?.message || error.message || '计算失败，请检查参数或稍后重试';
            }
            throw new Error(errorMsg);
        }
    }

    /**
     * 加载材料数据
     * @returns {Promise<Object>} 材料数据对象
     */
    async loadMaterials() {
        try {
            const response = await getMaterials();
            return response;
        } catch (error) {
            throw new Error('加载材料数据失败，请稍后重试');
        }
    }
}