/**
 * 表单验证工具函数
 * @file TypeScript 版本
 */
import { VALIDATION_CONFIG, ERROR_MESSAGES } from '../config/constants'

/**
 * 验证数值范围
 * @param value - 要验证的值
 * @param min - 最小值
 * @param max - 最大值
 * @param fieldName - 字段名称
 * @returns 错误信息或 null
 */
export const validateRange = (
  value: number,
  min: number,
  max: number,
  fieldName: string
): string | null => {
  if (isNaN(value) || value === null || value === undefined) {
    return `${fieldName}必须是有效数字`
  }

  if (value < min) {
    return `${fieldName}不能小于${min}`
  }

  if (value > max) {
    return `${fieldName}不能大于${max}`
  }

  return null
}

/**
 * 验证线宽
 * @param width - 线宽值
 * @returns 错误信息或 null
 */
export const validateWidth = (width: number): string | null => {
  return validateRange(
    width,
    VALIDATION_CONFIG.MIN_WIDTH,
    VALIDATION_CONFIG.MAX_WIDTH,
    '线宽'
  )
}

/**
 * 验证介质厚度
 * @param height - 厚度值
 * @returns 错误信息或 null
 */
export const validateHeight = (height: number): string | null => {
  return validateRange(
    height,
    VALIDATION_CONFIG.MIN_HEIGHT,
    VALIDATION_CONFIG.MAX_HEIGHT,
    '介质厚度'
  )
}

/**
 * 验证铜厚
 * @param thickness - 铜厚值
 * @returns 错误信息或 null
 */
export const validateThickness = (thickness: number): string | null => {
  return validateRange(
    thickness,
    VALIDATION_CONFIG.MIN_THICKNESS,
    VALIDATION_CONFIG.MAX_THICKNESS,
    '铜厚'
  )
}

/**
 * 验证介电常数
 * @param dielectric - 介电常数值
 * @returns 错误信息或 null
 */
export const validateDielectric = (dielectric: number): string | null => {
  return validateRange(
    dielectric,
    VALIDATION_CONFIG.MIN_DIELECTRIC,
    VALIDATION_CONFIG.MAX_DIELECTRIC,
    '介电常数'
  )
}

/**
 * 验证损耗角正切
 * @param lossTangent - 损耗角正切值
 * @returns 错误信息或 null
 */
export const validateLossTangent = (lossTangent: number): string | null => {
  return validateRange(
    lossTangent,
    VALIDATION_CONFIG.MIN_LOSS_TANGENT,
    VALIDATION_CONFIG.MAX_LOSS_TANGENT,
    '损耗角正切'
  )
}

/**
 * 验证表单字段
 * @param key - 字段键名
 * @param value - 字段值
 * @returns 错误信息或 null
 */
export const validateField = (
  key: string,
  value: number
): string | null => {
  switch (key) {
    case 'width':
      return validateWidth(value)
    case 'height':
      return validateHeight(value)
    case 'thickness':
      return validateThickness(value)
    case 'dielectric':
      return validateDielectric(value)
    case 'loss_tangent':
      return validateLossTangent(value)
    case 'spacing':
      return validateWidth(value) // 间距使用与线宽相同的验证规则
    case 'inner_diameter':
    case 'outer_diameter':
      return validateWidth(value) // 直径使用与线宽相同的验证规则
    default:
      return null
  }
}

/**
 * 验证整个表单
 * @param formFields - 表单字段数组
 * @returns 验证结果 { isValid: boolean, errors: Record<string, string> }
 */
export const validateForm = (
  formFields: Array<{ key: string; value: number; label?: string }>
): { isValid: boolean; errors: Record<string, string> } => {
  const errors: Record<string, string> = {}
  let isValid = true

  formFields.forEach((field) => {
    const error = validateField(field.key, field.value)
    if (error) {
      errors[field.key] = error
      isValid = false
    }
  })

  return { isValid, errors }
}

/**
 * 检查必填字段
 * @param formFields - 表单字段数组
 * @returns 缺失的必填字段标签数组
 */
export const checkRequiredFields = (
  formFields: Array<{ key: string; value: number; label?: string; required?: boolean }>
): string[] => {
  return formFields
    .filter((field) => {
      const value = field.value
      return value === null || value === undefined || value === '' || isNaN(value)
    })
    .map((field) => field.label || field.key)
}
