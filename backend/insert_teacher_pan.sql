
-- 插入或更新教师信息：潘卫华
INSERT INTO sys_teachers (name, department, title)
VALUES ('潘卫华', '信息技术学院', '副教授')
ON DUPLICATE KEY UPDATE 
    department = VALUES(department),
    title = VALUES(title);

-- 验证插入结果
SELECT id, name, department, title FROM sys_teachers WHERE name = '潘卫华';
