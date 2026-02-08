-- ============================================================
-- 一键创建 student001 账号（完整版）
-- 此脚本会自动清理旧数据并创建新账号
-- ============================================================

USE student_system;

-- 步骤 1: 清理旧数据
DELETE FROM sys_students WHERE user_id IN (SELECT id FROM sys_users WHERE username = 'student001');
DELETE FROM sys_users WHERE username = 'student001';

-- 步骤 2: 创建用户（密码: 123456）
INSERT INTO sys_users (username, password_hash, role, created_at) 
VALUES (
    'student001',
    '$argon2id$v=19$m=65536,t=3,p=4$wXnOuZcSIiRECA2BsLYWQg$9QYvZ3xJKqE8hF7yN2pLmR1sK4vH3nW6cX8bT0qA9uM',
    'student',
    NOW()
);

-- 步骤 3: 创建学生信息
INSERT INTO sys_students (user_id, student_number, name, major) 
VALUES (
    LAST_INSERT_ID(),
    '2021001',
    '张三',
    '计算机科学与技术'
);

-- 步骤 4: 验证创建结果
SELECT 
    u.id as 用户ID,
    u.username as 用户名,
    u.role as 角色,
    s.student_number as 学号,
    s.name as 姓名,
    s.major as 专业
FROM sys_users u
LEFT JOIN sys_students s ON u.id = s.user_id
WHERE u.username = 'student001';

-- 显示登录凭据
SELECT 
    'student001' as 用户名,
    '123456' as 密码,
    '✅ 账号已创建，请使用以上信息登录' as 提示;
