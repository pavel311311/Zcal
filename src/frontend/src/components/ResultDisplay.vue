<template>
  <div>
    <h2>计算结果</h2>
    <p> 🐸 以下是计算的最终结果：</p>
    <p> {{ store.result }}</p>
  </div>
</template>

<script setup>
import { useCalculationStore } from '../stores/calculation'

const store = useCalculationStore()


</script>
