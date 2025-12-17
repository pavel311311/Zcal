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
import { Calculator } from '../services/calculator'
import { useCalculationStore } from '../stores/calculationStore'

const props = defineProps({
  modelForm: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:modelForm', 'material-selected'])

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

// 使用材料参数更新模型表单
const updateModelFormWithMaterial = (material) => {
  if (!Array.isArray(props.modelForm)) return
  
  // 查找需要更新的字段并设置值
  const updatedForm = [...props.modelForm]
  updatedForm.forEach(field => {
    if (field.key === 'epsilon_r' && material.epsilon_r !== undefined) {
      field.value = material.epsilon_r
    } else if (field.key === 'tan_delta' && material.tan_delta !== undefined) {
      field.value = material.tan_delta
    } else if (field.key === 'h' && material.thickness !== undefined) {
      field.value = material.thickness
    }
  })
  
  emit('update:modelForm', updatedForm)
}

// 初始化加载材料数据
onMounted(() => {
  loadMaterials()
})
</script>

<style scoped>
.material-selector {
  margin-bottom: 20px;
}

.select-container {
  margin-bottom: 12px;
}

.material-label {
  display: block;
  margin-bottom: 6px;
  font-weight: bold;
  color: #333;
}

.select-wrapper {
  position: relative;
  width: 100%;
}

.material-select {
  width: 100%;
  padding: 10px 40px 10px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 16px;
  background-color: white;
  cursor: pointer;
  appearance: none;
  transition: all 0.3s ease;
}

.material-select:focus {
  outline: none;
  border-color: #4a90e2;
  box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.1);
}

.material-select:hover {
  border-color: #999;
}

.select-arrow {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #666;
  pointer-events: none;
  font-size: 12px;
}

.loading-indicator {
  margin-top: 15px;
  padding: 12px;
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 6px;
  text-align: center;
  color: #6c757d;
  font-size: 14px;
}

.error-message {
  margin-top: 10px;
  padding: 10px;
  background-color: #fff5f5;
  border: 1px solid #ffd5d5;
  border-radius: 6px;
  color: #e74c3c;
  font-size: 14px;
}

.material-info {
  margin-top: 15px;
  padding: 20px;
  background-color: #f0f7ff;
  border: 1px solid #d0e4ff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.material-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #d0e4ff;
}

.material-header h4 {
  margin: 0;
  color: #2c3e50;
  font-size: 18px;
}

.material-type-badge {
  padding: 4px 12px;
  background-color: #4a90e2;
  color: white;
  border-radius: 12px;
  font-size: 12px;
  font-weight: bold;
  text-transform: uppercase;
}

.material-params {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.param-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 12px;
  background-color: white;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.param-label {
  color: #555;
  font-weight: 500;
}

.param-value {
  color: #2c3e50;
  font-weight: bold;
  font-size: 16px;
}

.empty-state {
  margin-top: 15px;
  padding: 20px;
  background-color: #f8f9fa;
  border: 1px dashed #dee2e6;
  border-radius: 8px;
  text-align: center;
  color: #6c757d;
  font-size: 14px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .material-params {
    grid-template-columns: 1fr;
  }
  
  .material-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
}
</style>