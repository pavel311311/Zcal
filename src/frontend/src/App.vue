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
          <CalculatorForm />
        </section>
        <section>
          <ResultDisplay />
        </section>
      </div>
    </main>

    <footer class="app-footer">
      <p>&copy; 2025 PCB Impedance Calculator. All rights reserved.</p>
    </footer>
  </div>
</template>

<script setup>
import CalculatorForm from './components/CalculatorForm.vue'
import ResultDisplay from './components/ResultDisplay.vue'
</script>
