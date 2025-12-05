/**
 * API服务 - 与后端通信
 */
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

/**
 * 计算阻抗
 * @param {string} type - 计算类型
 * @param {object} params - 计算参数
 * @returns {Promise}
 */
export const calculateImpedance = (type, params) => {
  return apiClient.post('/calculate', {
    type,
    params
  })
}

/**
 * 获取材料库
 * @returns {Promise}
 */
export const getMaterials = () => {
  return apiClient.get('/materials')
}

export default apiClient
