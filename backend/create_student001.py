"""
创建 student001 测试账号
"""
import sys
from database import SessionLocal
from models import SysUser, Student, UserRole
from auth import get_password_hash

def create_student001():
    db = SessionLocal()
    try:
        print("=" * 70)
        print("创建测试账号: student001")
        print("=" * 70)
        
        # 1. 检查用户是否已存在
        print("\n[1] 检查用户是否已存在...")
        existing_user = db.query(SysUser).filter(SysUser.username == "student001").first()
        
        if existing_user:
            print("⚠️  用户 'student001' 已存在!")
            print(f"   用户ID: {existing_user.id}")
            print(f"   角色: {existing_user.role.value}")
            
            # 检查学生信息
            student = db.query(Student).filter(Student.user_id == existing_user.id).first()
            if student:
                print(f"   学生信息: {student.name} (学号: {student.student_id})")
            else:
                print("   ⚠️  缺少学生信息，正在创建...")
                student = Student(
                    user_id=existing_user.id,
                    student_id="2021001",
                    name="张三",
                    class_name="计算机1班"
                )
                db.add(student)
                db.commit()
                print("   ✅ 学生信息已创建")
            
            # 更新密码为标准测试密码
            print("\n[2] 更新密码为 'password123'...")
            existing_user.password_hash = get_password_hash("password123")
            db.commit()
            print("   ✅ 密码已更新")
            
            print("\n✅ 账号已就绪!")
            return
        
        # 2. 创建新用户
        print("✅ 用户不存在，开始创建...")
        
        user = SysUser(
            username="student001",
            password_hash=get_password_hash("password123"),
            role=UserRole.STUDENT
        )
        db.add(user)
        db.flush()  # 获取 user.id
        
        print(f"   ✅ 用户已创建 (ID: {user.id})")
        
        # 3. 创建学生信息
        print("\n[3] 创建学生信息...")
        student = Student(
            user_id=user.id,
            student_id="2021001",
            name="张三",
            class_name="计算机1班"
        )
        db.add(student)
        db.commit()
        
        print("   ✅ 学生信息已创建")
        
        # 4. 成功提示
        print("\n" + "=" * 70)
        print("✅ 测试账号创建成功!")
        print("=" * 70)
        print("\n📝 登录信息:")
        print("   用户名: student001")
        print("   密码:   password123")
        print("   姓名:   张三")
        print("   学号:   2021001")
        print("   班级:   计算机1班")
        print("\n" + "=" * 70)
        print("\n💡 使用说明:")
        print("1. 确保后端服务正在运行:")
        print("   uvicorn main:app --reload")
        print("\n2. 在前端登录页面输入:")
        print("   用户名: student001")
        print("   密码:   password123")
        print()
        
    except Exception as e:
        print(f"\n❌ 创建失败: {e}")
        print(f"   错误类型: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        db.rollback()
        sys.exit(1)
        
    finally:
        db.close()

if __name__ == "__main__":
    create_student001()
