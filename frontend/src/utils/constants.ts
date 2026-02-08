/**
 * 系统常量定义
 */

// ==================== 成果状态 ====================
export const ACHIEVEMENT_STATUS = {
    PENDING: 'pending',
    APPROVED: 'approved',
    REJECTED: 'rejected'
} as const

export type AchievementStatusType = typeof ACHIEVEMENT_STATUS[keyof typeof ACHIEVEMENT_STATUS]

// ==================== 成果类型 ====================
export const ACHIEVEMENT_TYPES = {
    COMPETITION: 'competition',
    PAPER: 'paper',
    PATENT: 'patent',
    PROJECT: 'project',
    CERTIFICATE: 'certificate'
} as const

export type AchievementTypeType = typeof ACHIEVEMENT_TYPES[keyof typeof ACHIEVEMENT_TYPES]

// ==================== 状态文本映射 ====================
export const STATUS_TEXT: Record<string, string> = {
    pending: '待审核',
    approved: '已通过',
    rejected: '已拒绝'
}

// ==================== 状态颜色映射（Element Plus Tag类型）====================
export const STATUS_COLOR: Record<string, 'warning' | 'success' | 'danger' | 'info'> = {
    pending: 'warning',
    approved: 'success',
    rejected: 'danger'
}

// ==================== 成果类型文本映射 ====================
export const ACHIEVEMENT_TYPE_TEXT: Record<string, string> = {
    competition: '竞赛',
    paper: '论文',
    patent: '专利',
    project: '项目',
    certificate: '证书'
}

// ==================== 审核操作类型 ====================
export const AUDIT_ACTION = {
    APPROVE: 'approve',
    REJECT: 'reject'
} as const

export type AuditActionType = typeof AUDIT_ACTION[keyof typeof AUDIT_ACTION]

// ==================== 分页默认配置 ====================
export const DEFAULT_PAGE_SIZE = 10
export const PAGE_SIZE_OPTIONS = [10, 20, 50, 100]
