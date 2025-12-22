import { defineStore } from "pinia"
import { ref, shallowRef } from "vue"
import { app } from '../services/index'


export const useCalculationStore = defineStore('calculatorStore', () => {

  //define state
  const isLoading = ref(false)
  const error = ref(null)
  //define state 
  const calculator = shallowRef(null)

  const selectedModel = ref(null)
  const modelForm = ref(null)
  const modelResult = ref(null)

  //action
  function init() {
    calculator.value = app
  }
  // 设置加载状态
  const setLoading = (flag) => {
    isLoading.value = flag
  }
  

    // 设置错误信息
  const setError = (err) => {
    error.value = err
  }

  // 清空所有状态
  const clear = () => {
    isLoading.value = false
    error.value = null
  }

  // set model

})