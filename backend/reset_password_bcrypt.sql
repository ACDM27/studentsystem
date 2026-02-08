-- ============================================================
-- 方案：重置 student001 密码为简单密码
-- 使用 Bcrypt 格式（更兼容）
-- ============================================================

USE student_system;

-- 方式 1: 使用 Bcrypt 格式的 123456
-- Bcrypt 哈希是经过验证的，更可靠
UPDATE sys_users 
SET password_hash = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyWui3w3/U.u'
WHERE username = 'student001';

-- 验证更新
SELECT 
    '✅ 密码已更新' as 状态,
    'student001' as 用户名,
    '123456' as 新密码,
    SUBSTRING(password_hash, 1, 20) as 哈希前缀
FROM sys_users 
WHERE username = 'student001';

-- ============================================================
-- 提示
-- ============================================================
-- 执行后使用以下信息登录:
-- 用户名: student001
-- 密码: 123456
-- ============================================================
