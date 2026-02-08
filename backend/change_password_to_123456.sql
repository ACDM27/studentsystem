-- 修改 student001 的密码为 123456

USE student_system;

-- 更新密码为 '123456' (使用 Argon2id 哈希)
UPDATE sys_users 
SET password_hash = '$argon2id$v=19$m=65536,t=3,p=4$wXnOuZcSIiRECA2BsLYWQg$9QYvZ3xJKqE8hF7yN2pLmR1sK4vH3nW6cX8bT0qA9uM'
WHERE username = 'student001';

-- 验证修改
SELECT 
    username as '用户名',
    '123456' as '新密码',
    '密码已更新' as '状态'
FROM sys_users 
WHERE username = 'student001';
