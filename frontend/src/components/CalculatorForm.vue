<template>
  <div class="calculator-form card">
    <h2>计算配置</h2>

    <div class="input-group">
      <label for="calcType">计算类型</label>
      <select v-model="selectedType" id="calcType" @change="updateFormFields">
        <option value="">-- 选择计算类型 --</option>
        <option v-for="(type, key) in calculationTypes" :key="key" :value="key">
          {{ type.name }}
        </option>
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
import { calculateImpedance, getMaterials as fetchMaterials, getFormFields, getCalculationTypes } from '../api/index'

const emit = defineEmits(['calculate'])

const selectedType = ref('')
const selectedMaterial = ref('')
const isLoading = ref(false)
const error = ref('')
const materials = ref({})
const calculationTypes = ref({})
const formData = reactive({})
const formFields = ref([])

// formDefinitions will be fetched from the backend; keep no local hardcoded map
const formDefinitions = ref({})

const isFormValid = computed(() => {
  if (!selectedType.value) return false
  const fields = formFields.value
  if (!fields || fields.length === 0) return false
  return fields.every(field => formData[field.key] !== undefined && formData[field.key] !== '')
})

const updateFormFields = () => {
  const defs = formDefinitions.value[selectedType.value] || []
  formFields.value = defs

  // reset formData values for the new fields
  Object.keys(formData).forEach(k => delete formData[k])
  defs.forEach(f => {
    formData[f.key] = undefined
  })

  selectedMaterial.value = ''
  error.value = ''
}

const applyMaterial = () => {
  if (selectedMaterial.value && materials.value[selectedMaterial.value]) {
    const material = materials.value[selectedMaterial.value]
    // try to set a dielectric field if exists
    // find dielectric-like keys in current formFields
    const dField = formFields.value.find(f => /dielectric|er/i.test(f.key))
    if (dField) formData[dField.key] = material.er
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
    const [matResp, formResp, typesResp] = await Promise.all([
      fetchMaterials(),
      getFormFields(),
      getCalculationTypes()
    ])
    materials.value = matResp.data
    formDefinitions.value = formResp.data || {}
    calculationTypes.value = typesResp.data || {}
  } catch (err) {
    console.error('Failed to load materials, form definitions or calculation types:', err)
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
