/**
 * 表单验证工具函数
 */
import { VALIDATION_CONFIG, ERROR_MESSAGES } from '../config/constants.js'

/**
 * 验证数值范围
 * @param {number} value - 要验证的值
 * @param {number} min - 最小值
 * @param {number} max - 最大值
 * @param {string} fieldName - 字段名称
 * @returns {string|null} 错误信息或null
 */
export const validateRange = (value, min, max, fieldName) => {
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
 * @param {number} width - 线宽值
 * @returns {string|null} 错误信息或null
 */
export const validateWidth = (width) => {
  return validateRange(
    width, 
    VALIDATION_CONFIG.MIN_WIDTH, 
    VALIDATION_CONFIG.MAX_WIDTH, 
    '线宽'
  )
}

/**
 * 验证介质厚度
 * @param {number} height - 厚度值
 * @returns {string|null} 错误信息或null
 */
export const validateHeight = (height) => {
  return validateRange(
    height, 
    VALIDATION_CONFIG.MIN_HEIGHT, 
    VALIDATION_CONFIG.MAX_HEIGHT, 
    '介质厚度'
  )
}

/**
 * 验证铜厚
 * @param {number} thickness - 铜厚值
 * @returns {string|null} 错误信息或null
 */
export const validateThickness = (thickness) => {
  return validateRange(
    thickness, 
    VALIDATION_CONFIG.MIN_THICKNESS, 
    VALIDATION_CONFIG.MAX_THICKNESS, 
    '铜厚'
  )
}

/**
 * 验证介电常数
 * @param {number} dielectric - 介电常数值
 * @returns {string|null} 错误信息或null
 */
export const validateDielectric = (dielectric) => {
  return validateRange(
    dielectric, 
    VALIDATION_CONFIG.MIN_DIELECTRIC, 
    VALIDATION_CONFIG.MAX_DIELECTRIC, 
    '介电常数'
  )
}

/**
 * 验证损耗角正切
 * @param {number} lossTangent - 损耗角正切值
 * @returns {string|null} 错误信息或null
 */
export const validateLossTangent = (lossTangent) => {
  return validateRange(
    lossTangent, 
    VALIDATION_CONFIG.MIN_LOSS_TANGENT, 
    VALIDATION_CONFIG.MAX_LOSS_TANGENT, 
    '损耗角正切'
  )
}

/**
 * 验证表单字段
 * @param {string} key - 字段键名
 * @param {number} value - 字段值
 * @returns {string|null} 错误信息或null
 */
export const validateField = (key, value) => {
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
 * @param {Array} formFields - 表单字段数组
 * @returns {Object} 验证结果 {isValid: boolean, errors: Object}
 */
export const validateForm = (formFields) => {
  const errors = {}
  let isValid = true
  
  formFields.forEach(field => {
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
 * @param {Array} formFields - 表单字段数组
 * @returns {Array} 缺失的必填字段
 */
export const checkRequiredFields = (formFields) => {
  return formFields.filter(field => {
    const value = field.value
    return value === null || value === undefined || value === '' || isNaN(value)
  }).map(field => field.label || field.key)
}