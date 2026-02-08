"""
简单的账号检查脚本
"""
import sys
import os

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import sessionmaker
    from config import settings
    
    print("=" * 70)
    print("检查 student001 账号")
    print("=" * 70)
    
    # 创建数据库连接
    print(f"\n数据库连接: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'unknown'}")
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    # 直接查询用户表
    print("\n[1] 查询用户表...")
    query = text("SELECT id, username, role, password_hash FROM sys_user WHERE username = :username")
    result = db.execute(query, {"username": "student001"}).fetchone()
    
    if result:
        print(f"✅ 找到用户:")
        print(f"   ID: {result[0]}")
        print(f"   用户名: {result[1]}")
        print(f"   角色: {result[2]}")
        print(f"   密码哈希前缀: {result[3][:20]}...")
        
        # 检查密码类型
        if result[3].startswith('$2b$') or result[3].startswith('$2a$'):
            print(f"   → Bcrypt 格式密码")
        elif result[3].startswith('$argon2'):
            print(f"   → Argon2 格式密码")
        
        # 查询学生信息
        print("\n[2] 查询学生信息...")
        student_query = text("SELECT student_id, name, class_name FROM student WHERE user_id = :user_id")
        student = db.execute(student_query, {"user_id": result[0]}).fetchone()
        
        if student:
            print(f"✅ 找到学生信息:")
            print(f"   学号: {student[0]}")
            print(f"   姓名: {student[1]}")
            print(f"   班级: {student[2]}")
        else:
            print(f"⚠️  未找到学生信息")
        
        # 尝试密码验证
        print("\n[3] 测试密码验证...")
        try:
            from auth import verify_password
            password_hash = result[3]
            test_password = "password123"
            
            is_valid = verify_password(test_password, password_hash)
            
            if is_valid:
                print(f"✅ 密码 '{test_password}' 验证成功！")
            else:
                print(f"❌ 密码 '{test_password}' 验证失败")
                print("   可能原因:")
                print("   1. 密码不是 'password123'")
                print("   2. 密码哈希格式有问题")
                
        except Exception as e:
            print(f"❌ 密码验证出错: {e}")
            print(f"   错误类型: {type(e).__name__}")
        
    else:
        print(f"❌ 用户不存在!")
        print(f"\n建议:")
        print(f"1. 运行创建账号脚本: python create_test_account.py")
        print(f"2. 或检查用户名拼写是否正确")
        
        # 列出所有用户
        print(f"\n[查询] 数据库中的所有用户:")
        all_users = db.execute(text("SELECT username, role FROM sys_user")).fetchall()
        if all_users:
            for user in all_users:
                print(f"   - {user[0]} ({user[1]})")
        else:
            print(f"   (没有任何用户)")
    
    db.close()
    
except Exception as e:
    print(f"\n❌ 发生错误: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("检查完成")
print("=" * 70 + "\n")
