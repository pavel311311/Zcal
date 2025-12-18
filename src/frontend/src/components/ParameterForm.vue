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
import { useCalculationStore } from '../stores/calculatorStore'

const store = useCalculationStore()

// 从store获取modelForm
const modelForm = computed(() => store.modelForm)

// 错误信息数组，与modelForm索引对应
const errors = ref([])

// 获取当前选中的模型名称
const modelName = computed(() => {
  return store.selectedModel || '未选择'
})

// 表单验证
const validateField = (index) => {
  const field = modelForm.value[index]
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
}

// 当模型表单变化时，重新验证
watch(() => modelForm.value.length, () => {
  // 重置错误信息并重新验证所有字段
  errors.value = new Array(modelForm.value.length).fill('')
  modelForm.value.forEach((_, index) => {
    validateField(index)
  })
}, { immediate: true })
</script>

