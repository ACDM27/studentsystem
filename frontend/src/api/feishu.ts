/**
 * Feishu Integration API
 * 飞书集成相关API调用
 */
import request from '@/utils/request'

export interface FeishuConfigCreate {
    app_id: string
    app_secret: string
}

export interface FeishuImportRequest {
    app_token: string
    table_id: string
    mapping_id?: number
    skip_invalid?: boolean
    preview_limit?: number
}

export interface QuickImportPreviewRequest {
    app_token: string
    table_id: string
    student_name: string
}

// ==================== 配置管理 ====================

export function saveFeishuConfig(data: FeishuConfigCreate) {
    return request.post('/api/v1/feishu/config', data)
}

export function getFeishuConfig() {
    return request.get('/api/v1/feishu/config')
}

export function testFeishuConnection() {
    return request.post('/api/v1/feishu/test-connection')
}

// ==================== 表格操作 ====================

export function listFeishuTables(appToken: string) {
    return request.get(`/api/v1/feishu/tables/${appToken}`)
}

// ==================== 导入功能 ====================

export function previewFeishuImport(data: FeishuImportRequest) {
    return request.post('/api/v1/feishu/preview', data)
}

export function executeFeishuImport(data: FeishuImportRequest) {
    return request.post('/api/v1/feishu/import', data)
}

export function getImportHistory(params: { page: number; page_size: number }) {
    return request.get('/api/v1/feishu/import-history', { params })
}

// ==================== 学生端快捷导入 ====================

export function studentQuickPreview(data: QuickImportPreviewRequest) {
    return request.post('/api/v1/feishu/student/quick-preview', data)
}

// ==================== 工具函数 ====================

/**
 * 解析飞书表格链接
 * @param url 飞书表格链接
 * @returns {app_token, table_id, view_id}
 */
export function parseFeishuLink(url: string): { appToken: string; tableId: string; viewId?: string } | null {
    try {
        const urlObj = new URL(url)

        // 提取 app_token (base/后面的部分)
        const pathMatch = urlObj.pathname.match(/\/base\/([^\/\?]+)/)
        const appToken = pathMatch?.[1]

        // 提取 table_id (URL参数)
        const tableId = urlObj.searchParams.get('table')

        // 可选：提取 view_id
        const viewId = urlObj.searchParams.get('view') || undefined

        if (!appToken || !tableId) {
            return null
        }

        return { appToken, tableId, viewId }
    } catch (error) {
        console.error('链接解析失败:', error)
        return null
    }
}

export default {
    saveFeishuConfig,
    getFeishuConfig,
    testFeishuConnection,
    listFeishuTables,
    previewFeishuImport,
    executeFeishuImport,
    getImportHistory,
    studentQuickPreview,
    parseFeishuLink
}
