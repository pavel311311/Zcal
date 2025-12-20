<template>
  <div class="parameter-form">
    <h3>🐼模型参数</h3>
    <div class="model-name">模型：{{ store.selectedModel }}</div>

    <div v-for="(field, index) in modelForm" :key="index" >
      <label :for="`model-field-${index}`" >
        {{ field.label }}
        <span class="required" v-if="field.required">*</span>
      </label>

      <div class="input-container">
        <input :id="`model-field-${index}`" v-model.number="field.value" type="number" :placeholder="field.placeholder"
          :step="field.step || 0.01" :min="field.min || 0" class="field-input" />
        <span class="field-unit" v-if="field.unit">{{ field.unit }}</span>
      </div>

    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { useCalculationStore } from '../stores/calculatorStore'
const modelForm = ref(null)

const store = useCalculationStore()
const calculator = store.calculator

// 从store获取modelForm
// const modelForm = computed(() => store.modelForm)
// modelForm.value = async () => {
//   console.log(store.selectedModel)
//   await calculator.loadFormFields(store.selectedModel)
// }


watch(
  () => store.selectedModel,
  (newModel) => {
    console.log(newModel);
    modelForm.value = calculator.loadFormFields(newModel)
    console.log(modelForm.value)
  })

</script>
