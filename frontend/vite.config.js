import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '127.0.0.1',
    strictPort: false,   // auto-pick next free port if 3000 is busy
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000',  // match Flask's bind address
        changeOrigin: true,
        secure: false,
      }
    }
  }
})
