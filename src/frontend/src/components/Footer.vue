<template>
  <div class="app-footer">
    <div class="footer-content">
      <p class="copyright">
        &copy; 2025 RF Impedance Calculator. All rights reserved.
      </p>
      <div class="footer-links">
        <span class="footer-link">Made by 芯片小土豆🥔</span>
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
  background: #f5f5f7;
  color: #86868b;
  padding: 0;
  height: 32px;
  flex-shrink: 0;
  border-top: 1px solid #e3e3e3;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1600px;
  margin: 0 auto;
  padding: 6px 20px;
  height: 100%;
}

.copyright {
  font-size: 11px;
  margin: 0;
  line-height: 1.2;
}

.footer-links {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 11px;
}

.footer-link {
  color: #86868b;
  transition: color 0.2s ease;
  line-height: 1.2;
}

.footer-link:hover {
  color: #1d1d1f;
}

.footer-separator {
  color: #d1d1d6;
}

@media (max-width: 768px) {
  .footer-content {
    flex-direction: row;
    gap: 6px;
    text-align: center;
    padding: 6px 16px;
  }
  
  .footer-links {
    justify-content: center;
    gap: 6px;
  }
  
  .copyright,
  .footer-links {
    font-size: 10px;
  }
}

@media (max-width: 480px) {
  .footer-content {
    flex-direction: column;
    gap: 2px;
    padding: 4px 12px;
  }
  
  .copyright {
    font-size: 9px;
  }
  
  .footer-links {
    font-size: 9px;
    gap: 4px;
  }
}
</style>