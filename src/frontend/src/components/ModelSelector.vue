<template>
  <div class="model-selector">
    <div class="selector-header">
      <h2 class="selector-title">
        <span class="title-icon">🤖</span>
        选择模型
      </h2>
      <div v-if="selectedModel" class="selected-info">
        当前选择: <span class="selected-model">{{ modelTypes[selectedModel]?.name || selectedModel }}</span>
      </div>
    </div>
    
    <div class="select-container">
      <select v-model="selectedModel" class="model-select">
        <option disabled value="">请选择一个模型</option>
        <option v-for="(item, key) in modelTypes" :key="key" :value="key">
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
        <!-- 图片加载失败时显示默认图片 -->
        <img 
          v-else-if="selectedModel && imageError" 
          src="/GSG.png" 
          :alt="`${modelTypes[selectedModel]?.name || selectedModel} 模型示意图（默认）`"
          class="model-image fallback-image"
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
  height: 100%;
  min-height: 0;
  font-size: 11px;
}

.selector-header {
  flex-shrink: 0;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 6px;
  margin-bottom: 8px;
}

.selector-title {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 4px 0;
}

.title-icon {
  font-size: 14px;
}

.selected-info {
  font-size: 10px;
  color: #6b7280;
}

.selected-model {
  font-weight: 600;
  color: #165DFF;
}

.select-container {
  flex-shrink: 0;
  margin-bottom: 8px;
}

.model-select {
  width: 100%;
  padding: 6px 8px;
  border: 1px solid #e5e7eb;
  border-radius: 3px;
  font-size: 11px;
  background: white;
  color: #374151;
  transition: all 0.2s ease;
  cursor: pointer;
}

.model-select:focus {
  outline: none;
  border-color: #165DFF;
  box-shadow: 0 0 0 2px rgba(22, 93, 255, 0.1);
}

.model-select:hover {
  border-color: #9ca3af;
}

.model-preview {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.preview-header {
  flex-shrink: 0;
  margin-bottom: 6px;
}

.preview-header h4 {
  font-size: 11px;
  font-weight: 600;
  color: #374151;
  margin: 0;
}

.img-container {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8fafc;
  border: 1px dashed #d1d5db;
  border-radius: 3px;
  padding: 6px;
  min-height: 80px;
  overflow: hidden;
  position: relative;
}

.img-container img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  border-radius: 2px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: opacity 0.3s ease;
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
  color: #9ca3af;
  gap: 6px;
}

.placeholder-icon {
  font-size: 24px;
  opacity: 0.6;
}

.placeholder-text {
  font-size: 10px;
  font-weight: 500;
  line-height: 1.2;
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
  color: #6b7280;
}

.no-model-placeholder .placeholder-icon {
  font-size: 20px;
}

/* 图片加载失败时的样式 */
.img-container img[src=""]:after {
  content: "图片加载失败";
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  background: #f3f4f6;
  color: #9ca3af;
  font-size: 10px;
  border-radius: 2px;
}

@media (max-width: 992px) {
  .model-preview {
    min-height: 60px;
  }
  
  .img-container {
    min-height: 60px;
    padding: 4px;
  }
  
  .placeholder-icon {
    font-size: 20px;
  }
  
  .placeholder-text {
    font-size: 9px;
  }
}
</style>