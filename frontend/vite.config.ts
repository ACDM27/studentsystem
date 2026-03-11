// vite.config.ts
import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import Components from 'unplugin-vue-components/vite'
import { resolve } from 'path'
import { readFileSync } from 'fs'
import type { Plugin } from 'vite'

// 开发服务器插件：/admin/* 路径直接响应 admin.html（经过 Vite 转换）
// 使用 transformIndexHtml 直接返回响应，而非 URL 重写，避免 SPA fallback 中间件干扰
function adminRewritePlugin(): Plugin {
  return {
    name: 'admin-rewrite',
    configureServer(server) {
      server.middlewares.use(async (req, res, next) => {
        if (!req.url) return next()

        // 从 URL 中提取 pathname（排除 query string）
        const pathname = req.url.split('?')[0]

        // 匹配 /admin/* 路径，排除已有扩展名的文件请求（.js .ts .vue 等）
        const isAdminPage =
          pathname.startsWith('/admin') &&
          !pathname.startsWith('/admin.html') &&
          !pathname.includes('.')

        if (!isAdminPage) return next()

        const adminHtmlPath = resolve(__dirname, 'admin.html')
        const adminHtml = readFileSync(adminHtmlPath, 'utf-8')
        const transformed = await server.transformIndexHtml(req.url, adminHtml)
        res.statusCode = 200
        res.setHeader('Content-Type', 'text/html; charset=utf-8')
        res.end(transformed)
      })
    }
  }
}

export default defineConfig(({ mode }) => {
  // 加载 .env 文件中的变量
  const env = loadEnv(mode, process.cwd())

  return {
    plugins: [
      vue(),
      Components({
        dts: true,
        resolvers: []
      }),
      adminRewritePlugin()
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
          changeOrigin: true
        },
        '/uploads': {
          target: 'http://localhost:8000',
          changeOrigin: true
        }
      }
    },
    build: {
      rollupOptions: {
        input: {
          main: resolve(__dirname, 'index.html'),
          admin: resolve(__dirname, 'admin.html')
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
