<template>
  <div class="calculator-form card">
    <h2>计算配置</h2>

    <div class="input-group">
      <label for="calcType">计算类型</label>
      <select v-model="selectedType" id="calcType" @change="updateFormFields">
        <option value="">-- 选择计算类型 --</option>
        <option value="microstrip">微带线 (Microstrip)</option>
        <option value="stripline">带状线 (Stripline)</option>
        <option value="differential">差分对 (Differential)</option>
        <option value="coaxial">同轴线 (Coaxial)</option>
        <option value="gssg">GSSG 差分对</option>
        <option value="embedded_microstrip">嵌入式微带线</option>
        <option value="offset_stripline">偏移带状线</option>
        <option value="gcpw">接地共面波导 (GCPW)</option>
        <option value="cpwg">CPWG 结构</option>
        <option value="broadside_coupled">宽边耦合带状线</option>
      </select>
    </div>

    <div v-if="selectedType" class="input-group">
      <label for="material">材料库（可选）</label>
      <select v-model="selectedMaterial" id="material" @change="applyMaterial">
        <option value="">-- 选择材料 --</option>
        <option v-for="(material, key) in materials" :key="key" :value="key">
          {{ material.name }}
        </option>
      </select>
    </div>

    <div class="form-fields">
      <div v-for="(field, index) in formFields" :key="index" class="input-group">
        <label :for="`field-${index}`">{{ field.label }}</label>
        <input
          :id="`field-${index}`"
          v-model.number="formData[field.key]"
          type="number"
          :placeholder="field.placeholder"
          :step="field.step || 0.01"
          :min="field.min || 0"
        />
      </div>
    </div>

    <button
      class="btn btn-primary"
      :disabled="!isFormValid || isLoading"
      @click="submitCalculation"
    >
      <span v-if="!isLoading">计算</span>
      <span v-else>计算中...</span>
    </button>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { calculateImpedance, getMaterials as fetchMaterials } from '../api/index'

const emit = defineEmits(['calculate'])

const selectedType = ref('')
const selectedMaterial = ref('')
const isLoading = ref(false)
const error = ref('')
const materials = ref({})
const formData = reactive({})
const formFields = ref([])

const typeFields = {
  microstrip: [
    { key: 'width', label: '线宽 (mm)', placeholder: '0.2', step: 0.01 },
    { key: 'height', label: '介质厚度 (mm)', placeholder: '1.6', step: 0.01 },
    { key: 'thickness', label: '铜厚 (mm)', placeholder: '0.035', step: 0.001 },
    { key: 'dielectric', label: '介电常数', placeholder: '4.3', step: 0.01 }
  ],
  stripline: [
    { key: 'width', label: '线宽 (mm)', placeholder: '0.2', step: 0.01 },
    { key: 'height', label: '介质总厚度 (mm)', placeholder: '1.6', step: 0.01 },
    { key: 'thickness', label: '铜厚 (mm)', placeholder: '0.035', step: 0.001 },
    { key: 'dielectric', label: '介电常数', placeholder: '4.3', step: 0.01 }
  ],
  differential: [
    { key: 'width', label: '线宽 (mm)', placeholder: '0.2', step: 0.01 },
    { key: 'spacing', label: '线间距 (mm)', placeholder: '0.2', step: 0.01 },
    { key: 'height', label: '介质厚度 (mm)', placeholder: '1.6', step: 0.01 },
    { key: 'thickness', label: '铜厚 (mm)', placeholder: '0.035', step: 0.001 },
    { key: 'dielectric', label: '介电常数', placeholder: '4.3', step: 0.01 }
  ],
  coaxial: [
    { key: 'inner_diameter', label: '内导体直径 (mm)', placeholder: '0.5', step: 0.01 },
    { key: 'outer_diameter', label: '外导体内径 (mm)', placeholder: '2.0', step: 0.01 },
    { key: 'dielectric', label: '介电常数', placeholder: '1.0', step: 0.01 }
  ],
  gssg: [
    { key: 'width', label: '信号线宽 (mm)', placeholder: '0.2', step: 0.01 },
    { key: 'spacing', label: '信号线间距 (mm)', placeholder: '0.2', step: 0.01 },
    { key: 'ground_spacing', label: '信号到地距离 (mm)', placeholder: '0.5', step: 0.01 },
    { key: 'height', label: '介质厚度 (mm)', placeholder: '1.6', step: 0.01 },
    { key: 'thickness', label: '铜厚 (mm)', placeholder: '0.035', step: 0.001 },
    { key: 'dielectric', label: '介电常数', placeholder: '4.3', step: 0.01 }
  ],
  embedded_microstrip: [
    { key: 'width', label: '线宽 (mm)', placeholder: '0.2', step: 0.01 },
    { key: 'upper_height', label: '上层介质厚度 (mm)', placeholder: '0.5', step: 0.01 },
    { key: 'lower_height', label: '下层介质厚度 (mm)', placeholder: '1.1', step: 0.01 },
    { key: 'thickness', label: '铜厚 (mm)', placeholder: '0.035', step: 0.001 },
    { key: 'upper_dielectric', label: '上层介电常数', placeholder: '4.3', step: 0.01 },
    { key: 'lower_dielectric', label: '下层介电常数', placeholder: '4.3', step: 0.01 }
  ],
  offset_stripline: [
    { key: 'width', label: '线宽 (mm)', placeholder: '0.2', step: 0.01 },
    { key: 'total_height', label: '总介质厚度 (mm)', placeholder: '1.6', step: 0.01 },
    { key: 'bottom_distance', label: '到下层接地距离 (mm)', placeholder: '0.8', step: 0.01 },
    { key: 'thickness', label: '铜厚 (mm)', placeholder: '0.035', step: 0.001 },
    { key: 'dielectric', label: '介电常数', placeholder: '4.3', step: 0.01 }
  ],
  gcpw: [
    { key: 'width', label: '信号线宽 (mm)', placeholder: '0.2', step: 0.01 },
    { key: 'gap', label: '到地线间距 (mm)', placeholder: '0.2', step: 0.01 },
    { key: 'height', label: '介质厚度 (mm)', placeholder: '1.6', step: 0.01 },
    { key: 'thickness', label: '铜厚 (mm)', placeholder: '0.035', step: 0.001 },
    { key: 'dielectric', label: '介电常数', placeholder: '4.3', step: 0.01 }
  ],
  cpwg: [
    { key: 'width', label: '信号线宽 (mm)', placeholder: '0.2', step: 0.01 },
    { key: 'gap', label: '线间间距 (mm)', placeholder: '0.2', step: 0.01 },
    { key: 'height', label: '介质厚度 (mm)', placeholder: '1.6', step: 0.01 },
    { key: 'thickness', label: '铜厚 (mm)', placeholder: '0.035', step: 0.001 },
    { key: 'dielectric', label: '介电常数', placeholder: '4.3', step: 0.01 }
  ],
  broadside_coupled: [
    { key: 'width', label: '线宽 (mm)', placeholder: '0.2', step: 0.01 },
    { key: 'height', label: '介质厚度 (mm)', placeholder: '1.6', step: 0.01 },
    { key: 'vertical_spacing', label: '垂直间距 (mm)', placeholder: '0.2', step: 0.01 },
    { key: 'thickness', label: '铜厚 (mm)', placeholder: '0.035', step: 0.001 },
    { key: 'dielectric', label: '介电常数', placeholder: '4.3', step: 0.01 }
  ]
}

const isFormValid = computed(() => {
  if (!selectedType.value) return false
  const fields = typeFields[selectedType.value]
  return fields.every(field => formData[field.key] !== undefined && formData[field.key] !== '')
})

const updateFormFields = () => {
  formFields.value = typeFields[selectedType.value] || []
  formData.width = undefined
  formData.height = undefined
  formData.thickness = undefined
  formData.dielectric = undefined
  selectedMaterial.value = ''
  error.value = ''
}

const applyMaterial = () => {
  if (selectedMaterial.value && materials.value[selectedMaterial.value]) {
    const material = materials.value[selectedMaterial.value]
    formData.dielectric = material.er
  }
}

const submitCalculation = async () => {
  error.value = ''
  isLoading.value = true

  try {
    const response = await calculateImpedance(selectedType.value, formData)
    emit('calculate', response.data)
  } catch (err) {
    error.value = err.response?.data?.message || '计算失败，请检查参数'
    console.error('Calculation error:', err)
  } finally {
    isLoading.value = false
  }
}

onMounted(async () => {
  try {
    const response = await fetchMaterials()
    materials.value = response.data
  } catch (err) {
    console.error('Failed to load materials:', err)
  }
})
</script>

<style scoped>
.calculator-form {
  position: sticky;
  top: 20px;
}

.calculator-form h2 {
  margin-bottom: 20px;
  color: #333;
  font-size: 1.5em;
  border-bottom: 2px solid #667eea;
  padding-bottom: 10px;
}

.form-fields {
  margin-bottom: 20px;
}

.input-group {
  margin-bottom: 15px;
}

.input-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #333;
}

.input-group input,
.input-group select {
  width: 100%;
  padding: 10px 12px;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 14px;
  transition: all 0.3s ease;
}

.input-group input:focus,
.input-group select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.btn {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-primary {
  background-color: #667eea;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #5568d3;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.btn-primary:disabled {
  background-color: #ccc;
  cursor: not-allowed;
  opacity: 0.6;
}

.error-message {
  background-color: #fee2e2;
  border: 1px solid #fecaca;
  color: #dc2626;
  padding: 12px 15px;
  border-radius: 8px;
  margin-top: 15px;
}
</style>
