import { createRouter, createWebHistory } from 'vue-router'
import { publicRoutes } from './public.routes'
import { studentRoutes } from './student.routes'
import { isTokenExpired } from '@/utils/auth'

// 学生端路由（管理端已独立为 admin-index.ts）
const routes = [
  ...publicRoutes,
  ...studentRoutes
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  if (!to.meta.requiresAuth) {
    next()
    return
  }

  const token = localStorage.getItem('token')
  if (!token) {
    next('/student/login')
    return
  }

  if (isTokenExpired(token)) {
    localStorage.removeItem('token')
    localStorage.removeItem('userInfo')
    next('/student/login')
    return
  }

  try {
    const userInfo = JSON.parse(localStorage.getItem('userInfo') || '{}')
    if (userInfo.role !== 'student') {
      localStorage.removeItem('token')
      localStorage.removeItem('userInfo')
      next('/student/login')
      return
    }
  } catch {
    localStorage.removeItem('token')
    localStorage.removeItem('userInfo')
    next('/student/login')
    return
  }

  next()
})

export default router
