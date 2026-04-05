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
    rollupOptions: {
      output: {
        manualChunks: {
          'vue-vendor': ['vue', 'pinia'],
          'pinia': ['pinia'],
          'vendor': ['axios'],
          'styles': [] // Will be extracted separately
        },
        chunkFileNames: 'assets/js/[name]-[hash].js',
        entryFileNames: 'assets/js/[name]-[hash].js',
        assetFileNames: 'assets/[ext]/[name]-[hash].[ext]'
      },
      // Optimize for better tree-shaking
      treeshake: {
        moduleSideEffects: false,
        propertyReadSideEffects: false
      }
    },
    chunkSizeWarningLimit: 1000,
    cssCodeSplit: true
  },
  optimizeDeps: {
    include: ['vue', 'pinia', 'axios'],
    exclude: []
  },
  css: {
    devSourcemap: true
  },
  // Performance optimization for large bundles
  esbuild: {
    drop: ['console', 'debugger']
  }
})
