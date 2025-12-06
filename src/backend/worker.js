/**
 * Cloudflare Workers 入口文件
 * 将Python Flask API转换为Cloudflare Workers格式
 */

import { Router } from 'itty-router'

// 创建路由器
const router = Router()

// 导入API处理函数
import { handleCalculator } from './api/calculator'
import { handleForm } from './api/form'
import { handleMaterial } from './api/material'

// CORS 处理中间件
const setCorsHeaders = (response) => {
  const headers = new Headers(response.headers)
  headers.set('Access-Control-Allow-Origin', '*')
  headers.set('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
  headers.set('Access-Control-Allow-Headers', 'Content-Type')
  return new Response(response.body, { ...response, headers })
}

// 计算器API路由
router.post('/api/calculate', handleCalculator)
router.get('/api/calculate/:type', handleCalculator)

// 表单定义API路由
router.get('/api/form/:type', handleForm)
router.get('/api/forms', handleForm)

// 材料库API路由
router.get('/api/materials', handleMaterial)
router.get('/api/material/:name', handleMaterial)

// 健康检查
router.get('/api/health', () => {
  return new Response(JSON.stringify({ status: 'ok', timestamp: new Date().toISOString() }), {
    headers: { 'Content-Type': 'application/json' }
  })
})

// OPTIONS 预检请求
router.options('*', () => {
  return new Response(null, {
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type'
    }
  })
})

// 404 处理
router.all('*', () => {
  return new Response(JSON.stringify({ error: 'Not Found' }), {
    status: 404,
    headers: { 'Content-Type': 'application/json' }
  })
})

// 导出处理函数
export default {
  fetch: (request, env, ctx) => {
    return router.handle(request, env, ctx).then(setCorsHeaders)
  }
}
