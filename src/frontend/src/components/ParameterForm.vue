<template>
  <div class="parameter-form">
    <div class="form-title">
      <span class="title-icon">🐼</span>
      模型参数
    </div>
    
    <!-- 空状态 -->
    <div v-if="modelForm.length === 0" class="empty-state">
      <div class="empty-icon">📝</div>
      <p>请先选择一个模型</p>
    </div>
    
    <!-- 表单内容 -->
    <div v-else class="form-content">
      <div class="parameters-grid">
        <div v-for="field in modelForm" :key="field.key" class="param-item">
          <label class="param-label">
            {{ field.label }}
            <span class="required" v-if="field.required">*</span>
          </label>
          <div class="param-input-group">
            <input 
              v-model.number="field.value" 
              type="number" 
              :placeholder="field.placeholder"
              :step="field.step || 0.01" 
              :min="field.min || 0" 
              class="param-input"
            />
            <span class="param-unit" v-if="field.unit">{{ field.unit }}</span>
          </div>
        </div>
      </div>
      
      <!-- 计算按钮 -->
      <button 
        :disabled="!isFormValid || isLoading" 
        @click="submitCalculation" 
        class="calculate-btn"
        :class="{ 'loading': isLoading }"
      >
        <span v-if="!isLoading">⚡ 开始计算</span>
        <span v-else>⏳ 计算中...</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useCalculationStore } from '../stores/calculatorStore'

const store = useCalculationStore()

const modelForm = computed(() => store.modelForm)
const isFormValid = computed(() => store.isFormValid)
const isLoading = computed(() => store.isLoading)

const submitCalculation = async () => {
  try {
    await store.submitCalculation()
  } catch (error) {
    console.error('计算失败:', error)
  }
}
</script>

<style scoped>
.parameter-form {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow: hidden;
}

.form-title {
  flex-shrink: 0;
  font-size: 13px;
  font-weight: 600;
  color: #1d1d1f;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.title-icon {
  font-size: 16px;
}

/* 空状态 */
.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #86868b;
  gap: 8px;
}

.empty-icon {
  font-size: 36px;
}

.empty-state p {
  font-size: 12px;
}

/* 表单内容 */
.form-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 10px;
  min-height: 0;
  overflow: hidden;
}

/* 参数网格 - 自适应列数 */
.parameters-grid {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 10px;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 2px;
}

/* 单个参数项 */
.param-item {
  background: #f5f5f7;
  border: 1px solid #e2e2e7;
  border-radius: 8px;
  padding: 10px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.param-label {
  font-size: 11px;
  font-weight: 600;
  color: #1d1d1f;
  display: flex;
  align-items: center;
  gap: 3px;
}

.required {
  color: #dc2626;
  font-size: 10px;
}

.param-input-group {
  display: flex;
  align-items: center;
  gap: 6px;
}

.param-input {
  flex: 1;
  padding: 8px 10px;
  border: 1px solid #e2e2e7;
  border-radius: 6px;
  font-size: 13px;
  font-family: 'Monaco', 'Menlo', monospace;
  background: #ffffff;
  min-width: 0;
}

.param-input:focus {
  border-color: #0066cc;
  box-shadow: 0 0 0 2px rgba(0, 102, 204, 0.1);
  outline: none;
}

.param-unit {
  font-size: 10px;
  color: #86868b;
  background: #f2f2f7;
  padding: 4px 6px;
  border-radius: 4px;
  white-space: nowrap;
  border: 1px solid #e2e2e7;
}

/* 计算按钮 */
.calculate-btn {
  flex-shrink: 0;
  padding: 12px 20px;
  background: #0066cc;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.calculate-btn:hover:not(:disabled) {
  background: #0052a3;
}

.calculate-btn:disabled {
  background: #d2d2d7;
  cursor: not-allowed;
}

.calculate-btn.loading {
  background: #34c759;
}
</style>
