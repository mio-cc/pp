import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

// 构建输出到 ../web，FastAPI 已把 web/ 挂到 /app/，无需改后端。
// base 用相对路径 './'，这样无论挂在 /app/ 还是根路径都能正确加载资源。
export default defineConfig({
  plugins: [vue()],
  base: './',
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  build: {
    outDir: '../web',
    emptyOutDir: true,
    chunkSizeWarningLimit: 1500,
    rollupOptions: {
      output: {
        manualChunks: {
          arco: ['@arco-design/web-vue'],
          vue: ['vue']
        }
      }
    }
  },
  server: {
    port: 5173,
    proxy: {
      // 开发模式把 /api 代理到本地 FastAPI
      '/api': 'http://127.0.0.1:8000'
    }
  }
})
