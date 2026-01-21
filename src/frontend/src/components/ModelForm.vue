<template>
  <div class="model-form">
    <div class="form-header">
      <h2>模型参数配置</h2>
      <div v-if="store.hasError" class="error-banner">
        {{ store.error }}
        <button @click="store.clearError" class="error-close">×</button>
      </div>
    </div>
    
    <!-- 模型选择器 -->
    <ModelSelector />
    
    <!-- 材料选择器 -->
    <MaterialSelector />
    
    <!-- 参数表单 -->
    <ParameterForm />
    
    <!-- 计算控制按钮 -->
    <CalculationControls />
  </div>
</template>

<script setup>
import { watch, onMounted } from 'vue'
import { useCalculationStore } from '../stores/calculatorStore'
import ModelSelector from './ModelSelector.vue'
import MaterialSelector from './MaterialSelector.vue'
import ParameterForm from './ParameterForm.vue'
import CalculationControls from './CalculationControls.vue'

const store = useCalculationStore()

// 监听selectedModel变化，加载对应的表单字段
watch(
  () => store.selectedModel,
  async (newModel) => {
    if (newModel) {
      console.log('🔄 模型切换为：', newModel)
      await store.loadFormFields(newModel)
    }
  }
)

// 组件挂载时初始化应用数据
onMounted(async () => {
  try {
    await store.initializeApp()
  } catch (error) {
    console.error('应用初始化失败:', error)
  }
})
</script>

<style scoped>
.model-form {
  padding: 20px;
  max-width: 500px;
}

.form-header {
  margin-bottom: 20px;
}

.form-header h2 {
  margin: 0 0 10px 0;
  color: #333;
}

.error-banner {
  background-color: #fee;
  border: 1px solid #fcc;
  border-radius: 4px;
  padding: 10px;
  color: #c33;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
}

.error-close {
  background: none;
  border: none;
  font-size: 18px;
  color: #c33;
  cursor: pointer;
  padding: 0;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.error-close:hover {
  background-color: #fcc;
  border-radius: 50%;
}
</style>

