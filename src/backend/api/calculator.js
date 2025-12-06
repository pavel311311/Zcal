/**
 * 计算器API处理函数
 * 移植自 backend/app/routes/calculator.py
 */

// 阻抗计算核心函数
const calculateMicrostrip = (params) => {
  const { width, height, thickness, dielectric } = params
  // Wyle计算公式
  const Z0 = (120 / Math.PI) * Math.log((8 * height) / (width + thickness * 2))
  const effectiveDielectric = (dielectric + 1) / 2
  return Math.round((Z0 / Math.sqrt(effectiveDielectric)) * 100) / 100
}

const calculateStripline = (params) => {
  const { width, height, spacing, thickness, dielectric } = params
  const effectiveHeight = spacing / 2 - height / 2
  const Z0 = (120 / Math.PI) * Math.acosh((2 * effectiveHeight + thickness) / (width + thickness * 2))
  const effectiveDielectric = Math.sqrt(dielectric)
  return Math.round((Z0 / effectiveDielectric) * 100) / 100
}

const calculateCoaxial = (params) => {
  const { innerDia, outerDia, dielectric } = params
  const Z0 = (276 / Math.sqrt(dielectric)) * Math.log10(outerDia / innerDia)
  return Math.round(Z0 * 100) / 100
}

const calculateDifferential = (params) => {
  const { width, height, spacing, thickness, dielectric } = params
  // 差分对单端阻抗
  const singleZ0 = calculateMicrostrip({ width, height, thickness, dielectric })
  // 差分阻抗约为单端的1.5倍（简化公式）
  const differentialZ0 = singleZ0 * 1.5 * (1 - spacing / (width * 3))
  return {
    single: singleZ0,
    differential: Math.round(differentialZ0 * 100) / 100
  }
}

export const handleCalculator = async (request, env) => {
  try {
    if (request.method === 'POST') {
      const data = await request.json()
      const { type, ...params } = data

      let result
      switch (type) {
        case 'microstrip':
          result = { type, impedance: calculateMicrostrip(params) }
          break
        case 'stripline':
          result = { type, impedance: calculateStripline(params) }
          break
        case 'coaxial':
          result = { type, impedance: calculateCoaxial(params) }
          break
        case 'differential':
          result = { type, ...calculateDifferential(params) }
          break
        default:
          return new Response(JSON.stringify({ error: 'Unknown type' }), {
            status: 400,
            headers: { 'Content-Type': 'application/json' }
          })
      }

      // 缓存结果（可选）
      if (env.CACHE) {
        const cacheKey = `calc_${type}_${JSON.stringify(params).hashCode()}`
        await env.CACHE.put(cacheKey, JSON.stringify(result), { expirationTtl: 3600 })
      }

      return new Response(JSON.stringify(result), {
        headers: { 'Content-Type': 'application/json' }
      })
    }

    return new Response(JSON.stringify({ error: 'Method not allowed' }), {
      status: 405,
      headers: { 'Content-Type': 'application/json' }
    })
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    })
  }
}
