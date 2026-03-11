/**
 * 此时JWT Token是否已过期
 */
export function isTokenExpired(token: string): boolean {
    try {
        const parts = token.split('.')
        if (parts.length !== 3) {
            return true
        }
        const payload = JSON.parse(atob(parts[1]))
        if (!payload.exp) {
            return false
        }
        const currentTime = Math.floor(Date.now() / 1000)
        return currentTime > payload.exp
    } catch (e) {
        console.error('Token解析失败', e)
        return true
    }
}
