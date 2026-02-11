<template>
  <div class="app-container">
    <!-- 顶部欢迎区域 -->
    <header class="app-header">
      <Welcome />
    </header>
    
    <!-- 主要内容区域 - 三列布局 -->
    <main class="app-main">
      <!-- 左侧：模型选择 -->
      <aside class="sidebar-left">
        <ModelSelector />
      </aside>
      
      <!-- 中间：参数输入区域 -->
      <section class="content-center">
        <div class="form-header">
          <h2>👾参数配置</h2>
          <div v-if="store.hasError" class="error-banner">
            {{ store.error }}
            <button @click="store.clearError" class="error-close">×</button>
          </div>
        </div>
        
        <!-- 材料选择器 -->
        <MaterialSelector />
        
        <!-- 参数表单（包含计算按钮） -->
        <ParameterForm />
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
import { analyticsHit } from './api'
import Welcome from './components/Welcome.vue'
import ModelSelector from './components/ModelSelector.vue'
import MaterialSelector from './components/MaterialSelector.vue'
import ParameterForm from './components/ParameterForm.vue'
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
    await analyticsHit(window.location.pathname)
  } catch (error) {
    console.error('应用初始化失败:', error)
  }
})
</script>

<style>
/* 全局样式 - 消除滚动条 */
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background-color: #f2f2f7;
}

/* 全局重置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
</style>

<style scoped>
/* 应用容器 - 自适应高度 */
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f2f2f7;
  font-size: 12px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

/* 顶部欢迎区域 - Mac风格 */
.app-header {
  background: #ffffff;
  color: #1d1d1f;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  flex-shrink: 0;
  z-index: 10;
  height: 44px;
  display: flex;
  align-items: center;
  border-bottom: 1px solid #e2e2e7;
}

/* 主要内容区域 - 三列布局 */
.app-main {
  flex: 1;
  display: grid;
  /* 比例型 - 完全响应式 */
  grid-template-columns: 1.5fr 2fr 1.5fr;
  grid-template-areas: "sidebar params results";
  gap: 12px;
  padding: 12px;
  max-width: 1600px;
  margin: 0 auto;
  width: 100%;
  min-height: 400px;
}

/* 左侧边栏 - 模型选择 */
.sidebar-left {
  grid-area: sidebar;
  background: #ffffff;
  border-radius: 10px;
  padding: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border: 1px solid #e2e2e7;
}

/* 中间参数区域 */
.content-center {
  grid-area: params;
  background: #ffffff;
  border-radius: 10px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  gap: 12px;
  overflow: hidden;
  min-height: 0;
  border: 1px solid #e2e2e7;
}

/* 右侧结果区域 */
.sidebar-right {
  grid-area: results;
  background: #ffffff;
  border-radius: 10px;
  padding: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  border: 1px solid #e2e2e7;
}

/* 表单头部 - Mac风格 */
.form-header {
  flex-shrink: 0;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #e2e2e7;
}

.form-header h2 {
  font-size: 14px;
  font-weight: 600;
  color: #1d1d1f;
  margin: 0 0 4px 0;
}

/* 错误提示 - Mac风格 */
.error-banner {
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 8px;
  padding: 6px 8px;
  color: #dc2626;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 6px;
  font-size: 11px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.error-close {
  background: none;
  border: none;
  font-size: 14px;
  color: #dc2626;
  cursor: pointer;
  padding: 2px;
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: background-color 0.2s ease;
}

.error-close:hover {
  background-color: rgba(220, 38, 38, 0.1);
}

/* 底部 - Mac风格 */
.app-footer {
  background: #ffffff;
  color: #86868b;
  flex-shrink: 0;
  z-index: 10;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  border-top: 1px solid #e2e2e7;
}

/* 响应式设计 */
@media (max-width: 1400px) {
  .app-main {
    grid-template-columns: 180px 1fr 260px;
    gap: 10px;
    padding: 10px;
  }
}

@media (max-width: 1200px) {
  .app-main {
    grid-template-columns: 1fr 1fr;
    grid-template-rows: auto auto;
    grid-template-areas: 
      "sidebar params"
      "results results";
    gap: 10px;
    padding: 10px;
  }
}

@media (max-width: 768px) {
  .app-main {
    grid-template-columns: 1fr;
    grid-template-rows: auto auto auto;
    grid-template-areas: 
      "sidebar"
      "params" 
      "results";
    gap: 10px;
    padding: 10px;
  }
  
  .app-header {
    height: 40px;
  }
  
  .app-footer {
    height: 28px;
  }
}

/* 滚动条美化 - Mac风格 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f5f5f5;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: #c6c6c8;
  border-radius: 4px;
  border: 2px solid #f5f5f5;
}

::-webkit-scrollbar-thumb:hover {
  background: #a1a1a6;
}

/* 确保子组件适应容器 */
.sidebar-left,
.content-center,
.sidebar-right {
  min-height: 0;
  max-height: 100%;
}

/* 通用按钮样式 - Mac风格 */
button {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  border-radius: 8px;
  transition: all 0.2s ease;
}

/* 通用输入框样式 - Mac风格 */
input, select {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  border-radius: 8px;
  transition: all 0.2s ease;
}

input:focus, select:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.1);
}
</style>
