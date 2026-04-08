<script setup lang="ts">
/**
 * Analytics 组件 - 延迟加载以减少初始包大小
 * 使用 defineAsyncComponent 实现代码分割
 */
import { defineAsyncComponent } from 'vue'

const AnalyticsBadge = defineAsyncComponent(() => import('./AnalyticsBadge.vue'))
</script>

<template>
  <Suspense>
    <template #default>
      <AnalyticsBadge />
    </template>
    <template #fallback>
      <!-- 加载中不显示占位，保持页面简洁 -->
    </template>
  </Suspense>
</template>
