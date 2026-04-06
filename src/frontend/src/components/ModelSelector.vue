<template>
  <div class="model-selector" role="region" aria-label="传输线模型选择">
    <div class="header">
      <span class="icon" aria-hidden="true">🤖</span>
      <span class="title">传输线模型</span>
    </div>

    <div class="select-wrapper">
      <label for="model-select" class="sr-only">选择传输线模型</label>
      <select
        id="model-select"
        v-model="selectedModel"
        class="model-select"
        aria-describedby="model-select-desc"
      >
        <option disabled value="">选择传输线模型...</option>
        <option v-for="item in modelTypes" :key="item.type" :value="item.type">
          {{ item.name }}
        </option>
      </select>
      <span id="model-select-desc" class="sr-only">
        选择微带线、带状线等不同的PCB传输线模型类型
      </span>
    </div>

    <div class="preview-area">
      <div class="preview-header" id="preview-label">模型示意图</div>
      <div
        class="preview-container"
        role="img"
        :aria-label="selectedModel ? getSelectedModelName(selectedModel) + ' 模型结构示意图' : '选择模型后显示示意图'"
        :aria-describedby="selectedModel ? undefined : 'preview-label'"
      >
        <img
          v-if="selectedModel && modelImageSrc && !imageError"
          :src="modelImageSrc"
          :alt="getSelectedModelName(selectedModel) + ' 模型示意图'"
          :aria-invalid="imageError ? 'true' : undefined"
          @load="imageLoading = false"
          @error="handleImageError"
        />
        <div v-else-if="selectedModel && imageLoading" class="loading" role="status" aria-live="polite">
          <div class="loading-icon" aria-hidden="true">📐</div>
          <span>加载中...</span>
        </div>
        <div v-else-if="selectedModel && imageError" class="error" role="alert" aria-live="assertive">
          <div class="error-icon" aria-hidden="true">🖼️</div>
          <span class="error-text">示意图加载失败</span>
          <span class="error-hint">该模型暂无示意图</span>
        </div>
        <div v-else class="empty" role="status">
          <div class="empty-icon" aria-hidden="true">🔍</div>
          <span>选择模型查看示意图</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { useCalculationStore } from '../stores/calculatorStore'

const store = useCalculationStore()

const modelTypes = computed(() => store.modelTypes)
const selectedModel = computed({
  get: () => store.selectedModel,
  set: (value) => store.selectModel(value),
})

function getSelectedModelName(modelType) {
  const model = modelTypes.value.find((item) => item.type === modelType)
  return model?.name || modelType
}

const imageError = ref(false)
const imageLoading = ref(false)

const modelImageMap = {
  microstrip: 'Microstrip.png',
  stripline: 'SymmetricStripline.png',
  differential_microstrip: 'DifferentialMicrostrip.png',
  coaxial: 'Coaxial.png',
  cpw: 'CPW.png',
  cpwg: 'CPWG.png',
  differential_cpw: 'DifferentialCPW.png',
  differential_cpwg: 'DifferentialCPWG.png',
}

const modelImageSrc = computed(() => {
  if (!selectedModel.value) return null
  const imageName = modelImageMap[selectedModel.value] || `${selectedModel.value}.png`
  return `/models/${imageName}`
})

function handleImageError() {
  imageError.value = true
  imageLoading.value = false
}

watch(selectedModel, () => {
  imageError.value = false
  imageLoading.value = true
})
</script>

<style scoped>
/* Screen-reader only class */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

.model-selector {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 16px;
  gap: 16px;
  overflow: hidden;
}

.header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header .icon {
  font-size: 16px;
}

.header .title {
  font-size: 14px;
  font-weight: 600;
  color: rgba(255,255,255,0.6);
}

.select-wrapper {
  position: relative;
}

.model-select {
  width: 100%;
  padding: 14px 16px;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 12px;
  color: #fff;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
  appearance: none;
  -webkit-appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='rgba(255,255,255,0.4)' d='M6 8L1 3h10z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 14px center;
  padding-right: 36px;
}

.model-select:hover {
  border-color: rgba(139, 92, 246, 0.5);
  background-color: rgba(139, 92, 246, 0.1);
}

.model-select:focus {
  outline: none;
  border-color: #8b5cf6;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2);
}

.model-select option {
  background: #1a1a2e;
  color: #fff;
}

.preview-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-height: 0;
}

.preview-header {
  font-size: 11px;
  font-weight: 600;
  color: rgba(255,255,255,0.4);
  text-transform: uppercase;
  letter-spacing: 1px;
}

.preview-container {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0,0,0,0.3);
  border: 1px dashed rgba(255,255,255,0.1);
  border-radius: 12px;
  padding: 16px;
  min-height: 150px;
}

.preview-container img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  filter: drop-shadow(0 4px 20px rgba(139, 92, 246, 0.3));
  transition: transform 0.3s;
}

.preview-container img:hover {
  transform: scale(1.05);
}

.loading,
.empty,
.error {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: rgba(255,255,255,0.3);
}

.loading-icon,
.empty-icon,
.error-icon {
  font-size: 36px;
  opacity: 0.5;
}

.loading span,
.empty span {
  font-size: 12px;
}

.error-icon {
  opacity: 0.4;
}

.error-text {
  font-size: 13px;
  font-weight: 500;
  color: rgba(255,255,255,0.5);
}

.error-hint {
  font-size: 11px;
  color: rgba(255,255,255,0.25);
}
</style>
