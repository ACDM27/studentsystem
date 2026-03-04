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
        // 代理 API 请求到后端（不做 rewrite，保持路径原样转发）
        '/api': {
          target: 'http://localhost:8000',
          changeOrigin: true
        },
        // 代理上传文件/证书图片访问到后端（修复管理员查看证书图片失败问题）
        '/uploads': {
          target: 'http://localhost:8000',
          changeOrigin: true
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
