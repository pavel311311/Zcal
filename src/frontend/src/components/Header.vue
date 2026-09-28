<template>
  <div class="welcome-header">
    <div class="header-content">
      <div class="title-section">
        <h1 class="app-title">
          <img
            src="/tudo500x500.png"
            alt="Logo"
            class="title-icon"
          >
          <span class="title-text">阻抗计算器</span>
          <small class="author-name">by 小土豆</small>
        </h1>
      </div>

      <div class="features-badges">
        <span class="feature-badge">⚡ 多模型</span>
        <span class="feature-badge">🎯 高精度</span>
        <span class="feature-badge">⚡ 实时计算</span>
      </div>

      <!-- 微信公众号 -->
      <div class="wechat-container">
        <div class="wechat-content">
          <img
            src="/wechat-icon.png"
            alt="WeChat"
            class="wechat-icon"
          >
          <span class="wechat-text">扫码关注</span>
        </div>
        <div class="qr-popup">
          <div class="qr-title">
            微信公众号
          </div>
          <img
            src="/wechat-qr.jpg"
            alt="微信公众号二维码"
            class="qr-code"
          >
          <div class="qr-footer">
            扫码关注获取更多内容
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.welcome-header {
  display: flex;
  align-items: center;
  width: 100%;
}

.header-content {
  display: flex;
  align-items: center;
  width: 100%;
  gap: 16px;
}

.title-section {
  flex: 1;
  min-width: 0;
  overflow: hidden;
}

.app-title {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #fff;
  white-space: nowrap;
}

.title-icon {
  width: 28px;
  height: 28px;
  object-fit: contain;
  border-radius: 6px;
  flex-shrink: 0;
}

.title-text {
  background: linear-gradient(135deg, #fff 0%, #a5b4fc 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.author-name {
  font-size: 11px;
  font-weight: 500;
  color: rgba(255,255,255,0.4);
  margin-left: 4px;
  white-space: nowrap;
}

.features-badges {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.feature-badge {
  padding: 5px 12px;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 20px;
  font-size: 11px;
  font-weight: 500;
  color: rgba(255,255,255,0.6);
  white-space: nowrap;
  transition: all 0.3s;
}

.feature-badge:hover {
  background: rgba(255,255,255,0.1);
  border-color: rgba(139, 92, 246, 0.3);
  color: #a78bfa;
}

/* 微信公众号 */
.wechat-container {
  position: relative;
  flex-shrink: 0;
  cursor: pointer;
}

.wechat-content {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 10px;
  transition: all 0.3s;
}

.wechat-content:hover {
  background: rgba(59, 130, 246, 0.15);
  border-color: rgba(59, 130, 246, 0.3);
}

.wechat-icon {
  width: 22px;
  height: 22px;
  flex-shrink: 0;
}

.wechat-text {
  font-size: 12px;
  font-weight: 500;
  color: rgba(255,255,255,0.8);
  white-space: nowrap;
}

.wechat-content:hover .wechat-text {
  color: #60a5fa;
}

/* 二维码弹出层 */
.qr-popup {
  position: absolute;
  top: calc(100% + 12px);
  right: 0;
  background: rgba(20, 20, 30, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 20px 50px rgba(0,0,0,0.5);
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 1000;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 260px;
}

.wechat-container:hover .qr-popup {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.qr-title {
  font-size: 14px;
  font-weight: 600;
  color: #fff;
  margin-bottom: 14px;
  text-align: center;
}

.qr-code {
  width: 200px;
  height: auto;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.3);
}

.qr-footer {
  font-size: 12px;
  color: rgba(255,255,255,0.5);
  margin-top: 14px;
  text-align: center;
}

/* 响应式 - 平板 */
@media (max-width: 768px) {
  .header-content {
    gap: 12px;
    flex-wrap: wrap;
  }
  
  .title-section {
    flex: 1 1 100%;
    min-width: 0;
  }
  
  .app-title {
    font-size: 14px;
    gap: 8px;
  }
  
  .title-icon {
    width: 24px;
    height: 24px;
  }
  
  .features-badges {
    display: none;
  }
  
  .wechat-container {
    flex-shrink: 0;
  }
  
  .wechat-content {
    padding: 6px 10px;
    gap: 6px;
  }
  
  .wechat-icon {
    width: 20px;
    height: 20px;
  }
  
  .wechat-text {
    font-size: 11px;
  }
  
  .qr-popup {
    right: 50%;
    transform: translateX(50%) translateY(-10px);
    min-width: 220px;
    padding: 16px;
  }
  
  .wechat-container:hover .qr-popup,
  .wechat-container:focus-within .qr-popup {
    transform: translateX(50%) translateY(0);
  }
  
  .qr-code {
    width: 180px;
  }
}

/* 响应式 - 小手机 */
@media (max-width: 480px) {
  .app-title {
    font-size: 13px;
    gap: 6px;
  }
  
  .title-icon {
    width: 22px;
    height: 22px;
  }
  
  .author-name {
    display: none;
  }
  
  .wechat-content {
    padding: 5px 8px;
  }
  
  .wechat-icon {
    width: 18px;
    height: 18px;
  }
  
  .wechat-text {
    font-size: 10px;
  }
  
  .qr-popup {
    min-width: 200px;
    padding: 14px;
  }
  
  .qr-code {
    width: 160px;
  }
  
  .qr-title {
    font-size: 13px;
    margin-bottom: 10px;
  }
  
  .qr-footer {
    font-size: 11px;
    margin-top: 10px;
  }
}
</style>
