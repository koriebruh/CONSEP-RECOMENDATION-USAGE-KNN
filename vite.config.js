import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  // Tambahkan konfigurasi untuk assets
  publicDir: 'public',
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
  },
})