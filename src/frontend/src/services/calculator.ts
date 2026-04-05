/**
 * 计算器服务 - 处理阻抗计算的核心业务逻辑
 * @file 遵循严格类型安全，使用 TypeScript + JSDoc 混合方案
 */
import type {
  FormField,
  ModelType,
  Material,
  CalculationParams,
  CalculationResult,
  CalculatorCache,
} from '../types'
import {
  getCalculationTypes,
  calculateImpedance,
  getFormFields,
  getMaterials,
} from '../api'

// ==================== 缓存管理 ====================

const cache: CalculatorCache = {
  modelTypes: null,
  formFields: new Map(),
  materials: null,
}

// ==================== Calculator 类 ====================

export class Calculator {
  /**
   * 加载计算模型类型
   * @returns {Promise<ModelType[]>} 模型类型数组
   */
  async loadModelTypes(): Promise<ModelType[]> {
    if (cache.modelTypes !== null) {
      return cache.modelTypes
    }
    try {
      const response = await getCalculationTypes()
      cache.modelTypes = response as ModelType[]
      return cache.modelTypes
    } catch (error) {
      const errorMsg =
        (error as { response?: { data?: { message?: string } } }).response?.data?.message ||
        '加载计算模型类型失败'
      throw new Error(`${errorMsg}，请检查网络连接或稍后重试`)
    }
  }

  /**
   * 加载模型表单字段
   * @param model - 模型名称
   * @returns {Promise<FormField[]>} 表单字段数组
   */
  async loadFormFields(model: string): Promise<FormField[]> {
    if (!model) {
      return []
    }
    if (cache.formFields.has(model)) {
      return cache.formFields.get(model)!
    }
    try {
      const response = (await getFormFields(model)) as FormField[]
      const processedFields: FormField[] = response.map((field) => ({
        ...field,
        value: field.value ?? field.defaultValue,
      }))
      cache.formFields.set(model, processedFields)
      return processedFields
    } catch (error) {
      const errorMsg =
        (error as { response?: { data?: { message?: string } } }).response?.data?.message ||
        `加载${model}模型的表单字段失败`
      throw new Error(`${errorMsg}，请确保模型名称正确或稍后重试`)
    }
  }

  /**
   * 验证表单是否有效
   * @param modelForm - 模型表单字段数组
   * @param selectedModel - 选中的计算模型
   * @returns {boolean} 表单是否有效
   */
  isFormValid(modelForm: FormField[], selectedModel: string): boolean {
    if (!selectedModel) {
      return false
    }
    if (!Array.isArray(modelForm) || modelForm.length === 0) {
      return false
    }
    return true
  }

  /**
   * 提交计算请求
   * @param modelForm - 模型表单字段数组
   * @param selectedModel - 选中的计算模型
   * @returns {Promise<CalculationResult>} 计算结果
   */
  async submitCalculation(
    modelForm: FormField[],
    selectedModel: string
  ): Promise<CalculationResult> {
    if (!this.isFormValid(modelForm, selectedModel)) {
      throw new Error('表单数据无效，请检查所有参数')
    }

    try {
      // 将 modelForm 数组转为键值对对象
      const requestData: CalculationParams = modelForm.reduce<CalculationParams>(
        (obj, field) => {
          if (field.key) {
            let value = field.value
            if (
              value === null ||
              value === undefined ||
              value === '' ||
              isNaN(Number(value))
            ) {
              value = (field.placeholder ?? field.defaultValue ?? 0) as number
            }
            obj[field.key] = Number(value)
          }
          return obj
        },
        {}
      )
      const response = await calculateImpedance(selectedModel, requestData)
      return response as CalculationResult
    } catch (error) {
      const err = error as {
        response?: { status?: number; data?: { message?: string } }
        message?: string
      }
      let errorMsg: string
      if (err.response?.status === 400) {
        errorMsg = err.response.data?.message || '参数有误，请检查输入值是否合法'
      } else if (err.response?.status === 500) {
        errorMsg = '服务器计算失败，请稍后重试'
      } else if (err.message?.includes('Network Error')) {
        errorMsg = '网络连接失败，请检查网络设置'
      } else {
        errorMsg = err.response?.data?.message || err.message || '计算失败，请检查参数或稍后重试'
      }
      throw new Error(errorMsg)
    }
  }

  /**
   * 加载材料数据
   * @returns {Promise<Record<string, Material>>} 材料数据对象
   */
  async loadMaterials(): Promise<Record<string, Material>> {
    if (cache.materials !== null) {
      return cache.materials
    }
    try {
      const response = await getMaterials()
      cache.materials = response as Record<string, Material>
      return cache.materials
    } catch (error) {
      throw new Error('加载材料数据失败，请稍后重试')
    }
  }
}
