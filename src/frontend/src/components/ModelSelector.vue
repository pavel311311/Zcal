<template>
  <div class="model-selector">
    <div class="selector-header">
      <h2 class="selector-title">
        <span class="title-icon">🤖</span>
        选择模型
      </h2>
      <div v-if="selectedModel" class="selected-info">
        当前: <span class="selected-model">{{ getSelectedModelName(selectedModel) }}</span>
      </div>
    </div>
    
    <div class="select-container">
      <select v-model="selectedModel" class="model-select">
        <option disabled value="">请选择一个模型</option>
        <option v-for="item in modelTypes" :key="item.type" :value="item.type">
          {{ item.name }}
        </option>
      </select>
    </div>
    
    <div class="model-preview">
      <div class="preview-header">
        <h4>模型示意图</h4>
      </div>
      <div class="img-container">
        <img 
          v-if="selectedModel && modelImageSrc && !imageError" 
          :src="modelImageSrc" 
          :alt="getSelectedModelName(selectedModel)"
          @error="handleImageError"
          @load="handleImageLoad"
          class="model-image"
        />
        <div v-else-if="selectedModel && !imageLoaded && !imageError" class="image-placeholder">
          <div class="placeholder-icon">📐</div>
          <div class="placeholder-text">加载中...</div>
        </div>
        <div v-else class="no-model-placeholder">
          <div class="placeholder-icon">🔍</div>
          <div class="placeholder-text">请选择模型查看示意图</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch, onMounted } from 'vue'
import { useCalculationStore } from '../stores/calculatorStore'

const store = useCalculationStore()

const modelTypes = computed(() => store.modelTypes)
const selectedModel = computed({
  get: () => store.selectedModel,
  set: (value) => store.selectModel(value)
})

const getSelectedModelName = (modelType) => {
  const model = modelTypes.value.find(item => item.type === modelType)
  return model?.name
}

const imageLoaded = ref(false)
const imageError = ref(false)

const modelImageMap = {
  microstrip: 'Microstrip.png',
  stripline: 'SymmetricStripline.png',
  differential_microstrip: 'DifferentialMicrostrip.png',
  coaxial: 'Coaxial.png',
  cpw: 'CPW.png',
  cpwg: 'CPWG.png',
  differential_cpw: 'DifferentialCPW.png',
  differential_cpwg: 'DifferentialCPWG.png'
}

const modelImageSrc = computed(() => {
  if (!selectedModel.value) return null
  const imageName = modelImageMap[selectedModel.value] || `${selectedModel.value}.png`
  return `/models/${imageName}`
})

const handleImageLoad = () => {
  imageLoaded.value = true
  imageError.value = false
}

const handleImageError = () => {
  imageError.value = true
  imageLoaded.value = false
}

watch(selectedModel, () => {
  imageLoaded.value = false
  imageError.value = false
})

onMounted(async () => {
  try {
    await store.loadModelTypes()
  } catch (error) {
    console.error('加载模型类型失败:', error)
  }
})
</script>

<style scoped>
.model-selector {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

.selector-header {
  flex-shrink: 0;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 12px;
  margin-bottom: 12px;
}

.selector-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 6px 0;
}

.title-icon {
  font-size: 18px;
}

.selected-info {
  font-size: 12px;
  color: var(--text-secondary);
}

.selected-model {
  font-weight: 600;
  color: var(--primary-color);
}

.select-container {
  flex-shrink: 0;
  margin-bottom: 12px;
}

.model-select {
  width: 100%;
  padding: 12px 14px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  font-size: 14px;
  background: var(--bg-card);
  color: var(--text-primary);
  cursor: pointer;
  transition: var(--transition-fast);
}

.model-select:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
}

.model-select:hover:not(:focus) {
  border-color: #c0c0c5;
  background-color: #fafafa;
}

.model-preview {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow: hidden;
}

.preview-header {
  flex-shrink: 0;
  margin-bottom: 8px;
}

.preview-header h4 {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-secondary);
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.img-container {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-main);
  border: 2px dashed var(--border-color);
  border-radius: var(--radius-md);
  padding: 16px;
  min-height: 150px;
  overflow: hidden;
}

.img-container img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  border-radius: var(--radius-sm);
  box-shadow: var(--shadow-sm);
  transition: var(--transition-fast);
}

.img-container img:hover {
  transform: scale(1.02);
}

.image-placeholder,
.no-model-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: var(--text-secondary);
  gap: 8px;
}

.placeholder-icon {
  font-size: 32px;
  opacity: 0.5;
}

.placeholder-text {
  font-size: 12px;
  font-weight: 500;
}

.image-placeholder .placeholder-icon {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 0.2; }
}

@media (max-width: 768px) {
  .selector-header {
    padding-bottom: 10px;
    margin-bottom: 10px;
  }
  
  .selector-title {
    font-size: 14px;
  }
  
  .title-icon {
    font-size: 16px;
  }
  
  .selected-info {
    font-size: 11px;
  }
  
  .model-select {
    padding: 10px 12px;
    font-size: 14px; /* 防止 iOS 缩放 */
  }
  
  .img-container {
    min-height: 120px;
    padding: 12px;
  }
  
  .placeholder-icon {
    font-size: 28px;
  }
  
  .placeholder-text {
    font-size: 11px;
  }
}
</style>
