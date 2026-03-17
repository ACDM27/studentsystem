import { RouteRecordRaw } from 'vue-router'

/**
 * 学生端路由配置
 * 所有路由都需要 student 角色权限
 */
export const studentRoutes: Array<RouteRecordRaw> = [
    // 学生端主路由
    {
        path: '/student',
        component: () => import('../layout/StudentLayout.vue'),
        meta: { requiresAuth: true, role: 'student' },
        children: [
            {
                path: 'achievement',
                name: 'studentAchievement',
                component: () => import('../components/student/honors/achievement.vue'),
                meta: { title: '成果收集与展示' }
            },
            {
                path: 'achievement-collect',
                name: 'achievementCollect',
                component: () => import('../components/student/honors/achievement-collect.vue'),
                meta: { title: '成果收集' }
            },
            {
                path: 'achievement-detail/:id',
                name: 'achievementDetail',
                component: () => import('../components/student/honors/AchievementDetail.vue'),
                meta: { title: '成果详情' }
            },
            {
                path: 'certificate-ocr',
                name: 'certificateOcr',
                component: () => import('../components/student/honors/CertificateOcr.vue'),
                meta: { title: '证书识别' }
            },
            {
                path: 'portrait',
                name: 'studentPortrait',
                component: () => import('../components/student/portrait/portrait-analysis.vue'),
                meta: { title: '个人画像' }
            },
            {
                path: 'portrait/ai-chat',
                name: 'studentPortraitAiChat',
                component: () => import('../components/student/portrait/ai-chat.vue'),
                meta: { title: 'AI智能对话' }
            },
            {
                path: 'profile',
                name: 'studentProfile',
                component: () => import('../components/student/profile/ProfilePage.vue'),
                meta: { title: '个人资料' }
            }
        ]
    }
]
