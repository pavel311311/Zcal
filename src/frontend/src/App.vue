<template>
  <div class="app-container">
    <!-- 顶部欢迎区域 -->
    <header class="app-header">
      <Welcome />
    </header>
    
    <!-- 主要内容区域 -->
    <main class="app-main">
      <!-- 左侧：模型选择 -->
      <aside class="sidebar-left">
        <ModelSelector />
      </aside>
      
      <!-- 中间：参数输入区域 -->
      <section class="content-center">
        <div class="form-header">
          <h2>模型参数配置</h2>
          <div v-if="store.hasError" class="error-banner">
            {{ store.error }}
            <button @click="store.clearError" class="error-close">×</button>
          </div>
        </div>
        
        <!-- 材料选择器 -->
        <MaterialSelector />
        
        <!-- 参数表单 -->
        <ParameterForm />
        
        <!-- 计算控制按钮 -->
        <CalculationControls />
      </section>
      
      <!-- 右侧：结果显示 -->
      <aside class="sidebar-right">
        <ResultDisplay />
      </aside>
    </main>
    
    <!-- 底部 -->
    <footer class="app-footer">
      <Footer />
    </footer>
  </div>
</template>

<script setup>
import { watch, onMounted } from 'vue'
import { useCalculationStore } from './stores/calculatorStore'
import Welcome from './components/Welcome.vue'
import ModelSelector from './components/ModelSelector.vue'
import MaterialSelector from './components/MaterialSelector.vue'
import ParameterForm from './components/ParameterForm.vue'
import CalculationControls from './components/CalculationControls.vue'
import ResultDisplay from './components/ResultDisplay.vue'
import Footer from './components/Footer.vue'

const store = useCalculationStore()

// 监听selectedModel变化，加载对应的表单字段
watch(
  () => store.selectedModel,
  async (newModel) => {
    if (newModel) {
      console.log('🔄 模型切换为：', newModel)
      await store.loadFormFields(newModel)
    }
  }
)

// 组件挂载时初始化应用数据
onMounted(async () => {
  try {
    await store.initializeApp()
  } catch (error) {
    console.error('应用初始化失败:', error)
  }
})
</script>

<style scoped>
/* 全局重置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* 应用容器 */
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f8fafc;
}

/* 顶部欢迎区域 */
.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* 主要内容区域 */
.app-main {
  flex: 1;
  display: grid;
  grid-template-columns: 300px 1fr 400px;
  gap: 20px;
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

/* 左侧边栏 */
.sidebar-left {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  height: fit-content;
  position: sticky;
  top: 20px;
}

/* 中间内容区域 */
.content-center {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 右侧边栏 */
.sidebar-right {
  background: white;
  border-radius: 12px;
  padding: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  height: fit-content;
  position: sticky;
  top: 20px;
  overflow: hidden;
}

/* 表单头部 */
.form-header {
  margin-bottom: 20px;
}

.form-header h2 {
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 10px 0;
}

/* 错误提示 */
.error-banner {
  background: linear-gradient(135deg, #fef2f2 0%, #fde8e8 100%);
  border: 1px solid #fecaca;
  border-radius: 8px;
  padding: 12px 16px;
  color: #dc2626;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 12px;
  font-size: 14px;
}

.error-close {
  background: none;
  border: none;
  font-size: 18px;
  color: #dc2626;
  cursor: pointer;
  padding: 4px;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: background-color 0.2s ease;
}

.error-close:hover {
  background-color: #fecaca;
}

/* 底部 */
.app-footer {
  background: #374151;
  color: white;
  padding: 16px 20px;
  text-align: center;
  margin-top: auto;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .app-main {
    grid-template-columns: 280px 1fr 350px;
    gap: 16px;
    padding: 16px;
  }
}

@media (max-width: 992px) {
  .app-main {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .sidebar-left,
  .sidebar-right {
    position: static;
  }
  
  .content-center {
    order: 1;
  }
  
  .sidebar-left {
    order: 0;
  }
  
  .sidebar-right {
    order: 2;
  }
}

@media (max-width: 768px) {
  .app-header {
    padding: 16px;
  }
  
  .app-main {
    padding: 12px;
    gap: 16px;
  }
  
  .sidebar-left,
  .content-center,
  .sidebar-right {
    padding: 16px;
  }
}

/* 滚动条美化 */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>