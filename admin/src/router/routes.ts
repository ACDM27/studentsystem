import { RouteRecordRaw } from 'vue-router'

export const adminRoutes: Array<RouteRecordRaw> = [
    {
        path: '/admin',
        component: () => import('../layout/AdminLayout.vue'),
        meta: { requiresAuth: true, role: 'admin' },
        children: [
            {
                path: 'dashboard',
                name: 'adminDashboard',
                component: () => import('../components/admin/dashboard/AdminDashboard.vue'),
                meta: { title: '管理端仪表盘' }
            },
            {
                path: 'achievements',
                name: 'adminAchievements',
                component: () => import('../components/admin/achievement/AchievementList.vue'),
                meta: { title: '成果审核' }
            }
        ]
    }
]
