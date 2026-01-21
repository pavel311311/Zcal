<template>
  <div class="material-selector">
    <div class="selector-header">
      <h3 class="selector-title">
        <span class="title-icon">🐻</span>
        材料特性
      </h3>
    </div>
    
    <div class="select-container">
      <label for="material-select" class="material-label">参考材料:</label>
      <div class="select-wrapper">
        <select v-model="selectedMaterial" id="material-select" class="material-select">
          <option value="">-- 请选择材料 --</option>
          <option v-for="(material, key) in materials" :key="key" :value="key">
            {{ material.name }}
          </option>
        </select>
      </div>
      
      <div v-if="selectedMaterial && materials[selectedMaterial]" class="material-info">
        <div class="material-details">
          <span class="material-name">{{ materials[selectedMaterial].name }}</span>
          <div class="material-params">
            <span class="param-item">
              <span class="param-label">εr:</span>
              <span class="param-value">{{ materials[selectedMaterial].er }}</span>
            </span>
            <span class="param-item">
              <span class="param-label">tanδ:</span>
              <span class="param-value">{{ materials[selectedMaterial].loss_tangent }}</span>
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useCalculationStore } from '../stores/calculatorStore'

const store = useCalculationStore()

// 从store获取材料数据和选中的材料
const materials = computed(() => store.materials)
const selectedMaterial = computed({
  get: () => store.selectedMaterial,
  set: (value) => store.selectMaterial(value)
})

// 初始化加载材料数据
onMounted(async () => {
  try {
    await store.loadMaterials()
  } catch (error) {
    console.error('加载材料数据失败:', error)
  }
})
</script>

<style scoped>
.material-selector {
  padding: 8px;
  background: #f8fafc;
  border-radius: 4px;
  border: 1px solid #e5e7eb;
  flex-shrink: 0;
  font-size: 11px;
}

.selector-header {
  margin-bottom: 6px;
}

.selector-title {
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

.select-container {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.material-label {
  font-size: 10px;
  font-weight: 500;
  color: #374151;
}

.select-wrapper {
  position: relative;
}

.material-select {
  width: 100%;
  padding: 6px 8px;
  border: 1px solid #d1d5db;
  border-radius: 3px;
  font-size: 11px;
  background: white;
  color: #374151;
  transition: all 0.2s ease;
  cursor: pointer;
}

.material-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
}

.material-select:hover {
  border-color: #9ca3af;
}

.material-info {
  padding: 6px;
  background: white;
  border: 1px solid #d1d5db;
  border-radius: 3px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.material-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.material-name {
  font-weight: 600;
  color: #1f2937;
  font-size: 11px;
}

.material-params {
  display: flex;
  gap: 8px;
}

.param-item {
  display: flex;
  align-items: center;
  gap: 2px;
}

.param-label {
  font-size: 10px;
  color: #6b7280;
  font-weight: 500;
}

.param-value {
  font-size: 10px;
  color: #1f2937;
  font-weight: 600;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
}

@media (max-width: 768px) {
  .material-params {
    flex-direction: column;
    gap: 3px;
  }
  
  .material-selector {
    padding: 6px;
  }
}
</style>