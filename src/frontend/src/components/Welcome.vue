<template>
  <div class="welcome-container">
    <div class="welcome-content">
      <h1 class="welcome-title">
        <span class="title-icon">⚡</span>
        PCB 阻抗计算工具
      </h1>
      <p class="welcome-subtitle">精确的传输线阻抗计算，支持多种PCB传输线模型</p>
      
      <div class="features-grid">
        <div class="feature-item">
          <span class="feature-icon">🎯</span>
          <span class="feature-text">多种传输线模型</span>
        </div>
        <div class="feature-item">
          <span class="feature-icon">📐</span>
          <span class="feature-text">精确阻抗计算</span>
        </div>
        <div class="feature-item">
          <span class="feature-icon">🎨</span>
          <span class="feature-text">友好用户界面</span>
        </div>
        <div class="feature-item">
          <span class="feature-icon">⚡</span>
          <span class="feature-text">实时结果展示</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Welcome组件 - 顶部欢迎区域
</script>

<style scoped>
.welcome-container {
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
}

.welcome-content {
  padding: 20px 0;
}

.welcome-title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  font-size: 32px;
  font-weight: 700;
  margin: 0 0 12px 0;
  color: white;
}

.title-icon {
  font-size: 36px;
}

.welcome-subtitle {
  font-size: 18px;
  opacity: 0.9;
  margin: 0 0 32px 0;
  line-height: 1.5;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
  max-width: 600px;
  margin: 0 auto;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  backdrop-filter: blur(10px);
  transition: all 0.2s ease;
}

.feature-item:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.feature-icon {
  font-size: 20px;
}

.feature-text {
  font-size: 14px;
  font-weight: 500;
}

@media (max-width: 768px) {
  .welcome-title {
    font-size: 24px;
    flex-direction: column;
    gap: 8px;
  }
  
  .title-icon {
    font-size: 28px;
  }
  
  .welcome-subtitle {
    font-size: 16px;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
}
</style>