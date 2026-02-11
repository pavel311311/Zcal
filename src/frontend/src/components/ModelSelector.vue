<template>
  <div class="model-selector">
    <div class="selector-header">
      <h2 class="selector-title">
          <span class="title-icon">🤖</span>
          选择模型
        </h2>
        <div v-if="selectedModel" class="selected-info">
          当前选择: <span class="selected-model">{{ getSelectedModelName(selectedModel) || selectedModel }}</span>
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
        <!-- 根据选择的模型显示对应图片 -->
        <img 
          v-if="selectedModel && modelImageSrc && !imageError" 
          :src="modelImageSrc" 
          :alt="`${modelTypes[selectedModel]?.name || selectedModel} 模型示意图`"
          @error="handleImageError"
          @load="handleImageLoad"
          class="model-image"
        />
        <!-- 加载状态 -->
        <div v-else-if="selectedModel && !imageLoaded && !imageError" class="image-placeholder">
          <div class="placeholder-icon">📐</div>
          <div class="placeholder-text">加载中...</div>
        </div>
        <!-- 未选择模型时的提示 -->
        <div v-else class="no-model-placeholder">
          <div class="placeholder-icon">🔍</div>
          <div class="placeholder-text">请选择模型查看示意图</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useCalculationStore } from '../stores/calculatorStore'

const store = useCalculationStore()

// 从store获取模型类型和选中的模型
const modelTypes = computed(() => store.modelTypes)
const selectedModel = computed({
  get: () => store.selectedModel,
  set: (value) => store.selectModel(value)
})

// 获取选中模型的名称
const getSelectedModelName = (modelType) => {
  const model = modelTypes.value.find(item => item.type === modelType)
  return model?.name
}

// 图片加载状态
const imageLoaded = ref(false)
const imageError = ref(false)

// 模型键名到图片文件名的映射
const modelImageMap = {
  microstrip: 'Microstrip.png',
  stripline: 'SymmetricStripline.png',
  differential_microstrip: 'DifferentialMicrostrip.png',
  coaxial: 'Coaxial.png',
  cpw: 'CPW.png',
  cpwg: 'CPWG.png',
  asymmetric_stripline: 'AsymmetricStripline.png',
  broadside_striplines: 'BroadsideStriplines.png',
  differential_striplines: 'DifferentialStriplines.png',
  differential_cpw: 'DifferentialCPW.png',
  differential_cpwg: 'DifferentialCPWG.png'
}

// 根据模型名称生成图片路径
const modelImageSrc = computed(() => {
  if (!selectedModel.value) return null
  
  // 根据映射获取图片文件名
  const imageName = modelImageMap[selectedModel.value] || `${selectedModel.value}.png`
  return `/models/${imageName}`
})

// 图片加载成功处理
const handleImageLoad = () => {
  imageLoaded.value = true
  imageError.value = false
}

// 图片加载失败处理
const handleImageError = () => {
  imageError.value = true
  imageLoaded.value = false
  console.warn(`模型图片加载失败: ${modelImageSrc.value}`)
}

// 监听模型变化，重置图片状态
watch(selectedModel, () => {
  imageLoaded.value = false
  imageError.value = false
})

onMounted(async () => {
  try {
    // 加载模型类型
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
  min-height: 200px;
  font-size: 12px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  /* 确保在不同显示比例下都能正确显示 */
  max-width: 100%;
  overflow-x: hidden;
  box-sizing: border-box;
}

.selector-header {
  flex-shrink: 0;
  border-bottom: 1px solid #e2e2e7;
  padding-bottom: 8px;
  margin-bottom: 12px;
}

.selector-title {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 600;
  color: #1d1d1f;
  margin: 0 0 6px 0;
}

.title-icon {
  font-size: 16px;
}

.selected-info {
  font-size: 11px;
  color: #86868b;
}

.selected-model {
  font-weight: 600;
  color: #0066cc;
}

.select-container {
  flex-shrink: 0;
  margin-bottom: 12px;
}

.model-select {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #e2e2e7;
  border-radius: 8px;
  font-size: 12px;
  background: #ffffff;
  color: #1d1d1f;
  transition: all 0.2s ease;
  cursor: pointer;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

.model-select:focus {
  outline: none;
  border-color: #0066cc;
  box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
}

.model-select:hover {
  border-color: #d2d2d7;
  background-color: #f2f2f7;
}

.model-preview {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.preview-header {
  flex-shrink: 0;
  margin-bottom: 8px;
}

.preview-header h4 {
  font-size: 12px;
  font-weight: 600;
  color: #1d1d1f;
  margin: 0;
}

.img-container {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f2f2f7;
  border: 1px dashed #d2d2d7;
  border-radius: 8px;
  padding: 16px;
  min-height: 100px;
  overflow: hidden;
  position: relative;
}

.img-container img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  transition: opacity 0.3s ease, transform 0.2s ease;
}

.img-container img:hover {
  transform: scale(1.02);
}

/* 模型图片样式 */
.model-image {
  opacity: 1;
}

/* 回退图片样式 */
.fallback-image {
  opacity: 0.7;
  filter: grayscale(20%);
}

/* 占位符样式 */
.image-placeholder,
.no-model-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: #86868b;
  gap: 8px;
}

.placeholder-icon {
  font-size: 28px;
  opacity: 0.6;
}

.placeholder-text {
  font-size: 11px;
  font-weight: 500;
  line-height: 1.3;
}

/* 加载状态 */
.image-placeholder .placeholder-icon {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 0.6;
  }
  50% {
    opacity: 0.3;
  }
}

/* 未选择模型状态 */
.no-model-placeholder {
  color: #86868b;
}

.no-model-placeholder .placeholder-icon {
  font-size: 24px;
}

/* 图片加载失败时的样式 */
.img-container img[src=""]:after {
  content: "图片加载失败";
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  background: #f2f2f7;
  color: #86868b;
  font-size: 11px;
  border-radius: 6px;
}

@media (max-width: 992px) {
  .model-preview {
    min-height: 80px;
  }
  
  .img-container {
    min-height: 80px;
    padding: 12px;
  }
  
  .placeholder-icon {
    font-size: 24px;
  }
  
  .placeholder-text {
    font-size: 10px;
  }
}

@media (max-width: 768px) {
  .model-selector {
    min-height: 180px;
    font-size: 11px;
    max-width: 100%;
    overflow-x: hidden;
  }
  
  .selector-header {
    margin-bottom: 10px;
    padding-bottom: 6px;
    max-width: 100%;
  }
  
  .selector-title {
    font-size: 12px;
    gap: 4px;
    max-width: 100%;
  }
  
  .title-icon {
    font-size: 14px;
  }
  
  .selected-info {
    font-size: 10px;
    max-width: 100%;
    overflow-x: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  .selected-model {
    max-width: 100%;
    overflow-x: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  .select-container {
    margin-bottom: 10px;
    max-width: 100%;
  }
  
  .model-select {
    padding: 8px 10px;
    font-size: 11px;
    max-width: 100%;
  }
  
  .model-preview {
    min-height: 60px;
    max-width: 100%;
  }
  
  .preview-header h4 {
    font-size: 11px;
    max-width: 100%;
  }
  
  .img-container {
    min-height: 60px;
    padding: 8px;
    max-width: 100%;
    overflow: hidden;
  }
  
  .placeholder-icon {
    font-size: 20px;
  }
  
  .placeholder-text {
    font-size: 9px;
    max-width: 100%;
    overflow-x: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  .img-container img {
    max-height: 80px;
    max-width: 100%;
    object-fit: contain;
  }
  
  /* 确保所有元素都不会超出容器 */
  * {
    max-width: 100%;
    box-sizing: border-box;
  }
}
</style>