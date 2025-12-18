<template>
  <div class="model-form">
    <h2>模型参数配置</h2>
    
    <!-- 模型选择器 -->
    <ModelSelector />
    
    <!-- 材料选择器 -->
    <MaterialSelector />
    
    <!-- 参数表单 -->
    <ParameterForm />
    
    <!-- 计算控制按钮 -->
    <CalculationControls />
  </div>
</template>

<script setup>
import { watch, onMounted } from 'vue'
import { useCalculationStore } from '../stores/calculatorStore'
import ModelSelector from './ModelSelector.vue'
import MaterialSelector from './MaterialSelector.vue'
import ParameterForm from './ParameterForm.vue'
import CalculationControls from './CalculationControls.vue'

const store = useCalculationStore()

// 监听selectedModel变化，加载对应的表单字段
watch(
  () => store.selectedModel,
  (newModel) => {
    console.log('🔄 模型切换为：', newModel);
    store.loadFormFields(newModel)
  },
  { immediate: true } // 初始加载时执行
)

// 组件挂载时加载模型类型和材料数据
onMounted(async () => {
  try {
    await Promise.all([
      store.loadModelTypes(),
      store.loadMaterials()
    ])
  } catch (error) {
    console.error('初始化数据失败:', error)
  }
})

</script>

