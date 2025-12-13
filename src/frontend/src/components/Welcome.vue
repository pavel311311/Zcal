<template>
  <h2> 欢迎使用阻抗计算工具</h2>
  <h3>🤖选择模型</h3>
  <div>Selected: {{ stores.selectedModel }}</div>
  <select v-model="stores.selectedModel">
    <option disabled value="">Please select one</option>
    <option v-for="(items, key) in modelTypes" :key="items.label" :value="items.label"> {{ items.name }} </option>
  </select>

  <div class="img-container">
    <img src="/GSG.png" alt="示例图片" style="max-width: 100%; max-height: 100%;" />
  </div>

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

<style scoped>
  /* 背景框+居中容器 */
.img-container {
  /* 水平居中 */
  margin: 20px auto;
  /* 淡化背景 + 圆角（视觉柔和） */
  background-color: #f5f5f5;
  border-radius: 8px;
  /* 内边距（背景框和图片的间距） */
  padding: 20px;
  /* 限制容器宽度（可选，根据需求调整） */
  max-width: 600px;
  /* 图片垂直+水平居中 */
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
