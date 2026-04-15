/**
 * 计算器 Store - 状态管理
 * @file Vue 3 Composition API + Pinia，JSDoc 类型标注
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { Calculator } from '../services/calculator'
import type {
  FormField,
  ModelType,
  Material,
  CalculationResult,
} from '../types'

// ==================== Store 状态接口 ====================

interface HistorySnapshot {
  modelForm: FormField[]
  selectedMaterial: string
  selectedModel: string
  result: CalculationResult
}

// ==================== Store 定义 ====================

export const useCalculationStore = defineStore('calculation', () => {
  // === 状态定义 ===
  const result = ref<CalculationResult>(null)
  const isLoading = ref(false)
  const selectedModel = ref('')
  const modelForm = ref<FormField[]>([])
  const selectedMaterial = ref('')
  const materials = ref<Record<string, Material>>({})
  const modelTypes = ref<ModelType[]>([])
  const error = ref<string | null>(null)

  // 计算器实例
  const calculator = ref(new Calculator())

  // === 撤销/重做历史 ===
  const MAX_HISTORY = 50
  const history = ref<HistorySnapshot[]>([])
  const historyIndex = ref(-1)

  function getHistorySnapshot(): HistorySnapshot {
    return {
      modelForm: JSON.parse(JSON.stringify(modelForm.value)),
      selectedMaterial: selectedMaterial.value,
      selectedModel: selectedModel.value,
      result: result.value,
    }
  }

  function pushHistory(): void {
    // 分支时截断前进历史
    history.value = history.value.slice(0, historyIndex.value + 1)
    history.value.push(getHistorySnapshot())
    if (history.value.length > MAX_HISTORY) {
      history.value.shift()
    }
    historyIndex.value = history.value.length - 1
  }

  const canUndo = computed(() => historyIndex.value > 0)
  const canRedo = computed(() => historyIndex.value < history.value.length - 1)

  function undo(): void {
    if (!canUndo.value) return
    historyIndex.value--
    const snap = history.value[historyIndex.value]
    modelForm.value = JSON.parse(JSON.stringify(snap.modelForm))
    selectedMaterial.value = snap.selectedMaterial
    selectedModel.value = snap.selectedModel
    result.value = snap.result
  }

  function redo(): void {
    if (!canRedo.value) return
    historyIndex.value++
    const snap = history.value[historyIndex.value]
    modelForm.value = JSON.parse(JSON.stringify(snap.modelForm))
    selectedMaterial.value = snap.selectedMaterial
    selectedModel.value = snap.selectedModel
    result.value = snap.result
  }

  // 初始化历史记录（空状态）
  pushHistory()

  // === 计算属性 ===
  const hasResult = computed(() => result.value !== null)
  const hasError = computed(() => error.value !== null)
  const isFormValid = computed(() => {
    return (
      selectedModel.value &&
      modelForm.value.length > 0 &&
      calculator.value.isFormValid(modelForm.value, selectedModel.value)
    )
  })

  // === 状态管理方法 ===
  function setLoading(flag: boolean): void {
    isLoading.value = flag
    if (flag) error.value = null
  }

  function setResult(res: CalculationResult): void {
    result.value = res
    error.value = null
  }

  function setError(err: string): void {
    error.value = err
    result.value = null
  }

  function clearError(): void {
    error.value = null
  }

  function clearAll(): void {
    result.value = null
    isLoading.value = false
    error.value = null
  }

  // === 业务逻辑方法 ===

  /**
   * 初始化应用数据
   */
  async function initializeApp(): Promise<void> {
    try {
      setLoading(true)
      await Promise.all([loadModelTypes(), loadMaterials()])
    } catch (err) {
      setError(`初始化失败: ${(err as Error).message}`)
      throw err
    } finally {
      setLoading(false)
    }
  }

  /**
   * 加载模型类型
   */
  async function loadModelTypes(): Promise<void> {
    try {
      const types = await calculator.value.loadModelTypes()
      modelTypes.value = types

      // 自动选择第一个模型
      if (types.length > 0 && !selectedModel.value) {
        selectedModel.value = types[0].type
      }
    } catch (err) {
      setError(`加载模型类型失败: ${(err as Error).message}`)
      throw err
    }
  }

  /**
   * 加载表单字段
   */
  async function loadFormFields(model: string): Promise<void> {
    if (!model) {
      modelForm.value = []
      return
    }

    try {
      const fields = await calculator.value.loadFormFields(model)
      modelForm.value = fields
    } catch (err) {
      setError(`加载表单字段失败: ${(err as Error).message}`)
      modelForm.value = []
    }
  }

  /**
   * 加载材料数据
   */
  async function loadMaterials(): Promise<void> {
    try {
      const matData = await calculator.value.loadMaterials()
      materials.value = matData
    } catch (err) {
      setError(`加载材料数据失败: ${(err as Error).message}`)
    }
  }

  /**
   * 选择模型
   */
  async function selectModel(model: string): Promise<void> {
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
  function selectMaterial(materialKey: string): void {
    selectedMaterial.value = materialKey

    // 自动填充材料参数到表单
    if (materialKey && materials.value[materialKey]) {
      const material = materials.value[materialKey]
      modelForm.value.forEach((field) => {
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
   * 提交计算（保存历史快照）
   */
  async function submitCalculation(): Promise<void> {
    // 保存当前状态快照到历史
    pushHistory()

    try {
      setLoading(true)
      const calcResult = await calculator.value.submitCalculation(
        modelForm.value,
        selectedModel.value
      )
      setResult(calcResult)
    } catch (err) {
      setError(`计算失败: ${(err as Error).message}`)
      throw err
    } finally {
      setLoading(false)
    }
  }

  /**
   * 重置表单（保存历史快照）
   */
  function resetForm(): void {
    pushHistory()
    modelForm.value.forEach((field) => {
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

    // 撤销/重做
    canUndo,
    canRedo,
    undo,
    redo,

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
    clearAll,
  }
})
