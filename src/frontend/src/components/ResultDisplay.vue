<template>
  <div class="result-display">
    <div class="result-header">
      <h2 class="result-title">计算结果</h2>
      <p class="result-description">📊 以下是计算的最终结果：</p>
    </div>
    
    <div v-if="store.result && store.result.status === 'success'" class="result-card">
      <div class="result-card-header">
        <div class="result-status">
          <span class="status-indicator success"></span>
          <span class="status-text">计算成功</span>
        </div>
      </div>
      
      <div class="result-content">
        <div class="result-item">
          <div class="result-label-container">
            <span class="result-label">有效宽度</span>
            <span class="result-label-desc">Effective Width</span>
          </div>
          <div class="result-value-container">
            <span class="result-value">{{ store.result.effective_width.toFixed(4) }}</span>
            <span class="result-unit">mm</span>
          </div>
        </div>
        
        <div class="result-item">
          <div class="result-label-container">
            <span class="result-label">有效介电常数</span>
            <span class="result-label-desc">Effective Dielectric Constant</span>
          </div>
          <div class="result-value-container">
            <span class="result-value">{{ store.result.er_eff.toFixed(3) }}</span>
          </div>
        </div>
        
        <div class="result-item highlight">
          <div class="result-label-container">
            <span class="result-label">阻抗</span>
            <span class="result-label-desc">Impedance</span>
          </div>
          <div class="result-value-container">
            <span class="result-value">{{ store.result.impedance.toFixed(2) }}</span>
            <span class="result-unit">Ω</span>
          </div>
        </div>
      </div>
      
      <div class="result-card-footer">
        <div class="result-timestamp">{{ currentTime }}</div>
      </div>
    </div>
    
    <div v-else-if="store.error" class="result-error">
      <div class="error-header">
        <span class="status-indicator error"></span>
        <span class="error-title">计算失败</span>
      </div>
      <p class="error-message">{{ store.error }}</p>
    </div>
    
    <div v-else class="result-empty">
      <div class="empty-icon">🔍</div>
      <h3 class="empty-title">等待计算</h3>
      <p class="empty-message">请输入参数并点击计算按钮开始分析</p>
    </div>
  </div>
</template>

<script setup>
import { useCalculationStore } from '../stores/calculationStore'
import { computed, ref, onMounted } from 'vue'

const store = useCalculationStore()
const result = computed(() => store.result)
const currentTime = ref('')

const updateCurrentTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  updateCurrentTime()
})
</script>


