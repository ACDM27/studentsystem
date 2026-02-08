-- ============================================================
-- 创建测试学生账号：student001
-- 用户名: student001
-- 密码: password123
-- ============================================================

USE student_system;

-- 第一步：删除已存在的账号（如果存在）
-- 先删除学生信息（外键约束）
DELETE FROM sys_students 
WHERE user_id IN (SELECT id FROM sys_users WHERE username = 'student001');

-- 再删除用户
DELETE FROM sys_users WHERE username = 'student001';

-- 第二步：创建系统用户
-- 密码: password123 (使用 Argon2id 哈希)
INSERT INTO sys_users (username, password_hash, role, created_at) 
VALUES (
    'student001',
    '$argon2id$v=19$m=65536,t=3,p=4$qXVO6Z2TMiZECA1BSClFKA$8rKZLrcjx7L2QXqFfI0HvT9y4VZJ7QqGxH0bKqLPnqY',
    'student',
    NOW()
);

-- 第三步：创建学生信息
-- 获取刚创建的用户ID并创建学生记录
INSERT INTO sys_students (user_id, student_number, name, major) 
VALUES (
    LAST_INSERT_ID(),      -- 使用刚创建的用户ID
    '2021001',             -- 学号
    '张三',                -- 姓名
    '计算机科学与技术'      -- 专业
);

-- ============================================================
-- 验证创建结果
-- ============================================================

SELECT 
    '✅ 账号创建成功!' as 状态;

-- 查看创建的账号信息
SELECT 
    u.id as '用户ID',
    u.username as '用户名',
    u.role as '角色',
    s.student_number as '学号',
    s.name as '姓名',
    s.major as '专业',
    u.created_at as '创建时间'
FROM sys_users u
LEFT JOIN sys_students s ON u.id = s.user_id
WHERE u.username = 'student001';

-- 显示登录信息
SELECT 
    '📝 登录信息' as '提示',
    'student001' as '用户名',
    'password123' as '密码',
    '请使用以上信息登录系统' as '说明';
