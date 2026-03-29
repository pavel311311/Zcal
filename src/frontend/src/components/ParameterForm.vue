<template>
  <div class="parameter-form">
    <div class="form-header">
      <span class="icon">🐼</span>
      <span class="title">模型参数</span>
    </div>
    
    <div v-if="modelForm.length === 0" class="empty-state">
      <div class="empty-icon">📝</div>
      <p>请先选择一个模型</p>
    </div>
    
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
      
      <button 
        :disabled="!isFormValid || isLoading" 
        @click="submitCalculation" 
        class="calculate-btn"
        :class="{ 'loading': isLoading }"
      >
        <span v-if="!isLoading" class="btn-content">
          <span class="btn-icon">⚡</span>
          开始计算
        </span>
        <span v-else class="btn-content">
          <span class="spinner"></span>
          计算中...
        </span>
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
  padding: 16px;
  gap: 16px;
  overflow: hidden;
}

.form-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.form-header .icon {
  font-size: 16px;
}

.form-header .title {
  font-size: 14px;
  font-weight: 600;
  color: rgba(255,255,255,0.6);
}

.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: rgba(255,255,255,0.3);
}

.empty-icon {
  font-size: 48px;
  opacity: 0.5;
}

.empty-state p {
  font-size: 14px;
}

.form-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 16px;
  overflow: hidden;
}

.parameters-grid {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 12px;
  overflow-y: auto;
  overflow-x: hidden;
}

.param-item {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 12px;
  padding: 14px;
  transition: all 0.3s;
}

.param-item:hover {
  border-color: rgba(139, 92, 246, 0.3);
  background: rgba(139, 92, 246, 0.05);
}

.param-label {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  font-weight: 500;
  color: rgba(255,255,255,0.7);
  margin-bottom: 10px;
}

.required {
  color: #f87171;
  font-size: 11px;
}

.param-input-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.param-input {
  flex: 1;
  min-width: 0; /* 允许收缩到比内容更小，防止溢出 */
  max-width: 100%; /* 确保不超过容器 */
  padding: 12px 14px;
  background: rgba(0,0,0,0.3);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 8px;
  color: #fff;
  font-size: 14px;
  font-family: 'SF Mono', Monaco, monospace;
  transition: all 0.3s;
}

.param-input:hover {
  border-color: rgba(255,255,255,0.2);
}

.param-input:focus {
  outline: none;
  border-color: #8b5cf6;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2);
  background: rgba(139, 92, 246, 0.1);
}

.param-input::placeholder {
  color: rgba(255,255,255,0.25);
}

.param-unit {
  font-size: 11px;
  color: rgba(255,255,255,0.4);
  background: rgba(255,255,255,0.05);
  padding: 6px 8px;
  border-radius: 6px;
  white-space: nowrap;
}

.calculate-btn {
  flex-shrink: 0;
  width: 100%;
  padding: 16px 24px;
  background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
  border: none;
  border-radius: 12px;
  color: #fff;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 20px rgba(139, 92, 246, 0.4);
}

.calculate-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(139, 92, 246, 0.5);
}

.calculate-btn:active:not(:disabled) {
  transform: translateY(0);
}

.calculate-btn:disabled {
  background: rgba(255,255,255,0.1);
  color: rgba(255,255,255,0.3);
  cursor: not-allowed;
  box-shadow: none;
}

.calculate-btn.loading {
  background: linear-gradient(135deg, #34d399 0%, #10b981 100%);
  box-shadow: 0 4px 20px rgba(52, 211, 153, 0.4);
}

.btn-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-icon {
  font-size: 18px;
}

.spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
