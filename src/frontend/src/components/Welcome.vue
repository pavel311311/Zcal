<template>
  <div class="welcome-header">
    <div class="header-content">
      <div class="title-section">
        <h1 class="app-title">
          <img src="/tudo500x500.png" alt="Logo" class="title-icon" />
          阻抗计算器<small class="author-name">小土豆</small>
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
          <div class="qr-title">微信公众号</div>
          <img src="/wechat-qr.jpg" alt="微信公众号" class="qr-code" />
          <div class="qr-footer">扫码关注获取更多内容</div>
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
  overflow-x: hidden;
}

.header-content {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 0 16px;
  gap: 16px;
  overflow-x: hidden;
  box-sizing: border-box;
}

.title-section {
  flex: 1;
  min-width: 0;
  overflow: hidden;
}

.wechat-container {
  margin-left: auto;
  flex-shrink: 0;
}

.app-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 17px;
  font-weight: 600;
  margin: 0;
  color: #1d1d1f;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  overflow: hidden;
  white-space: nowrap;
}

.author-name {
  font-size: 0.65em;
  font-weight: 500;
  color: #6e6e73;
  margin-left: 1px;
  font-style: normal;
  margin-bottom: 2px;
  line-height: 1;
  white-space: nowrap;
}

.title-icon {
  width: 28px;
  height: 28px;
  object-fit: contain;
  transition: transform 0.2s ease;
  flex-shrink: 0;
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
  white-space: nowrap;
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
  gap: 6px;
  padding: 8px 12px;
  border-radius: 8px;
  transition: background-color 0.2s ease;
  border: 1px solid #e2e2e7;
  background: white;
}

.wechat-content:hover {
  background-color: #f2f2f7;
}

.wechat-icon {
  width: 20px;
  height: 20px;
  transition: transform 0.2s ease;
  flex-shrink: 0;
}

.wechat-text {
  font-size: 12px;
  font-weight: 500;
  white-space: nowrap;
  color: #1d1d1f;
  letter-spacing: 0.5px;
  display: inline-block;
  padding: 2px 0;
  transition: all 0.2s ease;
  flex-shrink: 0;
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

/* 二维码弹出层 - 居中显示 */
.qr-popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) scale(0.95);
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15);
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 1000;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 280px;
  max-width: 90vw;
  border: 1px solid #e2e2e7;
}

.wechat-container:hover .qr-popup {
  opacity: 1;
  visibility: visible;
  transform: translate(-50%, -50%) scale(1);
}

.qr-code {
  width: 260px;
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

/* 添加二维码标题 */
.qr-title {
  font-size: 14px;
  font-weight: 600;
  color: #1d1d1f;
  margin-bottom: 12px;
  text-align: center;
}

.qr-footer {
  font-size: 12px;
  color: #86868b;
  margin-top: 12px;
  text-align: center;
}

/* 响应式设计 - 优化手机端显示 */
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
  .header-content {
    flex-direction: row;
    align-items: center;
    gap: 12px;
    padding: 0 12px;
  }

  .title-section {
    flex: 1;
    min-width: 0;
  }

  .app-title {
    justify-content: flex-start;
    font-size: 14px;
    gap: 6px;
    overflow: hidden;
  }

  .title-icon {
    width: 22px;
    height: 22px;
  }

  .author-name {
    font-size: 0.6em;
    margin-left: 1px;
    white-space: nowrap;
  }

  .features-badges {
    display: none;
  }

  .wechat-content {
    padding: 5px 8px;
  }

  .wechat-icon {
    width: 22px;
    height: 22px;
  }

  .wechat-text {
    font-size: 12px;
  }

  .qr-popup {
    min-width: 260px;
    padding: 12px;
  }

  .qr-code {
    width: 220px;
  }
}

@media (max-width: 480px) {
  .header-content {
    gap: 8px;
    padding: 0 8px;
  }

  .app-title {
    font-size: 13px;
    gap: 5px;
  }

  .title-icon {
    width: 20px;
    height: 20px;
  }

  .author-name {
    font-size: 0.55em;
  }

  /* 确保在手机端也显示"扫描关注"文字 */
  .wechat-text {
    display: inline-block;
    font-size: 11px;
  }

  .wechat-icon {
    width: 18px;
    height: 18px;
  }

  .wechat-content {
    padding: 5px 8px;
    gap: 4px;
  }

  .qr-popup {
    min-width: 240px;
    padding: 15px;
  }

  .qr-title {
    font-size: 13px;
    margin-bottom: 10px;
  }

  .qr-code {
    width: 200px;
  }

  .qr-footer {
    font-size: 11px;
    margin-top: 10px;
  }
}

@media (max-width: 360px) {
  .app-title {
    font-size: 12px;
  }

  .title-icon {
    width: 18px;
    height: 18px;
  }

  .author-name {
    font-size: 0.5em;
  }

  .wechat-container {
    margin-left: 4px;
  }

  .wechat-icon {
    width: 16px;
    height: 16px;
  }

  .wechat-text {
    font-size: 10px;
  }

  .wechat-content {
    padding: 4px 6px;
    gap: 3px;
  }

  .qr-popup {
    min-width: 200px;
    padding: 12px;
  }

  .qr-title {
    font-size: 12px;
    margin-bottom: 8px;
  }

  .qr-code {
    width: 180px;
  }

  .qr-footer {
    font-size: 10px;
    margin-top: 8px;
  }
}

/* 确保在所有手机端都能正确显示 */
@media (max-width: 320px) {
  .app-title {
    font-size: 11px;
  }

  .title-icon {
    width: 16px;
    height: 16px;
  }

  .author-name {
    display: none;
  }

  .wechat-icon {
    width: 14px;
    height: 14px;
  }

  .wechat-text {
    font-size: 9px;
  }

  .wechat-content {
    padding: 3px 5px;
    gap: 2px;
  }

  .qr-popup {
    min-width: 180px;
    padding: 10px;
  }

  .qr-title {
    font-size: 11px;
    margin-bottom: 6px;
  }

  .qr-code {
    width: 160px;
  }

  .qr-footer {
    font-size: 9px;
    margin-top: 6px;
  }
}
</style>