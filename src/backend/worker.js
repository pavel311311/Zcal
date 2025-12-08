/**
 * Cloudflare Workers 入口文件
 * PCB 阻抗计算器 API
 */

import { handleCalculator } from './api/calculator.js'
import { handleForm } from './api/form.js'
import { handleMaterial } from './api/material.js'

// CORS 头配置
const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type'
}

// 路由处理
async function handleRequest(request, env, ctx) {
  const url = new URL(request.url)
  const path = url.pathname
  const method = request.method

  // OPTIONS 预检请求
  if (method === 'OPTIONS') {
    return new Response(null, { headers: corsHeaders })
  }

  try {
    // 健康检查
    if (path === '/api/health') {
      return new Response(
        JSON.stringify({ status: 'ok', timestamp: new Date().toISOString() }),
        { headers: { 'Content-Type': 'application/json', ...corsHeaders } }
      )
    }

    // 计算器 API
    if (path.startsWith('/api/calculate')) {
      const response = await handleCalculator(request, env)
      response.headers.set('Access-Control-Allow-Origin', '*')
      return response
    }

    // 表单 API
    if (path.startsWith('/api/form')) {
      const response = await handleForm(request, env)
      response.headers.set('Access-Control-Allow-Origin', '*')
      return response
    }

    // 材料库 API
    if (path.startsWith('/api/material')) {
      const response = await handleMaterial(request, env)
      response.headers.set('Access-Control-Allow-Origin', '*')
      return response
    }

    // 404 处理
    return new Response(JSON.stringify({ error: 'Not Found' }), {
      status: 404,
      headers: { 'Content-Type': 'application/json', ...corsHeaders }
    })
  } catch (error) {
    console.error('Error:', error)
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json', ...corsHeaders }
    })
  }
}

// 导出处理函数
export default {
  fetch: handleRequest
}
