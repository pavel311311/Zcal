<template>
  <h2>模型参数显示</h2>

  <!--选择materials-->
  <h3>🐻材料选择</h3>
  <div>
    <label>参考材料:</label>
    <select v-model="selectedMaterial" @change="updateMaterialProperties">
      <option value="">-- 选择材料 --</option>
      <option v-for="(material, key) in materials" :key="key" :value="key">{{ material.name }}</option>
    </select>
  </div>
  <div style="display: flex; align-items: center; gap: 5px;">
    <label>DK </label>
    <input v-model="DK" type="number" step="0.01" min="0" />
    <label>DF </label>
    <input v-model="DF" type="number" step="0.0001" min="0" />
  </div>

  <h3>🐼模型参数</h3>
  <p>{{ modelForm }}</p>
  <!-- 渲染模型表单字段： -->
  <h4>模型：{{ store.selectedModel }}</h4>
  <div v-for="(field, index) in modelForm" :key="index">
    <label :for="`model-field-${index}`">{{ field.label }}</label>
    <input 
      :id="`model-field-${index}`" 
      v-model.number="field.value" 
      type="number" 
      :placeholder="field.placeholder"
      :step="field.step || 0.01" 
      :min="field.min || 0" 
    />
  </div>

  <h3>🐸计算模型</h3>
  <!--按钮-->
  <button :disabled="!isFormValid || store.isLoading" @click="submitCalculation">
    <span v-if="!store.isLoading">计算</span>
    <span v-else>计算中...</span>
  </button>
</template>

<script setup>
import { ref, watch, computed, onMounted } from 'vue'
import { useCalculationStore } from '../stores/calculation'
import { calculateImpedance, getFormFields, getMaterials } from '../api/index'

const store = useCalculationStore()
const modelForm = ref([])
const materials = ref({})
const selectedMaterial = ref('')
const DK = ref('')
const DF = ref('')
const error = ref('')

// 材料的er和loss_tangent赋值
function updateMaterialProperties() {
  if (selectedMaterial.value) {
    const material = materials.value[selectedMaterial.value]
    DK.value = material?.er ?? ''
    DF.value = material?.loss_tangent ?? ''
  } else {
    DK.value = ''
    DF.value = ''
  }
}

// 优化：完整的表单有效性校验（包含模型参数+材料参数）
const isFormValid = computed(() => {
  // 1. 模型是否选中
  if (!store.selectedModel) return false
  
  // 2. 模型表单字段校验：有值则校验数值有效性，无值则用后端默认值兜底
  const isModelValid = modelForm.value.every(field => {
    // 优先取输入值 → 后端默认值 → 无
    const finalValue = field.value ?? field.defaultValue
    // 校验：finalValue存在且为有效数值
    return finalValue !== undefined && finalValue !== null && !isNaN(Number(finalValue))
  })
  
  // 3. DK/DF校验（不变）
  const isDkValid = DK.value !== '' && DK.value !== undefined && DK.value !== null && !isNaN(Number(DK.value))
  const isDfValid = DF.value !== '' && DF.value !== undefined && DF.value !== null && !isNaN(Number(DF.value))

  return isModelValid && isDkValid && isDfValid
})


// 计算阻抗
const submitCalculation = async () => {
  error.value = ''
  store.setLoading(true)

  try {
    // 1. 将 modelForm 数组转为键值对对象
    const formData = modelForm.value.reduce((obj, field) => {
      obj[field.key] = Number(field.value) // 确保是数值类型
      return obj
    }, {})
    
    // 2. 合并 DK/DF 并转为数值
    const requestData = {
      ...formData,
      dk: Number(DK.value),
      df: Number(DF.value)
    }
    
    console.log('🚀 请求数据：', requestData)
    const response = await calculateImpedance(store.selectedModel, requestData)
    store.setResult(response.data)

  } catch (err) {
    error.value = '计算失败，请检查参数或重试'
    console.error('Calculation error:', err)
  } finally {
    store.setLoading(false)
  }
}

// 加载模型表单参数
async function loadFormFields(model) {
  if (!model) {
    modelForm.value = []
    return
  }
  try {
    const response = await getFormFields(model)
    // 关键：给每个字段初始化value，避免undefined导致校验失败
    modelForm.value = response.data.map(field => ({
      ...field,
      value: field.value ?? field.defaultValue // 优先用已有值→默认值
    }))
  } catch (error) {
    console.error('加载表单字段失败：', error)
    modelForm.value = []
  }
}

// 监听selectedModel变化（恢复immediate:true，初始加载执行）
watch(
  () => store.selectedModel,
  (newModel) => {
    console.log('🔄 模型切换为：', newModel);
    loadFormFields(newModel)
  },
  { immediate: true } // 关键：初始加载时执行
)

// 组件挂载时加载materials，并自动选中第一个材料（可选，提升体验）
onMounted(async () => {
  try {
    const response = await getMaterials()
    materials.value = response.data
    
    // 自动选中第一个材料（可选，根据业务需求决定是否开启）
    const materialKeys = Object.keys(materials.value)
    if (materialKeys.length > 0) {
      selectedMaterial.value = materialKeys[0]
      updateMaterialProperties() // 自动填充DK/DF
    }
  } catch (error) {
    console.error('加载材料数据失败：', error)
  }
})
</script>