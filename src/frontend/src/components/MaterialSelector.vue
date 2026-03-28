<template>
  <div class="material-selector">
    <div class="header">
      <span class="icon">🐻</span>
      <span class="title">参考材料</span>
    </div>
    
    <select v-model="selectedMaterial" class="material-select">
      <option value="">选择基板材料...</option>
      <option v-for="(material, key) in materials" :key="key" :value="key">
        {{ material.name }}
      </option>
    </select>
    
    <div v-if="selectedMaterial && materials[selectedMaterial]" class="material-info">
      <div class="param">
        <span class="label">εr</span>
        <span class="value">{{ materials[selectedMaterial].er }}</span>
      </div>
      <div class="divider"></div>
      <div class="param">
        <span class="label">tanδ</span>
        <span class="value">{{ materials[selectedMaterial].loss_tangent }}</span>
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
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  border-bottom: 1px solid rgba(255,255,255,0.06);
}

.header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header .icon {
  font-size: 14px;
}

.header .title {
  font-size: 13px;
  font-weight: 600;
  color: rgba(255,255,255,0.6);
}

.material-select {
  width: 100%;
  padding: 12px 14px;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 10px;
  color: #fff;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.3s;
}

.material-select:hover {
  border-color: rgba(59, 130, 246, 0.5);
  background: rgba(59, 130, 246, 0.1);
}

.material-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}

.material-select option {
  background: #1a1a2e;
  color: #fff;
}

.material-info {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 14px;
  background: rgba(59, 130, 246, 0.1);
  border: 1px solid rgba(59, 130, 246, 0.2);
  border-radius: 10px;
}

.param {
  display: flex;
  align-items: center;
  gap: 8px;
}

.param .label {
  font-size: 12px;
  color: rgba(255,255,255,0.5);
}

.param .value {
  font-size: 15px;
  font-weight: 700;
  font-family: 'SF Mono', Monaco, monospace;
  color: #60a5fa;
}

.divider {
  width: 1px;
  height: 20px;
  background: rgba(255,255,255,0.1);
}
</style>
