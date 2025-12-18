<template>
  <div class="model-selector">
    <h3>🤖选择模型</h3>
    <div class="selected-info">Selected: {{ selectedModel }}</div>
    <select v-model="selectedModel" class="model-select">
      <option disabled value="">请选择一个模型</option>
      <option v-for="item in modelTypes" :key="item.label" :value="item.label"> 
        {{ item.name }} 
      </option>
    </select>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useCalculationStore } from '../stores/calculationStore'

const modelTypes = ref([])
const selectedModel = ref('')
const store = useCalculationStore()

// 从store获取计算器实例
const calculator = store.calculator

// 监听模型选择变化，更新到store
watch(selectedModel, (newModel) => {
  store.setSelectedModel(newModel)
})

onMounted(async () => {
  try {
    store.setLoading(true)
    // 加载模型类型
    const types = await calculator.loadModelTypes()
    modelTypes.value = types
  } catch (error) {
    console.error('加载模型类型失败:', error)
    modelTypes.value = []
  } finally {
    store.setLoading(false)
  }
})
</script>

