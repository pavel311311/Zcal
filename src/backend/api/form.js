/**
 * 表单定义API处理函数
 * 移植自 backend/app/routes/form.py
 */

const formDefinitions = {
  microstrip: {
    type: 'microstrip',
    name: '微带线',
    description: '单层PCB上的微带线传输线',
    fields: [
      { name: 'width', label: '迹线宽度', unit: 'mil', type: 'number', required: true },
      { name: 'height', label: '绝缘体厚度', unit: 'mil', type: 'number', required: true },
      { name: 'thickness', label: '铜厚', unit: 'mil', type: 'number', default: 1.37, required: true },
      { name: 'dielectric', label: '相对介电常数', unit: '', type: 'number', default: 4.5, required: true }
    ]
  },
  stripline: {
    type: 'stripline',
    name: '带状线',
    description: '夹在两层地平面之间的传输线',
    fields: [
      { name: 'width', label: '迹线宽度', unit: 'mil', type: 'number', required: true },
      { name: 'height', label: '层间距', unit: 'mil', type: 'number', required: true },
      { name: 'spacing', label: '地平面间距', unit: 'mil', type: 'number', required: true },
      { name: 'thickness', label: '铜厚', unit: 'mil', type: 'number', default: 1.37, required: true },
      { name: 'dielectric', label: '相对介电常数', unit: '', type: 'number', default: 4.5, required: true }
    ]
  },
  coaxial: {
    type: 'coaxial',
    name: '同轴线',
    description: '同轴电缆传输线',
    fields: [
      { name: 'innerDia', label: '内导体直径', unit: 'mil', type: 'number', required: true },
      { name: 'outerDia', label: '外导体直径', unit: 'mil', type: 'number', required: true },
      { name: 'dielectric', label: '相对介电常数', unit: '', type: 'number', default: 2.25, required: true }
    ]
  },
  differential: {
    type: 'differential',
    name: '差分对',
    description: '差分信号传输线对',
    fields: [
      { name: 'width', label: '迹线宽度', unit: 'mil', type: 'number', required: true },
      { name: 'height', label: '绝缘体厚度', unit: 'mil', type: 'number', required: true },
      { name: 'spacing', label: '线间距', unit: 'mil', type: 'number', required: true },
      { name: 'thickness', label: '铜厚', unit: 'mil', type: 'number', default: 1.37, required: true },
      { name: 'dielectric', label: '相对介电常数', unit: '', type: 'number', default: 4.5, required: true }
    ]
  }
}

export const handleForm = async (request) => {
  try {
    const url = new URL(request.url)
    const type = url.pathname.split('/').pop()

    if (type === 'forms') {
      // 返回所有表单定义
      return new Response(
        JSON.stringify({
          forms: Object.values(formDefinitions)
        }),
        { headers: { 'Content-Type': 'application/json' } }
      )
    }

    if (formDefinitions[type]) {
      return new Response(
        JSON.stringify(formDefinitions[type]),
        { headers: { 'Content-Type': 'application/json' } }
      )
    }

    return new Response(JSON.stringify({ error: 'Form not found' }), {
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
