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
          />
          <span class="field-unit" v-if="field.unit">{{ field.unit }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useCalculationStore } from '../stores/calculatorStore'

const store = useCalculationStore()

// 从store获取modelForm
const modelForm = computed(() => store.modelForm)

// 获取当前选中的模型名称
const modelName = computed(() => {
  return store.selectedModel || '未选择'
})
</script>

