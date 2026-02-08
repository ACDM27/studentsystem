import { createRouter, createWebHistory } from 'vue-router'
import { publicRoutes } from './public.routes'
import { studentRoutes } from './student.routes'
import { adminRoutes } from './admin.routes'
import { isTokenExpired } from '@/utils/auth'

/**
 * 主路由配置
 * 组合公共路由、学生端路由和管理端路由
 */
const routes = [
  ...publicRoutes,
  ...studentRoutes,
  ...adminRoutes
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

/**
 * 全局前置守卫 - 权限验证
 */
router.beforeEach((to, from, next) => {
  console.log('路由守卫检查:', {
    to: to.path,
    from: from.path,
    requiresAuth: to.meta.requiresAuth,
    role: to.meta.role
  })

  // 如果路由需要认证
  if (to.meta.requiresAuth) {
    // 检查是否有token
    const token = localStorage.getItem('token')
    const userInfoStr = localStorage.getItem('userInfo')

    console.log('Token检查:', token ? '存在' : '不存在')

    if (!token) {
      // 没有token，根据目标路径跳转到对应登录页
      console.log('未登录，重定向到登录页')
      if (to.path.startsWith('/admin')) {
        next('/admin/login')
      } else {
        next('/student/login')  // ✅ 修复：使用规范的学生端登录路由
      }
      return
    }

    // 检查Token是否过期
    if (isTokenExpired(token)) {
      console.log('Token已过期，清除并重定向')
      localStorage.removeItem('token')
      localStorage.removeItem('userInfo')

      if (to.path.startsWith('/admin')) {
        next('/admin/login')
      } else {
        next('/student/login')
      }
      return
    }

    // 验证角色权限
    try {
      const userInfo = JSON.parse(userInfoStr || '{}')
      const requiredRole = to.meta.role as string | undefined

      if (requiredRole && userInfo.role !== requiredRole) {
        console.log('权限不足:', { userRole: userInfo.role, requiredRole })
        // 角色不匹配，跳转到对应的首页
        if (userInfo.role === 'admin') {
          next('/admin/dashboard')
        } else {
          next('/student/dashboard')
        }
        return
      }
    } catch (error) {
      console.error('解析用户信息失败:', error)
      // 解析失败，清除token，跳转登录
      localStorage.removeItem('token')
      localStorage.removeItem('userInfo')
      if (to.path.startsWith('/admin')) {
        next('/admin/login')
      } else {
        next('/student/login')  // ✅ 修复：使用规范的学生端登录路由
      }
      return
    }

    // 有token且角色匹配，继续导航
    console.log('已登录且权限验证通过，允许访问')
    next()
  } else {
    // 不需要认证的路由，直接通过
    console.log('公开路由，直接通过')
    next()
  }
})

export default router
