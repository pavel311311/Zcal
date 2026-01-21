<template>
  <div class="parameter-form">
    <div class="form-header">
      <h3 class="form-title">
        <span class="title-icon">🐼</span>
        模型参数
      </h3>
      <div class="model-name">模型：{{ modelName }}</div>
    </div>
    
    <div v-if="modelForm.length === 0" class="empty-state">
      <div class="empty-icon">📝</div>
      <p class="empty-message">请先选择一个模型</p>
    </div>
    
    <div v-else class="form-table-container">
      <table class="parameter-table">
        <thead>
          <tr>
            <th class="param-name-col">参数名称</th>
            <th class="param-value-col">数值</th>
            <th class="param-unit-col">单位</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(field, index) in modelForm" :key="index" class="parameter-row">
            <td class="param-name">
              <div class="param-label-container">
                <span class="param-label">{{ field.label }}</span>
                <span class="param-desc" v-if="field.description">{{ field.description }}</span>
                <span class="required-indicator" v-if="field.required">*</span>
              </div>
            </td>
            <td class="param-value">
              <div class="input-wrapper">
                <input 
                  :id="`model-field-${index}`" 
                  v-model.number="field.value" 
                  type="number" 
                  :placeholder="field.placeholder"
                  :step="field.step || 0.01" 
                  :min="field.min || 0" 
                  class="param-input"
                  :class="{ 'has-error': field.error }"
                />
              </div>
            </td>
            <td class="param-unit">
              <span class="unit-text" v-if="field.unit">{{ field.unit }}</span>
              <span class="unit-placeholder" v-else>-</span>
            </td>
          </tr>
        </tbody>
      </table>
      
      <!-- 表格底部信息 -->
      <div class="table-footer">
        <div class="param-count">
          共 {{ modelForm.length }} 个参数
        </div>
        <div class="required-note">
          <span class="required-indicator">*</span>
          表示必填参数
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

<style scoped>
.parameter-form {
  padding: 20px;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.form-header {
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 2px solid #e5e7eb;
}

.form-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 8px 0;
}

.title-icon {
  font-size: 20px;
}

.model-name {
  font-size: 14px;
  color: #6b7280;
  font-weight: 500;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #6b7280;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.empty-message {
  font-size: 16px;
  margin: 0;
}

/* 表格容器 */
.form-table-container {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* 参数表格 */
.parameter-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

/* 表头样式 */
.parameter-table thead {
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}

.parameter-table th {
  padding: 12px 16px;
  text-align: left;
  font-weight: 600;
  color: #374151;
  border-bottom: 2px solid #e5e7eb;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* 列宽设置 */
.param-name-col {
  width: 45%;
}

.param-value-col {
  width: 35%;
}

.param-unit-col {
  width: 20%;
}

/* 表格行样式 */
.parameter-row {
  transition: background-color 0.2s ease;
}

.parameter-row:nth-child(even) {
  background-color: #f9fafb;
}

.parameter-row:hover {
  background-color: #f3f4f6;
}

/* 表格单元格 */
.parameter-table td {
  padding: 12px 16px;
  border-bottom: 1px solid #e5e7eb;
  vertical-align: middle;
}

/* 参数名称列 */
.param-name {
  font-weight: 500;
}

.param-label-container {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.param-label {
  color: #1f2937;
  font-weight: 600;
  font-size: 14px;
}

.param-desc {
  color: #6b7280;
  font-size: 12px;
  font-style: italic;
}

.required-indicator {
  color: #dc2626;
  font-weight: 700;
  font-size: 14px;
  margin-left: 4px;
}

/* 参数值输入 */
.param-value {
  padding: 8px 16px;
}

.input-wrapper {
  width: 100%;
}

.param-input {
  width: 100%;
  padding: 8px 12px;
  border: 2px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
  background: white;
  color: #374151;
  transition: all 0.2s ease;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
}

.param-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.param-input:hover {
  border-color: #9ca3af;
}

.param-input::placeholder {
  color: #9ca3af;
  font-style: italic;
  font-family: system-ui, -apple-system, sans-serif;
}

.param-input.has-error {
  border-color: #dc2626;
  box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1);
}

/* 单位列 */
.param-unit {
  text-align: center;
  font-weight: 600;
  color: #374151;
}

.unit-text {
  background: #e5e7eb;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  color: #4b5563;
}

.unit-placeholder {
  color: #9ca3af;
  font-style: italic;
}

/* 表格底部 */
.table-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: #f8fafc;
  border-top: 1px solid #e5e7eb;
  font-size: 12px;
  color: #6b7280;
}

.param-count {
  font-weight: 500;
}

.required-note {
  display: flex;
  align-items: center;
  gap: 4px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .parameter-form {
    padding: 16px;
  }
  
  .parameter-table {
    font-size: 13px;
  }
  
  .parameter-table th,
  .parameter-table td {
    padding: 8px 12px;
  }
  
  .param-name-col {
    width: 40%;
  }
  
  .param-value-col {
    width: 40%;
  }
  
  .param-unit-col {
    width: 20%;
  }
  
  .param-input {
    padding: 6px 8px;
    font-size: 13px;
  }
  
  .table-footer {
    flex-direction: column;
    gap: 8px;
    text-align: center;
  }
}

/* 超小屏幕优化 */
@media (max-width: 480px) {
  .parameter-table th,
  .parameter-table td {
    padding: 6px 8px;
  }
  
  .param-label {
    font-size: 13px;
  }
  
  .param-desc {
    font-size: 11px;
  }
  
  .param-input {
    font-size: 12px;
  }
  
  .unit-text {
    font-size: 11px;
    padding: 2px 6px;
  }
}

/* 表格滚动优化 */
@media (max-width: 640px) {
  .form-table-container {
    overflow-x: auto;
  }
  
  .parameter-table {
    min-width: 480px;
  }
}

/* 打印样式 */
@media print {
  .parameter-form {
    background: white;
    border: 1px solid #000;
  }
  
  .parameter-table {
    border: 1px solid #000;
  }
  
  .parameter-table th,
  .parameter-table td {
    border: 1px solid #000;
  }
}
</style>