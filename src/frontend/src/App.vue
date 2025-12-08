<template>
  <h1>PCB 阻抗计算器</h1>
  <p>精确的传输线阻抗计算工具</p>

  <Welcome />
  <ModelForm />
  <!-- <CalculatorForm />
  <ResultDisplay /> -->
</template>

<script setup>
import CalculatorForm from './components/CalculatorForm.vue'
import ResultDisplay from './components/ResultDisplay.vue'
import Welcome from './components/Welcome.vue'
import ModelForm from './components/ModelForm.vue'
</script>
