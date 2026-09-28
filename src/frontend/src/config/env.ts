/**
 * 前端环境配置
 * @file TypeScript 版本
 */

/**
 * 获取 API 基础 URL
 * @returns API 基础 URL 字符串
 */
const getApiBaseUrl = (): string => {
  // 优先从全局配置对象读取（运行时注入）
  if (typeof window !== 'undefined' && (window as Window & { __APP_CONFIG__?: { API_URL?: string } }).__APP_CONFIG__?.API_URL) {
    return (window as Window & { __APP_CONFIG__?: { API_URL?: string } }).__APP_CONFIG__!.API_URL!
  }

  // 在浏览器环境中
  if (typeof window !== 'undefined') {
    const { protocol, hostname } = window.location

    // 如果是 Docker 容器间通信或生产环境
    if (hostname !== 'localhost' && hostname !== '127.0.0.1') {
      // 使用相同的协议和主机，但端口改为 5000
      return `${protocol}//${hostname}:5000/api`
    }

    // 开发环境回退到相对路径
    return `${window.location.origin}/api`
  }

  // 服务端渲染或其他环境的默认值
  return 'http://localhost:5000/api'
}

const API_BASE_URL = getApiBaseUrl()

/**
 * API 配置对象
 */
export const apiConfig = {
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
}

/**
 * 检查是否是 Cloudflare Pages 部署
 * @returns 是否是 Cloudflare Pages
 */
export const isCloudflarePages = (): boolean => {
  return typeof window !== 'undefined' &&
         (window.location.hostname.includes('pages.dev') ||
          window.location.hostname.includes('cloudflare.com'))
}

/**
 * 获取完整的 API URL
 * @param path - API 路径
 * @returns 完整的 API URL
 */
export const getApiUrl = (path: string): string => {
  const base = getApiBaseUrl()
  return `${base}${path}`
}
