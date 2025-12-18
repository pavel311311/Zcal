<template>
  <div class="parameter-form">
    <h3>🐼模型参数</h3>
    <div class="model-name">模型：{{ modelName }}</div>
    
    <div v-if="modelForm.length === 0" class="empty-state">
      <p>请先选择一个模型</p>
    </div>
    
    <div v-else class="form-fields">
      <div v-for="(field, index) in modelForm" :key="index" class="form-field">
        <label :for="`model-field-${index}`" class="field-label">
          {{ field.label }}
          <span class="required" v-if="field.required">*</span>
        </label>
        <div class="input-container">
          <input 
            :id="`model-field-${index}`" 
            v-model.number="field.value" 
            type="number" 
            :placeholder="field.placeholder"
            :step="field.step || 0.01" 
            :min="field.min || 0" 
            class="field-input"
            :class="{ 'input-error': errors[index] }"
            @input="validateField(index)"
          />
          <span class="field-unit" v-if="field.unit">{{ field.unit }}</span>
        </div>
        <p class="error-message" v-if="errors[index]">{{ errors[index] }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, watch, ref } from 'vue'
import { useCalculationStore } from '../stores/calculationStore'

const props = defineProps({
  modelForm: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:modelForm', 'form-validity-changed'])

const store = useCalculationStore()
const calculator = store.calculator

// 错误信息数组，与modelForm索引对应
const errors = ref([])

// 获取当前选中的模型名称
const modelName = computed(() => {
  return store.selectedModel || '未选择'
})

// 表单验证
const validateField = (index) => {
  const field = props.modelForm[index]
  let errorMessage = ''
  
  // 必填项验证
  if (field.required && (field.value === null || field.value === undefined || field.value === '')) {
    errorMessage = '此参数为必填项'
  }
  // 数值有效性验证
  else if (field.value !== null && field.value !== undefined && field.value !== '') {
    const numValue = Number(field.value)
    if (isNaN(numValue)) {
      errorMessage = '请输入有效的数值'
    } else if (field.min !== undefined && numValue < field.min) {
      errorMessage = `数值不能小于${field.min}`
    } else if (field.max !== undefined && numValue > field.max) {
      errorMessage = `数值不能大于${field.max}`
    }
  }
  
  // 更新错误信息
  errors.value[index] = errorMessage
  
  // 检查整个表单是否有效
  checkFormValidity()
}

// 检查整个表单的有效性
const checkFormValidity = () => {
  const isValid = errors.value.every(error => !error) && 
                 props.modelForm.every(field => 
                   !field.required || 
                   (field.value !== null && field.value !== undefined && field.value !== '')
                 )
  emit('form-validity-changed', isValid)
}

// 当模型表单变化时，重新验证
// 移除deep: true，只监听数组本身的变化
watch(() => props.modelForm.length, () => {
  // 重置错误信息并重新验证所有字段
  errors.value = new Array(props.modelForm.length).fill('')
  props.modelForm.forEach((_, index) => {
    validateField(index)
  })
}, { immediate: true })

// 初始化时验证所有字段
watch(() => props.modelForm.length, () => {
  errors.value = new Array(props.modelForm.length).fill('')
  props.modelForm.forEach((_, index) => {
    validateField(index)
  })
}, { immediate: true })
</script>

