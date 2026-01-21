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

const store = useCalculationStore()

// 计算属性：表单是否有效
const isFormValid = computed(() => {
  return store.isFormValid
})

// 计算属性：是否正在加载
const isLoading = computed(() => {
  return store.isLoading
})

// 提交计算
const submitCalculation = async () => {
  try {
    await store.submitCalculation()
  } catch (error) {
    console.error('计算失败:', error)
    // 错误信息已经在store中设置
  }
}

</script>

