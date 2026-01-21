<template>
  <div class="calculation-controls">
    <div class="controls-header">
      <h3 class="controls-title">
        <span class="title-icon">🐸</span>
        计算控制
      </h3>
    </div>
    
    <!-- 计算按钮 -->
    <button 
      :disabled="!isFormValid || isLoading" 
      @click="submitCalculation" 
      class="calculate-btn"
      :class="{ 'loading': isLoading, 'disabled': !isFormValid }"
    >
      <span v-if="!isLoading" class="btn-content">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" class="btn-icon">
          <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z" fill="currentColor"/>
        </svg>
        开始计算
      </span>
      <span v-else class="btn-content loading-content">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" class="btn-icon spinning">
          <path d="M8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71V3.5z" fill="currentColor"/>
          <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm7-8A7 7 0 1 1 1 8a7 7 0 0 1 14 0z" fill="currentColor"/>
        </svg>
        计算中...
      </span>
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useCalculationStore } from '../stores/calculatorStore'

const store = useCalculationStore()

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
.calculation-controls {
  padding: 8px;
  background: #f8fafc;
  border-radius: 4px;
  border: 1px solid #e5e7eb;
  flex-shrink: 0;
  font-size: 11px;
}

.controls-header {
  margin-bottom: 8px;
  padding-bottom: 6px;
  border-bottom: 1px solid #e5e7eb;
}

.controls-title {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.title-icon {
  font-size: 14px;
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

@media (max-width: 768px) {
  .calculation-controls {
    padding: 6px;
  }
  
  .calculate-btn {
    padding: 6px 10px;
    font-size: 11px;
  }
}
</style>