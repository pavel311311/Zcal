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
import { computed, onMounted } from 'vue'
import { useCalculationStore } from '../stores/calculatorStore'

const store = useCalculationStore()

// 从store获取模型类型和选中的模型
const modelTypes = computed(() => store.modelTypes)
const selectedModel = computed({
  get: () => store.selectedModel,
  set: (value) => store.setSelectedModel(value)
})

onMounted(async () => {
  try {
    // 加载模型类型
    await store.loadModelTypes()
  } catch (error) {
    console.error('加载模型类型失败:', error)
  }
})
</script>

