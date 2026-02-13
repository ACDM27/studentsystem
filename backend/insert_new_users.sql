-- 批量创建用户SQL脚本
-- 生成时间: 2026-02-10 22:15:22.951968
USE student_system;


-- 处理用户: huangkun (黄坤)
-- 1. 插入或更新 sys_users
INSERT INTO sys_users (username, password_hash, role, created_at)
VALUES ('huangkun', '$2b$12$NOCuGjdy30igkNd0FS034eyd1eB6E7eIXLf4reJncppQZV4BYyy6O', 'student', NOW())
ON DUPLICATE KEY UPDATE 
    password_hash = VALUES(password_hash),
    role = VALUES(role);

-- 获取用户ID
SET @user_id_huangkun = (SELECT id FROM sys_users WHERE username = 'huangkun');

-- 2. 插入或更新 sys_students
INSERT INTO sys_students (user_id, student_number, name, major)
VALUES (@user_id_huangkun, '2024001', '黄坤', '计算机科学与技术')
ON DUPLICATE KEY UPDATE
    name = VALUES(name),
    major = VALUES(major);


-- 处理用户: zhangzhenle (张振乐)
-- 1. 插入或更新 sys_users
INSERT INTO sys_users (username, password_hash, role, created_at)
VALUES ('zhangzhenle', '$2b$12$Q6mwdxtku2vfQzF3oFbvEusKr.K3FGTZCm9Tqi1LZZPx06HLlY3i.', 'student', NOW())
ON DUPLICATE KEY UPDATE 
    password_hash = VALUES(password_hash),
    role = VALUES(role);

-- 获取用户ID
SET @user_id_zhangzhenle = (SELECT id FROM sys_users WHERE username = 'zhangzhenle');

-- 2. 插入或更新 sys_students
INSERT INTO sys_students (user_id, student_number, name, major)
VALUES (@user_id_zhangzhenle, '2024002', '张振乐', '计算机科学与技术')
ON DUPLICATE KEY UPDATE
    name = VALUES(name),
    major = VALUES(major);


-- 处理用户: admin (系统管理员)
-- 1. 插入或更新 sys_users
INSERT INTO sys_users (username, password_hash, role, created_at)
VALUES ('admin', '$2b$12$6LBc2TLIk6xdMC57bSw7her9Mh5vbzvSgxwB6JWGqeOw2Ef7ycPKi', 'admin', NOW())
ON DUPLICATE KEY UPDATE 
    password_hash = VALUES(password_hash),
    role = VALUES(role);

-- 获取用户ID
SET @user_id_admin = (SELECT id FROM sys_users WHERE username = 'admin');

