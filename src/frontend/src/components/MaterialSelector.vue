<template>
  <div class="material-selector">
    <div class="selector-header">
      <span class="title-icon">🐻</span>
      <span class="title-text">参考材料</span>
    </div>
    
    <select v-model="selectedMaterial" class="material-select">
      <option value="">-- 请选择材料 --</option>
      <option v-for="(material, key) in materials" :key="key" :value="key">
        {{ material.name }}
      </option>
    </select>
    
    <div v-if="selectedMaterial && materials[selectedMaterial]" class="material-info">
      <div class="param">
        <span class="param-label">εr</span>
        <span class="param-value">{{ materials[selectedMaterial].er }}</span>
      </div>
      <div class="param">
        <span class="param-label">tanδ</span>
        <span class="param-value">{{ materials[selectedMaterial].loss_tangent }}</span>
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
  flex-shrink: 0;
  padding: 10px;
  background: #f5f5f7;
  border-radius: 8px;
  border: 1px solid #e2e2e7;
}

.selector-header {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 8px;
}

.title-icon {
  font-size: 14px;
}

.title-text {
  font-size: 12px;
  font-weight: 600;
  color: #1d1d1f;
}

.material-select {
  width: 100%;
  padding: 8px 10px;
  border: 1px solid #e2e2e7;
  border-radius: 6px;
  font-size: 12px;
  background: #ffffff;
  cursor: pointer;
}

.material-select:focus {
  border-color: #0066cc;
  outline: none;
}

.material-info {
  display: flex;
  gap: 16px;
  margin-top: 8px;
  padding: 8px 10px;
  background: #ffffff;
  border-radius: 6px;
  border: 1px solid #e2e2e7;
}

.param {
  display: flex;
  align-items: center;
  gap: 6px;
}

.param-label {
  font-size: 11px;
  color: #86868b;
}

.param-value {
  font-size: 13px;
  font-weight: 600;
  font-family: 'Monaco', 'Menlo', monospace;
  color: #1d1d1f;
}
</style>
