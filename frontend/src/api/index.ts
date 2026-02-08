/**
 * 统一API调用层
 * 基于FastAPI后端，所有API端点完全匹配后端路由
 * 响应已由request.ts拦截器转换，直接返回data部分
 */
import request from '@/utils/request'
import type {
    LoginRequest,
    LoginResponse,
    ID,
    TeachersResponse,
    UploadFileResponse,
    CertificateRecognitionResponse,
    AchievementCreateRequest,
    AchievementCreateResponse,
    AchievementsResponse,
    AchievementsReviewQuery,
    AchievementsReviewResponse,
    AuditAchievementRequest,
    ChatRequest,
    ChatResponse,
    StudentPersonaResponse,
    CertificatesResponse
} from './types'
import type { IGetAssignmentsResp } from '@/types/api'

// ==================== 认证相关 ====================

/**
 * 用户登录
 * POST /api/v1/auth/login
 */
export function login(data: LoginRequest): Promise<LoginResponse> {
    return request.post('/api/v1/auth/login', data)
}

/**
 * 用户登出（前端清除token即可，无需调用后端）
 */
export function logout(): void {
    localStorage.removeItem('token')
    localStorage.removeItem('userInfo')
    window.location.href = '/student/login'
}

// ==================== 公共API ====================

/**
 * 获取教师列表
 * GET /api/v1/common/teachers
 */
export function getTeachers(): Promise<TeachersResponse> {
    return request.get('/api/v1/common/teachers')
}

/**
 * 获取教师详情
 * GET /api/v1/common/teachers/{id}
 */
export function getTeacherById(id: ID): Promise<any> {
    return request.get(`/api/v1/common/teachers/${id}`)
}


/**
 * 上传文件
 * POST /api/v1/common/upload
 */
export function uploadFile(file: File): Promise<UploadFileResponse> {
    const formData = new FormData()
    formData.append('file', file)
    return request.post('/api/v1/common/upload', formData)
}

// ==================== 学生端API ====================

/**
 * 获取当前学生基本信息
 * GET /api/v1/student/me
 */
export function getStudentMe(): Promise<any> {
    return request.get('/api/v1/student/me')
}

/**
 * 获取学生详细档案
 * GET /api/v1/student/profile
 */
export function getStudentProfile(): Promise<any> {
    return request.get('/api/v1/student/profile')
}

/**
 * 证书OCR识别（步骤1：上传并识别）
 * POST /api/v1/student/ocr/recognize
 */
export function recognizeCertificate(file: File): Promise<CertificateRecognitionResponse> {
    const formData = new FormData()
    formData.append('file', file)
    return request.post('/api/v1/student/ocr/recognize', formData, {
        timeout: 60000 // OCR识别可能需要更长时间
    })
}

/**
 * 提交成果（步骤2：确认信息后提交）
 * POST /api/v1/student/achievements
 */
export function submitAchievement(data: AchievementCreateRequest): Promise<AchievementCreateResponse> {
    return request.post('/api/v1/student/achievements', data)
}

/**
 * 获取我的成果列表
 * GET /api/v1/student/achievements
 * @param status - 可选，筛选状态 pending/approved/rejected
 */
export function getMyAchievements(status?: string): Promise<AchievementsResponse> {
    const params = status ? { status } : {}
    return request.get('/api/v1/student/achievements', { params })
}

/**
 * 获取我的证书列表
 * GET /api/v1/student/certificates
 */
export function getMyCertificates(): Promise<CertificatesResponse> {
    return request.get('/api/v1/student/certificates')
}

/**
 * AI对话
 * POST /api/v1/student/ai/chat
 */
export function chatWithAI(data: ChatRequest): Promise<ChatResponse> {
    return request.post('/api/v1/student/ai/chat', data)
}

/**
 * 获取学生画像
 * GET /api/v1/student/persona
 */
export function getStudentPersona(): Promise<StudentPersonaResponse> {
    return request.get('/api/v1/student/persona')
}

/**
 * 获取学生画像（根据学号）
 * GET /api/v1/student/portrait/{student_id}
 */
export function fetchStudentPortraitByStudentId(student_id: string): Promise<any> {
    return request.get(`/api/v1/student/portrait/${student_id}`)
}

/**
 * 创建学生画像
 * POST /api/v1/student/portrait
 */
export function createStudentPortrait(data: any): Promise<any> {
    return request.post('/api/v1/student/portrait', data)
}

/**
 * 添加问答历史
 * POST /api/v1/student/portrait/{id}/qa
 */
export function addQaHistory(portraitId: string, data: any): Promise<any> {
    return request.post(`/api/v1/student/portrait/${portraitId}/qa`, data)
}

/**
 * 查询学生信息（结合AI和学生档案）
 * 这是一个组合函数，先获取学生信息，然后进行AI查询
 */
export async function queryStudentInfo(data: { question: string; student_id?: string }): Promise<any> {
    try {
        // 1. 获取学生档案信息
        const profileData = await getStudentProfile()

        // 2. 构建包含学生信息的上下文
        const context = `学生档案信息：
- 姓名：${profileData.basic_info?.name}
- 学号：${profileData.basic_info?.student_id}
- 专业：${profileData.basic_info?.major}
- 班级：${profileData.basic_info?.class_name}
- 成果统计：
  * 总成果数：${profileData.statistics?.total_achievements}
  * 已通过：${profileData.statistics?.approved_achievements}
  * 待审核：${profileData.statistics?.pending_achievements}
  * 通过率：${profileData.statistics?.approval_rate}%`

        // 3. 调用AI对话，传入上下文
        const aiResponse = await chatWithAI({
            session_id: null,
            message: `${context}\n\n问题：${data.question}`
        })

        return {
            data: {
                response: aiResponse.message,
                student_id: data.student_id,
                profile: profileData
            }
        }
    } catch (error) {
        console.error('queryStudentInfo失败:', error)
        // 返回错误提示
        return {
            data: {
                response: '抱歉，无法获取学生信息进行分析。请稍后再试。',
                error: true
            }
        }
    }
}

// ==================== 管理员API ====================

/**
 * 获取成果审核列表
 * GET /api/v1/admin/achievements
 */
export function getAchievementsForReview(params?: AchievementsReviewQuery): Promise<AchievementsReviewResponse> {
    return request.get('/api/v1/admin/achievements', { params })
}

/**
 * 审核成果
 * PATCH /api/v1/admin/achievements/{id}/audit
 */
export function auditAchievement(achievementId: number, data: AuditAchievementRequest): Promise<void> {
    return request.patch(`/api/v1/admin/achievements/${achievementId}/audit`, data)
}

// ==================== 工具函数 ====================

/**
 * 获取完整的文件URL
 * 后端返回的是相对路径，需要拼接baseURL
 */
export function getFileUrl(relativePath: string): string {
    if (!relativePath) return ''
    if (relativePath.startsWith('http')) return relativePath

    const baseURL = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/$/, '')
    const path = relativePath.startsWith('/') ? relativePath : `/${relativePath}`

    return `${baseURL}${path}`
}

/**
 * 格式化日期
 */
export function formatDate(dateStr: string, format: string = 'YYYY-MM-DD HH:mm'): string {
    if (!dateStr) return ''
    const date = new Date(dateStr)

    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    const hours = String(date.getHours()).padStart(2, '0')
    const minutes = String(date.getMinutes()).padStart(2, '0')
    const seconds = String(date.getSeconds()).padStart(2, '0')

    return format
        .replace('YYYY', String(year))
        .replace('MM', month)
        .replace('DD', day)
        .replace('HH', hours)
        .replace('mm', minutes)
        .replace('ss', seconds)
}

// ==================== 活动API ====================

/**
 * 获取活动列表
 * GET /api/v1/activities
 */
export function getActivities(params?: { page?: number; page_size?: number; status?: string }): Promise<any> {
    return request.get('/api/v1/activities', { params })
}

/**
 * 获取活动详情
 * GET /api/v1/activities/{id}
 */
export function getActivityById(id: number): Promise<any> {
    return request.get(`/api/v1/activities/${id}`)
}

// ==================== 反馈API ====================

/**
 * 获取反馈列表
 * GET /api/v1/feedbacks
 */
export function getFeedbacks(params?: { page?: number; pageSize?: number }): Promise<any> {
    return request.get('/api/v1/feedbacks', { params })
}

/**
 * 提交反馈
 * POST /api/v1/feedbacks
 */
export function postFeedback(data: any): Promise<any> {
    return request.post('/api/v1/feedbacks', data)
}

// ==================== 咨询API ====================

/**
 * 获取咨询师列表
 */
export function getConsultTeachers(): Promise<any> {
    return request.get('/api/v1/consulting/teachers')
}

/**
 * 根据类型获取咨询师
 */
export function getConsultTeachersByType(type: string): Promise<any> {
    return request.get('/api/v1/consulting/teachers', { params: { type } })
}

/**
 * 获取在线咨询师
 */
export function getOnlineConsultTeachers(): Promise<any> {
    return request.get('/api/v1/consulting/teachers/online')
}

/**
 * 获取咨询师详情
 */
export function getConsultTeacherById(id: ID): Promise<any> {
    return request.get(`/api/v1/consulting/teachers/${id}`)
}


// ==================== 课程API ====================

/**
 * 获取课程列表
 * GET /api/v1/courses
 */
export function getCourses(params?: { page?: number; page_size?: number; semester?: string; category?: string }): Promise<any> {
    return request.get('/api/v1/courses', { params })
}

/**
 * 获取课程详情
 * GET /api/v1/courses/{id}
 */
export function getCourseById(id: number): Promise<any> {
    return request.get(`/api/v1/courses/${id}`)
}

/**
 * 获取作业列表
 * GET /api/v1/assignments
 */
export function getAssignments(): Promise<IGetAssignmentsResp> {
    return request.get('/api/v1/assignments')
}

// 默认导出所有API函数（更新版）
export default {
    // 认证
    login,
    logout,
    // 公共
    getTeachers,
    uploadFile,
    // 学生
    getStudentMe,
    getStudentProfile,
    recognizeCertificate,
    submitAchievement,
    getMyAchievements,
    getMyCertificates,
    chatWithAI,
    getStudentPersona,
    fetchStudentPortraitByStudentId,
    createStudentPortrait,
    addQaHistory,
    queryStudentInfo,
    // 管理员
    getAchievementsForReview,
    auditAchievement,
    // 活动
    getActivities,
    getActivityById,
    // 反馈
    getFeedbacks,
    postFeedback,
    // 咨询
    getConsultTeachers,
    getConsultTeacherById,
    getConsultTeachersByType,
    getOnlineConsultTeachers,
    // 课程

    getCourses,
    getCourseById,
    // 作业
    getAssignments,
    // 工具
    getFileUrl,
    formatDate
}
