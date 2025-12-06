// 前端环境配置
const API_BASE_URL = import.meta.env.VITE_API_URL || 
  (typeof window !== 'undefined' ? `${window.location.origin}/api` : 'http://localhost:5000/api')

export const apiConfig = {
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
}

// Cloudflare Pages部署时的API代理
export const isCloudflarePages = () => {
  return typeof window !== 'undefined' && 
         (window.location.hostname.includes('pages.dev') || 
          window.location.hostname.includes('cloudflare.com'))
}

// 获取实际的API URL
export const getApiUrl = (path) => {
  const base = import.meta.env.VITE_API_URL || 
    (isCloudflarePages() ? '/api' : 'http://localhost:5000/api')
  return `${base}${path}`
}
