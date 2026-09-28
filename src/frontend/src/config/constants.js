/**
 * 应用常量配置
 */

// 表单验证配置
export const VALIDATION_CONFIG = {
  MIN_WIDTH: 0.01,        // 最小线宽 (mm)
  MAX_WIDTH: 100,         // 最大线宽 (mm)
  MIN_HEIGHT: 0.01,       // 最小介质厚度 (mm)
  MAX_HEIGHT: 100,        // 最大介质厚度 (mm)
  MIN_THICKNESS: 0.001,   // 最小铜厚 (mm)
  MAX_THICKNESS: 1,       // 最大铜厚 (mm)
  MIN_DIELECTRIC: 1,      // 最小介电常数
  MAX_DIELECTRIC: 100,    // 最大介电常数
  MIN_LOSS_TANGENT: 0,    // 最小损耗角正切
  MAX_LOSS_TANGENT: 1     // 最大损耗角正切
}

// 计算精度配置
export const PRECISION_CONFIG = {
  IMPEDANCE: 2,           // 阻抗精度 (小数位)
  ER_EFF: 3,             // 有效介电常数精度
  WIDTH: 4,              // 线宽精度
  LOSS: 4                // 损耗精度
}

// 错误消息
export const ERROR_MESSAGES = {
  NETWORK_ERROR: '网络连接失败，请检查网络设置',
  SERVER_ERROR: '服务器错误，请稍后重试',
  VALIDATION_ERROR: '输入参数不符合要求',
  CALCULATION_ERROR: '计算过程中发生错误',
  UNKNOWN_ERROR: '未知错误，请联系技术支持'
}