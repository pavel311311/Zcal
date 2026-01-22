/**
 * API服务 - 与后端通信
 */
import axios from 'axios'

// 智能获取API基础URL
const getApiBaseUrl = () => {
  // 优先使用环境变量
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL
  }
  
  // 在浏览器环境中
  if (typeof window !== 'undefined') {
    const { protocol, hostname } = window.location
    
    // 如果不是localhost，说明是生产环境或Docker环境
    if (hostname !== 'localhost' && hostname !== '127.0.0.1') {
      // 使用相同的协议和主机，但端口改为5000
      return `${protocol}//${hostname}:5000/api`
    }
  }
  
  // 开发环境默认值
  return 'http://localhost:5000/api'
}

const API_BASE_URL = getApiBaseUrl()

// 创建axios实例
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
apiClient.interceptors.request.use(
  (config) => {
    console.log(`🚀 API请求: ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    console.error('❌ 请求拦截器错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
apiClient.interceptors.response.use(
  (response) => {
    console.log(`✅ API响应: ${response.config.url}`, response.data)
    return response
  },
  (error) => {
    console.error('❌ API响应错误:', error)
    
    // 统一错误处理
    let errorMessage = '网络请求失败'
    
    if (error.response) {
      // 服务器返回错误状态码
      const { status, data } = error.response
      switch (status) {
        case 400:
          errorMessage = data?.message || '请求参数错误'
          break
        case 404:
          errorMessage = '请求的资源不存在'
          break
        case 500:
          errorMessage = data?.message || '服务器内部错误'
          break
        default:
          errorMessage = data?.message || `请求失败 (${status})`
      }
    } else if (error.request) {
      // 请求发出但没有收到响应
      errorMessage = '网络连接失败，请检查网络设置'
    } else {
      // 其他错误
      errorMessage = error.message || '未知错误'
    }
    
    // 创建统一的错误对象
    const apiError = new Error(errorMessage)
    apiError.originalError = error
    apiError.status = error.response?.status
    
    return Promise.reject(apiError)
  }
)

/**
 * 计算阻抗
 * @param {string} type - 计算类型
 * @param {object} params - 计算参数
 * @returns {Promise<object>} 计算结果
 */
export const calculateImpedance = async (type, params) => {
  if (!type) {
    throw new Error('计算类型不能为空')
  }
  if (!params || Object.keys(params).length === 0) {
    throw new Error('计算参数不能为空')
  }
  
  const response = await apiClient.post('/calculate', { type, params })
  return response.data
}

/**
 * 获取材料库
 * @returns {Promise<object>} 材料数据
 */
export const getMaterials = async () => {
  const response = await apiClient.get('/materials')
  return response.data
}

/**
 * 获取表单字段定义
 * @param {string} model - 模型类型
 * @returns {Promise<Array>} 表单字段数组
 */
export const getFormFields = async (model) => {
  if (!model) {
    throw new Error('模型类型不能为空')
  }
  
  const response = await apiClient.get('/form_fields', { 
    params: { model } 
  })
  return response.data
}

/**
 * 获取计算类型列表
 * @returns {Promise<object>} 计算类型数据
 */
export const getCalculationTypes = async () => {
  const response = await apiClient.get('/calculation_types')
  return response.data
}

// 导出配置好的axios实例，供其他模块使用
export default apiClient
