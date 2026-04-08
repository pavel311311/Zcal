/**
 * API服务 - 与后端通信
 */
import axios, { type AxiosInstance, type AxiosError, type InternalAxiosRequestConfig, type AxiosResponse } from 'axios'
import type { CalculationParams, ModelType, FormField, Material, ApiError } from '../types'

// ==================== 类型定义 ====================

/** 计算请求参数 */
interface CalculateRequest {
  type: string
  params: CalculationParams
}

/** 计算响应 */
interface CalculateResponse {
  status: 'success' | 'error'
  [key: string]: unknown
}

/** 分析请求参数 */
interface AnalyticsHitRequest {
  path?: string
}

/** 分析统计数据 */
interface AnalyticsStatsRequest {
  date?: string
}

// ==================== API 错误类 ====================

class ApiError extends Error {
  status?: number
  originalError?: unknown

  constructor(message: string, status?: number, originalError?: unknown) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.originalError = originalError
  }
}

// ==================== API 客户端 ====================

function getApiBaseUrl(): string {
  // 优先使用环境变量
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL
  }
  // 在开发环境中，使用相对路径，依赖 Vite 代理
  return '/api'
}

const API_BASE_URL = getApiBaseUrl()

// 创建 axios 实例
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => config,
  (error: AxiosError) => Promise.reject(error)
)

// 响应拦截器
apiClient.interceptors.response.use(
  (response: AxiosResponse) => response.data,
  (error: AxiosError) => {
    let errorMessage = '网络请求失败'

    if (error.response) {
      const { status, data } = error.response as AxiosResponse
      switch (status) {
        case 400:
          errorMessage = (data as { message?: string })?.message || '请求参数错误'
          break
        case 404:
          errorMessage = '请求的资源不存在'
          break
        case 500:
          errorMessage = (data as { message?: string })?.message || '服务器内部错误'
          break
        default:
          errorMessage = (data as { message?: string })?.message || `请求失败 (${status})`
      }
    } else if (error.request) {
      // 请求发出但没有收到响应
      errorMessage = '网络连接失败，请检查网络设置'
    } else {
      // 其他错误
      errorMessage = error.message || '未知错误'
    }

    const apiErr = new ApiError(
      errorMessage,
      error.response?.status,
      error
    )
    return Promise.reject(apiErr)
  }
)

// ==================== API 函数 ====================

/**
 * 阻抗计算
 * @param type - 计算类型
 * @param params - 计算参数
 */
async function calculateImpedance(type: string, params: CalculationParams): Promise<CalculateResponse> {
  if (!type) throw new Error('计算类型不能为空')
  if (!params || Object.keys(params).length === 0) throw new Error('计算参数不能为空')
  const request: CalculateRequest = { type, params }
  return apiClient.post<CalculateRequest, CalculateResponse>('/calculate', request)
}

/**
 * 获取材料列表
 */
async function getMaterials(): Promise<Record<string, Material>> {
  return apiClient.get<Record<string, Material>>('/materials')
}

/**
 * 获取表单字段定义
 * @param model - 模型类型
 */
async function getFormFields(model: string): Promise<FormField[]> {
  if (!model) throw new Error('模型类型不能为空')
  return apiClient.get<FormField[]>('/form_fields', { params: { model } })
}

/**
 * 获取计算类型列表
 */
async function getCalculationTypes(): Promise<ModelType[]> {
  return apiClient.get<ModelType[]>('/calculation_types')
}

/**
 * 上报页面访问
 * @param path - 页面路径
 */
async function analyticsHit(path = '/'): Promise<{ status: string }> {
  try {
    const request: AnalyticsHitRequest = { path }
    return apiClient.post<AnalyticsHitRequest, { status: string }>('/analytics/hit', request)
  } catch {
    return { status: 'ignored' }
  }
}

/**
 * 获取分析统计数据
 * @param date - 可选日期参数
 */
async function getAnalyticsStats(date?: string): Promise<unknown> {
  const params: AnalyticsStatsRequest = date ? { date } : {}
  return apiClient.get('/analytics/stats', { params })
}

// ==================== 导出 ====================

export {
  calculateImpedance,
  getMaterials,
  getFormFields,
  getCalculationTypes,
  analyticsHit,
  getAnalyticsStats,
  apiClient,
  ApiError,
}

export type { CalculateRequest, CalculateResponse }
