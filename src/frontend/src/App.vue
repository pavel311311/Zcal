<template>
  <div class="app-container">
    <!-- 顶部欢迎区域 -->
    <header class="app-header">
      <Welcome />
    </header>
    
    <!-- 主要内容区域 - 四列布局 -->
    <main class="app-main">
      <!-- 左侧：模型选择 -->
      <aside class="sidebar-left">
        <ModelSelector />
      </aside>
      
      <!-- 中间：参数输入区域 -->
      <section class="content-center">
        <div class="form-header">
          <h2>参数配置</h2>
          <div v-if="store.hasError" class="error-banner">
            {{ store.error }}
            <button @click="store.clearError" class="error-close">×</button>
          </div>
        </div>
        
        <!-- 材料选择器 -->
        <MaterialSelector />
        
        <!-- 参数表单 -->
        <ParameterForm />
      </section>
      
      <!-- 控制区域 -->
      <section class="content-controls">
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

/* 应用容器 - 固定视口高度 */
.app-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f8fafc;
  overflow: hidden;
  font-size: 12px; /* 全局字体缩小 */
}

/* 顶部欢迎区域 - 更紧凑 */
.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  flex-shrink: 0;
  z-index: 10;
  height: 50px; /* 固定高度 */
  display: flex;
  align-items: center;
}

/* 主要内容区域 - 四列布局 */
.app-main {
  flex: 1;
  display: grid;
  grid-template-columns: 200px 1fr 1fr 280px;
  grid-template-areas: "sidebar params controls results";
  gap: 8px;
  padding: 8px;
  max-width: 1600px;
  margin: 0 auto;
  width: 100%;
  min-height: 0;
  overflow: hidden;
  height: calc(100vh - 50px - 32px); /* 减去header和footer */
}

/* 左侧边栏 - 模型选择 */
.sidebar-left {
  grid-area: sidebar;
  background: white;
  border-radius: 6px;
  padding: 8px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 中间参数区域 - 占用两列 */
.content-center {
  grid-area: params;
  background: white;
  border-radius: 6px;
  padding: 8px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 8px;
  overflow: hidden;
  min-height: 0;
}

/* 控制区域 */
.content-controls {
  grid-area: controls;
  display: flex;
  flex-direction: column;
  gap: 8px;
  overflow: hidden;
}

/* 右侧结果区域 */
.sidebar-right {
  grid-area: results;
  background: white;
  border-radius: 6px;
  padding: 0;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* 表单头部 - 极简设计 */
.form-header {
  flex-shrink: 0;
  margin-bottom: 8px;
  padding-bottom: 6px;
  border-bottom: 1px solid #e5e7eb;
}

.form-header h2 {
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 2px 0;
}

/* 错误提示 - 极简设计 */
.error-banner {
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 3px;
  padding: 4px 6px;
  color: #dc2626;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 4px;
  font-size: 11px;
}

.error-close {
  background: none;
  border: none;
  font-size: 12px;
  color: #dc2626;
  cursor: pointer;
  padding: 1px;
  width: 14px;
  height: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 2px;
  transition: background-color 0.2s ease;
}

.error-close:hover {
  background-color: #fecaca;
}

/* 底部 - 极简 */
.app-footer {
  background: #374151;
  color: white;
  flex-shrink: 0;
  z-index: 10;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
}

/* 响应式设计 */
@media (max-width: 1400px) {
  .app-main {
    grid-template-columns: 180px 1fr 1fr 260px;
    gap: 6px;
    padding: 6px;
  }
}

@media (max-width: 1200px) {
  .app-main {
    grid-template-columns: 1fr 1fr;
    grid-template-rows: auto auto;
    grid-template-areas: 
      "sidebar params"
      "controls results";
    height: calc(100vh - 50px - 32px);
  }
  
  .content-center {
    overflow-y: auto;
  }
}

@media (max-width: 768px) {
  .app-main {
    grid-template-columns: 1fr;
    grid-template-rows: auto auto auto auto;
    grid-template-areas: 
      "sidebar"
      "params" 
      "controls"
      "results";
    overflow-y: auto;
  }
  
  .app-header {
    height: 40px;
  }
  
  .app-footer {
    height: 24px;
  }
}

/* 滚动条美化 */
::-webkit-scrollbar {
  width: 3px;
  height: 3px;
}

::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 2px;
}

::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 2px;
}

::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* 确保子组件适应容器 */
.sidebar-left,
.content-center,
.content-controls,
.sidebar-right {
  min-height: 0;
  max-height: 100%;
}
</style>