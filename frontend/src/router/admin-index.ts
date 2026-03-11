import { createRouter, createWebHistory } from 'vue-router'
import { adminRoutes } from './admin.routes'
import { isTokenExpired } from '@/utils/auth'

const routes = [
    {
        path: '/admin/login',
        name: 'adminLogin',
        component: () => import('../components/admin/login/AdminLogin.vue'),
        meta: { title: '管理端登录' }
    },
    ...adminRoutes,
    // 根路径和 /admin 都重定向到登录页
    {
        path: '/',
        redirect: '/admin/login'
    }
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
        next('/admin/login')
        return
    }

    if (isTokenExpired(token)) {
        localStorage.removeItem('token')
        localStorage.removeItem('userInfo')
        next('/admin/login')
        return
    }

    try {
        const userInfo = JSON.parse(localStorage.getItem('userInfo') || '{}')
        if (userInfo.role !== 'admin') {
            localStorage.removeItem('token')
            localStorage.removeItem('userInfo')
            next('/admin/login')
            return
        }
    } catch {
        localStorage.removeItem('token')
        localStorage.removeItem('userInfo')
        next('/admin/login')
        return
    }

    next()
})

export default router
