import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import naiveUI from './plugins/naive-ui' // 导入Naive UI插件
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
// 导入API调试工具
// import './utils/api-debug' // 已注释：文件不存在

// 创建Vue应用实例
const app = createApp(App)

// 注册全局组件和插件
app.use(router)
app.use(store)
app.use(naiveUI)
app.use(ElementPlus)

// 挂载应用
app.mount('#app')

// 开发环境下的调试信息
try {
  if (typeof import.meta !== 'undefined' && import.meta.env && import.meta.env.VITE_API_BASE_URL) {
    console.log('应用运行在开发模式')
    console.log('API_BASE_URL:', import.meta.env.VITE_API_BASE_URL)
  }
} catch (error) {
  console.warn('无法获取环境变量:', error)
}