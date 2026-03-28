<template>
  <div class="app-container">
    <!-- 顶部欢迎区域 -->
    <header class="app-header">
      <Welcome />
    </header>
    
    <!-- 主要内容区域 -->
    <main class="app-main">
      <!-- 移动端 Tab 导航 -->
      <nav class="mobile-tabs">
        <button 
          v-for="(tab, index) in tabs" 
          :key="tab.id"
          :class="['tab-btn', { active: activeTab === index }]"
          @click="activeTab = index"
        >
          <span class="tab-icon">{{ tab.icon }}</span>
          <span class="tab-label">{{ tab.label }}</span>
        </button>
      </nav>
      
      <!-- 左侧：模型选择 -->
      <aside class="sidebar-left" :class="{ 'mobile-hidden': activeTab !== 0 }">
        <ModelSelector />
      </aside>
      
      <!-- 中间：参数输入区域 -->
      <section class="content-center" :class="{ 'mobile-hidden': activeTab !== 1 }">
        <div class="form-header">
          <h2>⚙️ 参数配置</h2>
          <div v-if="store.hasError" class="error-banner">
            <span>{{ store.error }}</span>
            <button @click="store.clearError" class="error-close">×</button>
          </div>
        </div>
        
        <!-- 材料选择器 -->
        <MaterialSelector />
        
        <!-- 参数表单（包含计算按钮） -->
        <ParameterForm />
      </section>
      
      <!-- 右侧：结果显示 -->
      <aside class="sidebar-right" :class="{ 'mobile-hidden': activeTab !== 2 }">
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
import { ref, watch, onMounted } from 'vue'
import { useCalculationStore } from './stores/calculatorStore'
import { analyticsHit } from './api'
import Welcome from './components/Welcome.vue'
import ModelSelector from './components/ModelSelector.vue'
import MaterialSelector from './components/MaterialSelector.vue'
import ParameterForm from './components/ParameterForm.vue'
import ResultDisplay from './components/ResultDisplay.vue'
import Footer from './components/Footer.vue'

const store = useCalculationStore()

// 移动端 Tab 状态
const tabs = [
  { id: 'model', label: '模型', icon: '🤖' },
  { id: 'params', label: '参数', icon: '⚙️' },
  { id: 'result', label: '结果', icon: '📊' }
]
const activeTab = ref(1) // 默认打开"参数"标签页

// 监听 selectedModel 变化，加载对应的表单字段
watch(
  () => store.selectedModel,
  async (newModel) => {
    if (newModel) {
      console.log('🔄 模型切换为：', newModel)
      await store.loadFormFields(newModel)
      // 自动切换到参数标签页
      activeTab.value = 1
    }
  }
)

// 组件挂载时初始化应用数据
onMounted(async () => {
  try {
    await store.initializeApp()
    await analyticsHit(window.location.pathname)
    const loadingContainer = document.getElementById('loading-container')
    if (loadingContainer) {
      loadingContainer.classList.add('hidden')
    }
  } catch (error) {
    console.error('应用初始化失败:', error)
    const loadingContainer = document.getElementById('loading-container')
    if (loadingContainer) {
      loadingContainer.classList.add('hidden')
    }
  }
})
</script>

<style>
/* ========== CSS 变量定义 ========== */
:root {
  --primary-color: #0066cc;
  --primary-hover: #0052a3;
  --success-color: #34c759;
  --error-color: #dc2626;
  --warning-bg: #fef2f2;
  --warning-border: #fecaca;
  --bg-main: #f2f2f7;
  --bg-card: #ffffff;
  --text-primary: #1d1d1f;
  --text-secondary: #86868b;
  --border-color: #e2e2e7;
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.08);
  --radius-sm: 8px;
  --radius-md: 10px;
  --radius-lg: 12px;
  --font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  --font-mono: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  --transition-fast: 0.2s ease;
  --transition-normal: 0.3s ease;
}

/* ========== 全局重置 ========== */
*, *::before, *::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  width: 100%;
  height: 100%;
  overflow-x: hidden;
  background-color: var(--bg-main);
  font-family: var(--font-family);
  font-size: 14px;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  width: 100%;
  max-width: 100vw;
  overflow-x: hidden;
}

/* ========== 滚动条美化 ========== */
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

/* ========== 通用元素样式 ========== */
button {
  font-family: var(--font-family);
  cursor: pointer;
  transition: var(--transition-fast);
}

input, select {
  font-family: var(--font-family);
  border-radius: var(--radius-sm);
  transition: var(--transition-fast);
}

input:focus, select:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.15);
}
</style>

<style scoped>
/* ========== 应用容器 ========== */
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: var(--bg-main);
}

/* ========== 顶部导航 ========== */
.app-header {
  background: var(--bg-card);
  color: var(--text-primary);
  box-shadow: var(--shadow-sm);
  flex-shrink: 0;
  z-index: 100;
  height: 48px;
  display: flex;
  align-items: center;
  border-bottom: 1px solid var(--border-color);
  padding: 0 16px;
}

/* ========== 主内容区域 ========== */
.app-main {
  flex: 1;
  display: grid;
  grid-template-columns: 280px 1fr 300px;
  grid-template-areas: "sidebar params results";
  gap: 16px;
  padding: 16px;
  max-width: 1600px;
  margin: 0 auto;
  width: 100%;
}

/* ========== 移动端 Tab 导航 ========== */
.mobile-tabs {
  display: none;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: var(--bg-card);
  border-top: 1px solid var(--border-color);
  padding: 8px 12px;
  gap: 8px;
  z-index: 1000;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
}

.tab-btn {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 8px 12px;
  background: var(--bg-main);
  border: 2px solid transparent;
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  font-size: 11px;
  font-weight: 500;
}

.tab-btn.active {
  background: rgba(0, 102, 204, 0.1);
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.tab-icon {
  font-size: 18px;
}

.tab-label {
  font-size: 10px;
}

/* ========== 左侧边栏 - 模型选择 ========== */
.sidebar-left {
  grid-area: sidebar;
  background: var(--bg-card);
  border-radius: var(--radius-md);
  padding: 16px;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-color);
  overflow: hidden;
}

/* ========== 中间参数区域 ========== */
.content-center {
  grid-area: params;
  background: var(--bg-card);
  border-radius: var(--radius-md);
  padding: 16px;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  gap: 12px;
  overflow: hidden;
  min-height: 0;
}

/* ========== 右侧结果区域 ========== */
.sidebar-right {
  grid-area: results;
  background: var(--bg-card);
  border-radius: var(--radius-md);
  padding: 0;
  box-shadow: var(--shadow-sm);
  overflow: hidden;
  border: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
}

/* ========== 表单头部 ========== */
.form-header {
  flex-shrink: 0;
}

.form-header h2 {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

/* ========== 错误提示 ========== */
.error-banner {
  background: var(--warning-bg);
  border: 1px solid var(--warning-border);
  border-radius: var(--radius-sm);
  padding: 8px 12px;
  color: var(--error-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 8px;
  font-size: 12px;
}

.error-close {
  background: none;
  border: none;
  font-size: 18px;
  color: var(--error-color);
  cursor: pointer;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: var(--transition-fast);
}

.error-close:hover {
  background-color: rgba(220, 38, 38, 0.1);
}

/* ========== 底部 ========== */
.app-footer {
  background: var(--bg-card);
  color: var(--text-secondary);
  flex-shrink: 0;
  z-index: 10;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  border-top: 1px solid var(--border-color);
}

/* ========== 响应式设计 ========== */
@media (max-width: 1200px) {
  .app-main {
    grid-template-columns: 240px 1fr 260px;
    gap: 12px;
    padding: 12px;
  }
}

@media (max-width: 992px) {
  .app-main {
    grid-template-columns: 220px 1fr 240px;
    gap: 10px;
  }
}

@media (max-width: 768px) {
  .app-main {
    grid-template-columns: 1fr;
    grid-template-areas: 
      "params"
      "results"
      "sidebar";
    gap: 0;
    padding: 12px;
    padding-bottom: 80px; /* 为底部 Tab 留出空间 */
  }
  
  .mobile-tabs {
    display: flex;
  }
  
  .sidebar-left,
  .content-center,
  .sidebar-right {
    border-radius: var(--radius-md);
    margin-bottom: 12px;
  }
  
  .sidebar-left {
    display: flex;
    flex-direction: column;
  }
  
  .mobile-hidden {
    display: none;
  }
  
  .app-header {
    height: 44px;
    padding: 0 12px;
  }
  
  .app-footer {
    display: none;
  }
}

@media (max-width: 480px) {
  .app-main {
    padding: 8px;
    padding-bottom: 70px;
    gap: 0;
  }
  
  .sidebar-left,
  .content-center,
  .sidebar-right {
    margin-bottom: 8px;
    padding: 12px;
  }
  
  .mobile-tabs {
    padding: 6px 8px;
    gap: 6px;
  }
  
  .tab-btn {
    padding: 6px 8px;
  }
  
  .tab-icon {
    font-size: 16px;
  }
}
</style>
