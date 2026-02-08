// vite.config.ts
import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import Components from 'unplugin-vue-components/vite'
import { resolve } from 'path'

export default defineConfig(({ mode }) => {
  // 加载 .env 文件中的变量
  const env = loadEnv(mode, process.cwd())

  return {
    plugins: [
      vue(),
      Components({
        dts: true,
        resolvers: []
      })
    ],
    resolve: {
      alias: {
        '@': resolve(__dirname, 'src')
      }
    },
    server: {
      host: '0.0.0.0',
      port: 5173,
      proxy: {
        '/api': {
          target: 'http://localhost:8000',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, '')
        }
      }
    },
    define: {
      'process.env': env
    },
    optimizeDeps: {
      include: ['@tabler/icons-vue']
    }
  }
})
