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
import { Calculator } from '../services/calculator'

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
watch(() => [...props.modelForm], (newForm) => {
  emit('update:modelForm', newForm)
  
  // 重置错误信息并重新验证所有字段
  errors.value = new Array(newForm.length).fill('')
  newForm.forEach((_, index) => {
    validateField(index)
  })
}, { deep: true })

// 初始化时验证所有字段
watch(() => props.modelForm.length, () => {
  errors.value = new Array(props.modelForm.length).fill('')
  props.modelForm.forEach((_, index) => {
    validateField(index)
  })
}, { immediate: true })
</script>

<style scoped>
.parameter-form {
  margin-bottom: 20px;
}

.model-name {
  margin-bottom: 15px;
  font-weight: bold;
  color: #333;
  font-size: 16px;
}

.empty-state {
  padding: 20px;
  text-align: center;
  color: #999;
  background-color: #fafafa;
  border-radius: 4px;
}

.form-fields {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field-label {
  font-weight: bold;
  color: #333;
  font-size: 14px;
}

.required {
  color: #e74c3c;
  margin-left: 4px;
}

.input-container {
  display: flex;
  align-items: center;
  gap: 8px;
}

.field-input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  transition: border-color 0.3s ease;
}

.field-input:focus {
  outline: none;
  border-color: #4a90e2;
  box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
}

.field-input.input-error {
  border-color: #e74c3c;
  background-color: #fff5f5;
}

.field-input.input-error:focus {
  border-color: #e74c3c;
  box-shadow: 0 0 0 2px rgba(231, 76, 60, 0.2);
}

.field-unit {
  color: #666;
  font-weight: bold;
  min-width: 60px;
  text-align: right;
}

.error-message {
  color: #e74c3c;
  font-size: 12px;
  margin: 2px 0 0 0;
  padding: 0;
  line-height: 1.4;
}
</style>