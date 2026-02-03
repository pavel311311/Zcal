<template>
  <div class="welcome-header">
    <div class="header-content">
      <div class="title-section">
        <h1 class="app-title">
          <img src="/tudo500x500.png" alt="Logo" class="title-icon" />
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
// Welcome组件 - Mac风格顶部标题栏
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
  padding: 0 20px;
  gap: 24px;
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
  gap: 10px;
  font-size: 17px;
  font-weight: 600;
  margin: 0;
  color: #1d1d1f;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

.title-icon {
  width: 28px;
  height: 28px;
  object-fit: contain;
  transition: transform 0.2s ease;
}

.title-icon:hover {
  transform: scale(1.05);
}

.features-badges {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.feature-badge {
  padding: 4px 12px;
  background: #f2f2f7;
  border-radius: 16px;
  font-size: 11px;
  font-weight: 500;
  transition: all 0.2s ease;
  border: 1px solid #e2e2e7;
  color: #1d1d1f;
}

.feature-badge:hover {
  background: #ebebf0;
  border-color: #d2d2d7;
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
  padding: 8px 12px;
  border-radius: 8px;
  transition: background-color 0.2s ease;
}

.wechat-content:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.wechat-icon {
  width: 24px;
  height: 24px;
  transition: transform 0.2s ease;
}

.wechat-text {
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
  color: #1d1d1f;
  letter-spacing: 0.5px;
  display: inline-block;
  padding: 2px 0;
  transition: all 0.2s ease;
}

.wechat-text:hover {
  color: #0066cc;
}

.wechat-content:hover .wechat-text {
  transform: scale(1.02);
  transition: transform 0.2s ease;
}

.wechat-icon:hover {
  transform: scale(1.05);
}

.qr-popup {
  position: absolute;
  top: calc(100% + 10px);
  right: 0;
  background: white;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  opacity: 0;
  visibility: hidden;
  transform: translateY(-8px) scale(0.95);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 1000;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 320px;
  border: 1px solid #e2e2e7;
}

.wechat-container:hover .qr-popup {
  opacity: 1;
  visibility: visible;
  transform: translateY(0) scale(1);
}

.qr-code {
  width: 280px;
  height: auto;
  max-width: 100%;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
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
    gap: 8px;
    text-align: center;
    padding: 0 16px;
  }
  
  .features-badges {
    justify-content: center;
    gap: 6px;
  }
  
  .app-title {
    justify-content: center;
    font-size: 15px;
    gap: 8px;
  }
  
  .title-icon {
    width: 24px;
    height: 24px;
  }
}

@media (max-width: 768px) {
  .app-title {
    font-size: 14px;
  }
  
  .title-icon {
    width: 22px;
    height: 22px;
  }
  
  .feature-badge {
    padding: 3px 10px;
    font-size: 10px;
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
    width: 22px;
    height: 22px;
  }
}

@media (max-width: 480px) {
  .app-title {
    font-size: 13px;
  }
  
  .title-icon {
    width: 20px;
    height: 20px;
  }

  .wechat-text {
    display: none;
  }
  
  .wechat-icon {
    width: 22px;
    height: 22px;
  }
}

@media (max-width: 360px) {
  .wechat-container {
    display: none;
  }
}
</style>