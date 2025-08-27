import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
import svgr from 'vite-plugin-svgr';

export default defineConfig(({ mode }) => {
  // Load env file based on `mode` in the current working directory.
  const env = loadEnv(mode, process.cwd(), '')
  
  return {
    plugins: [react(), svgr()],
    server: {
      proxy: {
        '/api': {
          target: env.BACKEND_API_URL,
          changeOrigin: true,
          configure: (proxy) => {
            console.log('Proxying /api to:', env.BACKEND_API_URL);
          }
        },
      },
    },
  }
})
