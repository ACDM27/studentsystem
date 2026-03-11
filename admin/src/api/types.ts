/**
 * 管理端 API 类型定义
 */

export type ID = string | number

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
    is_first_login: boolean
    userInfo: {
        id: number
        username: string
        role: 'student' | 'admin'
        name: string
        student_id?: string
        avatar_url?: string
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
    student_number?: string
    student_major?: string
    student_class?: string
}

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
