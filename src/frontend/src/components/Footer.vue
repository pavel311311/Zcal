<template>
  <div class="app-footer">
    <div class="footer-content">
      <p class="copyright">
        &copy; 2025 RF Impedance Calculator. All rights reserved.
      </p>
      <div class="footer-links">
        <span class="footer-link">Made with ❤️</span>
        <span class="footer-separator">•</span>
        <span class="footer-link">Version 1.0</span>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>
<style scoped>
.app-footer {
  background: #8b8e93;
  color: #d1d5db;
  padding: 0;
  height: 30px; /* 固定高度，非常窄 */
  flex-shrink: 0;
}

.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1400px;
  margin: 0 auto;
  padding: 6px 16px; /* 大幅减少内边距 */
  height: 100%;
}

.copyright {
  font-size: 11px; /* 更小的字体 */
  margin: 0;
  line-height: 1.2;
}

.footer-links {
  display: flex;
  align-items: center;
  gap: 6px; /* 减少间距 */
  font-size: 11px; /* 更小的字体 */
}

.footer-link {
  color: #9ca3af;
  transition: color 0.2s ease;
  line-height: 1.2;
}

.footer-link:hover {
  color: #d1d5db;
}

.footer-separator {
  color: #6b7280;
}

@media (max-width: 768px) {
  .footer-content {
    flex-direction: row; /* 保持水平布局 */
    gap: 4px;
    text-align: center;
    padding: 4px 12px; /* 移动端更小的内边距 */
  }
  
  .footer-links {
    justify-content: center;
    gap: 4px;
  }
  
  .copyright,
  .footer-links {
    font-size: 10px; /* 移动端更小字体 */
  }
}
</style>