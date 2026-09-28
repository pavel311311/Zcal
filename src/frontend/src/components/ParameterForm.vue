<template>
  <div
    class="parameter-form"
    role="form"
    aria-label="PCB阻抗计算参数配置"
  >
    <div class="form-header">
      <span
        class="icon"
        aria-hidden="true"
      >🐼</span>
      <span class="title">模型参数</span>
    </div>

    <div
      v-if="modelForm.length === 0"
      class="empty-state"
      role="status"
      aria-live="polite"
    >
      <div
        class="empty-icon"
        aria-hidden="true"
      >
        📝
      </div>
      <p>请先选择一个模型</p>
    </div>

    <div
      v-else
      class="form-content"
      aria-label="参数输入表单"
    >
      <div
        class="parameters-grid"
        role="group"
        aria-label="参数列表"
      >
        <div
          v-for="field in modelForm"
          :key="field.key"
          class="param-item"
        >
          <label
            :for="`param-${field.key}`"
            class="param-label"
          >
            {{ field.label }}
            <span
              v-if="field.required"
              class="required"
              aria-label="必填"
            >*</span>
          </label>
          <div class="param-input-group">
            <input
              :id="`param-${field.key}`"
              v-model.number="field.value"
              type="number"
              :placeholder="String(field.placeholder || '')"
              :step="field.step || 0.01"
              :min="field.min || 0"
              :max="field.max"
              class="param-input"
              :aria-describedby="`param-desc-${field.key}`"
              :aria-invalid="field.required && !field.value ? 'true' : undefined"
              :aria-required="field.required"
            >
            <span
              v-if="field.unit"
              :id="`param-desc-${field.key}`"
              class="param-unit"
              aria-label="单位"
            >{{ field.unit }}</span>
          </div>
        </div>
      </div>

      <div
        class="action-row"
        role="group"
        aria-label="操作按钮"
      >
        <!-- Undo/Redo -->
        <button
          type="button"
          class="action-btn undo-btn"
          :disabled="!store.canUndo"
          :aria-label="store.canUndo ? '撤销上一步' : '无可撤销操作'"
          :title="store.canUndo ? '撤销 (Ctrl+Z)' : '无可撤销操作'"
          @click="handleUndo"
        >
          <span aria-hidden="true">↩️</span>
          撤销
        </button>
        <button
          type="button"
          class="action-btn redo-btn"
          :disabled="!store.canRedo"
          :aria-label="store.canRedo ? '重做上一步' : '无重做操作'"
          :title="store.canRedo ? '重做 (Ctrl+Y)' : '无重做操作'"
          @click="handleRedo"
        >
          <span aria-hidden="true">↪️</span>
          重做
        </button>
      </div>

      <button
        type="button"
        :disabled="!isFormValid || isLoading"
        class="calculate-btn"
        :class="{ loading: isLoading }"
        :aria-label="isLoading ? '计算中...' : '开始计算阻抗'"
        :aria-busy="isLoading"
        @click="submitCalculation"
      >
        <span
          v-if="!isLoading"
          class="btn-content"
        >
          <span
            class="btn-icon"
            aria-hidden="true"
          >⚡</span>
          开始计算
        </span>
        <span
          v-else
          class="btn-content"
          role="status"
          aria-live="polite"
        >
          <span
            class="spinner"
            aria-hidden="true"
          />
          计算中...
        </span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted } from 'vue'
import { useCalculationStore } from '../stores/calculatorStore'

const store = useCalculationStore()

const modelForm = computed(() => store.modelForm)
const isFormValid = computed(() => store.isFormValid)
const isLoading = computed(() => store.isLoading)

async function submitCalculation() {
  try {
    await store.submitCalculation()
  } catch (error) {
    console.error('计算失败:', error)
  }
}

function handleUndo() {
  store.undo()
}

function handleRedo() {
  store.redo()
}

// 键盘快捷键：Ctrl+Z 撤销，Ctrl+Y / Ctrl+Shift+Z 重做
function handleKeydown(e: KeyboardEvent) {
  const isMac = navigator.platform.toUpperCase().includes('MAC')
  const modifier = isMac ? e.metaKey : e.ctrlKey
  if (modifier && e.key === 'z' && !e.shiftKey) {
    e.preventDefault()
    handleUndo()
  } else if (modifier && (e.key === 'y' || (e.key === 'z' && e.shiftKey))) {
    e.preventDefault()
    handleRedo()
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
.parameter-form {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 16px;
  gap: 16px;
  overflow: hidden;
}

.form-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.form-header .icon {
  font-size: 16px;
}

.form-header .title {
  font-size: 14px;
  font-weight: 600;
  color: rgba(255,255,255,0.6);
}

.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: rgba(255,255,255,0.3);
}

.empty-icon {
  font-size: 48px;
  opacity: 0.5;
}

.empty-state p {
  font-size: 14px;
}

.form-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
  overflow: hidden;
}

.parameters-grid {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 12px;
  overflow-y: auto;
  overflow-x: hidden;
}

.param-item {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 12px;
  padding: 14px;
  transition: all 0.3s;
}

.param-item:hover {
  border-color: rgba(139, 92, 246, 0.3);
  background: rgba(139, 92, 246, 0.05);
}

.param-label {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  font-weight: 500;
  color: rgba(255,255,255,0.7);
  margin-bottom: 10px;
  cursor: default;
}

.required {
  color: #f87171;
  font-size: 11px;
}

.param-input-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.param-input {
  flex: 1;
  min-width: 0;
  max-width: 100%;
  padding: 12px 14px;
  background: rgba(0,0,0,0.3);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 8px;
  color: #fff;
  font-size: 14px;
  font-family: 'SF Mono', Monaco, monospace;
  transition: all 0.3s;
}

.param-input:hover {
  border-color: rgba(255,255,255,0.2);
}

.param-input:focus {
  outline: none;
  border-color: #8b5cf6;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2);
  background: rgba(139, 92, 246, 0.1);
}

.param-input::placeholder {
  color: rgba(255,255,255,0.25);
}

.param-input[aria-invalid="true"] {
  border-color: #f87171;
}

.param-input[aria-invalid="true"]:focus {
  box-shadow: 0 0 0 3px rgba(248, 113, 113, 0.2);
}

.param-unit {
  font-size: 11px;
  color: rgba(255,255,255,0.4);
  background: rgba(255,255,255,0.05);
  padding: 6px 8px;
  border-radius: 6px;
  white-space: nowrap;
}

.action-row {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.action-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 8px 12px;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 8px;
  color: rgba(255,255,255,0.7);
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn:hover:not(:disabled) {
  background: rgba(255,255,255,0.1);
  border-color: rgba(255,255,255,0.2);
}

.action-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.calculate-btn {
  flex-shrink: 0;
  width: 100%;
  padding: 16px 24px;
  background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
  border: none;
  border-radius: 12px;
  color: #fff;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 20px rgba(139, 92, 246, 0.4);
}

.calculate-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(139, 92, 246, 0.5);
}

.calculate-btn:active:not(:disabled) {
  transform: translateY(0);
}

.calculate-btn:disabled {
  background: rgba(255,255,255,0.1);
  color: rgba(255,255,255,0.3);
  cursor: not-allowed;
  box-shadow: none;
}

.calculate-btn.loading {
  background: linear-gradient(135deg, #34d399 0%, #10b981 100%);
  box-shadow: 0 4px 20px rgba(52, 211, 153, 0.4);
}

.btn-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-icon {
  font-size: 18px;
}

.spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
