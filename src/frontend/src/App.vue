<template>
  <h1>阻抗计算器</h1>
  <p>精确的传输线阻抗计算工具</p>
  <div class="page-container">
    <!-- 三列布局容器 -->
    <div class="three-col-layout">
      <!-- 左列 -->
      <div class="col col-1">
        <Welcome />
      </div>
      <!-- 中列 -->
      <div class="col col-2">
        <ModelForm />
      </div>
      <!-- 右列 -->
      <div class="col col-3">
        <ResultDisplay />
      </div>
    </div>
  </div>
</template>

<script setup>
import ResultDisplay from './components/ResultDisplay.vue'
import Welcome from './components/Welcome.vue'
import ModelForm from './components/ModelForm.vue'
</script>

<style scoped>
/* 全局重置，消除默认边距和盒模型问题 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* 页面容器：确保占满浏览器可视区域，居中且有最小宽度 */
.page-container {
  width: 100%;
  max-width: 1440px;
  /* 限制最大宽度，避免大屏拉伸 */
  min-width: 320px;
  /* 适配移动端最小宽度 */
  margin: 0 auto;
  /* 水平居中 */
  padding: 20px;
  height: 100vh;
  /* 占满浏览器可视高度 */
}

/* 三列布局容器：核心 Flex 配置 */
.three-col-layout {
  display: flex;
  /* 启用 Flex 布局 */
  gap: 20px;
  /* 列之间的间距（替代 margin，更简洁） */
  height: 100%;
  /* 继承容器高度 */
}

/* 三列通用样式 */
.col {
  border: 1px solid #e5e7eb;
  /* 边框便于区分区域 */
  border-radius: 8px;
  /* 圆角优化视觉 */
  padding: 16px;
  background-color: #f9fafb;
  /* 溢出内容滚动，避免布局错乱 */
  overflow: auto;
}

/* 方案1：三列等分（最常用） */
.col-1,
.col-2,
.col-3 {
  flex: 1;
  /* 每列占比相同，自动平分剩余空间 */
}

/* 方案2：固定宽度 + 自适应（按需替换） */
/* .col-1 { width: 200px; }  左列固定200px */
/* .col-2 { flex: 1; }       中列自适应 */
/* .col-3 { width: 300px; }  右列固定300px */

/* 响应式适配：移动端自动堆叠为单列 */
@media (max-width: 768px) {
  .three-col-layout {
    flex-direction: column;
    /* 从横向改为纵向 */
    gap: 16px;
    /* 减小间距 */
  }

  /* 移动端每列占满宽度，高度自适应 */
  .col {
    height: auto;
    min-height: 200px;
    /* 保证最小高度 */
  }
}
</style>