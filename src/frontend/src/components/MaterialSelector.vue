<template>
  <div class="material-selector">
    <h3>🐻材料特性</h3>
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
  set: (value) => store.setSelectedMaterial(value)
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

