<template>
  <div class="analytics-badge" v-if="stats">
    <span class="badge-item">今日访问 {{ stats.daily_visits }}</span>
    <span class="separator">•</span>
    <span class="badge-item">历史访问 {{ stats.total_visits }}</span>
  </div>
  <div class="analytics-badge" v-else>
    <span class="badge-item">统计加载中</span>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getAnalyticsStats } from '../api'

const stats = ref(null)

const loadStats = async () => {
  try {
    stats.value = await getAnalyticsStats()
  } catch (e) {
    stats.value = null
  }
}

onMounted(async () => {
  await loadStats()
  setInterval(loadStats, 60000)
})
</script>

<style scoped>
.analytics-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 11px;
  color: #86868b;
}
.badge-item {
  white-space: nowrap;
}
.separator {
  color: #d1d1d6;
}
</style>
