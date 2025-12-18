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
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useCalculationStore } from '../stores/calculatorStore'

const props = defineProps({
  modelForm: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits([])

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
    store.setError(null) // 清空之前的错误
    const result = await calculator.submitCalculation(props.modelForm, store.selectedModel)
    store.setResult(result)
  } catch (error) {
    console.error('计算失败:', error)
    // 使用更友好的错误提示
    const errorMessage = error.message || '计算失败，请检查参数或重试'
    store.setError(errorMessage)
  } finally {
    store.setLoading(false)
  }
}


</script>

