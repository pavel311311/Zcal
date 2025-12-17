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
import { Calculator } from '../services/calculator'

const modelTypes = ref([])
const selectedModel = ref('')
const store = useCalculationStore()

// 初始化计算器实例
const calculator = new Calculator()

// 监听模型选择变化，更新到store
watch(selectedModel, (newModel) => {
  store.setSelectedModel(newModel)
})

onMounted(async () => {
  try {
    // 加载模型类型
    const types = await calculator.loadModelTypes()
    modelTypes.value = types
  } catch (error) {
    console.error('加载模型类型失败:', error)
    modelTypes.value = []
  }
})
</script>

<style scoped>
.model-selector {
  margin-bottom: 20px;
}

.selected-info {
  margin-bottom: 8px;
  font-weight: bold;
  color: #333;
}

.model-select {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  background-color: white;
  cursor: pointer;
}

.model-select:focus {
  outline: none;
  border-color: #4a90e2;
  box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
}
</style>