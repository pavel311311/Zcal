<template>
  <h2>模型参数显示</h2>

  <!--选择materials-->
  <h3>🐻材料特性</h3>
  <div>
    <label>参考材料:</label>
    <select v-model="selectedMaterial">
      <option value="">-- 选择材料 --</option>
      <option v-for="(material, key) in materials" :key="key" :value="key">{{ material.name }}</option>
    </select>
    <div v-if="selectedMaterial">
      <p>推荐参数: {{ materials[selectedMaterial] }} </p>
    </div>
  </div>

  <h3>🐼模型参数</h3>
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
import { ref, watch, computed, onMounted } from 'vue'
import { useCalculationStore } from '../stores/calculationStore'

const store = useCalculationStore()

const modelForm = ref([])
const materials = ref({})
const selectedMaterial = ref('')
const error = ref('')

const calculator = store.calculator

// 计算阻抗
const submitCalculation = async () => {
  error.value = ''
  try {
    await calculator.submitCalculation(modelForm.value)
  } catch (err) {
    error.value = '计算失败，请检查参数或重试'
  }
}

// 加载模型表单参数
async function loadFormFields(model) {
  modelForm.value = await calculator.loadFormFields(model)
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

// 表单有效性校验
const isFormValid = computed(() => {
  return calculator.isFormValid(modelForm.value)
})

// 组件挂载时加载materials
onMounted(async () => {
  materials.value = await calculator.loadMaterials()
})
</script>