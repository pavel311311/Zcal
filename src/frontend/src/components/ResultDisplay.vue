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
    
    <div v-else-if="store.result" class="result-error">
      <div class="error-header">
        <span class="status-indicator error"></span>
        <span class="error-title">计算失败</span>
      </div>
      <p class="error-message">{{ result.message || '未知错误' }}</p>
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

<style scoped>
.result-display {
  margin-top: 30px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

.result-header {
  text-align: center;
  margin-bottom: 25px;
}

.result-title {
  color: #2d3748;
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 8px;
  letter-spacing: -0.5px;
}

.result-description {
  color: #718096;
  font-size: 1rem;
  margin: 0;
}

.result-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  padding: 0;
  margin-top: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15), 0 3px 10px rgba(0, 0, 0, 0.1);
  color: white;
  overflow: hidden;
  transition: all 0.3s ease;
  animation: slideUp 0.5s ease-out;
}

.result-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2), 0 5px 15px rgba(0, 0, 0, 0.1);
}

.result-card-header {
  padding: 20px 25px;
  background: rgba(255, 255, 255, 0.1);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.result-status {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  font-size: 1.1rem;
}

.status-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  flex-shrink: 0;
}

.status-indicator.success {
  background-color: #48bb78;
  box-shadow: 0 0 10px rgba(72, 187, 120, 0.5);
}

.status-indicator.error {
  background-color: #f56565;
  box-shadow: 0 0 10px rgba(245, 101, 101, 0.5);
}

.result-content {
  padding: 25px;
}

.result-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 15px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.result-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.result-item:hover {
  background: rgba(255, 255, 255, 0.05);
  padding: 15px 10px;
  border-radius: 8px;
}

.result-label-container {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.result-label {
  font-weight: 600;
  font-size: 1rem;
  opacity: 0.9;
}

.result-label-desc {
  font-size: 0.75rem;
  opacity: 0.6;
  font-weight: 400;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.result-value-container {
  display: flex;
  align-items: baseline;
  gap: 6px;
}

.result-value {
  font-size: 1.3rem;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.result-unit {
  font-size: 0.9rem;
  opacity: 0.8;
  font-weight: 500;
}

.result-item.highlight {
  background: rgba(255, 255, 255, 0.1);
  padding: 20px 15px;
  border-radius: 10px;
  margin-top: 10px;
  margin-bottom: 10px;
  border-left: 4px solid #ffd700;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.result-item.highlight:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateX(5px);
}

.result-item.highlight .result-value {
  font-size: 1.6rem;
  color: #ffd700;
  text-shadow: 0 2px 10px rgba(255, 215, 0, 0.3);
}

.result-card-footer {
  padding: 15px 25px;
  background: rgba(0, 0, 0, 0.1);
  border-top: 1px solid rgba(255, 255, 255, 0.2);
}

.result-timestamp {
  font-size: 0.8rem;
  opacity: 0.7;
  text-align: right;
}

.result-error {
  background: #fff5f5;
  border: 1px solid #fed7d7;
  border-radius: 12px;
  padding: 20px;
  margin-top: 20px;
  transition: all 0.3s ease;
  animation: slideUp 0.5s ease-out;
}

.result-error:hover {
  box-shadow: 0 5px 15px rgba(245, 101, 101, 0.1);
}

.error-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
}

.error-title {
  color: #c53030;
  font-weight: 600;
  font-size: 1.1rem;
}

.error-message {
  color: #742a2a;
  margin: 0;
  line-height: 1.5;
}

.result-empty {
  background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
  padding: 60px 30px;
  border-radius: 16px;
  margin-top: 20px;
  text-align: center;
  border: 2px dashed #cbd5e0;
  transition: all 0.3s ease;
  animation: slideUp 0.5s ease-out;
}

.result-empty:hover {
  background: linear-gradient(135deg, #edf2f7 0%, #e2e8f0 100%);
  border-color: #a0aec0;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 15px;
  opacity: 0.5;
  animation: bounce 2s infinite;
}

.empty-title {
  color: #4a5568;
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 8px;
}

.empty-message {
  color: #718096;
  margin: 0;
  font-size: 0.95rem;
  max-width: 400px;
  margin: 0 auto;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-10px);
  }
  60% {
    transform: translateY(-5px);
  }
}

@media (max-width: 768px) {
  .result-display {
    margin-top: 20px;
  }
  
  .result-header {
    margin-bottom: 20px;
  }
  
  .result-title {
    font-size: 1.5rem;
  }
  
  .result-card {
    border-radius: 12px;
  }
  
  .result-content {
    padding: 20px;
  }
  
  .result-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
    text-align: left;
  }
  
  .result-value-container {
    align-self: flex-end;
  }
  
  .result-item.highlight {
    padding: 15px;
  }
  
  .result-item.highlight .result-value {
    font-size: 1.4rem;
  }
  
  .result-empty {
    padding: 40px 20px;
  }
}
</style>
