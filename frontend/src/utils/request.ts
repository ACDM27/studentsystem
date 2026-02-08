/**
 * 统一的HTTP请求工具
 * 基于axios封装，适配FastAPI后端响应格式
 */
import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios'
import { ElMessage } from 'element-plus'

// FastAPI标准响应格式
interface FastAPIResponse<T = any> {
    code: number
    msg: string
    data: T
}

// 创建axios实例
const request: AxiosInstance = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
    timeout: 30000,
    headers: {
        'Content-Type': 'application/json'
    }
})

// 请求拦截器
request.interceptors.request.use(
    (config) => {
        // 添加Token
        const token = localStorage.getItem('token')
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }

        // FormData请求自动设置正确的Content-Type
        if (config.data instanceof FormData) {
            // Axios 1.x 使用 AxiosHeaders，需要用 delete 方法
            if (config.headers && typeof (config.headers as any).delete === 'function') {
                (config.headers as any).delete('Content-Type')
            } else {
                delete config.headers['Content-Type']
            }
        }

        console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`)
        return config
    },
    (error) => {
        console.error('[API] 请求错误:', error)
        return Promise.reject(error)
    }
)

// 响应拦截器 - 核心：将FastAPI响应格式转换为前端直接可用的数据
request.interceptors.response.use(
    (response: AxiosResponse<FastAPIResponse>) => {
        const { code, msg, data } = response.data

        console.log(`[API] 响应成功:`, { code, msg, dataType: typeof data })

        // FastAPI成功响应：code === 200
        if (code === 200) {
            // 直接返回data部分，前端组件无需关心code和msg
            return data
        } else {
            // 业务错误
            ElMessage.error(msg || '请求失败')
            return Promise.reject(new Error(msg || '请求失败'))
        }
    },
    (error) => {
        console.error('[API] 响应错误:', error)

        // 网络错误或服务器未响应
        if (!error.response) {
            ElMessage.error('网络错误，请检查：\n1. 后端服务是否启动\n2. 端口8000是否可访问')
            return Promise.reject(error)
        }

        const { status, data } = error.response

        // HTTP状态码错误处理
        switch (status) {
            case 401:
                // Token过期或未登录
                ElMessage.error('登录已过期，请重新登录')
                localStorage.removeItem('token')
                localStorage.removeItem('userInfo')
                // 根据当前路径跳转到对应登录页
                if (typeof window !== 'undefined') {
                    if (window.location.pathname.startsWith('/admin')) {
                        window.location.href = '/admin/login'
                    } else {
                        window.location.href = '/student/login'
                    }
                }
                break

            case 403:
                ElMessage.error('权限不足')
                break

            case 404:
                ElMessage.error('请求的资源不存在')
                break

            case 422:
                // FastAPI参数验证错误
                const detail = data?.detail
                if (Array.isArray(detail)) {
                    const errors = detail.map((e: any) => e.msg).join(', ')
                    ElMessage.error(`参数错误: ${errors}`)
                } else {
                    ElMessage.error(data?.msg || '参数验证失败')
                }
                break

            case 500:
                ElMessage.error('服务器内部错误')
                break

            default:
                ElMessage.error(data?.msg || `请求失败 (${status})`)
        }

        return Promise.reject(error)
    }
)

export default request
