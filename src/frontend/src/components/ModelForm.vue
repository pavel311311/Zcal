<template>
  <h2>模型参数显示</h2>

  <!--选择materials-->
  <!-- <p>{{ materials }}</p> -->
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
    <input v-model="DK" />
    <label>DF </label>
    <input v-model="DF" />
  </div>

  <h3>🐼模型参数</h3>
  <p>{{ modelForm }}</p>
  <!-- 渲染模型表单字段： -->
  <h4>模型：{{ store.selectedModel }}</h4>
  <div v-for="(field, index) in modelForm" :key="index">
    <label :for="`model-field-${index}`">{{ field.label }}</label>
    <input :id="`model-field-${index}`" v-model.number="field.value" type="number" :placeholder="field.placeholder"
      :step="field.step || 0.01" :min="field.min || 0" />
  </div>

  <h3>🐸计算模型</h3>
  <!--按钮-->
  <button :disabled="!isFormValid || store.isLoading" @click="submitCalculation">
    <span v-if="!store.isLoading">计算</span>
    <span v-else>计算中...</span>
  </button>


</template>

<script setup>
import { ref, watch, computed, onMounted, hasInjectionContext } from 'vue'
import { useCalculationStore } from '../stores/calculation'
import { calculateImpedance, getFormFields, getMaterials } from '../api/index'

const store = useCalculationStore()
const modelForm = ref([])
const materials = ref({})
const selectedMaterial = ref('')
const DK = ref('')
const DF = ref('')
const error = ref('')

//材料的er和loss_tangent
function updateMaterialProperties() {
  if (selectedMaterial.value) {
    const material = materials.value[selectedMaterial.value]
    DK.value = material ? material.er : ''
    DF.value = material ? material.loss_tangent : ''
  } else {
    DK.value = ''
    DF.value = ''
  }
}

// 计算表单有效性
const isFormValid = computed(() => {
  return modelForm.value.every(field => field.value !== undefined && field.value !== null && field.value !== '')
})

//计算阻抗
const submitCalculation = async () => {
  error.value = ''
  store.setLoading(true)

  try {
    // 1. 将 modelForm 数组转为键值对对象（假设 field.label 是后端需要的字段名）
    const formData = modelForm.value.reduce((obj, field) => {
      obj[field.key] = field.value // 比如 { "宽度": 10, "高度": 5 }
      return obj
    }, {})
    // 2. 合并 DK/DF 到对象中（按后端要求的字段名调整 key）
    const requestData = {
      ...formData,
      dk: DK.value, // 后端接收的 DK 字段名，比如 dk/er/dielectricConstant
      df: DF.value  // 后端接收的 DF 字段名，比如 df/lossTangent
    }
    // 3. 发送请求（注意：需确认接口是否支持接收对象，若原接口期望数组则用方式1）
    // 若接口仍需数组格式，可忽略步骤1-2，直接用方式1
    console.log('🚀 请求数据：', requestData)
    const response = await calculateImpedance(store.selectedModel, requestData)
    store.setResult(response.data)

  } catch (err) {
    console.error('Calculation error:', err)
  } finally {
    store.setLoading(false)
  }
}

// 封装异步加载表单字段的函数
async function loadFormFields(model) {
  if (!model) {
    modelForm.value = []
    return
  }
  try {
    const response = await getFormFields(model)
    modelForm.value = response.data
  } catch (error) {
    console.error('加载表单字段失败：', error)
    modelForm.value = []
  }
}

// 监听selectedModel变化，触发数据加载
watch(
  () => store.selectedModel,
  (newModel) => {
    console.log('🔄 模型切换为：', newModel);
    loadFormFields(newModel)
  },
  //   { immediate: true } //初始加载时也执行
)

// 组件挂载时加载materials
onMounted(async () => {
  try {
    const response = await getMaterials()
    materials.value = response.data
  } catch (error) {
    console.error('加载材料数据失败：', error)
  }

})



</script>