import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// 构建输出到 ../web，FastAPI 已把 web/ 挂到 /app/。base 相对路径，挂任意路径都能加载。
export default defineConfig({
  plugins: [vue()],
  base: './',
  build: { outDir: '../web', emptyOutDir: true, chunkSizeWarningLimit: 1500 },
  server: { port: 5173, proxy: { '/api': 'http://127.0.0.1:8000' } }
})
