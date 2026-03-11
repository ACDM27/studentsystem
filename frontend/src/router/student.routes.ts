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
                path: 'achievement-settings',
                name: 'achievementSettings',
                component: () => import('../components/student/honors/AchievementSettings.vue'),
                meta: { title: '成果设置' }
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
                path: 'portrait/chat',
                name: 'studentPortraitChat',
                component: () => import('../components/student/portrait/portrait-chat.vue'),
                meta: { title: '画像对话' }
            },
            {
                path: 'portrait/ai-chat',
                name: 'studentPortraitAiChat',
                component: () => import('../components/student/portrait/ai-chat.vue'),
                meta: { title: 'AI智能对话' }
            }
        ]
    }
]
