import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  base: '/BubblePopKungFu/',
  plugins: [vue()],
  server: {
    port: 9202,
    cors: true,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization'
    },
    https: false
  },
  build: {
    chunkSizeWarningLimit: 1600,
    rollupOptions: {
      external: ['@mediapipe/pose', '@mediapipe/camera_utils', '@mediapipe/drawing_utils'],
      output: {
        assetFileNames: (assetInfo) => {
          if (assetInfo.name.endsWith('.css')) {
            return 'Assets/css/[name]-[hash][extname]'
          }
          return 'Assets/[name]-[hash][extname]'
        },
        chunkFileNames: 'Assets/js/[name]-[hash].js',
        entryFileNames: 'Assets/js/[name]-[hash].js'
      }
    }
  }
}) 
