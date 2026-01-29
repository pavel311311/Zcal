// 前端环境配置
const getApiBaseUrl = () => {
  // 优先从全局配置对象读取（运行时注入）
  if (window.__APP_CONFIG__ && window.__APP_CONFIG__.API_URL) {
    return window.__APP_CONFIG__.API_URL
  }
  
  // 在浏览器环境中
  if (typeof window !== 'undefined') {
    const { protocol, hostname, port } = window.location
    
    // 如果是Docker容器间通信或生产环境
    if (hostname !== 'localhost' && hostname !== '127.0.0.1') {
      // 使用相同的协议和主机，但端口改为5000
      return `${protocol}//${hostname}:5000/api`
    }
    
    // 开发环境回退到相对路径
    return `${window.location.origin}/api`
  }
  
  // 服务端渲染或其他环境的默认值
  return 'http://localhost:5000/api'
}

const API_BASE_URL = getApiBaseUrl()

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
  const base = getApiBaseUrl()
  return `${base}${path}`
}
