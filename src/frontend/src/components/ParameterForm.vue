<template>
  <div class="parameter-form">
    <div class="form-header">
      <h3 class="form-title">
        <span class="title-icon">🐼</span>
        模型参数
      </h3>
      <!-- <div class="model-name">{{ modelName }}</div> -->
    </div>
    
    <div v-if="modelForm.length === 0" class="empty-state">
      <div class="empty-icon">📝</div>
      <p class="empty-message">请先选择一个模型</p>
    </div>
    
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
            <svg width="14" height="14" viewBox="0 0 16 16" fill="none" class="btn-icon">
              <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z" fill="currentColor"/>
            </svg>
            开始计算
          </span>
          <span v-else class="btn-content loading-content">
            <svg width="14" height="14" viewBox="0 0 16 16" fill="none" class="btn-icon spinning">
              <path d="M8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71V3.5z" fill="currentColor"/>
              <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm7-8A7 7 0 1 1 1 8a7 7 0 0 1 14 0z" fill="currentColor"/>
            </svg>
            计算中...
          </span>
        </button>
      </div>
      
      <!-- 参数统计 -->
      <div class="param-stats">
        <span class="param-count">{{ modelForm.length }} 个参数</span>
        <span class="required-note">
          <span class="required">*</span> 必填
        </span>
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

// 计算属性：表单是否有效
const isFormValid = computed(() => {
  return store.isFormValid
})

// 计算属性：是否正在加载
const isLoading = computed(() => {
  return store.isLoading
})

// 提交计算
const submitCalculation = async () => {
  try {
    await store.submitCalculation()
  } catch (error) {
    console.error('计算失败:', error)
    // 错误信息已经在store中设置
  }
}
</script>

<style scoped>
.parameter-form {
  padding: 8px;
  background: #f8fafc;
  border-radius: 4px;
  border: 1px solid #e5e7eb;
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
  font-size: 11px;
}

.form-header {
  flex-shrink: 0;
  margin-bottom: 8px;
  padding-bottom: 6px;
  border-bottom: 1px solid #e5e7eb;
}

.form-title {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 3px 0;
}

.title-icon {
  font-size: 14px;
}

.model-name {
  font-size: 10px;
  color: #6b7280;
  font-weight: 500;
}

.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 20px;
  color: #6b7280;
}

.empty-icon {
  font-size: 24px;
  margin-bottom: 6px;
}

.empty-message {
  font-size: 11px;
  margin: 0;
}

/* 表单内容容器 */
.form-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-height: 0;
}

/* 参数网格布局 - 关键改进 */
.parameters-grid {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 8px;
  padding: 4px;
  overflow-y: auto;
  max-height: 100%;
}

/* 单个参数项 */
.param-item {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  padding: 6px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  transition: all 0.2s ease;
  min-height: 60px;
}

.param-item:hover {
  border-color: #cbd5e1;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* 参数标签 */
.param-label {
  font-size: 10px;
  font-weight: 600;
  color: #374151;
  line-height: 1.2;
  display: flex;
  align-items: center;
  gap: 2px;
}

.required {
  color: #dc2626;
  font-weight: 700;
  font-size: 9px;
}

/* 输入组 */
.param-input-group {
  display: flex;
  align-items: center;
  gap: 4px;
  flex: 1;
}

/* 参数输入框 */
.param-input {
  flex: 1;
  padding: 3px 4px;
  border: 1px solid #d1d5db;
  border-radius: 3px;
  font-size: 10px;
  background: white;
  color: #374151;
  transition: all 0.2s ease;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  min-width: 0;
}

.param-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
}

.param-input:hover {
  border-color: #9ca3af;
}

.param-input::placeholder {
  color: #9ca3af;
  font-style: italic;
  font-family: system-ui, -apple-system, sans-serif;
}

/* 单位显示 */
.param-unit {
  font-size: 9px;
  color: #6b7280;
  font-weight: 500;
  background: #f3f4f6;
  padding: 2px 4px;
  border-radius: 2px;
  white-space: nowrap;
  flex-shrink: 0;
}

/* 计算按钮区域 */
.calculation-section {
  flex-shrink: 0;
  padding: 6px 0;
}

.calculate-btn {
  width: 100%;
  padding: 8px 12px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 6px rgba(59, 130, 246, 0.3);
  position: relative;
  overflow: hidden;
}

.calculate-btn:hover:not(.disabled):not(.loading) {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  transform: translateY(-1px);
  box-shadow: 0 3px 8px rgba(59, 130, 246, 0.4);
}

.calculate-btn:active:not(.disabled):not(.loading) {
  transform: translateY(0);
}

.calculate-btn.disabled {
  background: linear-gradient(135deg, #9ca3af 0%, #6b7280 100%);
  cursor: not-allowed;
  box-shadow: none;
  transform: none;
}

.calculate-btn.loading {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  cursor: wait;
}

.btn-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
}

.btn-icon {
  transition: transform 0.2s ease;
  width: 12px;
  height: 12px;
}

.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.loading-content {
  color: white;
}

/* 按钮波纹效果 */
.calculate-btn::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
}

.calculate-btn:active:not(.disabled)::before {
  width: 150px;
  height: 150px;
}

/* 参数统计 */
.param-stats {
  flex-shrink: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 4px 6px;
  background: #f8fafc;
  border-top: 1px solid #e5e7eb;
  font-size: 9px;
  color: #6b7280;
  border-radius: 3px;
}

.param-count {
  font-weight: 500;
}

.required-note {
  display: flex;
  align-items: center;
  gap: 2px;
}

/* 响应式网格调整 */
@media (min-width: 400px) {
  .parameters-grid {
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  }
}

@media (min-width: 600px) {
  .parameters-grid {
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  }
}

@media (min-width: 800px) {
  .parameters-grid {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  }
}

/* 当参数较少时，限制列数 */
.parameters-grid:has(.param-item:nth-child(-n+4)) {
  grid-template-columns: repeat(2, 1fr);
}

.parameters-grid:has(.param-item:nth-child(-n+6)) {
  grid-template-columns: repeat(3, 1fr);
}

/* 自定义滚动条 */
.parameters-grid::-webkit-scrollbar {
  width: 3px;
}

.parameters-grid::-webkit-scrollbar-track {
  background: #f1f5f9;
}

.parameters-grid::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 2px;
}

.parameters-grid::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* 移动端优化 */
@media (max-width: 768px) {
  .parameter-form {
    padding: 6px;
  }
  
  .parameters-grid {
    grid-template-columns: 1fr 1fr;
    gap: 6px;
  }
  
  .param-item {
    padding: 4px;
    min-height: 50px;
  }
  
  .param-input {
    padding: 2px 3px;
    font-size: 9px;
  }
  
  .calculate-btn {
    padding: 6px 10px;
    font-size: 11px;
  }
}
</style>