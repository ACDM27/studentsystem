import { RouteRecordRaw } from 'vue-router'

/**
 * 学生端路由配置
 * 所有路由都需要 student 角色权限
 */
export const studentRoutes: Array<RouteRecordRaw> = [
    // 旧的 /dashboard 路由（保持兼容性）
    {
        path: '/dashboard',
        name: 'dashboard',
        component: () => import('../components/student/dashboard/DashboardPage.vue'),
        meta: { requiresAuth: true, role: 'student', title: '学生仪表盘' }
    },
    // 学生端主路由
    {
        path: '/student',
        component: () => import('../layout/StudentLayout.vue'),
        meta: { requiresAuth: true, role: 'student' },
        children: [
            {
                path: 'dashboard',
                name: 'studentDashboard',
                component: () => import('../components/student/dashboard/DashboardPage.vue'),
                meta: { title: '仪表盘' }
            },
            {
                path: 'stastic',
                name: 'studentStastic',
                component: () => import('../components/student/stastic/data-screen.vue'),
                meta: { title: '数据统计' }
            },
            {
                path: 'data-screen',
                name: 'studentDataScreen',
                component: () => import('../components/student/stastic/data-screen.vue'),
                meta: { title: '数据大屏' }
            },
            {
                path: 'homework',
                name: 'studentHomework',
                component: () => import('../components/student/assignments/assignments.vue'),
                meta: { title: '作业管理' }
            },
            {
                path: 'courses',
                name: 'studentCourses',
                component: () => import('../components/student/courses/CoursesPage.vue'),
                meta: { title: '课程' }
            },
            {
                path: 'course-schedule',
                name: 'courseSchedule',
                component: () => import('../components/student/courses/CoursesPage.vue'),
                meta: { title: '课程安排' }
            },
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
                path: 'teachers',
                name: 'studentTeachers',
                component: () => import('../components/student/teachers/teachers.vue'),
                meta: { title: '教师信息' }
            },
            {
                path: 'teacher-info',
                name: 'teacherInfo',
                component: () => import('../components/student/teachers/teachers.vue'),
                meta: { title: '教师信息查询' }
            },
            {
                path: 'teacher-detail/:id',
                name: 'teacherDetail',
                component: () => import('../components/student/teachers/TeacherDetail.vue'),
                meta: { title: '教师详情' }
            },
            {
                path: 'teacher-favorites',
                name: 'teacherFavorites',
                component: () => import('../components/student/teachers/teachers.vue'),
                meta: { title: '收藏教师' }
            },
            {
                path: 'consult',
                name: 'studentConsult',
                component: () => import('../components/student/consulting/consulting.vue'),
                meta: { title: '咨询服务' }
            },
            {
                path: 'resume',
                name: 'studentResume',
                component: () => import('../components/student/resume/resume.vue'),
                meta: { title: '简历生成' }
            },
            {
                path: 'feedback',
                name: 'studentFeedback',
                component: () => import('../components/student/feedback/feedback.vue'),
                meta: { title: '意见反馈' }
            },
            {
                path: 'survey',
                name: 'studentSurvey',
                component: () => import('../components/student/vote-survey/vote-survey.vue'),
                meta: { title: '问卷调查' }
            },
            {
                path: 'consultant-detail/:id',
                name: 'consultantDetail',
                component: () => import('../components/student/consulting/consulting.vue'),
                meta: { title: '咨询师详情' }
            },
            {
                path: 'book-consultation/:id',
                name: 'bookConsultation',
                component: () => import('../components/student/consulting/consulting.vue'),
                meta: { title: '预约咨询' }
            },
            {
                path: 'job-recommendation',
                name: 'jobRecommendation',
                component: () => import('../components/student/job/jobpage.vue'),
                meta: { title: '就业推荐' }
            },
            {
                path: 'activities',
                name: 'studentActivities',
                component: () => import('../components/student/activities/college-activity.vue'),
                meta: { title: '校园活动' }
            },
            {
                path: 'talent-market',
                name: 'talentMarket',
                component: () => import('../components/student/talent-market/talent-market.vue'),
                meta: { title: '人才市场' }
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
