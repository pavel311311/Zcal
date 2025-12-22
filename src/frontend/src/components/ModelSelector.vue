<template>
  <div class="model-selector">
    <h3>🤖选择模型</h3>
    <div class="selected-info">Selected: {{ selectedModel }}</div>
    <select v-model="selectedModel" class="model-select">
      <option disabled value="">请选择一个模型</option>
      <option v-for="item in modelTypes" :key="item.label" :value="item.label">{{ item.name }}</option>
    </select>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { useCalculationStore } from '../stores/calculatorStore'

const modelTypes = ref([])
const store = useCalculationStore()

// 使用计算属性来双向绑定选择的模型
const selectedModel = computed({
  get: () => store.calculator.value?.selectedModel || null,
  set: (val) => {
    store.updateModel(val)
    console.log(store.calculator.value?.selectedModel)
  }
})

onMounted(async () => {
  modelTypes.value = await store.loadModelTypes()
})
</script>
