<template>
<p>模型表格显示</p>

<p> {{ modelForm }}</p>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useCalculationStore } from '../stores/calculation'
import { getFormFields } from '../api/index'
const store = useCalculationStore()
mm = 'microstrip'
const modelForm = ref({})

onMounted(() => {
  loadFormFields(mm)
})

function loadFormFields(model) {
  getFormFields(model).then((response) => {
    modelForm.value = response.data
  })
}

</script>