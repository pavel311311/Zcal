<template>
  <div class="app-footer">
    <div class="footer-content">
      <p class="copyright">
        &copy; 2025 PCB Impedance Calculator. All rights reserved.
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
  background: #374151;
  color: #d1d5db;
  padding: 0;
}

.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1400px;
  margin: 0 auto;
  padding: 16px 20px;
}

.copyright {
  font-size: 14px;
  margin: 0;
}

.footer-links {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}

.footer-link {
  color: #9ca3af;
  transition: color 0.2s ease;
}

.footer-link:hover {
  color: #d1d5db;
}

.footer-separator {
  color: #6b7280;
}

@media (max-width: 768px) {
  .footer-content {
    flex-direction: column;
    gap: 8px;
    text-align: center;
  }
  
  .footer-links {
    justify-content: center;
  }
}
</style>