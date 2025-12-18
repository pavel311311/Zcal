<template>
  <div class="model-form">
    <h2>模型参数配置</h2>
    
    <!-- 模型选择器 -->
    <ModelSelector />
    
    <!-- 材料选择器 -->
    <MaterialSelector />
    
    <!-- 参数表单 -->
    <ParameterForm 
      v-model:modelForm="modelForm" 
    />
    
    <!-- 计算控制按钮 -->
    <CalculationControls 
      :modelForm="modelForm" 
    />
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useCalculationStore } from '../stores/calculatorStore'
import ModelSelector from './ModelSelector.vue'
import MaterialSelector from './MaterialSelector.vue'
import ParameterForm from './ParameterForm.vue'
import CalculationControls from './CalculationControls.vue'

const store = useCalculationStore()
const calculator = store.calculator

const modelForm = ref([])

// 加载模型表单参数
async function loadFormFields(model) {
  if (!model) {
    modelForm.value = []
    return
  }
  
  try {
    const fields = await calculator.loadFormFields(model)
    modelForm.value = fields
  } catch (error) {
    console.error('加载表单字段失败:', error)
    modelForm.value = []
  }
}

// 监听selectedModel变化，加载对应的表单字段
watch(
  () => store.selectedModel,
  (newModel) => {
    console.log('🔄 模型切换为：', newModel);
    loadFormFields(newModel)
  },
  { immediate: true } // 初始加载时执行
)


</script>

