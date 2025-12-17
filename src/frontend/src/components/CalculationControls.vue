<template>
  <div class="calculation-controls">
    <h3>🐸计算模型</h3>
    
    <!-- 计算按钮 -->
    <button 
      :disabled="!isFormValid || isLoading" 
      @click="submitCalculation" 
      class="calculate-btn"
    >
      <span v-if="!isLoading">计算</span>
      <span v-else>计算中...</span>
    </button>
    
    <!-- 重置按钮 -->
    <button @click="resetForm" class="reset-btn">
      重置
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useCalculationStore } from '../stores/calculationStore'
import { Calculator } from '../services/calculator'

const props = defineProps({
  modelForm: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['reset'])

const store = useCalculationStore()
const calculator = store.calculator

// 计算属性：表单是否有效
const isFormValid = computed(() => {
  return calculator.isFormValid(props.modelForm, store.selectedModel)
})

// 计算属性：是否正在加载
const isLoading = computed(() => {
  return store.isLoading
})

// 提交计算
const submitCalculation = async () => {
  try {
    store.setLoading(true)
    const result = await calculator.submitCalculation(props.modelForm, store.selectedModel)
    store.setResult(result)
  } catch (error) {
    console.error('计算失败:', error)
    alert('计算失败，请检查参数或重试')
  } finally {
    store.setLoading(false)
  }
}

// 重置表单
const resetForm = () => {
  emit('reset')
}
</script>

<style scoped>
.calculation-controls {
  margin-top: 20px;
}

.calculate-btn {
  width: 100%;
  padding: 12px;
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;
}

.calculate-btn:hover:not(:disabled) {
  background-color: #357abd;
}

.calculate-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.reset-btn {
  width: 100%;
  padding: 12px;
  margin-top: 10px;
  background-color: #f0f0f0;
  color: #333;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.reset-btn:hover {
  background-color: #e0e0e0;
}
</style>