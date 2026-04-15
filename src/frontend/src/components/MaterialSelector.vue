<template>
  <div
    class="material-selector"
    role="region"
    aria-label="基板材料选择"
  >
    <div class="header">
      <span
        class="icon"
        aria-hidden="true"
      >🐻</span>
      <span class="title">参考材料</span>
    </div>

    <div class="select-wrapper">
      <label
        for="material-select"
        class="sr-only"
      >选择基板材料</label>
      <select
        id="material-select"
        v-model="selectedMaterial"
        class="material-select"
        aria-describedby="material-desc"
      >
        <option value="">
          选择基板材料...
        </option>
        <option
          v-for="(material, key) in materials"
          :key="key"
          :value="key"
        >
          {{ material.name }}
        </option>
      </select>
      <span
        id="material-desc"
        class="sr-only"
      >
        选择基板材料将自动填充介电常数和损耗角正切参数
      </span>
    </div>

    <div
      v-if="selectedMaterial && materials[selectedMaterial]"
      class="material-info"
      role="region"
      aria-label="材料参数信息"
    >
      <div
        class="param"
        role="group"
        aria-label="相对介电常数"
      >
        <span
          class="label"
          aria-label="介电常数符号"
        >εr</span>
        <span
          class="value"
          aria-label="介电常数值"
        >{{ materials[selectedMaterial].er }}</span>
      </div>
      <div
        class="divider"
        aria-hidden="true"
      />
      <div
        class="param"
        role="group"
        aria-label="损耗角正切"
      >
        <span
          class="label"
          aria-label="损耗角正切符号"
        >tanδ</span>
        <span
          class="value"
          aria-label="损耗角正切值"
        >{{ materials[selectedMaterial].loss_tangent }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useCalculationStore } from '../stores/calculatorStore'

const store = useCalculationStore()

const materials = computed(() => store.materials)
const selectedMaterial = computed({
  get: () => store.selectedMaterial,
  set: (value) => store.selectMaterial(value),
})
</script>

<style scoped>
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

.material-selector {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  border-bottom: 1px solid rgba(255,255,255,0.06);
}

.header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header .icon {
  font-size: 14px;
}

.header .title {
  font-size: 13px;
  font-weight: 600;
  color: rgba(255,255,255,0.6);
}

.select-wrapper {
  position: relative;
}

.material-select {
  width: 100%;
  padding: 12px 14px;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 10px;
  color: #fff;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.3s;
  appearance: none;
  -webkit-appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='rgba(255,255,255,0.4)' d='M6 8L1 3h10z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  padding-right: 32px;
}

.material-select:hover {
  border-color: rgba(59, 130, 246, 0.5);
  background-color: rgba(59, 130, 246, 0.1);
}

.material-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}

.material-select option {
  background: #1a1a2e;
  color: #fff;
}

.material-info {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 14px;
  background: rgba(59, 130, 246, 0.1);
  border: 1px solid rgba(59, 130, 246, 0.2);
  border-radius: 10px;
}

.param {
  display: flex;
  align-items: center;
  gap: 8px;
}

.param .label {
  font-size: 12px;
  color: rgba(255,255,255,0.5);
}

.param .value {
  font-size: 15px;
  font-weight: 700;
  font-family: 'SF Mono', Monaco, monospace;
  color: #60a5fa;
}

.divider {
  width: 1px;
  height: 20px;
  background: rgba(255,255,255,0.1);
}
</style>
