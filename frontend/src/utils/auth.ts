/**
 * 此时JWT Token是否已过期
 * @param token JWT Token字符串
 * @returns boolean
 */
export function isTokenExpired(token: string): boolean {
    try {
        // JWT由三部分组成，用.分隔
        const parts = token.split('.')
        if (parts.length !== 3) {
            return true
        }

        // 解析Payload (第二部分)
        const payload = JSON.parse(atob(parts[1]))

        // 检查exp字段 (Unix时间戳)
        if (!payload.exp) {
            return false // 没有过期时间，假定不过期
        }

        // 比较当前时间 (转换为秒)
        const currentTime = Math.floor(Date.now() / 1000)

        // 如果当前时间 > 过期时间，则已过期
        return currentTime > payload.exp
    } catch (e) {
        console.error('Token解析失败', e)
        return true // 解析失败视为过期
    }
}
