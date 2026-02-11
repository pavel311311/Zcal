<template>
  <div class="material-selector">
    <div class="selector-header">
      <h3 class="selector-title">
        <span class="title-icon">🐻</span>
        材料
      </h3>
    </div>
    
    <div class="select-container">
      <div class="select-row">
        <label for="material-select" class="material-label">参考材料:</label>
        <div class="select-wrapper">
          <select v-model="selectedMaterial" id="material-select" class="material-select">
            <option value="">-- 请选择 --</option>
            <option v-for="(material, key) in materials" :key="key" :value="key">
              {{ material.name }}
            </option>
          </select>
        </div>
      </div>
      
      <div v-if="selectedMaterial && materials[selectedMaterial]" class="material-info">
        <div class="material-details">
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
  background: #f5f5f7;
  border-radius: 6px;
  border: 1px solid #e3e3e3;
  flex-shrink: 0;
  font-size: 11px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  /* 确保在不同显示比例下都能正确显示 */
  max-width: 100%;
  overflow-x: hidden;
  box-sizing: border-box;
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
  color: #1d1d1f;
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

.select-row {
  display: flex;
  align-items: center;
  gap: 6px;
}

.material-label {
  font-size: 10px;
  font-weight: 500;
  color: #1d1d1f;
  white-space: nowrap;
}

.select-wrapper {
  flex: 1;
  position: relative;
}

.material-select {
  width: 100%;
  padding: 6px 8px;
  border: 1px solid #e3e3e3;
  border-radius: 4px;
  font-size: 11px;
  background: #ffffff;
  color: #1d1d1f;
  transition: all 0.2s ease;
  cursor: pointer;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

.material-select:focus {
  outline: none;
  border-color: #0066cc;
  box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
}

.material-select:hover {
  border-color: #d1d1d6;
  background-color: #f5f5f7;
}

.material-info {
  padding: 6px 8px;
  background: #ffffff;
  border: 1px solid #e3e3e3;
  border-radius: 4px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  transition: all 0.2s ease;
}

.material-info:hover {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
}

.material-details {
  display: flex;
  align-items: center;
}

.material-params {
  display: flex;
  gap: 10px;
  width: 100%;
}

.param-item {
  display: flex;
  align-items: center;
  gap: 3px;
  flex: 1;
}

.param-label {
  font-size: 10px;
  color: #86868b;
  font-weight: 500;
  white-space: nowrap;
}

.param-value {
  font-size: 10px;
  color: #1d1d1f;
  font-weight: 600;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  flex: 1;
}

@media (max-width: 768px) {
  .material-selector {
    padding: 6px;
    font-size: 10px;
    max-width: 100%;
    overflow-x: hidden;
  }
  
  .selector-header {
    margin-bottom: 4px;
    max-width: 100%;
  }
  
  .selector-title {
    font-size: 11px;
    gap: 3px;
    max-width: 100%;
  }
  
  .title-icon {
    font-size: 12px;
  }
  
  .select-container {
    max-width: 100%;
  }
  
  .select-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
    max-width: 100%;
  }
  
  .material-label {
    font-size: 9px;
    max-width: 100%;
    overflow-x: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  .select-wrapper {
    max-width: 100%;
  }
  
  .material-select {
    padding: 6px 8px;
    font-size: 10px;
    min-height: 32px;
    max-width: 100%;
  }
  
  .material-info {
    padding: 6px 8px;
    max-width: 100%;
  }
  
  .material-details {
    max-width: 100%;
  }
  
  .material-params {
    flex-direction: column;
    gap: 3px;
    max-width: 100%;
  }
  
  .param-item {
    gap: 2px;
    max-width: 100%;
  }
  
  .param-label {
    font-size: 9px;
    max-width: 100%;
    overflow-x: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  .param-value {
    font-size: 9px;
    max-width: 100%;
    overflow-x: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  /* 确保所有元素都不会超出容器 */
  * {
    max-width: 100%;
    box-sizing: border-box;
  }
}
</style>