"""
数据库账号检查脚本
查询 student001 账号是否存在
"""
import pymysql
from config import settings

def check_account():
    # 解析数据库连接字符串
    # 格式: mysql+pymysql://user:password@host:port/database
    db_url = settings.DATABASE_URL.replace('mysql+pymysql://', '')
    
    # 分割连接信息
    user_pass, host_db = db_url.split('@')
    user, password = user_pass.split(':')
    host_port, database = host_db.split('/')
    host, port = host_port.split(':')
    
    print("=" * 70)
    print("数据库账号检查")
    print("=" * 70)
    print(f"\n数据库: {database}@{host}:{port}")
    print(f"查询账号: student001\n")
    
    try:
        # 连接数据库
        connection = pymysql.connect(
            host=host,
            port=int(port),
            user=user,
            password=password,
            database=database,
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            # 1. 查询用户是否存在
            print("[1] 查询系统用户表 (sys_user)...")
            sql = """
                SELECT id, username, role, 
                       SUBSTRING(password_hash, 1, 30) as hash_prefix,
                       LENGTH(password_hash) as hash_length,
                       created_at
                FROM sys_user 
                WHERE username = %s
            """
            cursor.execute(sql, ('student001',))
            user_result = cursor.fetchone()
            
            if user_result:
                print(f"✅ 找到用户!")
                print(f"   ID: {user_result[0]}")
                print(f"   用户名: {user_result[1]}")
                print(f"   角色: {user_result[2]}")
                print(f"   密码哈希前缀: {user_result[3]}...")
                print(f"   密码哈希长度: {user_result[4]} 字符")
                print(f"   创建时间: {user_result[5]}")
                
                # 判断密码类型
                if user_result[3].startswith('$2b$') or user_result[3].startswith('$2a$'):
                    print(f"   密码格式: Bcrypt (旧格式)")
                elif user_result[3].startswith('$argon2'):
                    print(f"   密码格式: Argon2 (新格式)")
                else:
                    print(f"   密码格式: 未知")
                
                user_id = user_result[0]
                
                # 2. 查询学生信息
                print(f"\n[2] 查询学生信息表 (student)...")
                sql = """
                    SELECT id, student_id, name, class_name, created_at
                    FROM student 
                    WHERE user_id = %s
                """
                cursor.execute(sql, (user_id,))
                student_result = cursor.fetchone()
                
                if student_result:
                    print(f"✅ 找到学生信息!")
                    print(f"   学生表ID: {student_result[0]}")
                    print(f"   学号: {student_result[1]}")
                    print(f"   姓名: {student_result[2]}")
                    print(f"   班级: {student_result[3]}")
                    print(f"   创建时间: {student_result[4]}")
                else:
                    print(f"⚠️  未找到学生信息!")
                    print(f"   账号存在但缺少学生信息")
                
                # 总结
                print(f"\n" + "=" * 70)
                print("检查结果")
                print("=" * 70)
                print(f"✅ 账号存在: student001")
                print(f"✅ 用户ID: {user_id}")
                print(f"✅ 角色: {user_result[2]}")
                if student_result:
                    print(f"✅ 学生信息: {student_result[2]} ({student_result[1]})")
                else:
                    print(f"⚠️  学生信息: 缺失")
                
                print(f"\n如果无法登录，可能原因:")
                print(f"1. 密码不是 'password123'")
                print(f"2. 后端服务未运行")
                print(f"3. 前端连接配置错误")
                
            else:
                print(f"❌ 未找到用户 'student001'")
                
                # 列出所有用户
                print(f"\n[查询] 数据库中的所有用户:")
                sql = "SELECT username, role FROM sys_user ORDER BY id"
                cursor.execute(sql)
                all_users = cursor.fetchall()
                
                if all_users:
                    print(f"   共 {len(all_users)} 个用户:")
                    for user in all_users:
                        print(f"   - {user[0]} ({user[1]})")
                else:
                    print(f"   数据库中没有任何用户!")
                
                print(f"\n建议操作:")
                print(f"1. 运行创建账号脚本:")
                print(f"   python create_test_account.py")
                print(f"\n2. 或手动创建账号（见创建测试账号指南.md）")
        
        connection.close()
        
    except Exception as e:
        print(f"\n❌ 数据库连接或查询失败:")
        print(f"   错误: {e}")
        print(f"\n请检查:")
        print(f"1. MySQL 服务是否运行")
        print(f"2. .env 文件中的数据库配置是否正确")
        print(f"3. 数据库 '{database}' 是否存在")

if __name__ == "__main__":
    check_account()
    print()
