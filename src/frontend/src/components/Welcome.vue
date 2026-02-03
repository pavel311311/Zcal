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
        <div class="wechat-content">
          <img src="/wechat-icon.png" alt="WeChat" class="wechat-icon" />
          <span class="wechat-text">扫码关注</span>
        </div>
        <div class="qr-popup">
          <img src="/wechat-qr.png" alt="微信公众号" class="qr-code" />
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
  width: 100%;
}

.header-content {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 0 16px;
  gap: 20px;
}

.title-section {
  flex: 1;
  min-width: 0;
}

.wechat-container {
  margin-left: auto;
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
  margin-left: auto;
  position: relative;
  flex-shrink: 0;
  cursor: pointer;
}

.wechat-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

.wechat-icon {
  width: 28px;
  height: 28px;
  transition: transform 0.2s ease;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
}

.wechat-text {
  font-size: 12px;
  font-weight: 500;
  color: white;
  white-space: nowrap;
}

.wechat-icon:hover {
  transform: scale(1.1);
}

.qr-popup {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  background: white;
  border-radius: 10px;
  padding: 12px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.18);
  opacity: 0;
  visibility: hidden;
  transform: translateY(-8px) scale(0.95);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 1000;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 380px;
  border: 1px solid rgba(0, 0, 0, 0.08);
}

.wechat-container:hover .qr-popup {
  opacity: 1;
  visibility: visible;
  transform: translateY(0) scale(1);
}

.qr-code {
  width: 360px;
  height: auto;
  max-width: 100%;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  object-fit: contain;
  transition: transform 0.2s ease;
}

.qr-code:hover {
  transform: scale(1.02);
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

@media (max-width: 576px) {
  .features-badges {
    display: none;
  }
  
  .app-title {
    font-size: 14px;
  }
  
  .title-icon {
    font-size: 16px;
  }
}

@media (max-width: 480px) {
  .app-title {
    font-size: 13px;
  }
  
  .title-icon {
    font-size: 15px;
  }

  .wechat-text {
    display: none;
  }
  
  .wechat-icon {
    width: 24px;
    height: 24px;
  }
}

@media (max-width: 400px) {
  .app-title {
    font-size: 12px;
  }
  
  .title-icon {
    font-size: 14px;
  }
}

@media (max-width: 360px) {
  .wechat-container {
    display: none;
  }
}
</style>