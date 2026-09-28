/**
 * 应用常量配置
 */

// 表单验证配置
// 所有长度单位均为 mm；频率单位为 GHz；介电常数为无量纲
// 上下限取值兼顾物理可行性与实际 PCB 工艺范围
// 新增字段时需同步在 validation.js 的 validateField 中注册
// 宽高比提示相关参数请参考 WIDTHS 参数
// MAX_DIAMETER 用于 inner_diameter / outer_diameter（同轴线）
// MAX_SPACING 用于 spacing（线间距）
// MIN_FREQUENCY / MAX_FREQUENCY 用于 frequency（GHz）
// MIN_DIELECTRIC_THICKNESS / MAX_DIELECTRIC_THICKNESS 用于 dielectric_thickness（介质厚度，如 CPW 差分）
// MIN_HEIGHT1 / MAX_HEIGHT1、MIN_HEIGHT2 / MAX_HEIGHT2 用于非对称带状线的上下介质层厚度
export const VALIDATION_CONFIG = {
  MIN_WIDTH: 0.01,        // 最小线宽 (mm)
  MAX_WIDTH: 100,         // 最大线宽 (mm)
  MIN_HEIGHT: 0.01,       // 最小介质厚度 (mm)
  MAX_HEIGHT: 100,        // 最大介质厚度 (mm)
  MIN_DIELECTRIC_THICKNESS: 0.01, // 最小介质厚度 (mm)，与 height 共用范围
  MAX_DIELECTRIC_THICKNESS: 100,  // 最大介质厚度 (mm)
  MIN_HEIGHT1: 0.01,      // 非对称带状线上层介质厚度最小值 (mm)
  MAX_HEIGHT1: 100,       // 非对称带状线上层介质厚度最大值 (mm)
  MIN_HEIGHT2: 0.01,      // 非对称带状线下层介质厚度最小值 (mm)
  MAX_HEIGHT2: 100,       // 非对称带状线下层介质厚度最大值 (mm)
  MIN_THICKNESS: 0.001,   // 最小铜厚 (mm)
  MAX_THICKNESS: 1,       // 最大铜厚 (mm)
  MIN_DIAMETER: 0.01,     // 最小直径 (mm)，同轴线内外径
  MAX_DIAMETER: 100,      // 最大直径 (mm)
  MIN_SPACING: 0.01,      // 最小线间距 (mm)
  MAX_SPACING: 100,       // 最大线间距 (mm)
  MIN_GAP: 0.01,          // 最小缝隙宽度 (mm)，如 CPW 缝隙
  MAX_GAP: 100,           // 最大缝隙宽度 (mm)
  MIN_FREQUENCY: 0.000001,// 最小频率 (GHz)，约 1 Hz，留余量避免 0
  MAX_FREQUENCY: 1000,    // 最大频率 (GHz)，覆盖到太赫兹以下
  MIN_DIELECTRIC: 1,      // 最小介电常数（真空=1）
  MAX_DIELECTRIC: 100,    // 最大介电常数
  MIN_LOSS_TANGENT: 0,    // 最小损耗角正切
  MAX_LOSS_TANGENT: 1,    // 最大损耗角正切
  // 宽高比提示阈值：仅作软提示使用，超出不会阻断提交
  WIDTH_HEIGHT_RATIO_MIN: 0.05, // 线宽 / 介质厚度 建议下限
  WIDTH_HEIGHT_RATIO_MAX: 20    // 线宽 / 介质厚度 建议上限
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
