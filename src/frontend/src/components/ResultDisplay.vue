<template>
  <div class="result-display">
    <div class="result-header">
      <h2>📊 计算结果</h2>
    </div>
    
    <!-- 成功结果 -->
    <div v-if="store.result && store.result.status === 'success'" class="result-content">
      <div class="result-status">
        <span class="status-badge">✓ 计算成功</span>
        <span class="status-time">{{ currentTime }}</span>
      </div>
      
      <div class="result-list">
        <div 
          v-for="(def, index) in resultDefinitions" 
          :key="def.key" 
          class="result-item"
          :class="{ primary: index === 0 }"
        >
          <div class="result-icon">{{ getResultIcon(def.key, index) }}</div>
          <div class="result-info">
            <div class="result-label">{{ def.label }}</div>
            <div class="result-sublabel" v-if="index === 0">{{ getEnglishLabel(def.label) }}</div>
          </div>
          <div class="result-value">
            <span class="value">{{ formatNumber(store.result[def.key], def.precision) }}</span>
            <span class="unit" v-if="def.unit">{{ def.unit }}</span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 错误状态 -->
    <div v-else-if="store.error" class="result-error">
      <div class="error-icon">⚠️</div>
      <div class="error-info">
        <div class="error-title">计算失败</div>
        <div class="error-message">{{ store.error }}</div>
      </div>
      <button @click="store.clearError" class="retry-btn">重试</button>
    </div>
    
    <!-- 空状态 -->
    <div v-else class="result-empty">
      <div class="empty-icon">🔍</div>
      <div class="empty-title">等待计算</div>
      <div class="empty-message">请选择模型并输入参数，然后点击计算按钮</div>
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
  const icons = ['⚡', '📊', '📏', '🔗', '📉', '⭕', '⚖️']
  return icons[index % icons.length]
}

const getEnglishLabel = (label) => {
  const map = {
    '特征阻抗': 'Characteristic Impedance',
    '有效介电常数': 'Effective Dielectric Constant',
    '有效宽度': 'Effective Width',
    '耦合系数': 'Coupling Coefficient',
    '损耗': 'Loss',
    '直径比': 'Diameter Ratio',
    '不对称因子': 'Asymmetry Factor'
  }
  return map[label] || ''
}

const formatNumber = (value, decimals = 2) => {
  if (value === null || value === undefined || isNaN(value)) return '--'
  return Number(value).toFixed(decimals)
}

const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
}

watch(() => store.result, (newResult) => {
  if (newResult) updateTime()
})

onMounted(() => {
  updateTime()
})
</script>

<style scoped>
.result-display {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 14px;
  min-height: 0;
  overflow: hidden;
}

.result-header {
  flex-shrink: 0;
  margin-bottom: 12px;
}

.result-header h2 {
  font-size: 15px;
  font-weight: 600;
  color: #1d1d1f;
}

/* 结果内容 */
.result-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 10px;
  overflow: hidden;
}

.result-status {
  flex-shrink: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: #f5f5f7;
  border-radius: 8px;
}

.status-badge {
  font-size: 12px;
  font-weight: 600;
  color: #34c759;
}

.status-time {
  font-size: 11px;
  color: #86868b;
}

/* 结果列表 */
.result-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
  overflow-y: auto;
}

.result-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px;
  background: #f5f5f7;
  border-radius: 10px;
  border: 1px solid #e2e2e7;
}

.result-item.primary {
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.08), rgba(0, 102, 204, 0.03));
  border-color: rgba(0, 102, 204, 0.2);
}

.result-icon {
  font-size: 22px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.result-info {
  flex: 1;
  min-width: 0;
}

.result-label {
  font-size: 13px;
  font-weight: 600;
  color: #1d1d1f;
}

.result-sublabel {
  font-size: 10px;
  color: #86868b;
  margin-top: 2px;
}

.result-value {
  text-align: right;
  flex-shrink: 0;
}

.value {
  font-size: 20px;
  font-weight: 700;
  font-family: 'Monaco', 'Menlo', monospace;
  color: #1d1d1f;
}

.unit {
  font-size: 12px;
  color: #86868b;
  margin-left: 4px;
}

/* 错误状态 */
.result-error {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  background: #fef2f2;
  border-radius: 10px;
  padding: 20px;
  text-align: center;
}

.error-icon {
  font-size: 36px;
}

.error-title {
  font-size: 14px;
  font-weight: 600;
  color: #dc2626;
}

.error-message {
  font-size: 12px;
  color: #7f1d1d;
}

.retry-btn {
  padding: 8px 16px;
  background: #dc2626;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 12px;
  cursor: pointer;
}

/* 空状态 */
.result-empty {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  text-align: center;
}

.empty-icon {
  font-size: 48px;
  opacity: 0.5;
}

.empty-title {
  font-size: 15px;
  font-weight: 600;
  color: #1d1d1f;
}

.empty-message {
  font-size: 12px;
  color: #86868b;
  max-width: 200px;
}
</style>
