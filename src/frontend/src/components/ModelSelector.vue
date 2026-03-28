<template>
  <div class="model-selector">
    <div class="selector-header">
      <h2>🤖 选择模型</h2>
      <div v-if="selectedModel" class="selected-info">
        当前: <span class="model-name">{{ getSelectedModelName(selectedModel) }}</span>
      </div>
    </div>
    
    <select v-model="selectedModel" class="model-select">
      <option disabled value="">请选择一个模型</option>
      <option v-for="item in modelTypes" :key="item.type" :value="item.type">
        {{ item.name }}
      </option>
    </select>
    
    <div class="model-preview">
      <div class="preview-header">模型示意图</div>
      <div class="img-container">
        <img 
          v-if="selectedModel && modelImageSrc && !imageError" 
          :src="modelImageSrc" 
          :alt="getSelectedModelName(selectedModel)"
          @error="handleImageError"
        />
        <div v-else-if="selectedModel" class="loading-placeholder">
          <span>📐</span>
          <p>加载中...</p>
        </div>
        <div v-else class="empty-placeholder">
          <span>🔍</span>
          <p>请选择模型查看示意图</p>
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
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 14px;
  gap: 12px;
  overflow: hidden;
}

.selector-header {
  flex-shrink: 0;
}

.selector-header h2 {
  font-size: 15px;
  font-weight: 600;
  color: #1d1d1f;
  margin-bottom: 4px;
}

.selected-info {
  font-size: 11px;
  color: #86868b;
}

.model-name {
  color: #0066cc;
  font-weight: 600;
}

.model-select {
  flex-shrink: 0;
  padding: 10px 12px;
  border: 1px solid #e2e2e7;
  border-radius: 8px;
  font-size: 13px;
  background: #ffffff;
  cursor: pointer;
}

.model-select:focus {
  border-color: #0066cc;
  outline: none;
  box-shadow: 0 0 0 2px rgba(0, 102, 204, 0.1);
}

/* 预览区域 */
.model-preview {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow: hidden;
}

.preview-header {
  flex-shrink: 0;
  font-size: 11px;
  font-weight: 600;
  color: #86868b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 8px;
}

.img-container {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f7;
  border: 2px dashed #e2e2e7;
  border-radius: 10px;
  padding: 12px;
  min-height: 0;
  overflow: hidden;
}

.img-container img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  border-radius: 6px;
}

.loading-placeholder,
.empty-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: #86868b;
  font-size: 12px;
}

.loading-placeholder span,
.empty-placeholder span {
  font-size: 28px;
  opacity: 0.5;
}
</style>
