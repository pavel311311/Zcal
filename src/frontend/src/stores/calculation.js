import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useCalculationStore = defineStore('calculation', () => {
  //状态
  const result = ref(null)
  const isLoading = ref(false)

  //方法
  const setLoading = (flag) => {
    isLoading.value = flag
  }

  const setResult = (res) => {
    result.value = res
  }

  const clear = () => {
    result.value = null
    isLoading.value = false
  }

  return {
    result, isLoading, setLoading, setResult, clear,
  }
})
