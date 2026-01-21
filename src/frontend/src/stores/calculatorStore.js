import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { Calculator } from '../services/calculator'

export const useCalculationStore = defineStore('calculation', () => {
  // === 状态定义 ===
  const result = ref(null)
  const isLoading = ref(false)
  const selectedModel = ref('')
  const modelForm = ref([])
  const selectedMaterial = ref('')
  const materials = ref([])
  const modelTypes = ref([])
  const error = ref(null)
  
  // 计算器实例
  const calculator = ref(new Calculator())

  // === 计算属性 ===
  const hasResult = computed(() => result.value !== null)
  const hasError = computed(() => error.value !== null)
  const isFormValid = computed(() => {
    return selectedModel.value && 
           modelForm.value.length > 0 && 
           calculator.value.isFormValid(modelForm.value, selectedModel.value)
  })

  // === 状态管理方法 ===
  const setLoading = (flag) => {
    isLoading.value = flag
    if (flag) error.value = null // 开始加载时清除错误
  }

  const setResult = (res) => {
    result.value = res
    error.value = null
  }

  const setError = (err) => {
    error.value = err
    result.value = null
  }

  const clearError = () => {
    error.value = null
  }

  const clearAll = () => {
    result.value = null
    isLoading.value = false
    error.value = null
  }

  // === 业务逻辑方法 ===
  
  /**
   * 初始化应用数据
   */
  const initializeApp = async () => {
    try {
      setLoading(true)
      await Promise.all([
        loadModelTypes(),
        loadMaterials()
      ])
    } catch (err) {
      setError(`初始化失败: ${err.message}`)
      throw err
    } finally {
      setLoading(false)
    }
  }

  /**
   * 加载模型类型
   */
  const loadModelTypes = async () => {
    try {
      const types = await calculator.value.loadModelTypes()
      modelTypes.value = types
      
      // 自动选择第一个模型
      if (Object.keys(types).length > 0 && !selectedModel.value) {
        selectedModel.value = Object.keys(types)[0]
      }
    } catch (err) {
      setError(`加载模型类型失败: ${err.message}`)
      throw err
    }
  }

  /**
   * 加载表单字段
   */
  const loadFormFields = async (model) => {
    if (!model) {
      modelForm.value = []
      return
    }

    try {
      const fields = await calculator.value.loadFormFields(model)
      modelForm.value = fields
    } catch (err) {
      setError(`加载表单字段失败: ${err.message}`)
      modelForm.value = []
    }
  }

  /**
   * 加载材料数据
   */
  const loadMaterials = async () => {
    try {
      const matData = await calculator.value.loadMaterials()
      materials.value = matData
    } catch (err) {
      setError(`加载材料数据失败: ${err.message}`)
      throw err
    }
  }

  /**
   * 选择模型
   */
  const selectModel = async (model) => {
    if (selectedModel.value === model) return
    
    selectedModel.value = model
    clearAll()
    
    if (model) {
      await loadFormFields(model)
    }
  }

  /**
   * 选择材料
   */
  const selectMaterial = (materialKey) => {
    selectedMaterial.value = materialKey
    
    // 自动填充材料参数到表单
    if (materialKey && materials.value[materialKey]) {
      const material = materials.value[materialKey]
      modelForm.value.forEach(field => {
        if (field.key === 'dielectric' && material.er) {
          field.value = material.er
        }
        if (field.key === 'loss_tangent' && material.loss_tangent) {
          field.value = material.loss_tangent
        }
      })
    }
  }

  /**
   * 提交计算
   */
  const submitCalculation = async () => {
    if (!isFormValid.value) {
      setError('请填写完整的表单数据')
      return
    }

    try {
      setLoading(true)
      const result = await calculator.value.submitCalculation(modelForm.value, selectedModel.value)
      setResult(result)
    } catch (err) {
      setError(`计算失败: ${err.message}`)
      throw err
    } finally {
      setLoading(false)
    }
  }

  /**
   * 重置表单
   */
  const resetForm = () => {
    modelForm.value.forEach(field => {
      field.value = field.placeholder || ''
    })
    clearAll()
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
    
    // 计算属性
    hasResult,
    hasError,
    isFormValid,
    
    // 方法
    initializeApp,
    loadModelTypes,
    loadFormFields,
    loadMaterials,
    selectModel,
    selectMaterial,
    submitCalculation,
    resetForm,
    clearError,
    clearAll
  }
})
