<template>
<h2> 欢迎使用阻抗计算工具</h2>
<h3>🤖选择模型</h3>
<div>Selected: {{ stores.selectedModel }}</div>
<select v-model="stores.selectedModel">
  <option disabled value="">Please select one</option>
  <option v-for="(items, key) in modelTypes" :key="items.label" :value="items.label"> {{ items.name }} </option>
</select>

</template>
<script setup>

import { ref, onMounted, computed, watch } from 'vue'
import { useCalculationStore } from '../stores/calculation'
import { getCalculationTypes } from '../api/index'

const modelTypes = ref({})
const stores = useCalculationStore()


// 获取模型类型列表
onMounted(async () => {
  // 这里可以添加任何需要在组件挂载时执行的逻辑
  try {
    // 模拟异步数据获取
    const response = await getCalculationTypes()
    modelTypes.value = response.data
  } catch (error) {
    console.error('获取模型类型失败:', error)
  }
})

</script>

