<template>
  <div class="app-wrapper">
    <!-- 背景装饰 -->
    <div class="bg-gradient"></div>
    <div class="bg-grid"></div>
    
    <div class="app-container">
      <!-- 顶部导航 -->
      <header class="app-header">
        <Header />
      </header>
      
      <!-- 主内容区域 - 完全填充 -->
      <main class="app-main">
        <!-- 左侧面板 -->
        <aside class="panel panel-left glass">
          <div class="panel-header">
            <h2>🤖 传输线模型</h2>
            <p>选择微带线、带状线等模型</p>
          </div>
          <ModelSelector />
        </aside>
        
        <!-- 中间面板 -->
        <section class="panel panel-center glass">
          <div class="panel-header">
            <h2>⚙️ 参数配置</h2>
            <p>输入物理参数开始计算</p>
          </div>
          <MaterialSelector />
          <ParameterForm />
        </section>
        
        <!-- 右侧面板 -->
        <aside class="panel panel-right glass">
          <div class="panel-header">
            <h2>📊 计算结果</h2>
            <p>实时显示阻抗分析数据</p>
          </div>
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
import { onMounted, watch } from 'vue'
import { useCalculationStore } from './stores/calculatorStore'
import { analyticsHit } from './api'
import ModelSelector from './components/ModelSelector.vue'
import MaterialSelector from './components/MaterialSelector.vue'
import ParameterForm from './components/ParameterForm.vue'
import ResultDisplay from './components/ResultDisplay.vue'
import Footer from './components/Footer.vue'
import Header from './components/Header.vue'

const store = useCalculationStore()

onMounted(async () => {
  try {
    await store.initializeApp()
    await analyticsHit(window.location.pathname)
    const loadingContainer = document.getElementById('loading-container')
    if (loadingContainer) loadingContainer.classList.add('hidden')
  } catch (error) {
    console.error('应用初始化失败:', error)
    const loadingContainer = document.getElementById('loading-container')
    if (loadingContainer) loadingContainer.classList.add('hidden')
  }
})

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
  font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

#app {
  width: 100%;
  height: 100%;
  height: 100dvh; /* 动态视口高度，解决移动端地址栏问题 */
  overflow: hidden;
}

/* 滚动条 */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.2); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.3); }
</style>

<style scoped>
/* 外层容器 - 填满整个窗口 */
.app-wrapper {
  width: 100%;
  height: 100%;
  height: 100dvh;
  overflow: hidden;
  position: relative;
  background: #0a0a0f;
}

/* 渐变背景 */
.bg-gradient {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: 
    radial-gradient(ellipse 80% 50% at 20% 40%, rgba(59, 130, 246, 0.15), transparent),
    radial-gradient(ellipse 60% 40% at 80% 60%, rgba(139, 92, 246, 0.1), transparent),
    radial-gradient(ellipse 50% 30% at 50% 80%, rgba(236, 72, 153, 0.08), transparent);
  pointer-events: none;
}

/* 网格背景 */
.bg-grid {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
  background-size: 40px 40px;
  pointer-events: none;
}

/* 内层容器 - 完全填充 */
.app-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: transparent;
}

/* 顶部导航 */
.app-header {
  flex-shrink: 0;
  padding: 12px 16px;
  background: rgba(255,255,255,0.02);
  border-bottom: 1px solid rgba(255,255,255,0.06);
}

/* 主内容区域 - 完全填充 */
.app-main {
  flex: 1;
  display: grid;
  grid-template-columns: minmax(240px, 1fr) minmax(300px, 2fr) minmax(240px, 1fr);
  gap: 16px;
  padding: 16px;
  min-height: 0;
  overflow: hidden;
}

/* 手机端响应式 - 单栏布局 */
@media (max-width: 768px) {
  .app-main {
    grid-template-columns: 1fr;
    gap: 12px;
    padding: 12px;
    overflow-y: auto;
    overflow-x: hidden;
  }
  
  .panel {
    min-width: 0;
    max-width: 100%;
  }
}

/* 玻璃面板 */
.glass {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px;
  backdrop-filter: blur(20px);
  box-shadow: 
    0 8px 32px rgba(0,0,0,0.3),
    inset 0 1px 0 rgba(255,255,255,0.05);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.panel {
  min-width: 0; /* 防止内容溢出 */
}

.panel-header {
  padding: 16px 18px 14px;
  border-bottom: 1px solid rgba(255,255,255,0.06);
  flex-shrink: 0;
}

.panel-header h2 {
  font-size: 14px;
  font-weight: 600;
  color: #fff;
  margin-bottom: 4px;
}

.panel-header p {
  font-size: 12px;
  color: rgba(255,255,255,0.4);
}

/* 底部 */
.app-footer {
  height: 36px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255,255,255,0.02);
  border-top: 1px solid rgba(255,255,255,0.04);
}
</style>
