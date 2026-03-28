<template>
  <div class="material-selector">
    <div class="selector-header">
      <h3 class="selector-title">
        <span class="title-icon">🐻</span>
        参考材料
      </h3>
    </div>
    
    <div class="select-container">
      <select v-model="selectedMaterial" class="material-select">
        <option value="">-- 请选择材料 --</option>
        <option v-for="(material, key) in materials" :key="key" :value="key">
          {{ material.name }}
        </option>
      </select>
      
      <div v-if="selectedMaterial && materials[selectedMaterial]" class="material-info">
        <div class="material-params">
          <div class="param-item">
            <span class="param-label">εr</span>
            <span class="param-value">{{ materials[selectedMaterial].er }}</span>
          </div>
          <div class="param-item">
            <span class="param-label">tanδ</span>
            <span class="param-value">{{ materials[selectedMaterial].loss_tangent }}</span>
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

const materials = computed(() => store.materials)
const selectedMaterial = computed({
  get: () => store.selectedMaterial,
  set: (value) => store.selectMaterial(value)
})

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
  padding: 12px;
  background: var(--bg-main);
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-color);
  flex-shrink: 0;
}

.selector-header {
  margin-bottom: 10px;
}

.selector-title {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.title-icon {
  font-size: 14px;
}

.select-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.material-select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  font-size: 13px;
  background: var(--bg-card);
  color: var(--text-primary);
  cursor: pointer;
  transition: var(--transition-fast);
}

.material-select:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
}

.material-select:hover:not(:focus) {
  border-color: #c0c0c5;
  background-color: #fafafa;
}

.material-info {
  padding: 10px 12px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  box-shadow: var(--shadow-sm);
}

.material-params {
  display: flex;
  gap: 16px;
}

.param-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.param-label {
  font-size: 11px;
  color: var(--text-secondary);
  font-weight: 500;
}

.param-value {
  font-size: 13px;
  color: var(--text-primary);
  font-weight: 600;
  font-family: var(--font-mono);
}

@media (max-width: 768px) {
  .material-selector {
    padding: 10px;
  }
  
  .selector-title {
    font-size: 12px;
  }
  
  .title-icon {
    font-size: 13px;
  }
  
  .material-select {
    padding: 10px;
    font-size: 14px; /* 防止 iOS 缩放 */
  }
  
  .material-info {
    padding: 8px 10px;
  }
  
  .material-params {
    gap: 12px;
  }
  
  .param-label {
    font-size: 10px;
  }
  
  .param-value {
    font-size: 12px;
  }
}
</style>
