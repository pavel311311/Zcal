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
 * 验证介质厚度（通用 height 字段）
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
 * 验证介质厚度（dielectric_thickness 字段，与 height 共用范围）
 * @param {number} dielectricThickness - 介质厚度值
 * @returns {string|null} 错误信息或null
 */
export const validateDielectricThickness = (dielectricThickness) => {
  return validateRange(
    dielectricThickness,
    VALIDATION_CONFIG.MIN_DIELECTRIC_THICKNESS,
    VALIDATION_CONFIG.MAX_DIELECTRIC_THICKNESS,
    '介质厚度'
  )
}

/**
 * 验证非对称带状线上层介质厚度（height1）
 * @param {number} height1 - 上层介质厚度值
 * @returns {string|null} 错误信息或null
 */
export const validateHeight1 = (height1) => {
  return validateRange(
    height1,
    VALIDATION_CONFIG.MIN_HEIGHT1,
    VALIDATION_CONFIG.MAX_HEIGHT1,
    '上层介质厚度'
  )
}

/**
 * 验证非对称带状线下层介质厚度（height2）
 * @param {number} height2 - 下层介质厚度值
 * @returns {string|null} 错误信息或null
 */
export const validateHeight2 = (height2) => {
  return validateRange(
    height2,
    VALIDATION_CONFIG.MIN_HEIGHT2,
    VALIDATION_CONFIG.MAX_HEIGHT2,
    '下层介质厚度'
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
 * 验证频率（GHz），必须 > 0
 * @param {number} frequency - 频率值
 * @returns {string|null} 错误信息或null
 */
export const validateFrequency = (frequency) => {
  if (isNaN(frequency) || frequency === null || frequency === undefined) {
    return '频率必须是有效数字'
  }
  if (frequency <= 0) {
    return '频率必须大于0'
  }
  return validateRange(
    frequency,
    VALIDATION_CONFIG.MIN_FREQUENCY,
    VALIDATION_CONFIG.MAX_FREQUENCY,
    '频率'
  )
}

/**
 * 验证线间距（spacing）
 * @param {number} spacing - 线间距值
 * @returns {string|null} 错误信息或null
 */
export const validateSpacing = (spacing) => {
  return validateRange(
    spacing,
    VALIDATION_CONFIG.MIN_SPACING,
    VALIDATION_CONFIG.MAX_SPACING,
    '线间距'
  )
}

/**
 * 验证缝隙宽度（gap，CPW 类使用）
 * @param {number} gap - 缝隙宽度值
 * @returns {string|null} 错误信息或null
 */
export const validateGap = (gap) => {
  return validateRange(
    gap,
    VALIDATION_CONFIG.MIN_GAP,
    VALIDATION_CONFIG.MAX_GAP,
    '缝隙宽度'
  )
}

/**
 * 验证同轴线直径（inner/outer）
 * @param {number} diameter - 直径值
 * @returns {string|null} 错误信息或null
 */
export const validateDiameter = (diameter) => {
  return validateRange(
    diameter,
    VALIDATION_CONFIG.MIN_DIAMETER,
    VALIDATION_CONFIG.MAX_DIAMETER,
    '直径'
  )
}

/**
 * 线宽 / 介质厚度 宽高比软提示（非阻塞）
 * 返回 null 表示通过；返回字符串仅作为 UI 提示，不阻断提交
 * @param {number} width - 线宽
 * @param {number} height - 介质厚度
 * @returns {string|null} 提示文案或 null
 */
export const suggestWidthHeightRatio = (width, height) => {
  if (
    isNaN(width) || width === null || width === undefined ||
    isNaN(height) || height === null || height === undefined
  ) {
    return null
  }
  if (height <= 0) return null
  const ratio = width / height
  if (ratio < VALIDATION_CONFIG.WIDTH_HEIGHT_RATIO_MIN) {
    return `提示：线宽/介质厚度 = ${ratio.toFixed(2)} 偏小，可能影响阻抗精度`
  }
  if (ratio > VALIDATION_CONFIG.WIDTH_HEIGHT_RATIO_MAX) {
    return `提示：线宽/介质厚度 = ${ratio.toFixed(2)} 偏大，可能影响阻抗精度`
  }
  return null
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
    case 'dielectric_thickness':
      return validateDielectricThickness(value)
    case 'height1':
      return validateHeight1(value)
    case 'height2':
      return validateHeight2(value)
    case 'thickness':
      return validateThickness(value)
    case 'dielectric':
      return validateDielectric(value)
    case 'loss_tangent':
      return validateLossTangent(value)
    case 'frequency':
      return validateFrequency(value)
    case 'spacing':
      return validateSpacing(value)
    case 'gap':
      return validateGap(value)
    case 'inner_diameter':
    case 'outer_diameter':
      return validateDiameter(value)
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
