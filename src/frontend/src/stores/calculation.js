import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useCalculationStore = defineStore('calculation', () => {
  //状态
  const result = ref(null)
  const isLoading = ref(false)
  const selectedModel = ref('')

  //方法
  const setLoading = (flag) => {
    isLoading.value = flag
  }

  const setResult = (res) => {
    result.value = res
  }

  const setSelectedModel = (model) => {
    selectedModel.value = model
  }

  const clear = () => {
    result.value = null
    isLoading.value = false
    selectedModel.value = ''
  }

  return {
    result, isLoading, selectedModel, setLoading, setResult, setSelectedModel, clear,
  }
})
