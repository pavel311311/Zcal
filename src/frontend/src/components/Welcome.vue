<template>
  <div class="welcome-header">
    <div class="header-content">
      <div class="title-section">
        <h1 class="app-title">
          <span class="title-icon">⚡</span>
          PCB 阻抗计算工具
        </h1>
        <p class="app-subtitle">精确的传输线阻抗计算</p>
      </div>
      
      <div class="features-badges">
        <span class="feature-badge">
          <span class="badge-icon">🎯</span>
          多模型
        </span>
        <span class="feature-badge">
          <span class="badge-icon">📐</span>
          高精度
        </span>
        <span class="feature-badge">
          <span class="badge-icon">⚡</span>
          实时计算
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
// Welcome组件 - 紧凑的顶部标题栏
</script>

<style scoped>
.welcome-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 16px 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
  gap: 24px;
}

.title-section {
  flex: 1;
  min-width: 0;
}

.app-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 24px;
  font-weight: 700;
  margin: 0 0 4px 0;
  color: white;
}

.title-icon {
  font-size: 28px;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
}

.app-subtitle {
  font-size: 14px;
  opacity: 0.9;
  margin: 0;
  font-weight: 400;
}

.features-badges {
  display: flex;
  gap: 12px;
  flex-shrink: 0;
}

.feature-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 20px;
  backdrop-filter: blur(10px);
  font-size: 12px;
  font-weight: 500;
  transition: all 0.2s ease;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.feature-badge:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: translateY(-1px);
}

.badge-icon {
  font-size: 14px;
}

/* 响应式设计 */
@media (max-width: 992px) {
  .header-content {
    flex-direction: column;
    gap: 12px;
    text-align: center;
  }
  
  .features-badges {
    justify-content: center;
    flex-wrap: wrap;
    gap: 8px;
  }
  
  .app-title {
    justify-content: center;
    font-size: 22px;
  }
  
  .title-icon {
    font-size: 24px;
  }
}

@media (max-width: 768px) {
  .welcome-header {
    padding: 12px 0;
  }
  
  .header-content {
    padding: 0 16px;
    gap: 8px;
  }
  
  .app-title {
    font-size: 20px;
    gap: 8px;
  }
  
  .title-icon {
    font-size: 22px;
  }
  
  .app-subtitle {
    font-size: 13px;
  }
  
  .feature-badge {
    padding: 4px 8px;
    font-size: 11px;
    gap: 4px;
  }
  
  .badge-icon {
    font-size: 12px;
  }
}

@media (max-width: 480px) {
  .features-badges {
    display: none; /* 在超小屏幕上隐藏功能标签 */
  }
  
  .app-title {
    font-size: 18px;
  }
  
  .title-icon {
    font-size: 20px;
  }
}

/* 打印样式 */
@media print {
  .welcome-header {
    background: white !important;
    color: black !important;
    box-shadow: none;
    border-bottom: 2px solid #000;
  }
  
  .features-badges {
    display: none;
  }
}
</style>