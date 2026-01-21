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

/* 应用容器 - 固定视口高度 */
.app-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f8fafc;
  overflow: hidden; /* 防止整体滚动 */
}

/* 顶部欢迎区域 - 固定高度 */
.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  flex-shrink: 0; /* 防止压缩 */
  z-index: 10;
}

/* 主要内容区域 - 占用剩余空间 */
.app-main {
  flex: 1;
  display: grid;
  grid-template-columns: 240px 1fr 320px;
  gap: 12px;
  padding: 12px;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
  min-height: 0; /* 允许网格项目收缩 */
  overflow: hidden;
}

/* 左侧边栏 - 固定宽度，内容可滚动 */
.sidebar-left {
  background: white;
  border-radius: 8px;
  padding: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 中间内容区域 - 弹性布局 */
.content-center {
  background: white;
  border-radius: 8px;
  padding: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 12px;
  overflow: hidden;
  min-height: 0;
}

/* 右侧边栏 - 固定宽度，内容可滚动 */
.sidebar-right {
  background: white;
  border-radius: 8px;
  padding: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* 表单头部 - 紧凑设计 */
.form-header {
  flex-shrink: 0;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #e5e7eb;
}

.form-header h2 {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 4px 0;
}

/* 错误提示 - 紧凑设计 */
.error-banner {
  background: linear-gradient(135deg, #fef2f2 0%, #fde8e8 100%);
  border: 1px solid #fecaca;
  border-radius: 4px;
  padding: 6px 8px;
  color: #dc2626;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 6px;
  font-size: 12px;
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
  border-radius: 2px;
  transition: background-color 0.2s ease;
}

.error-close:hover {
  background-color: #fecaca;
}

/* 底部 - 固定高度 */
.app-footer {
  background: #374151;
  color: white;
  flex-shrink: 0;
  z-index: 10;
}

/* 内容区域滚动优化 */
.content-center > *:not(.form-header) {
  flex-shrink: 0;
}

/* 确保组件内部可以滚动 */
.sidebar-left > *,
.sidebar-right > * {
  min-height: 0;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .app-main {
    grid-template-columns: 260px 1fr 340px;
    gap: 12px;
    padding: 12px;
  }
  
  .content-center {
    padding: 16px;
    gap: 12px;
  }
  
  .sidebar-left {
    padding: 12px;
  }
}

@media (max-width: 992px) {
  .app-main {
    grid-template-columns: 1fr;
    grid-template-rows: auto auto auto;
    gap: 12px;
    overflow-y: auto; /* 在中等屏幕允许滚动 */
  }
  
  .sidebar-left,
  .sidebar-right {
    position: static;
    height: auto;
    max-height: none;
  }
  
  .content-center {
    order: 1;
    min-height: auto;
  }
  
  .sidebar-left {
    order: 0;
    max-height: 300px;
    overflow-y: auto;
  }
  
  .sidebar-right {
    order: 2;
    max-height: 400px;
    overflow-y: auto;
  }
}

@media (max-width: 768px) {
  .app-main {
    padding: 8px;
    gap: 8px;
  }
  
  .sidebar-left,
  .content-center,
  .sidebar-right {
    padding: 12px;
  }
  
  .form-header h2 {
    font-size: 18px;
  }
}

/* 滚动条美化 */
::-webkit-scrollbar {
  width: 4px;
  height: 4px;
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
.sidebar-right {
  min-height: 0;
  max-height: 100%;
}

/* 防止内容溢出 */
.app-main > * {
  min-height: 0;
  overflow: hidden;
}

/* 桌面端固定高度优化 */
@media (min-width: 993px) {
  .app-main {
    height: calc(100vh - 70px - 48px); /* 减去header和footer的高度 */
    max-height: calc(100vh - 70px - 48px);
  }
  
  .sidebar-left,
  .content-center,
  .sidebar-right {
    height: 100%;
    max-height: 100%;
  }
}
</style>