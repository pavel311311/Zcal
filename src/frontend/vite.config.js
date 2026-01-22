import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  base: '/', // 确保基础路径正确
  server: {
    port: 3000,
    host: '0.0.0.0',
    proxy: {
      '/api': {
        target: process.env.VITE_API_URL || 'http://localhost:5000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '/api')
      }
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
    assetsDir: 'assets', // 明确指定资源目录
    rollupOptions: {
      output: {
        manualChunks: {
          'vue': ['vue'],
          'vendor': ['axios', 'pinia']
        },
        // 确保资源文件名一致
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
