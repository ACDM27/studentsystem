
from passlib.context import CryptContext
import datetime

# 初始化密码上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hash(password):
    return pwd_context.hash(password)

# 用户数据
users = [
    {
        "username": "huangkun",
        "password": "123456",
        "role": "student",
        "name": "黄坤",
        "student_number": "2024001",
        "major": "计算机科学与技术"
    },
    {
        "username": "zhangzhenle",
        "password": "123456",
        "role": "student",
        "name": "张振乐",
        "student_number": "2024002",
        "major": "计算机科学与技术"
    },
    {
        "username": "admin",
        "password": "admin123",
        "role": "admin",
        "name": "系统管理员",
        "student_number": None,
        "major": None
    }
]

sql_content = """-- 批量创建用户SQL脚本
-- 生成时间: {}
USE student_system;

""".format(datetime.datetime.now())

for user in users:
    password_hash = get_hash(user["password"])
    
    # 1. 插入用户 (使用 INSERT IGNORE 避免重复报错，或者 ON DUPLICATE KEY UPDATE)
    # 为了简单且安全，我们先尝试删除旧的（如果是测试数据），或者根据用户名判断
    # 这里使用 INSERT INTO ... ON DUPLICATE KEY UPDATE 来确保幂等性
    
    # 注意：SysUser表结构
    # id, username, password_hash, role, avatar_url, created_at
    
    sql_content += f"""
-- 处理用户: {user['username']} ({user['name']})
-- 1. 插入或更新 sys_users
INSERT INTO sys_users (username, password_hash, role, created_at)
VALUES ('{user['username']}', '{password_hash}', '{user['role']}', NOW())
ON DUPLICATE KEY UPDATE 
    password_hash = VALUES(password_hash),
    role = VALUES(role);

-- 获取用户ID
SET @user_id_{user['username']} = (SELECT id FROM sys_users WHERE username = '{user['username']}');
"""

    if user["role"] == "student":
        # 2. 插入学生信息
        # id, user_id, student_number, name, major, persona_cache
        sql_content += f"""
-- 2. 插入或更新 sys_students
INSERT INTO sys_students (user_id, student_number, name, major)
VALUES (@user_id_{user['username']}, '{user['student_number']}', '{user['name']}', '{user['major']}')
ON DUPLICATE KEY UPDATE
    name = VALUES(name),
    major = VALUES(major);
"""

    sql_content += "\n"

# 写入文件
output_file = "d:\\student_system\\backend\\insert_new_users.sql"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(sql_content)

print(f"SQL文件生成成功: {output_file}")
