<template>
  <p>模型表格显示</p>
  <p>{{ modelForm }}</p>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useCalculationStore } from '../stores/calculation'
import { getFormFields } from '../api/index'

const store = useCalculationStore()
const modelForm = ref([])

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
    loadFormFields(newModel)
  },
//   { immediate: true } //初始加载时也执行
)

</script>