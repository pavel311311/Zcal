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
  padding: 8px;
  height: 100%;
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow: hidden;
  font-size: 11px;
}

/* 标题区域 */
.result-header {
  flex-shrink: 0;
  margin-bottom: 8px;
}

.result-title {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.title-icon {
  font-size: 16px;
}

/* 结果卡片 */
.result-card {
  flex: 1;
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  border-radius: 12px;
  box-shadow: 
    0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -1px rgba(0, 0, 0, 0.06),
    0 0 0 1px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.result-card:hover {
  box-shadow: 
    0 10px 15px -3px rgba(0, 0, 0, 0.1),
    0 4px 6px -2px rgba(0, 0, 0, 0.05),
    0 0 0 1px rgba(0, 0, 0, 0.05);
  transform: translateY(-2px);
}

/* 卡片头部 */
.result-card-header {
  flex-shrink: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
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
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

.status-indicator.success {
  background: rgba(255, 255, 255, 0.2);
}

.status-text {
  font-weight: 500;
  font-size: 16px;
}

.result-timestamp {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  opacity: 0.9;
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
  gap: 16px;
  padding: 20px;
  border-radius: 12px;
  transition: all 0.2s ease;
  margin-bottom: 16px;
}

.result-item:last-child {
  margin-bottom: 0;
}

.result-item {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
}

.result-item:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
}

.result-icon {
  font-size: 24px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.1);
  flex-shrink: 0;
}

.result-item:not(.primary) .result-icon {
  background: #e2e8f0;
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
  font-size: 16px;
}

.result-label-desc {
  font-size: 12px;
  opacity: 0.7;
  font-weight: 400;
}

.result-value-container {
  display: flex;
  align-items: baseline;
  gap: 8px;
  text-align: right;
}

.result-value {
  font-size: 20px;
  font-weight: 700;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
}

.result-unit {
  font-size: 16px;
  font-weight: 500;
  opacity: 0.8;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .result-display {
    padding: 16px;
  }
  
  .result-card-header {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
  
  .result-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .result-info {
    width: 100%;
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .result-value-container {
    align-self: flex-end;
  }
}

/* 错误状态 */
.result-error {
  background: linear-gradient(135deg, #fef2f2 0%, #fde8e8 100%);
  border: 1px solid #fecaca;
  border-radius: 16px;
  padding: 24px;
}

.error-content {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.error-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
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
  font-size: 18px;
  font-weight: 600;
  color: #dc2626;
  margin: 0 0 8px 0;
}

.error-message {
  color: #7f1d1d;
  margin: 0 0 16px 0;
  line-height: 1.5;
}

.retry-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: #dc2626;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.retry-btn:hover {
  background: #b91c1c;
  transform: translateY(-1px);
}

/* 空状态 */
.result-empty {
  text-align: center;
  padding: 48px 24px;
}

.empty-content {
  max-width: 400px;
  margin: 0 auto;
}

.empty-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 24px;
  border-radius: 20px;
  background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #9ca3af;
}

.empty-title {
  font-size: 20px;
  font-weight: 600;
  color: #374151;
  margin: 0 0 12px 0;
}

.empty-message {
  color: #6b7280;
  line-height: 1.6;
  margin: 0;
}

/* 动画效果 */
@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
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

/* 深色模式支持 */
@media (prefers-color-scheme: dark) {
  .result-card {
    background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
    color: #f9fafb;
  }
  
  .result-item.secondary {
    background: #374151;
    border-color: #4b5563;
    color: #f9fafb;
  }
  
  .result-item.secondary:hover {
    background: #4b5563;
    border-color: #6b7280;
  }
}
</style>