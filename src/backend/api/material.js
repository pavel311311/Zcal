/**
 * 材料库API处理函数
 * 移植自 backend/app/routes/material.py
 */

const materialsDatabase = {
  'FR4': {
    name: 'FR4',
    dielectric: 4.5,
    tanD: 0.015,
    frequency: '1 MHz',
    description: '标准玻璃纤维增强环氧树脂',
    frequency_range: '1MHz - 5GHz'
  },
  'FR4_HF': {
    name: 'FR4 (High Frequency)',
    dielectric: 4.2,
    tanD: 0.008,
    frequency: '1 GHz',
    description: '高频FR4，损耗更低',
    frequency_range: '1GHz - 20GHz'
  },
  'Rogers_4003C': {
    name: 'Rogers 4003C',
    dielectric: 3.55,
    tanD: 0.0027,
    frequency: '10 GHz',
    description: '微波级陶瓷填充聚四氟乙烯',
    frequency_range: '1GHz - 50GHz'
  },
  'Rogers_4350B': {
    name: 'Rogers 4350B',
    dielectric: 3.48,
    tanD: 0.004,
    frequency: '10 GHz',
    description: '高性能微波PCB材料',
    frequency_range: '1GHz - 40GHz'
  },
  'Isola_370HR': {
    name: 'Isola 370HR',
    dielectric: 3.66,
    tanD: 0.009,
    frequency: '10 GHz',
    description: '低损耗高可靠性PCB材料',
    frequency_range: '1GHz - 30GHz'
  },
  'Teflon_PTFE': {
    name: 'Teflon / PTFE',
    dielectric: 2.1,
    tanD: 0.0005,
    frequency: '10 GHz',
    description: '聚四氟乙烯，极低损耗',
    frequency_range: '1GHz - 100GHz'
  },
  'Polyimide': {
    name: 'Polyimide',
    dielectric: 3.5,
    tanD: 0.01,
    frequency: '1 GHz',
    description: '聚酰亚胺，高温稳定性',
    frequency_range: '1MHz - 10GHz'
  },
  'Ceramic': {
    name: 'Ceramic',
    dielectric: 9.8,
    tanD: 0.002,
    frequency: '10 GHz',
    description: '陶瓷基复合材料',
    frequency_range: '1GHz - 50GHz'
  }
}

export const handleMaterial = async (request) => {
  try {
    const url = new URL(request.url)
    const pathParts = url.pathname.split('/')
    const name = pathParts[pathParts.length - 1]

    if (name === 'materials') {
      // 返回所有材料
      return new Response(
        JSON.stringify({
          materials: Object.values(materialsDatabase),
          count: Object.keys(materialsDatabase).length
        }),
        { headers: { 'Content-Type': 'application/json' } }
      )
    }

    if (materialsDatabase[name]) {
      return new Response(
        JSON.stringify(materialsDatabase[name]),
        { headers: { 'Content-Type': 'application/json' } }
      )
    }

    return new Response(JSON.stringify({ error: 'Material not found' }), {
      status: 404,
      headers: { 'Content-Type': 'application/json' }
    })
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    })
  }
}
