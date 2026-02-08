/**
 * FastAPI后端API类型定义
 * 基于后端API协作文档生成
 */

// ============= 通用类型 =============

export type ID = string | number

// FastAPI标准响应格式（已在request.ts的拦截器中处理，这里定义是为了类型完整性）
export interface FastAPIResponse<T = any> {
    code: number
    msg: string
    data: T
}

// ============= 认证相关 =============

export interface LoginRequest {
    username: string
    password: string
}

export interface LoginResponse {
    access_token: string
    refresh_token: string
    token_type: string
    userInfo: {
        id: number
        username: string
        role: 'student' | 'admin'
        name: string
        student_id?: string
        avatar_url?: string
    }
}

// ============= 教师相关 =============

export interface Teacher {
    id: number
    name: string
    department: string
    title?: string
    email?: string
}

export type TeachersResponse = Teacher[]

// ============= 文件上传 =============

export interface UploadFileResponse {
    url: string
    filename: string
    size: number
    upload_time: string
}

// ============= 证书OCR识别 =============

export interface RecognizedData {
    title: string
    type: string
    issuer: string
    date: string
    award_level?: string
    certificate_number?: string
    recipient_name?: string
    suggested_type: string
    award?: string
    advisor_name?: string
    // 以下为扩展识别字段
    project_name?: string
    team_members?: string[]
    advisors?: string[]  // 指导老师数组（与后端API保持一致）
    additional_info?: string
}

export interface CertificateRecognitionResponse {
    recognized_data: RecognizedData
    file_url: string
    file_info: {
        filename: string
        size: number
        upload_time: string
    }
    ai_metadata: {
        model: string
        confidence: number
    }
    usage?: {
        prompt_tokens: number
        completion_tokens: number
    }
}

// ============= 成果相关 =============

export type AchievementStatus = 'pending' | 'approved' | 'rejected'
export type AchievementType = 'competition' | 'paper' | 'patent' | 'project' | 'certificate'

export interface Achievement {
    id: number
    student_id: number
    student_name: string
    teacher_id: number
    teacher_name: string
    title: string
    type: AchievementType
    content_json: {
        issuing_organization?: string
        issue_date?: string
        award_level?: string
        certificate_number?: string
        [key: string]: any
    }
    evidence_url: string
    status: AchievementStatus
    audit_comment?: string
    created_at: string
    create_time?: string
    student_number?: string // 增强字段
    student_major?: string  // 增强字段
    student_class?: string  // 增强字段
}

export interface AchievementCreateRequest {
    teacher_id: number
    title: string
    type: AchievementType
    content_json?: Record<string, any>
    evidence_url?: string
}

export interface AchievementCreateResponse {
    id: number
}

export type AchievementsResponse = Achievement[]

// ============= 管理员审核 =============

export interface AchievementsReviewQuery {
    status?: AchievementStatus
    student_name?: string
    page?: number
    page_size?: number
}

export interface AchievementsReviewResponse {
    list: Achievement[]
    total: number
}

export interface AuditAchievementRequest {
    action: 'approve' | 'reject'
    comment?: string
}

// ============= AI对话 =============

export interface ChatRequest {
    session_id?: string | null
    message: string
}

export interface ChatResponse {
    session_id: string
    message: string
    timestamp?: string
}

// ============= 学生画像 =============

export interface StudentPersona {
    summary: string
    skills: string[]
    interests: string[]
    achievements_count: number
    recent_activities: string[]
    strengths: string[]
    suggestions: string[]
}

export type StudentPersonaResponse = StudentPersona

// ============= 证书列表 =============

export interface Certificate {
    file_url: string
    filename: string
    upload_time: string
    recognized_title?: string
}

export interface CertificatesResponse {
    certificates: Certificate[]
    total: number
}
