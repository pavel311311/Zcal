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

// ==================== Runtime Type Guards ====================

/**
 * 验证并转换模型类型数据
 * @param item - 模型类型数据项
 * @param index - 索引（用于错误日志）
 * @returns 验证后的 ModelType 或 null
 */
function validateModelType(item: unknown, index: number): ModelType | null {
  if (!item || typeof item !== 'object') {
    console.warn(`[Calculator] 模型类型数据项 #${index} 格式无效，已跳过`, item)
    return null
  }
  
  const obj = item as Record<string, unknown>
  if (typeof obj.type !== 'string' || !obj.type) {
    console.warn(`[Calculator] 模型类型数据项 #${index} 缺少有效的 type 字段，已跳过`, item)
    return null
  }
  
  return {
    type: obj.type as string,
    name: (obj.name as string) || obj.type,
    description: obj.description as string | undefined,
    icon: obj.icon as string | undefined
  } as ModelType
}

/**
 * 验证并转换表单字段数据
 * @param field - 表单字段数据项
 * @param index - 索引（用于错误日志）
 * @returns 验证后的 FormField 或 null
 */
function validateFormField(field: unknown, index: number): FormField | null {
  if (!field || typeof field !== 'object') {
    console.warn(`[Calculator] 表单字段数据项 #${index} 格式无效，已跳过`, field)
    return null
  }
  
  const obj = field as Record<string, unknown>
  
  return {
    key: (obj.key as string) || `field_${index}`,
    label: (obj.label as string) || `字段 #${index}`,
    type: (obj.type as FormField['type']) || 'text',
    placeholder: obj.placeholder as string | number | undefined,
    defaultValue: obj.defaultValue as string | number | undefined,
    value: (obj.value as string | number | undefined) ?? obj.defaultValue,
    unit: obj.unit as string | undefined,
    step: obj.step as number | undefined,
    min: obj.min as number | undefined,
    max: obj.max as number | undefined,
    required: obj.required as boolean | undefined,
    options: obj.options as FormField['options'] | undefined,
    description: obj.description as string | undefined
  } as FormField
}

/**
 * 验证材料数据
 * @param value - 材料数据项
 * @param key - 材料键名
 * @returns 验证后的 Material 或 null
 */
function validateMaterial(value: unknown, key: string): Material | null {
  if (!value || typeof value !== 'object') {
    console.warn(`[Calculator] 材料数据项 ${key} 格式无效，已跳过`, value)
    return null
  }
  
  const obj = value as Record<string, unknown>
  
  if (typeof obj.name !== 'string' || !obj.name) {
    console.warn(`[Calculator] 材料数据项 ${key} 缺少有效的 name 字段，已跳过`, value)
    return null
  }
  
  return {
    name: obj.name as string,
    er: typeof obj.er === 'number' ? obj.er : 0,
    loss_tangent: typeof obj.loss_tangent === 'number' ? obj.loss_tangent : 0,
    description: obj.description as string | undefined
  } as Material
}

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
      if (!Array.isArray(response)) {
        throw new Error('API 返回数据格式错误：期望数组，但收到未知类型')
      }
      
      const validatedTypes = response
        .map((item, index) => validateModelType(item, index))
        .filter((item): item is ModelType => item !== null)

      if (validatedTypes.length === 0) {
        throw new Error('API 返回的模型类型数据为空或格式完全无效')
      }

      cache.modelTypes = validatedTypes
      return validatedTypes
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
      const response = await getFormFields(model)
      if (!Array.isArray(response)) {
        throw new Error(`API 返回数据格式错误：期望数组，但收到未知类型`)
      }

      const processedFields = response
        .map((field, index) => validateFormField(field, index))
        .filter((field): field is FormField => field !== null)

      if (processedFields.length === 0) {
        console.warn(`模型 ${model} 的表单字段数据为空或格式无效`)
      }

      cache.formFields.set(model, processedFields)
      return processedFields
    } catch (err) {
      const errorMsg =
        (err as { response?: { data?: { message?: string } } }).response?.data?.message ||
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
      const requestData: CalculationParams = {}
      let validFieldCount = 0
      let invalidFieldCount = 0

      for (const field of modelForm) {
        if (!field.key) {
          invalidFieldCount++
          continue
        }

        let value = field.value
        if (
          value === null ||
          value === undefined ||
          value === '' ||
          isNaN(Number(value))
        ) {
          value = (field.placeholder ?? field.defaultValue ?? 0) as number
        }

        const numValue = Number(value)
        if (isNaN(numValue)) {
          invalidFieldCount++
          continue
        }

        requestData[field.key] = numValue
        validFieldCount++
      }

      if (validFieldCount === 0) {
        throw new Error('表单数据无效：所有字段值均无法解析为有效数字')
      }

      if (invalidFieldCount > 0) {
        console.warn(
          `[Calculator] 提交计算时跳过了 ${invalidFieldCount} 个无效字段`,
          modelForm.filter(f => !f.key || isNaN(Number(f.value)))
        )
      }

      const response = await calculateImpedance(selectedModel, requestData)
      
      // Runtime validation of API response
      if (!response || typeof response !== 'object') {
        throw new Error('API 返回数据格式错误：期望对象，但收到未知类型')
      }

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
      if (!response || typeof response !== 'object') {
        throw new Error('API 返回数据格式错误：期望对象，但收到未知类型')
      }

      const validatedMaterials: Record<string, Material> = {}
      for (const [key, value] of Object.entries(response)) {
        const validated = validateMaterial(value, key)
        if (validated) {
          validatedMaterials[key] = validated
        }
      }

      if (Object.keys(validatedMaterials).length === 0) {
        throw new Error('API 返回的材料数据为空或格式完全无效')
      }

      cache.materials = validatedMaterials
      return validatedMaterials
    } catch {
      throw new Error('加载材料数据失败，请稍后重试')
    }
  }
}
