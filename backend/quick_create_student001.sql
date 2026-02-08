-- 快速创建 student001 账号
-- 可以直接复制到 MySQL 客户端执行

USE student_system;

-- 先删除可能存在的旧数据
DELETE FROM student WHERE user_id IN (SELECT id FROM sys_user WHERE username = 'student001');
DELETE FROM sys_user WHERE username = 'student001';

-- 创建用户（密码: password123）
INSERT INTO sys_user (username, password_hash, role) VALUES
('student001', '$argon2id$v=19$m=65536,t=3,p=4$qXVO6Z2TMiZECA1BSClFKA$8rKZLrcjx7L2QXqFfI0HvT9y4VZJ7QqGxH0bKqLPnqY', 'student');

-- 创建学生信息
INSERT INTO student (user_id, student_id, name, class_name) VALUES
(LAST_INSERT_ID(), '2021001', '张三', '计算机1班');

-- 验证
SELECT '✅ 账号创建成功!' as 状态;
SELECT 
    u.username as 用户名,
    s.name as 姓名,
    s.student_id as 学号
FROM sys_user u
JOIN student s ON u.id = s.user_id
WHERE u.username = 'student001';

-- 显示登录信息
SELECT 
    'student001' as 用户名,
    'password123' as 密码,
    '请使用此信息登录' as 提示;
