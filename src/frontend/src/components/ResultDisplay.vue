<template>
  <div
    class="result-display"
    role="region"
    aria-label="计算结果展示"
    aria-live="polite"
  >
    <!-- 成功结果 -->
    <div
      v-if="store.result && store.result.status === 'success'"
      class="result-content"
    >
      <div class="status-bar">
        <div
          class="status-badge success"
          role="status"
          aria-label="计算状态: 成功"
        >
          <span
            class="dot"
            aria-hidden="true"
          />
          计算成功
        </div>
        <div
          class="status-time"
          aria-label="计算时间"
        >
          {{ currentTime }}
        </div>
      </div>

      <div
        class="result-list"
        role="list"
        aria-label="阻抗计算结果列表"
      >
        <div
          v-for="(def, index) in resultDefinitions"
          :key="def.key"
          class="result-item"
          :class="{ primary: index === 0 }"
          role="listitem"
        >
          <div
            class="result-icon"
            aria-hidden="true"
          >
            {{ getResultIcon(def.key, index) }}
          </div>
          <div class="result-info">
            <div
              :id="`result-label-${def.key}`"
              class="result-label"
            >
              {{ def.label }}
            </div>
            <div
              v-if="index === 0"
              class="result-sublabel"
              :aria-labelledby="`result-label-${def.key}`"
            >
              {{ getEnglishLabel(def.label) }}
            </div>
          </div>
          <div
            class="result-value"
            role="meter"
            :aria-label="`${def.label}数值: ${formatNumber(store.result[def.key], def.precision)} ${def.unit || ''}`"
            :aria-valuenow="Number(store.result[def.key])"
            :aria-valuemin="0"
            :aria-valuetext="`${def.label} = ${formatNumber(store.result[def.key], def.precision)} ${def.unit || ''}`"
          >
            <span class="value">{{ formatNumber(store.result[def.key], def.precision) }}</span>
            <span
              v-if="def.unit"
              class="unit"
            >{{ def.unit }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 错误状态 -->
    <div
      v-else-if="store.error"
      class="result-error"
      role="alert"
      aria-live="assertive"
    >
      <div
        class="error-icon"
        aria-hidden="true"
      >
        ⚠️
      </div>
      <div class="error-title">
        计算失败
      </div>
      <div class="error-message">
        {{ store.error }}
      </div>
      <button
        class="retry-btn"
        type="button"
        @click="store.clearError"
      >
        重试
      </button>
    </div>

    <!-- 空状态 -->
    <div
      v-else
      class="result-empty"
      role="status"
    >
      <div
        class="empty-visual"
        aria-hidden="true"
      >
        <div class="empty-circle" />
        <div class="empty-icon">
          📊
        </div>
      </div>
      <div class="empty-title">
        等待计算
      </div>
      <div class="empty-message">
        配置参数后点击计算<br>即可获得阻抗分析结果
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted, watch } from 'vue'
import { useCalculationStore } from '../stores/calculatorStore'

const store = useCalculationStore()
const currentTime = ref('')

const resultDefinitions = computed(() => {
  return store.result?.resultDefinitions || []
})

function getResultIcon(key, index) {
  const icons = ['⚡', '📊', '📏', '🔗', '📉', '⭕', '⚖️']
  return icons[index % icons.length]
}

function getEnglishLabel(label) {
  const map = {
    '特征阻抗': 'Characteristic Impedance',
    '有效介电常数': 'Effective Dielectric Constant',
    '有效宽度': 'Effective Width',
    '耦合系数': 'Coupling Coefficient',
    '损耗': 'Loss',
    '直径比': 'Diameter Ratio',
    '不对称因子': 'Asymmetry Factor',
  }
  return map[label] || ''
}

function formatNumber(value, decimals = 2) {
  if (value === null || value === undefined || isNaN(value)) return '--'
  return Number(value).toFixed(decimals)
}

function updateTime() {
  const now = new Date()
  currentTime.value = now.toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  })
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
  padding: 16px;
  overflow: hidden;
}

.status-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding: 10px 14px;
  background: rgba(52, 211, 153, 0.1);
  border: 1px solid rgba(52, 211, 153, 0.2);
  border-radius: 10px;
}

.status-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
}

.status-badge.success {
  color: #34d399;
}

.status-badge .dot {
  width: 8px;
  height: 8px;
  background: #34d399;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.status-time {
  font-size: 12px;
  color: rgba(255,255,255,0.4);
  font-family: 'SF Mono', Monaco, monospace;
}

.result-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
  overflow-y: auto;
}

.result-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 14px;
  transition: all 0.3s;
}

.result-item:hover {
  background: rgba(255,255,255,0.05);
  border-color: rgba(255,255,255,0.1);
  transform: translateX(4px);
}

.result-item.primary {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.15), rgba(99, 102, 241, 0.1));
  border: 1px solid rgba(139, 92, 246, 0.3);
  box-shadow: 0 4px 20px rgba(139, 92, 246, 0.2);
}

.result-item.primary:hover {
  border-color: rgba(139, 92, 246, 0.5);
}

.result-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  background: rgba(255,255,255,0.05);
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.2);
}

.result-info {
  flex: 1;
  min-width: 0;
}

.result-label {
  font-size: 14px;
  font-weight: 600;
  color: #fff;
  margin-bottom: 4px;
}

.result-sublabel {
  font-size: 11px;
  color: rgba(255,255,255,0.4);
}

.result-value {
  text-align: right;
  flex-shrink: 0;
}

.value {
  font-size: 24px;
  font-weight: 800;
  font-family: 'SF Mono', Monaco, monospace;
  background: linear-gradient(135deg, #fff 0%, #a5b4fc 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.unit {
  display: block;
  font-size: 12px;
  color: rgba(255,255,255,0.4);
  margin-top: 2px;
}

.result-error {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  text-align: center;
}

.error-icon {
  font-size: 48px;
  opacity: 0.8;
}

.error-title {
  font-size: 18px;
  font-weight: 600;
  color: #f87171;
}

.error-message {
  font-size: 13px;
  color: rgba(255,255,255,0.5);
  max-width: 200px;
}

.retry-btn {
  padding: 10px 20px;
  background: #f87171;
  border: none;
  border-radius: 8px;
  color: #fff;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.retry-btn:hover {
  background: #ef4444;
  transform: translateY(-2px);
}

.result-empty {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 20px;
  text-align: center;
}

.empty-visual {
  position: relative;
  width: 100px;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-circle {
  position: absolute;
  width: 100%;
  height: 100%;
  border: 2px dashed rgba(255,255,255,0.1);
  border-radius: 50%;
  animation: rotate 20s linear infinite;
}

@keyframes rotate {
  to { transform: rotate(360deg); }
}

.empty-icon {
  font-size: 36px;
  opacity: 0.5;
}

.empty-title {
  font-size: 18px;
  font-weight: 600;
  color: rgba(255,255,255,0.8);
}

.empty-message {
  font-size: 13px;
  color: rgba(255,255,255,0.4);
  line-height: 1.6;
}
</style>
