<template>
  <div class="app-wrapper">
    <div class="app-container" :style="containerStyle">
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
            <h2>⚙️ 参数配置</h2>
            <div v-if="store.hasError" class="error-banner">
              <span>{{ store.error }}</span>
              <button @click="store.clearError" class="error-close">×</button>
            </div>
          </div>
          
          <!-- 材料选择器 -->
          <MaterialSelector />
          
          <!-- 参数表单 -->
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
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useCalculationStore } from './stores/calculatorStore'
import { analyticsHit } from './api'
import Welcome from './components/Welcome.vue'
import ModelSelector from './components/ModelSelector.vue'
import MaterialSelector from './components/MaterialSelector.vue'
import ParameterForm from './components/ParameterForm.vue'
import ResultDisplay from './components/ResultDisplay.vue'
import Footer from './components/Footer.vue'

const store = useCalculationStore()

// 设计稿尺寸
const BASE_WIDTH = 1440
const BASE_HEIGHT = 900

// 当前缩放比例
const scale = ref(1)

// 计算缩放后的容器样式
const containerStyle = computed(() => ({
  transform: `scale(${scale.value})`,
  transformOrigin: 'top left',
  width: `${BASE_WIDTH}px`,
  minHeight: `${BASE_HEIGHT}px`
}))

// 计算缩放比例
const calculateScale = () => {
  const windowWidth = window.innerWidth
  const windowHeight = window.innerHeight
  
  const scaleX = windowWidth / BASE_WIDTH
  const scaleY = windowHeight / BASE_HEIGHT
  
  scale.value = Math.min(scaleX, scaleY, 1)
}

// 监听窗口变化
onMounted(() => {
  calculateScale()
  window.addEventListener('resize', calculateScale)
  initializeApp()
})

onUnmounted(() => {
  window.removeEventListener('resize', calculateScale)
})

const initializeApp = async () => {
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
}

watch(
  () => store.selectedModel,
  async (newModel) => {
    if (newModel) {
      console.log('🔄 模型切换为：', newModel)
      await store.loadFormFields(newModel)
    }
  }
)
</script>

<style>
/* 全局重置 */
*, *::before, *::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  width: 100%;
  height: 100%;
  overflow: hidden;
  background-color: #f2f2f7;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

#app {
  width: 100%;
  height: 100%;
  overflow: hidden;
}

/* 滚动条 */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: #f5f5f5;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb {
  background: #c6c6c8;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a1a1a6;
}
</style>

<style scoped>
/* 外层容器 - 填满窗口 */
.app-wrapper {
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  position: relative;
}

/* 内层容器 - 设计尺寸，缩放适配 */
.app-container {
  position: absolute;
  top: 0;
  left: 0;
  display: flex;
  flex-direction: column;
  background-color: #f2f2f7;
}

/* 顶部导航 */
.app-header {
  height: 44px;
  flex-shrink: 0;
  background: #ffffff;
  border-bottom: 1px solid #e2e2e7;
  display: flex;
  align-items: center;
  padding: 0 16px;
}

/* 主内容区域 */
.app-main {
  flex: 1;
  display: grid;
  grid-template-columns: 260px 1fr 280px;
  grid-template-areas: "sidebar params results";
  gap: 12px;
  padding: 12px;
  min-height: 0;
  overflow: hidden;
}

/* 左侧边栏 */
.sidebar-left {
  grid-area: sidebar;
  background: #ffffff;
  border-radius: 10px;
  border: 1px solid #e2e2e7;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

/* 中间区域 */
.content-center {
  grid-area: params;
  background: #ffffff;
  border-radius: 10px;
  border: 1px solid #e2e2e7;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  overflow: hidden;
  min-height: 0;
}

/* 右侧结果 */
.sidebar-right {
  grid-area: results;
  background: #ffffff;
  border-radius: 10px;
  border: 1px solid #e2e2e7;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

/* 表单头部 */
.form-header {
  flex-shrink: 0;
  padding-bottom: 10px;
  border-bottom: 1px solid #e2e2e7;
}

.form-header h2 {
  font-size: 15px;
  font-weight: 600;
  color: #1d1d1f;
}

/* 错误提示 */
.error-banner {
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 6px;
  padding: 6px 10px;
  color: #dc2626;
  font-size: 11px;
  margin-top: 6px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.error-close {
  background: none;
  border: none;
  color: #dc2626;
  font-size: 16px;
  cursor: pointer;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.error-close:hover {
  background: rgba(220, 38, 38, 0.1);
}

/* 底部 */
.app-footer {
  height: 32px;
  flex-shrink: 0;
  background: #ffffff;
  border-top: 1px solid #e2e2e7;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  color: #86868b;
}
</style>
