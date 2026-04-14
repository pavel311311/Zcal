import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'

// 创建 Vue 应用实例
const app = createApp(App)

// 注册 Pinia 状态管理
app.use(createPinia())

// 挂载到 #app 容器
app.mount('#app')
