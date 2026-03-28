<template>
  <div class="parameter-form">
    <div class="form-header">
      <h3 class="form-title">
        <span class="title-icon">🐼</span>
        模型参数
      </h3>
    </div>
    
    <!-- 空状态 -->
    <div v-if="modelForm.length === 0" class="empty-state">
      <div class="empty-icon">📝</div>
      <p class="empty-message">请先选择一个模型</p>
    </div>
    
    <!-- 表单内容 -->
    <div v-else class="form-content">
      <div class="parameters-grid">
        <div v-for="field in modelForm" :key="field.key" class="param-item">
          <label :for="`model-field-${field.key}`" class="param-label">
            {{ field.label }}
            <span class="required" v-if="field.required">*</span>
          </label>
          <div class="param-input-group">
            <input 
              :id="`model-field-${field.key}`" 
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
      <div class="calculation-section">
        <button 
          :disabled="!isFormValid || isLoading" 
          @click="submitCalculation" 
          class="calculate-btn"
          :class="{ 'loading': isLoading, 'disabled': !isFormValid }"
        >
          <span v-if="!isLoading" class="btn-content">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" class="btn-icon">
              <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z" fill="currentColor"/>
            </svg>
            开始计算
          </span>
          <span v-else class="btn-content loading-content">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" class="btn-icon spinning">
              <path d="M8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71V3.5z" fill="currentColor"/>
              <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm7-8A7 7 0 1 1 1 8a7 7 0 0 1 14 0z" fill="currentColor"/>
            </svg>
            计算中...
          </span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useCalculationStore } from '../stores/calculatorStore'

const store = useCalculationStore()

const modelForm = computed(() => store.modelForm)
const modelName = computed(() => store.selectedModel || '未选择')
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
  padding: 12px;
  background: var(--bg-main);
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-color);
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow: hidden;
}

.form-header {
  flex-shrink: 0;
  margin-bottom: 12px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--border-color);
}

.form-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.title-icon {
  font-size: 18px;
}

/* 空状态 */
.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 40px 20px;
  color: var(--text-secondary);
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 12px;
  opacity: 0.6;
}

.empty-message {
  font-size: 14px;
  margin: 0;
}

/* 表单内容 */
.form-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 16px;
  min-height: 0;
  overflow: hidden;
}

/* 参数网格布局 */
.parameters-grid {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 12px;
  padding: 4px;
  overflow-y: auto;
  overflow-x: hidden;
  max-height: 100%;
}

/* 单个参数项 */
.param-item {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  transition: var(--transition-fast);
}

.param-item:hover {
  border-color: #d0d0d5;
  box-shadow: var(--shadow-sm);
}

/* 参数标签 */
.param-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.3;
  display: flex;
  align-items: center;
  gap: 4px;
}

.required {
  color: var(--error-color);
  font-size: 11px;
}

/* 输入组 */
.param-input-group {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
}

/* 输入框 */
.param-input {
  flex: 1;
  padding: 10px 12px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  font-size: 14px;
  font-family: var(--font-mono);
  background: var(--bg-card);
  color: var(--text-primary);
  min-width: 0;
}

.param-input:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
}

.param-input:hover:not(:focus) {
  border-color: #c0c0c5;
  background-color: #fafafa;
}

.param-input::placeholder {
  color: var(--text-secondary);
  font-style: italic;
  font-family: var(--font-family);
}

/* 单位 */
.param-unit {
  font-size: 11px;
  color: var(--text-secondary);
  font-weight: 500;
  background: var(--bg-main);
  padding: 6px 8px;
  border-radius: 4px;
  white-space: nowrap;
  flex-shrink: 0;
  border: 1px solid var(--border-color);
}

/* 计算按钮 */
.calculation-section {
  flex-shrink: 0;
  padding-top: 8px;
}

.calculate-btn {
  width: 100%;
  padding: 14px 20px;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: var(--radius-sm);
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: var(--transition-normal);
  box-shadow: 0 2px 8px rgba(0, 102, 204, 0.25);
  position: relative;
  overflow: hidden;
}

.calculate-btn:hover:not(.disabled):not(.loading) {
  background: var(--primary-hover);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 102, 204, 0.35);
}

.calculate-btn:active:not(.disabled):not(.loading) {
  transform: translateY(0);
}

.calculate-btn.disabled {
  background: #d2d2d7;
  cursor: not-allowed;
  box-shadow: none;
}

.calculate-btn.loading {
  background: var(--success-color);
  cursor: wait;
}

.btn-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-icon {
  width: 16px;
  height: 16px;
}

.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 响应式 */
@media (max-width: 768px) {
  .parameter-form {
    padding: 10px;
  }
  
  .parameters-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
  }
  
  .param-item {
    padding: 10px;
    gap: 6px;
  }
  
  .param-label {
    font-size: 11px;
  }
  
  .param-input {
    padding: 10px;
    font-size: 16px; /* 防止 iOS 缩放 */
  }
  
  .param-unit {
    font-size: 10px;
    padding: 4px 6px;
  }
  
  .calculate-btn {
    padding: 14px;
    font-size: 15px;
  }
}

@media (max-width: 480px) {
  .parameters-grid {
    grid-template-columns: 1fr;
  }
  
  .form-header {
    margin-bottom: 10px;
  }
  
  .form-title {
    font-size: 13px;
  }
  
  .empty-state {
    padding: 30px 16px;
  }
  
  .empty-icon {
    font-size: 40px;
  }
  
  .empty-message {
    font-size: 13px;
  }
}
</style>
