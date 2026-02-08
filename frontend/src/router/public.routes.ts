import { RouteRecordRaw } from 'vue-router'

/**
 * 公共路由配置
 * 这些路由不需要认证即可访问
 */
export const publicRoutes: Array<RouteRecordRaw> = [
    {
        path: '/',
        name: 'home',
        component: () => import('../components/HomePage.vue'),
        meta: { title: '首页' }
    },
    {
        path: '/student/login',
        name: 'studentLogin',
        component: () => import('../components/student/login/LoginPage.vue'),
        meta: { title: '学生登录' }
    },
    {
        path: '/admin/login',
        name: 'adminLogin',
        component: () => import('../components/admin/login/AdminLogin.vue'),
        meta: { title: '管理端登录' }
    }
]
