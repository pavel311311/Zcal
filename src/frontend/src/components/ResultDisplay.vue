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
            <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
              <path d="M13.854 3.646a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6.5 10.293l6.646-6.647a.5.5 0 0 1 .708 0z" fill="currentColor"/>
            </svg>
          </div>
          <span class="status-text">计算成功</span>
        </div>
        <div class="result-timestamp">
          <svg width="12" height="12" viewBox="0 0 16 16" fill="none">
            <path d="M8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71V3.5z" fill="currentColor"/>
            <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm7-8A7 7 0 1 1 1 8a7 7 0 0 1 14 0z" fill="currentColor"/>
          </svg>
          {{ currentTime }}
        </div>
      </div>
      
      <div class="result-content">
        <div v-for="(def, index) in resultDefinitions" :key="def.key" class="result-item" :class="{ primary: index === 0 }">
          <div class="result-icon">{{ getResultIcon(def.key, index) }}</div>
          <div class="result-info">
            <div class="result-label-container">
              <span class="result-label">{{ def.label }}</span>
              <span v-if="index === 0" class="result-label-desc">{{ getEnglishLabel(def.label) }}</span>
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
            <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
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
import { computed, ref, onMounted, watch } from 'vue'
import { useCalculationStore } from '../stores/calculatorStore'

const store = useCalculationStore()
const currentTime = ref('')

const resultDefinitions = computed(() => {
  return store.result?.resultDefinitions || []
})

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
  return iconMap[key] || ['⚡', '📊', '📏', '🔗', '📉', '⭕'][index % 6]
}

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

const formatNumber = (value, decimals = 2) => {
  if (value === null || value === undefined || isNaN(value)) return '--'
  return Number(value).toFixed(decimals)
}

const updateCurrentTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

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
  padding: 16px;
  display: flex;
  flex-direction: column;
  min-height: 300px;
  height: 100%;
}

.result-header {
  flex-shrink: 0;
  margin-bottom: 12px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--border-color);
}

.result-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.title-icon {
  font-size: 18px;
}

/* 结果卡片 */
.result-card {
  flex: 1;
  background: var(--bg-card);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
  transition: var(--transition-normal);
  display: flex;
  flex-direction: column;
  border: 1px solid var(--border-color);
}

.result-card:hover {
  box-shadow: var(--shadow-md);
}

.result-card-header {
  flex-shrink: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: var(--bg-main);
  border-bottom: 1px solid var(--border-color);
}

.result-status {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-indicator {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: var(--success-color);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
}

.status-text {
  font-weight: 500;
  font-size: 13px;
  color: var(--text-primary);
}

.result-timestamp {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 11px;
  color: var(--text-secondary);
}

.result-content {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
}

.result-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px;
  border-radius: var(--radius-sm);
  transition: var(--transition-fast);
  margin-bottom: 10px;
  background: var(--bg-main);
  border: 1px solid var(--border-color);
}

.result-item:last-child {
  margin-bottom: 0;
}

.result-item:hover {
  background: #f0f0f5;
}

.result-item.primary {
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.08), rgba(0, 102, 204, 0.04));
  border-color: rgba(0, 102, 204, 0.2);
}

.result-icon {
  font-size: 24px;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-sm);
  background: var(--bg-card);
  flex-shrink: 0;
  box-shadow: var(--shadow-sm);
}

.result-info {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
  min-width: 0;
}

.result-label-container {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.result-label {
  font-weight: 600;
  font-size: 13px;
  color: var(--text-primary);
}

.result-label-desc {
  font-size: 11px;
  color: var(--text-secondary);
  font-weight: 400;
}

.result-value-container {
  display: flex;
  align-items: baseline;
  gap: 6px;
  text-align: right;
}

.result-value {
  font-size: 22px;
  font-weight: 700;
  font-family: var(--font-mono);
  color: var(--text-primary);
}

.result-unit {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
}

/* 错误状态 */
.result-error {
  flex: 1;
  background: var(--warning-bg);
  border: 1px solid var(--warning-border);
  border-radius: var(--radius-md);
  padding: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.error-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 12px;
}

.error-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: #fee2e2;
  color: var(--error-color);
  display: flex;
  align-items: center;
  justify-content: center;
}

.error-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--error-color);
  margin: 0;
}

.error-message {
  color: #7f1d1d;
  margin: 0;
  line-height: 1.5;
  font-size: 13px;
}

.retry-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: var(--error-color);
  color: white;
  border: none;
  border-radius: var(--radius-sm);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: var(--transition-fast);
}

.retry-btn:hover {
  background: #b91c1c;
}

/* 空状态 */
.result-empty {
  flex: 1;
  text-align: center;
  padding: 40px 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-content {
  max-width: 280px;
}

.empty-icon {
  width: 72px;
  height: 72px;
  margin: 0 auto 16px;
  border-radius: var(--radius-lg);
  background: var(--bg-main);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
}

.empty-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 8px 0;
}

.empty-message {
  color: var(--text-secondary);
  line-height: 1.5;
  margin: 0;
  font-size: 13px;
}

/* 动画 */
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

/* 响应式 */
@media (max-width: 768px) {
  .result-display {
    padding: 12px;
    min-height: 250px;
  }
  
  .result-header {
    margin-bottom: 10px;
  }
  
  .result-title {
    font-size: 14px;
  }
  
  .result-card-header {
    flex-direction: column;
    gap: 8px;
    align-items: flex-start;
    padding: 10px 12px;
  }
  
  .result-content {
    padding: 12px;
  }
  
  .result-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
    padding: 14px;
  }
  
  .result-icon {
    width: 40px;
    height: 40px;
    font-size: 20px;
  }
  
  .result-info {
    width: 100%;
    flex-direction: column;
    align-items: flex-start;
    gap: 6px;
  }
  
  .result-value-container {
    align-self: flex-end;
  }
  
  .result-value {
    font-size: 20px;
  }
  
  .result-empty {
    padding: 30px 16px;
  }
  
  .empty-icon {
    width: 60px;
    height: 60px;
  }
  
  .empty-icon svg {
    width: 32px;
    height: 32px;
  }
}
</style>
