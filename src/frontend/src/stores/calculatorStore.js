import { defineStore } from 'pinia'
import { ref, shallowRef } from 'vue'
import { Calculator } from '../services/calculator'

export const useCalculationStore = defineStore('calculation', () => {
  // 状态
  const result = ref(null)
  const isLoading = ref(false)
  const selectedModel = ref('')
  const error = ref(null)
  // 直接创建calculator实例，不需要手动初始化
  const calculator = shallowRef(new Calculator())

  // 方法
  function initCalculator() {
    // 保持向后兼容性，如果需要重新初始化可以调用此方法
    calculator.value = new Calculator()
  }
  const setLoading = (flag) => {
    isLoading.value = flag
  }

  const setResult = (res) => {
    result.value = res
  }

  const setSelectedModel = (model) => {
    selectedModel.value = model
  }

  const setError = (err) => {
    error.value = err
  }

  const clear = () => {
    result.value = null
    isLoading.value = false
    selectedModel.value = ''
    error.value = null
  }

  return {
    result, isLoading, selectedModel, error, calculator, initCalculator, setLoading, setResult, setSelectedModel, setError, clear
  }
})
