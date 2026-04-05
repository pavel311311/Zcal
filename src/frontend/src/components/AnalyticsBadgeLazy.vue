/**
 * Analytics 组件 - 延迟加载以减少初始包大小
 * @file 使用动态导入实现代码分割
 */

export default {
  name: 'AnalyticsBadge',
  setup() {
    // 懒加载 analytics 模块
    return () => import('./AnalyticsBadge.vue')
  }
}
