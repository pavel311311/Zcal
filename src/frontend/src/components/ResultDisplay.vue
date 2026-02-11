<template>
  <div class="result-display">
    <div class="result-header">
      <h2 class="result-title">
        <span class="title-icon">📊</span>
        计算结果
      </h2>
    </div>
    
    <!-- 成功结果 -->
    <div v-if="store.result && store.result.status === 'success'" class="result-card">
      <div class="result-card-header">
        <div class="result-status">
          <div class="status-indicator success">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M13.854 3.646a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6.5 10.293l6.646-6.647a.5.5 0 0 1 .708 0z" fill="currentColor"/>
            </svg>
          </div>
          <span class="status-text">计算成功</span>
        </div>
        <div class="result-timestamp">
          <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
            <path d="M8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71V3.5z" fill="currentColor"/>
            <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm7-8A7 7 0 1 1 1 8a7 7 0 0 1 14 0z" fill="currentColor"/>
          </svg>
          {{ currentTime }}
        </div>
      </div>
      
      <div class="result-content">
        <!-- 动态结果项 - 根据 resultDefinitions 渲染 -->
        <div v-for="(def, index) in resultDefinitions" :key="def.key" class="result-item" :class="{ primary: index === 0 }">
          <div class="result-icon">{{ getResultIcon(def.key, index) }}</div>
          <div class="result-info">
            <div class="result-label-container">
              <span class="result-label">{{ def.label }}</span>
              <span v-if="def.key !== 'impedance' && index === 0" class="result-label-desc">{{ getEnglishLabel(def.label) }}</span>
            </div>
            <div class="result-value-container">
              <span class="result-value">{{ formatNumber(store.result[def.key], def.precision) }}</span>
              <span v-if="def.unit" class="result-unit">{{ def.unit }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 错误状态 -->
    <div v-else-if="store.error" class="result-error">
      <div class="error-content">
        <div class="error-icon">
          <svg width="24" height="24" viewBox="0 0 16 16" fill="none">
            <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293 5.354 4.646z" fill="currentColor"/>
          </svg>
        </div>
        <div class="error-info">
          <h3 class="error-title">计算失败</h3>
          <p class="error-message">{{ store.error }}</p>
          <button @click="store.clearError" class="retry-btn">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M11.534 7h3.932a.25.25 0 0 1 .192.41l-1.966 2.36a.25.25 0 0 1-.384 0l-1.966-2.36a.25.25 0 0 1 .192-.41zm-11 2h3.932a.25.25 0 0 0 .192-.41L2.692 6.23a.25.25 0 0 0-.384 0L.342 8.59A.25.25 0 0 0 .534 9z" fill="currentColor"/>
              <path d="M8 3c-1.552 0-2.94.707-3.857 1.818a.5.5 0 1 1-.771-.636A6.002 6.002 0 0 1 13.917 7H12.9A5.002 5.002 0 0 0 8 3zM3.1 9a5.002 5.002 0 0 0 8.757 2.182.5.5 0 1 1 .771.636A6.002 6.002 0 0 1 2.083 9H3.1z" fill="currentColor"/>
            </svg>
            重试
          </button>
        </div>
      </div>
    </div>
    
    <!-- 空状态 -->
    <div v-else class="result-empty">
      <div class="empty-content">
        <div class="empty-icon">
          <svg width="48" height="48" viewBox="0 0 16 16" fill="none">
            <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z" fill="currentColor"/>
          </svg>
        </div>
        <h3 class="empty-title">等待计算</h3>
        <p class="empty-message">请选择模型并输入参数，然后点击计算按钮开始分析</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useCalculationStore } from '../stores/calculatorStore'
import { computed, ref, onMounted, watch } from 'vue'

const store = useCalculationStore()
const currentTime = ref('')

// 计算结果定义
const resultDefinitions = computed(() => {
  return store.result?.resultDefinitions || []
})

// 获取结果项的图标（根据key或按顺序）
const getResultIcon = (key, index) => {
  const iconMap = {
    'impedance': '⚡',
    'er_eff': '📊',
    'effective_width': '📏',
    'coupling_coefficient': '🔗',
    'loss_db_per_mm': '📉',
    'diameter_ratio': '⭕',
    'asymmetry_factor': '⚖️',
    'single_ended_impedance': '➡️'
  }
  
  // 如果有对应的 icon map，使用它；否则使用递增的图标
  return iconMap[key] || ['⚡', '📊', '📏', '🔗', '📉', '⭕'][index % 6]
}

// 获取英文标签（用于某些字段的描述）
const getEnglishLabel = (label) => {
  const labelMap = {
    '特征阻抗': 'Characteristic Impedance',
    '有效介电常数': 'Effective Dielectric Constant',
    '有效宽度': 'Effective Width',
    '耦合系数': 'Coupling Coefficient',
    '损耗': 'Loss',
    '直径比': 'Diameter Ratio',
    '不对称因子': 'Asymmetry Factor',
    '差分阻抗': 'Differential Impedance',
    '单端阻抗': 'Single-ended Impedance'
  }
  return labelMap[label] || ''
}

// 格式化数字显示
const formatNumber = (value, decimals = 2) => {
  if (value === null || value === undefined || isNaN(value)) return '--'
  return Number(value).toFixed(decimals)
}

// 更新时间
const updateCurrentTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

// 监听结果变化，更新时间
watch(() => store.result, (newResult) => {
  if (newResult) {
    updateCurrentTime()
  }
})

onMounted(() => {
  updateCurrentTime()
})
</script>



<style scoped>
.result-display {
  padding: 12px;
  display: flex;
  flex-direction: column;
  min-height: 200px;
  font-size: 12px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  /* 确保在不同显示比例下都能正确显示 */
  max-width: 100%;
  overflow-x: hidden;
  box-sizing: border-box;
}

/* 标题区域 */
.result-header {
  flex-shrink: 0;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #e2e2e7;
}

.result-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #1d1d1f;
  margin: 0;
}

.title-icon {
  font-size: 16px;
}

/* 结果卡片 */
.result-card {
  flex: 1;
  background: #ffffff;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  min-height: 0;
  border: 1px solid #e2e2e7;
}

.result-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transform: translateY(-1px);
}

/* 卡片头部 */
.result-card-header {
  flex-shrink: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: #f2f2f7;
  color: #1d1d1f;
  border-bottom: 1px solid #e2e2e7;
}

.result-status {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #34c759;
  color: white;
}

.status-indicator.success {
  background: #34c759;
}

.status-text {
  font-weight: 500;
  font-size: 13px;
}

.result-timestamp {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  color: #86868b;
}

/* 结果内容 */
.result-content {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
  min-height: 0;
}

.result-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border-radius: 8px;
  transition: all 0.2s ease;
  margin-bottom: 12px;
}

.result-item:last-child {
  margin-bottom: 0;
}

.result-item {
  background: #f2f2f7;
  border: 1px solid #e2e2e7;
}

.result-item:hover {
  background: #ebebf0;
  border-color: #d2d2d7;
}

.result-icon {
  font-size: 20px;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  background: #ffffff;
  flex-shrink: 0;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.result-item:not(.primary) .result-icon {
  background: #ffffff;
}

.result-info {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.result-label-container {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.result-label {
  font-weight: 600;
  font-size: 13px;
  color: #1d1d1f;
}

.result-label-desc {
  font-size: 11px;
  opacity: 0.7;
  font-weight: 400;
  color: #86868b;
}

.result-value-container {
  display: flex;
  align-items: baseline;
  gap: 6px;
  text-align: right;
}

.result-value {
  font-size: 18px;
  font-weight: 600;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  color: #1d1d1f;
}

.result-unit {
  font-size: 13px;
  font-weight: 500;
  color: #86868b;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .result-display {
    padding: 8px;
    font-size: 11px;
    max-width: 100%;
    overflow-x: hidden;
  }
  
  .result-header {
    margin-bottom: 10px;
    padding-bottom: 6px;
    max-width: 100%;
  }
  
  .result-title {
    font-size: 12px;
    gap: 6px;
    max-width: 100%;
  }
  
  .title-icon {
    font-size: 14px;
  }
  
  .result-card-header {
    flex-direction: column;
    gap: 6px;
    align-items: flex-start;
    padding: 10px 12px;
    max-width: 100%;
  }
  
  .result-status {
    gap: 6px;
    max-width: 100%;
  }
  
  .status-indicator {
    width: 16px;
    height: 16px;
  }
  
  .status-indicator svg {
    width: 12px;
    height: 12px;
  }
  
  .status-text {
    font-size: 12px;
    max-width: 100%;
    overflow-x: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  .result-timestamp {
    gap: 4px;
    font-size: 10px;
    max-width: 100%;
    overflow-x: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  .result-timestamp svg {
    width: 12px;
    height: 12px;
  }
  
  .result-content {
    padding: 12px;
    max-width: 100%;
    overflow-x: hidden;
  }
  
  .result-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
    padding: 12px;
    margin-bottom: 8px;
    max-width: 100%;
  }
  
  .result-info {
    width: 100%;
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
    max-width: 100%;
  }
  
  .result-label-container {
    max-width: 100%;
  }
  
  .result-label {
    font-size: 12px;
    max-width: 100%;
    overflow-x: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  .result-label-desc {
    font-size: 10px;
    max-width: 100%;
    overflow-x: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  .result-value-container {
    align-self: flex-end;
    max-width: 100%;
  }
  
  .result-value {
    font-size: 16px;
    max-width: 100%;
    overflow-x: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  .result-unit {
    font-size: 12px;
    white-space: nowrap;
  }
  
  .result-icon {
    font-size: 16px;
    width: 32px;
    height: 32px;
  }
  
  .result-empty {
    padding: 24px 16px;
    max-width: 100%;
  }
  
  .empty-icon {
    width: 48px;
    height: 48px;
    margin-bottom: 12px;
  }
  
  .empty-icon svg {
    width: 32px;
    height: 32px;
  }
  
  .empty-title {
    font-size: 14px;
    margin-bottom: 6px;
    max-width: 100%;
    overflow-x: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  .empty-message {
    font-size: 11px;
    max-width: 100%;
    overflow-x: hidden;
    text-overflow: ellipsis;
  }
  
  .result-error {
    padding: 12px;
    max-width: 100%;
  }
  
  .error-content {
    gap: 8px;
    max-width: 100%;
  }
  
  .error-icon {
    width: 32px;
    height: 32px;
  }
  
  .error-icon svg {
    width: 20px;
    height: 20px;
  }
  
  .error-info {
    max-width: 100%;
  }
  
  .error-title {
    font-size: 12px;
    margin-bottom: 4px;
    max-width: 100%;
    overflow-x: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  .error-message {
    font-size: 11px;
    margin-bottom: 8px;
    max-width: 100%;
    overflow-x: hidden;
    text-overflow: ellipsis;
  }
  
  .retry-btn {
    padding: 6px 10px;
    font-size: 11px;
    min-height: 32px;
    max-width: 100%;
  }
  
  .retry-btn svg {
    width: 14px;
    height: 14px;
  }
  
  /* 确保所有元素都不会超出容器 */
  * {
    max-width: 100%;
    box-sizing: border-box;
  }
}

/* 错误状态 */
.result-error {
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 10px;
  padding: 16px;
}

.error-content {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.error-icon {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: #fee2e2;
  color: #dc2626;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.error-info {
  flex: 1;
}

.error-title {
  font-size: 14px;
  font-weight: 600;
  color: #dc2626;
  margin: 0 0 6px 0;
}

.error-message {
  color: #7f1d1d;
  margin: 0 0 12px 0;
  line-height: 1.4;
  font-size: 12px;
}

.retry-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: #dc2626;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

.retry-btn:hover {
  background: #b91c1c;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(220, 38, 38, 0.2);
}

/* 空状态 */
.result-empty {
  text-align: center;
  padding: 32px 24px;
}

.empty-content {
  max-width: 400px;
  margin: 0 auto;
}

.empty-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 16px;
  border-radius: 12px;
  background: #f2f2f7;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #86868b;
  border: 1px solid #e2e2e7;
}

.empty-title {
  font-size: 16px;
  font-weight: 600;
  color: #1d1d1f;
  margin: 0 0 8px 0;
}

.empty-message {
  color: #86868b;
  line-height: 1.4;
  margin: 0;
  font-size: 12px;
}

/* 动画效果 */
@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.result-card,
.result-error,
.result-empty {
  animation: slideIn 0.3s ease-out;
}

/* 滚动条美化 */
.result-content::-webkit-scrollbar {
  width: 8px;
}

.result-content::-webkit-scrollbar-track {
  background: #f5f5f5;
  border-radius: 4px;
}

.result-content::-webkit-scrollbar-thumb {
  background: #c6c6c8;
  border-radius: 4px;
  border: 2px solid #f5f5f5;
}

.result-content::-webkit-scrollbar-thumb:hover {
  background: #a1a1a6;
}
</style>