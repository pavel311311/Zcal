<template>
  <div class="model-selector">
    <div class="selector-header">
      <h3 class="selector-title">
        <span class="title-icon">🤖</span>
        选择模型
      </h3>
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
        <img src="/GSG.png" alt="传输线模型示意图" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useCalculationStore } from '../stores/calculatorStore'

const store = useCalculationStore()

// 从store获取模型类型和选中的模型
const modelTypes = computed(() => store.modelTypes)
const selectedModel = computed({
  get: () => store.selectedModel,
  set: (value) => store.selectModel(value)
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
  gap: 20px;
  height: 100%;
}

.selector-header {
  border-bottom: 2px solid #e5e7eb;
  padding-bottom: 16px;
}

.selector-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 12px 0;
}

.title-icon {
  font-size: 20px;
}

.selected-info {
  font-size: 14px;
  color: #6b7280;
}

.selected-model {
  font-weight: 600;
  color: #3b82f6;
}

.select-container {
  margin-bottom: 8px;
}

.model-select {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  background: white;
  color: #374151;
  transition: all 0.2s ease;
  cursor: pointer;
}

.model-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.model-select:hover {
  border-color: #9ca3af;
}

.model-preview {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 200px;
}

.preview-header {
  margin-bottom: 12px;
}

.preview-header h4 {
  font-size: 16px;
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
  border: 2px dashed #d1d5db;
  border-radius: 8px;
  padding: 20px;
  min-height: 200px;
}

.img-container img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

@media (max-width: 992px) {
  .model-preview {
    min-height: 150px;
  }
  
  .img-container {
    min-height: 150px;
    padding: 16px;
  }
}
</style>