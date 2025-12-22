import { defineStore } from "pinia"
import { ref, shallowRef } from "vue"
import { app } from '../services/index'


export const useCalculationStore = defineStore('calculatorStore', () => {

  //define state
  const isLoading = ref(false)
  const error = ref(null)
  //define state 
  const calculator = shallowRef(null)

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

  //业务数据状态处理
  // update result
  const updateResult = (result) => {
    calculator.value.result = result
  }
  // update model
  const updateModel = (model) => {
    calculator.value.model = model
  }
    // 加载模型类型
  function loadModelTypes() {
    return calculator.value.loadModelTypes()
  }


  return {
    isLoading, error,calculator, setLoading, setError, init, clear, updateModel,updateResult,loadModelTypes
  }
})