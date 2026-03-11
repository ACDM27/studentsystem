/**
 * 管理端 API 调用层
 */
import request from '@/utils/request'
import type {
    LoginRequest,
    LoginResponse,
    AchievementsReviewQuery,
    AchievementsReviewResponse,
    AuditAchievementRequest
} from './types'

// ==================== 认证 ====================

export function login(data: LoginRequest): Promise<LoginResponse> {
    return request.post('/api/v1/auth/login', data)
}

// ==================== 管理员 API ====================

export function getAchievementsForReview(params?: AchievementsReviewQuery): Promise<AchievementsReviewResponse> {
    return request.get('/api/v1/admin/achievements', { params })
}

export function auditAchievement(achievementId: number, data: AuditAchievementRequest): Promise<void> {
    return request.patch(`/api/v1/admin/achievements/${achievementId}/audit`, data)
}

// ==================== 工具函数 ====================

export function getFileUrl(relativePath: string): string {
    if (!relativePath) return ''
    if (relativePath.startsWith('http')) return relativePath

    const path = relativePath.startsWith('/') ? relativePath : `/${relativePath}`

    if (path.startsWith('/uploads/')) {
        const token = localStorage.getItem('token')
        if (token) {
            const separator = path.includes('?') ? '&' : '?'
            return `${path}${separator}token=${encodeURIComponent(token)}`
        }
        return path
    }

    let baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
    if (baseURL === '/' || baseURL === '') {
        baseURL = ''
    } else {
        try {
            const url = new URL(baseURL)
            baseURL = `${url.protocol}//${url.host}`
        } catch {
            baseURL = baseURL.replace(/\/$/, '').replace(/\/api$/, '')
        }
    }

    return `${baseURL}${path}`
}

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

export default {
    login,
    getAchievementsForReview,
    auditAchievement,
    getFileUrl,
    formatDate
}
