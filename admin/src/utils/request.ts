/**
 * 统一的HTTP请求工具
 * 基于axios封装，适配FastAPI后端响应格式
 */
import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios'
import { ElMessage } from 'element-plus'

interface FastAPIResponse<T = any> {
    code: number
    msg: string
    data: T
}

const request: AxiosInstance = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL ?? '',
    timeout: 30000,
    headers: {
        'Content-Type': 'application/json'
    }
})

request.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token')
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        if (config.data instanceof FormData) {
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

request.interceptors.response.use(
    (response: AxiosResponse<FastAPIResponse>) => {
        const { code, msg, data } = response.data
        console.log(`[API] 响应成功:`, { code, msg, dataType: typeof data })
        if (code === 200) {
            return data
        } else {
            ElMessage.error(msg || '请求失败')
            return Promise.reject(new Error(msg || '请求失败'))
        }
    },
    (error) => {
        console.error('[API] 响应错误:', error)
        if (!error.response) {
            ElMessage.error('网络错误，请检查：\n1. 后端服务是否启动\n2. 端口8000是否可访问')
            return Promise.reject(error)
        }
        const { status, data } = error.response
        switch (status) {
            case 401:
                ElMessage.error('登录已过期，请重新登录')
                localStorage.removeItem('token')
                localStorage.removeItem('userInfo')
                if (typeof window !== 'undefined') {
                    window.location.href = '/admin/login'
                }
                break
            case 403:
                ElMessage.error('权限不足')
                break
            case 404:
                ElMessage.error('请求的资源不存在')
                break
            case 422:
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
