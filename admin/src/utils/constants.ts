/**
 * 系统常量定义
 */

export const ACHIEVEMENT_STATUS = {
    PENDING: 'pending',
    APPROVED: 'approved',
    REJECTED: 'rejected'
} as const

export type AchievementStatusType = typeof ACHIEVEMENT_STATUS[keyof typeof ACHIEVEMENT_STATUS]

export const ACHIEVEMENT_TYPES = {
    COMPETITION: 'competition',
    PAPER: 'paper',
    PATENT: 'patent',
    PROJECT: 'project',
    CERTIFICATE: 'certificate'
} as const

export type AchievementTypeType = typeof ACHIEVEMENT_TYPES[keyof typeof ACHIEVEMENT_TYPES]

export const STATUS_TEXT: Record<string, string> = {
    pending: '待审核',
    approved: '已通过',
    rejected: '已拒绝'
}

export const STATUS_COLOR: Record<string, 'warning' | 'success' | 'danger' | 'info'> = {
    pending: 'warning',
    approved: 'success',
    rejected: 'danger'
}

export const ACHIEVEMENT_TYPE_TEXT: Record<string, string> = {
    competition: '竞赛',
    paper: '论文',
    patent: '专利',
    project: '项目',
    certificate: '证书'
}

export const AUDIT_ACTION = {
    APPROVE: 'approve',
    REJECT: 'reject'
} as const

export type AuditActionType = typeof AUDIT_ACTION[keyof typeof AUDIT_ACTION]

export const DEFAULT_PAGE_SIZE = 10
export const PAGE_SIZE_OPTIONS = [10, 20, 50, 100]
