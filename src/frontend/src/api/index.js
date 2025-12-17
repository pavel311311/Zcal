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
  return apiClient.post('/calculate', {type,params})
}

/**
 * 获取材料库
 * @returns {Promise}
 */
export const getMaterials = () => {
  return apiClient.get('/materials')
}

/**
 * 获取表单字段定义（由后端提供）
 * @returns {Promise}
 */
export const getFormFields = (model) => {
  return apiClient.get('/form_fields'
    , { params: { model: model }}
  )
}


/**
 * 获取计算类型列表
 * @returns {Promise}
 */
export const getCalculationTypes = () => {
  return apiClient.get('/calculation_types')
}

export default apiClient
