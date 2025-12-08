<template>
  <h1>PCB 阻抗计算器</h1>
  <p>精确的传输线阻抗计算工具</p>

  <Welcome />
  <CalculatorForm />
  <ResultDisplay />
  <Footer />

</template>

<script setup>
import CalculatorForm from './components/CalculatorForm.vue'
import ResultDisplay from './components/ResultDisplay.vue'
import Footer from './components/Footer.vue'
import Welcome from './components/Welcome.vue';
</script>
