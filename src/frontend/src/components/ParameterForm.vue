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
  padding: 12px;
  background: #f8fafc;
  border-radius: 6px;
  border: 1px solid #e5e7eb;
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.form-header {
  flex-shrink: 0;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #e5e7eb;
}

.form-title {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 4px 0;
}

.title-icon {
  font-size: 16px;
}

.model-name {
  font-size: 11px;
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
  font-size: 32px;
  margin-bottom: 8px;
}

.empty-message {
  font-size: 13px;
  margin: 0;
}

/* 表格容器 - 可滚动 */
.form-table-container {
  flex: 1;
  background: white;
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  min-height: 0;
}

/* 参数表格 */
.parameter-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
  table-layout: fixed;
}

/* 表头样式 - 固定 */
.parameter-table thead {
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}

.parameter-table th {
  padding: 8px 10px;
  text-align: left;
  font-weight: 600;
  color: #374151;
  border-bottom: 1px solid #e5e7eb;
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  position: sticky;
  top: 0;
  background: inherit;
  z-index: 1;
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

/* 表格体容器 */
.parameter-table tbody {
  display: block;
  height: 200px;
  overflow-y: auto;
}

.parameter-table thead,
.parameter-table tbody tr {
  display: table;
  width: 100%;
  table-layout: fixed;
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
  padding: 6px 10px;
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
  font-size: 12px;
  line-height: 1.2;
}

.param-desc {
  color: #6b7280;
  font-size: 9px;
  font-style: italic;
  line-height: 1.1;
}

.required-indicator {
  color: #dc2626;
  font-weight: 700;
  font-size: 11px;
  margin-left: 3px;
}

/* 参数值输入 */
.param-value {
  padding: 4px 8px;
}

.input-wrapper {
  width: 100%;
}

.param-input {
  width: 100%;
  padding: 4px 6px;
  border: 1px solid #d1d5db;
  border-radius: 3px;
  font-size: 11px;
  background: white;
  color: #374151;
  transition: all 0.2s ease;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
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

.param-input.has-error {
  border-color: #dc2626;
  box-shadow: 0 0 0 2px rgba(220, 38, 38, 0.1);
}

/* 单位列 */
.param-unit {
  text-align: center;
  font-weight: 600;
  color: #374151;
}

.unit-text {
  background: #e5e7eb;
  padding: 2px 4px;
  border-radius: 2px;
  font-size: 9px;
  color: #4b5563;
}

.unit-placeholder {
  color: #9ca3af;
  font-style: italic;
  font-size: 10px;
}

/* 表格底部 - 固定 */
.table-footer {
  flex-shrink: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 10px;
  background: #f8fafc;
  border-top: 1px solid #e5e7eb;
  font-size: 10px;
  color: #6b7280;
}

.param-count {
  font-weight: 500;
}

.required-note {
  display: flex;
  align-items: center;
  gap: 3px;
}

/* 自定义滚动条 */
.parameter-table tbody::-webkit-scrollbar {
  width: 4px;
}

.parameter-table tbody::-webkit-scrollbar-track {
  background: #f1f5f9;
}

.parameter-table tbody::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 2px;
}

.parameter-table tbody::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .parameter-form {
    padding: 10px;
  }
  
  .parameter-table {
    font-size: 11px;
  }
  
  .parameter-table th,
  .parameter-table td {
    padding: 4px 6px;
  }
  
  .param-input {
    padding: 3px 4px;
    font-size: 10px;
  }
  
  .table-footer {
    flex-direction: column;
    gap: 4px;
    text-align: center;
  }
}
</style>