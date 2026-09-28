import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  base: '/',
  server: {
    port: 3000,
    host: '0.0.0.0',
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true
      }
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
    minify: 'esbuild',
    chunkSizeWarningLimit: 1000,
    cssCodeSplit: true,
    // ========== 性能优化配置 ==========
    // 手动分包策略：将 node_modules 和 vendor 代码分离
    rollupOptions: {
      output: {
        // 手动指定 chunk 分割策略
        manualChunks: {
          // Vue 核心库（很少变化，长期缓存）
          'vendor-vue': ['vue', 'pinia'],
          // Axios HTTP 客户端
          'vendor-axios': ['axios'],
        },
        // 静态资源命名
        assetFileNames: (assetInfo) => {
          const info = assetInfo.name || ''
          if (/\.(woff2?|eot|ttf|otf)$/i.test(info)) {
            return 'fonts/[name]-[hash][extname]'
          }
          if (/\.png|jpe?g|svg|gif|webp|avif$/i.test(info)) {
            return 'images/[name]-[hash][extname]'
          }
          return 'assets/[name]-[hash][extname]'
        },
        // 动态导入 chunk 命名
        chunkFileNames: 'assets/js/[name]-[hash].js',
        entryFileNames: 'assets/js/[name]-[hash].js',
      },
    },
    // 启用 CSS 资源映射（开发用）
    cssDevSourcemap: true,
  },
  css: {
    devSourcemap: true
  },
  esbuild: {
    // 生产构建移除 console 和 debugger
    drop: ['console', 'debugger'],
    // 目标环境
    target: 'es2020',
  },
  // 解析别名
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  // 依赖优化
  optimizeDeps: {
    include: ['vue', 'pinia', 'axios'],
  },
})
