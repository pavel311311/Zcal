/**
 * Zcal 应用类型定义
 */

// ==================== 表单相关类型 ====================

/** 表单字段类型 */
export type FieldType = 'number' | 'text' | 'select' | 'checkbox'

/** 表单字段定义 */
export interface FormField {
  key: string
  label: string
  type: FieldType
  placeholder?: string | number
  defaultValue?: string | number
  value?: string | number
  unit?: string
  step?: number
  min?: number
  max?: number
  required?: boolean
  options?: Array<{ label: string; value: string | number }>
  description?: string
}

/** 模型类型 */
export interface ModelType {
  type: string
  name: string
  description?: string
  icon?: string
}

// ==================== 材料相关类型 ====================

/** 材料定义 */
export interface Material {
  name: string
  er: number           // 相对介电常数 (Dk)
  loss_tangent: number // 损耗角正切 (Df)
  description?: string
}

// ==================== 计算相关类型 ====================

/** 计算请求参数 */
export interface CalculationParams {
  [key: string]: number
}

/** 计算结果定义 */
export interface ResultDefinition {
  key: string
  label: string
  unit?: string
  precision?: number
  description?: string
}

/** 计算结果状态 */
export type CalculationStatus = 'success' | 'error' | 'idle'

/** 计算成功结果 */
export interface CalculationSuccessResult {
  status: 'success'
  resultDefinitions: ResultDefinition[]
  // 动态键值，如 Z0, Er_eff 等
  [key: string]: unknown
}

/** 计算错误结果 */
export interface CalculationErrorResult {
  status: 'error'
  message: string
}

/** 计算结果联合类型 */
export type CalculationResult = CalculationSuccessResult | CalculationErrorResult | null

// ==================== Store 状态类型 ====================

/** Calculator Service 的缓存结构 */
export interface CalculatorCache {
  modelTypes: ModelType[] | null
  formFields: Map<string, FormField[]>
  materials: Record<string, Material> | null
}

// ==================== API 相关类型 ====================

/** API 错误 */
export interface ApiError extends Error {
  status?: number
  originalError?: unknown
}

/** axios 响应拦截器错误 */
export interface AxiosErrorResponse {
  status: number
  data: {
    message?: string
    [key: string]: unknown
  }
}
