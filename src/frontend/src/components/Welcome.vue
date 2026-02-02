<template>
  <div class="welcome-header">
    <div class="header-content">
      <div class="title-section">
        <h1 class="app-title">
          <span class="title-icon">⚡</span>
           阻抗计算工具
        </h1>
      </div>
      
      <div class="features-badges">
        <span class="feature-badge">多模型</span>
        <span class="feature-badge">高精度</span>
        <span class="feature-badge">实时计算</span>
      </div>

      <!-- 微信公众号 -->
      <div class="wechat-container">
        <img src="/wechat-icon.png" alt="WeChat" class="wechat-icon" />
        <div class="qr-popup">
          <img src="/wechat-qr.jpg" alt="扫码关注微信公众号" class="qr-code" />
          <p class="qr-text">扫码关注</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Welcome组件 - 极简顶部标题栏
</script>

<style scoped>
.welcome-header {
  height: 100%;
  display: flex;
  align-items: center;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1600px;
  margin: 0 auto;
  padding: 0 16px;
  gap: 20px;
  width: 100%;
}

.title-section {
  flex: 1;
  min-width: 0;
}

.app-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 700;
  margin: 0;
  color: white;
}

.title-icon {
  font-size: 20px;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
}

.features-badges {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.feature-badge {
  padding: 3px 8px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  backdrop-filter: blur(10px);
  font-size: 10px;
  font-weight: 500;
  transition: all 0.2s ease;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.feature-badge:hover {
  background: rgba(255, 255, 255, 0.25);
}

/* 微信公众号样式 */
.wechat-container {
  position: relative;
  flex-shrink: 0;
  cursor: pointer;
}

.wechat-icon {
  width: 28px;
  height: 28px;
  transition: transform 0.2s ease;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
}

.wechat-icon:hover {
  transform: scale(1.1);
}

.qr-popup {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 8px;
  background: white;
  border-radius: 8px;
  padding: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  opacity: 0;
  visibility: hidden;
  transform: translateY(-8px);
  transition: all 0.3s ease;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.wechat-container:hover .qr-popup {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.qr-code {
  width: 120px;
  height: 120px;
  border-radius: 4px;
}

.qr-text {
  font-size: 12px;
  color: #333;
  margin: 0;
  font-weight: 500;
}

/* 响应式设计 */
@media (max-width: 992px) {
  .header-content {
    flex-direction: column;
    gap: 6px;
    text-align: center;
    padding: 0 12px;
  }
  
  .features-badges {
    justify-content: center;
    gap: 6px;
  }
  
  .app-title {
    justify-content: center;
    font-size: 16px;
    gap: 6px;
  }
  
  .title-icon {
    font-size: 18px;
  }
}

@media (max-width: 768px) {
  .app-title {
    font-size: 14px;
  }
  
  .title-icon {
    font-size: 16px;
  }
  
  .feature-badge {
    padding: 2px 6px;
    font-size: 9px;
  }
}

@media (max-width: 480px) {
  .features-badges {
    display: none;
  }
  
  .app-title {
    font-size: 13px;
  }
  
  .title-icon {
    font-size: 15px;
  }

  .wechat-container {
    display: none;
  }
}
</style>