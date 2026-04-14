<template>
  <div class="app-footer">
    <div class="footer-content">
      <span class="copyright">© 2025 Zcal 阻抗计算器</span>
      <div class="footer-right">
        <span class="author">Made by 芯片小土豆 🥔</span>
        <span class="divider">•</span>
        <AnalyticsBadge />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineAsyncComponent } from 'vue'
const AnalyticsBadge = defineAsyncComponent(() => import('./AnalyticsBadge.vue'))
</script>

<style scoped>
.app-footer {
  padding: 0 20px;
}

.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.copyright {
  font-size: 11px;
  color: rgba(255,255,255,0.3);
}

.footer-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.author {
  font-size: 11px;
  color: rgba(255,255,255,0.3);
}

.divider {
  color: rgba(255,255,255,0.15);
  font-size: 11px;
}
</style>
