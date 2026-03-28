<template>
  <div class="model-selector">
    <select v-model="selectedModel" class="model-select">
      <option disabled value="">选择传输线模型...</option>
      <option v-for="item in modelTypes" :key="item.type" :value="item.type">
        {{ item.name }}
      </option>
    </select>
    
    <div class="preview-area">
      <div class="preview-header">模型示意图</div>
      <div class="preview-container">
        <img 
          v-if="selectedModel && modelImageSrc && !imageError" 
          :src="modelImageSrc" 
          :alt="getSelectedModelName(selectedModel)"
          @error="handleImageError"
        />
        <div v-else-if="selectedModel" class="loading">
          <div class="loading-icon">📐</div>
          <span>加载中...</span>
        </div>
        <div v-else class="empty">
          <div class="empty-icon">🔍</div>
          <span>选择模型查看示意图</span>
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

const handleImageError = () => {
  imageError.value = true
}

watch(selectedModel, () => {
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
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 16px;
  gap: 16px;
  overflow: hidden;
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
}

.model-select:hover {
  border-color: rgba(139, 92, 246, 0.5);
  background: rgba(139, 92, 246, 0.1);
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

.loading, .empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  color: rgba(255,255,255,0.3);
}

.loading-icon, .empty-icon {
  font-size: 36px;
  opacity: 0.5;
}

.loading span, .empty span {
  font-size: 12px;
}
</style>
