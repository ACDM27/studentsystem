-- 数据库账号检查 SQL
-- 在 MySQL 客户端或 phpMyAdmin 中执行

USE student_system;

-- 1. 查询 student001 用户
SELECT 
    '=== 系统用户信息 ===' as 检查项;

SELECT 
    id as 用户ID,
    username as 用户名,
    role as 角色,
    SUBSTRING(password_hash, 1, 30) as 密码哈希前缀,
    LENGTH(password_hash) as 哈希长度,
    created_at as 创建时间
FROM sys_user 
WHERE username = 'student001';

-- 2. 如果上面有结果，查询对应的学生信息
-- 替换 @user_id 为上面查询到的用户ID
SELECT 
    '=== 学生信息 ===' as 检查项;

SELECT 
    s.id as 学生表ID,
    s.student_id as 学号,
    s.name as 姓名,
    s.class_name as 班级,
    s.user_id as 关联用户ID,
    s.created_at as 创建时间
FROM student s
WHERE s.user_id = (SELECT id FROM sys_user WHERE username = 'student001');

-- 3. 列出所有系统用户（如果 student001 不存在）
SELECT 
    '=== 所有系统用户 ===' as 检查项;

SELECT 
    id,
    username,
    role,
    SUBSTRING(password_hash, 1, 20) as 密码前缀,
    created_at
FROM sys_user
ORDER BY id;

-- 4. 统计信息
SELECT 
    '=== 统计信息 ===' as 检查项;

SELECT 
    (SELECT COUNT(*) FROM sys_user) as 用户总数,
    (SELECT COUNT(*) FROM sys_user WHERE role = 'student') as 学生账号数,
    (SELECT COUNT(*) FROM sys_user WHERE role = 'admin') as 管理员账号数,
    (SELECT COUNT(*) FROM student) as 学生信息记录数;
