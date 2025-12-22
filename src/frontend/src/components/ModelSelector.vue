<template>
  <div class="model-selector">
    <h3>🤖选择模型</h3>
    <div class="selected-info">Selected: {{ selectedModel }}</div>
    <select v-model="selectedModel" class="model-select">
      <option disabled value="">请选择一个模型</option>
      <option v-for="item in modelTypes" :key="item.label" :value="item.label">
        {{ item.name }}
      </option>
    </select>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useCalculationStore } from '../stores/calculatorStore'
const selectedModel = ref()
const modelTypes = ref()

const store = useCalculationStore()

onMounted(async () => {
  store.init();
  modelTypes.value = await store.loadModelTypes()
})
</script>
