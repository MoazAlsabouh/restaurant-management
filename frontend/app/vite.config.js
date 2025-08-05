import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  // تحميل متغيرات البيئة من ملف .env في مجلد المشروع
  const env = loadEnv(mode, process.cwd());

  return {
    base: '/restaurant-management/',  // أضف هذا السطر لضبط قاعدة المسارات
    plugins: [react()],
    server: {
      proxy: {
        '/api': {
          target: env.VITE_API_BASE_URL,
          changeOrigin: true,
          secure: false,
        }
      }
    }
  }
})