/**
 * 管理端认证工具函数
 */
import { ElMessage } from 'element-plus'
import router from '@/router'

/**
 * 检查用户是否为管理员
 */
export function isAdmin(): boolean {
    try {
        const userInfoStr = localStorage.getItem('userInfo')
        if (!userInfoStr) return false

        const userInfo = JSON.parse(userInfoStr)
        return userInfo.role === 'admin'
    } catch (error) {
        console.error('解析用户信息失败:', error)
        return false
    }
}

/**
 * 获取当前管理员信息
 */
export function getAdminInfo() {
    try {
        const userInfoStr = localStorage.getItem('userInfo')
        if (!userInfoStr) return null

        const userInfo = JSON.parse(userInfoStr)
        if (userInfo.role !== 'admin') return null

        return userInfo
    } catch (error) {
        console.error('获取管理员信息失败:', error)
        return null
    }
}

/**
 * 管理员退出登录
 */
export function adminLogout() {
    localStorage.removeItem('token')
    localStorage.removeItem('userInfo')
    ElMessage.success('已退出登录')
    router.push('/admin/login')
}

/**
 * 检查是否已登录
 */
export function isLoggedIn(): boolean {
    const token = localStorage.getItem('token')
    return !!token
}
