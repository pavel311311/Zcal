import { defineStore } from 'pinia'
import { ref, shallowRef } from 'vue'
import { Calculator } from '../services/calculator'

export const useCalculationStore = defineStore('calculation', () => {
  // 状态
  const result = ref(null)
  const isLoading = ref(false)
  const selectedModel = ref('')
  const modelForm = ref([])
  const selectedMaterial = ref('')
  const materials = ref([])
  const modelTypes = ref([])
  const error = ref(null)
  
  // 直接创建calculator实例
  const calculator = shallowRef(new Calculator())

  // 方法
  function initCalculator() {
    calculator.value = new Calculator()
  }

  // 设置加载状态
  const setLoading = (flag) => {
    isLoading.value = flag
  }

  // 设置计算结果
  const setResult = (res) => {
    result.value = res
  }

  // 设置选中的模型
  const setSelectedModel = (model) => {
    selectedModel.value = model
  }

  // 设置模型表单
  const setModelForm = (form) => {
    modelForm.value = form
  }

  // 设置选中的材料
  const setSelectedMaterial = (material) => {
    selectedMaterial.value = material
  }

  // 设置材料列表
  const setMaterials = (matList) => {
    materials.value = matList
  }

  // 设置模型类型列表
  const setModelTypes = (types) => {
    modelTypes.value = types
  }

  // 设置错误信息
  const setError = (err) => {
    error.value = err
  }

  // 清空所有状态
  const clear = () => {
    result.value = null
    isLoading.value = false
    selectedModel.value = ''
    modelForm.value = []
    selectedMaterial.value = ''
    materials.value = []
    modelTypes.value = []
    error.value = null
  }

  // 加载模型类型
  const loadModelTypes = async () => {
    try {
      const types = await calculator.value.loadModelTypes()
      setModelTypes(types)
    } catch (err) {
      setError(err.message)
      throw err
    }
  }

  // 加载模型表单字段
  const loadFormFields = async (model) => {
    try {
      const fields = await calculator.value.loadFormFields(model)
      setModelForm(fields)
    } catch (err) {
      setError(err.message)
      setModelForm([])
    }
  }

  // 加载材料数据
  const loadMaterials = async () => {
    try {
      const matData = await calculator.value.loadMaterials()
      setMaterials(matData)
    } catch (err) {
      setError(err.message)
      throw err
    }
  }

  // 提交计算
  const submitCalculation = async () => {
    try {
      setLoading(true)
      setError(null)
      
      const result = await calculator.value.submitCalculation(modelForm.value, selectedModel.value)
      setResult(result)
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }

  // 检查表单是否有效
  const isFormValid = () => {
    return calculator.value.isFormValid(modelForm.value, selectedModel.value)
  }

  return {
    // 状态
    result,
    isLoading,
    selectedModel,
    modelForm,
    selectedMaterial,
    materials,
    modelTypes,
    error,
    
    // 实例
    calculator,
    
    // 方法
    initCalculator,
    setLoading,
    setResult,
    setSelectedModel,
    setModelForm,
    setSelectedMaterial,
    setMaterials,
    setModelTypes,
    setError,
    clear,
    loadModelTypes,
    loadFormFields,
    loadMaterials,
    submitCalculation,
    isFormValid
  }
})
