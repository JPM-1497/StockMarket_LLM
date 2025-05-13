// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0', // Required so Docker container can serve to your browser
    port: 3000,      // Ensure this matches the exposed port
    proxy: {
      '/api': 'http://backend:8000', // Proxy to FastAPI backend
    },
  },
});
