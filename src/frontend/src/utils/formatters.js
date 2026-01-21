/**
 * 数据格式化工具函数
 */
import { PRECISION_CONFIG } from '../config/constants.js'

/**
 * 格式化数字到指定精度
 * @param {number} value - 要格式化的数值
 * @param {number} precision - 精度（小数位数）
 * @returns {string} 格式化后的字符串
 */
export const formatNumber = (value, precision = 2) => {
  if (isNaN(value) || value === null || value === undefined) {
    return '--'
  }
  return Number(value).toFixed(precision)
}

/**
 * 格式化阻抗值
 * @param {number} impedance - 阻抗值
 * @returns {string} 格式化后的阻抗字符串
 */
export const formatImpedance = (impedance) => {
  return `${formatNumber(impedance, PRECISION_CONFIG.IMPEDANCE)} Ω`
}

/**
 * 格式化有效介电常数
 * @param {number} erEff - 有效介电常数
 * @returns {string} 格式化后的字符串
 */
export const formatErEff = (erEff) => {
  return formatNumber(erEff, PRECISION_CONFIG.ER_EFF)
}

/**
 * 格式化线宽
 * @param {number} width - 线宽值
 * @returns {string} 格式化后的线宽字符串
 */
export const formatWidth = (width) => {
  return `${formatNumber(width, PRECISION_CONFIG.WIDTH)} mm`
}

/**
 * 格式化损耗
 * @param {number} loss - 损耗值
 * @returns {string} 格式化后的损耗字符串
 */
export const formatLoss = (loss) => {
  return `${formatNumber(loss, PRECISION_CONFIG.LOSS)} dB/mm`
}

/**
 * 格式化百分比
 * @param {number} value - 数值
 * @param {number} precision - 精度
 * @returns {string} 格式化后的百分比字符串
 */
export const formatPercentage = (value, precision = 2) => {
  return `${formatNumber(value * 100, precision)}%`
}

/**
 * 格式化计算结果
 * @param {Object} result - 计算结果对象
 * @returns {Object} 格式化后的结果对象
 */
export const formatCalculationResult = (result) => {
  if (!result || result.status !== 'success') {
    return result
  }

  const formatted = { ...result }

  // 格式化各种结果值
  if (result.impedance !== undefined) {
    formatted.impedance_formatted = formatImpedance(result.impedance)
  }

  if (result.er_eff !== undefined) {
    formatted.er_eff_formatted = formatErEff(result.er_eff)
  }

  if (result.effective_width !== undefined) {
    formatted.effective_width_formatted = formatWidth(result.effective_width)
  }

  if (result.loss_db_per_mm !== undefined) {
    formatted.loss_formatted = formatLoss(result.loss_db_per_mm)
  }

  if (result.single_ended_impedance !== undefined) {
    formatted.single_ended_impedance_formatted = formatImpedance(result.single_ended_impedance)
  }

  if (result.coupling_coefficient !== undefined) {
    formatted.coupling_coefficient_formatted = formatPercentage(result.coupling_coefficient)
  }

  if (result.diameter_ratio !== undefined) {
    formatted.diameter_ratio_formatted = formatNumber(result.diameter_ratio, 3)
  }

  return formatted
}

/**
 * 格式化材料信息
 * @param {Object} material - 材料对象
 * @returns {string} 格式化后的材料信息字符串
 */
export const formatMaterialInfo = (material) => {
  if (!material) return ''
  
  const parts = []
  
  if (material.name) {
    parts.push(material.name)
  }
  
  if (material.er) {
    parts.push(`εr=${formatNumber(material.er, 2)}`)
  }
  
  if (material.loss_tangent) {
    parts.push(`tanδ=${formatNumber(material.loss_tangent, 4)}`)
  }
  
  return parts.join(', ')
}

/**
 * 格式化文件大小
 * @param {number} bytes - 字节数
 * @returns {string} 格式化后的文件大小字符串
 */
export const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 B'
  
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`
}

/**
 * 格式化时间戳
 * @param {number|Date} timestamp - 时间戳或Date对象
 * @returns {string} 格式化后的时间字符串
 */
export const formatTimestamp = (timestamp) => {
  const date = new Date(timestamp)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}