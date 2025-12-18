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
        <div class="select-arrow">▼</div>
      </div>
    </div>
    
    <div v-if="loading" class="loading-indicator">
      <span>加载材料参数中...</span>
    </div>
    
    <div v-else-if="selectedMaterial" class="material-info">
      <div class="material-header">
        <h4>{{ materials[selectedMaterial].name }}</h4>
        <div class="material-type-badge" v-if="materials[selectedMaterial].type">
          {{ materials[selectedMaterial].type }}
        </div>
      </div>
      <div class="material-params">
        <div class="param-item">
          <span class="param-label">介电常数:</span>
          <span class="param-value">{{ materials[selectedMaterial].epsilon_r }}</span>
        </div>
        <div class="param-item">
          <span class="param-label">损耗角正切:</span>
          <span class="param-value">{{ materials[selectedMaterial].tan_delta }}</span>
        </div>
        <div class="param-item">
          <span class="param-label">厚度:</span>
          <span class="param-value">{{ materials[selectedMaterial].thickness }} mm</span>
        </div>
        <!-- 显示更多可能的材料参数 -->
        <div class="param-item" v-if="materials[selectedMaterial].conductivity">
          <span class="param-label">电导率:</span>
          <span class="param-value">{{ materials[selectedMaterial].conductivity }} S/m</span>
        </div>
        <div class="param-item" v-if="materials[selectedMaterial].permeability">
          <span class="param-label">磁导率:</span>
          <span class="param-value">{{ materials[selectedMaterial].permeability }}</span>
        </div>
      </div>
    </div>
    
    <div v-else class="empty-state">
      <p>请选择一种材料查看其特性参数</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useCalculationStore } from '../stores/calculationStore'

const emit = defineEmits(['material-selected']) 

const calculationStore = useCalculationStore()
const materials = ref({})
const selectedMaterial = ref('')
const loading = ref(false)
const error = ref('')
const calculator = calculationStore.calculator

// 加载材料数据
const loadMaterials = async () => {
  loading.value = true
  error.value = ''
  try {
    materials.value = await calculator.loadMaterials()
  } catch (err) {
    console.error('加载材料数据失败:', err)
    error.value = '加载材料数据失败，请稍后重试'
    materials.value = {}
  } finally {
    loading.value = false
  }
}

// 监听材料选择变化
watch(selectedMaterial, (newMaterial) => {
  if (newMaterial && materials.value[newMaterial]) {
    // 当选择材料时，更新模型表单中的相关参数
    updateModelFormWithMaterial(materials.value[newMaterial])
    // 通知父组件材料已选择
    emit('material-selected', {
      materialKey: newMaterial,
      materialData: materials.value[newMaterial]
    })
  }
})

// 当选择材料时，通知父组件但不直接修改表单
// 表单修改逻辑应该在父组件中处理

// 初始化加载材料数据
onMounted(() => {
  loadMaterials()
})
</script>

