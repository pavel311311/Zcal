<template>
  <div class="welcome-container">
    <h2>欢迎使用阻抗计算工具</h2>
    <p>这是一个精确的传输线阻抗计算工具，支持多种PCB传输线模型的阻抗计算。</p>
    
    <div class="features">
      <h3>主要功能</h3>
      <ul>
        <li>支持多种传输线模型</li>
        <li>精确的阻抗计算</li>
        <li>友好的用户界面</li>
        <li>实时计算结果展示</li>
      </ul>
    </div>

    <div class="img-container">
      <img src="/GSG.png" alt="示例图片" style="max-width: 100%; max-height: 100%;" />
    </div>
  </div>
</template>

<script setup>
// 简化的Welcome组件，只包含欢迎信息
</script>

<style scoped>
.welcome-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.features {
  margin: 15px 0;
}

.features ul {
  list-style-type: disc;
  padding-left: 20px;
  margin-top: 8px;
}

.features li {
  margin-bottom: 5px;
  color: #555;
}

/* 背景框+居中容器 */
.img-container {
  /* 水平居中 */
  margin: 20px auto;
  /* 淡化背景 + 圆角（视觉柔和） */
  background-color: #f5f5f5;
  border-radius: 8px;
  /* 内边距（背景框和图片的间距） */
  padding: 20px;
  /* 限制容器宽度（可选，根据需求调整） */
  max-width: 600px;
  /* 图片垂直+水平居中 */
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
