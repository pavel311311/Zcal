<template>
  <div id="app">
    <header class="app-header">
      <div class="header-content">
        <h1>PCB 阻抗计算器</h1>
        <p>精确的传输线阻抗计算工具</p>
      </div>
    </header>

    <main class="container">
      <div class="grid grid-2">
        <section>
          <CalculatorForm @calculate="handleCalculate" />
        </section>
        <section>
          <ResultDisplay :result="calculationResult" :loading="isLoading" />
        </section>
      </div>
    </main>

    <footer class="app-footer">
      <p>&copy; 2025 PCB Impedance Calculator. All rights reserved.</p>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import CalculatorForm from './components/CalculatorForm.vue'
import ResultDisplay from './components/ResultDisplay.vue'

const calculationResult = ref(null)
const isLoading = ref(false)

const handleCalculate = (result) => {
  isLoading.value = false
  calculationResult.value = result
}
</script>

<style scoped>
.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 40px 20px;
  text-align: center;
  margin-bottom: 40px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
}

.header-content h1 {
  font-size: 2.5em;
  margin-bottom: 10px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.header-content p {
  font-size: 1.1em;
  opacity: 0.9;
}

.app-footer {
  background: rgba(0, 0, 0, 0.8);
  color: white;
  text-align: center;
  padding: 20px;
  margin-top: 60px;
}

@media (max-width: 768px) {
  .header-content h1 {
    font-size: 1.8em;
  }

  .header-content p {
    font-size: 1em;
  }
}
</style>
