<template>
  <h2> 欢迎使用阻抗计算工具</h2>
  <h3>🤖选择模型</h3>
  <div>Selected: {{ selectedModel }}</div>
  <select v-model="selectedModel">
    <option disabled value="">Please select one</option>
    <option v-for="item in modelTypes" :key="item.label" :value="item.label"> {{ item.name }} </option>
  </select>

  <p>{{ modelTypes }}</p>

  <div class="img-container">
    <img src="/GSG.png" alt="示例图片" style="max-width: 100%; max-height: 100%;" />
  </div>

</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useCalculationStore } from '../stores/calculationStore'
import { Calculator } from '../services/calculator'

const modelTypes = ref([])
const selectedModel = ref('')
const store = useCalculationStore()

// 监听模型选择变化，更新到store
watch(selectedModel, (newModel) => {
  store.setSelectedModel(newModel)
})

onMounted( async () => {
  const calculator = new Calculator();
  modelTypes.value = await calculator.loadModelTypes();
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
