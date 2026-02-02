import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  base: '/',
  define: {
    __DEV__: JSON.stringify(false)
  },
  server: {
    port: 3000,
    host: '0.0.0.0',
    // 配置API代理，解决跨域问题
    proxy: {
      '/api': {
        target: 'http://localhost:5000', // 使用服务器的实际IP地址
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '/api')
      }
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
    assetsDir: 'assets',
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true
      },
      format: {
        comments: false
      }
    },
    rollupOptions: {
      output: {
        manualChunks: {
          'vue': ['vue'],
          'vendor': ['axios', 'pinia']
        },
        assetFileNames: 'assets/[name]-[hash][extname]',
        chunkFileNames: 'assets/[name]-[hash].js',
        entryFileNames: 'assets/[name]-[hash].js'
      }
    }
  },
  // Cloudflare Pages优化
  preview: {
    port: 3000,
    host: '0.0.0.0'
  }
})
