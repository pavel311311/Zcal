<template>
<p> 欢迎使用阻抗计算工具</p>
<li v-for="items in modelTypes" :key="items.id">{{ items.name }}</li>

</template>
<script setup>

import { ref, onMounted } from 'vue'
import { useCalculationStore } from '../stores/calculation'
import { getCalculationTypes } from '../api/index'

const modelTypes = ref([])


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

