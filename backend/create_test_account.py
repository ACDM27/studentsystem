"""
Quick test to create admin/admin account
"""
from database import SessionLocal
from models import SysUser, SysStudent, UserRole
from auth import get_password_hash

def create_test_account():
    db = SessionLocal()
    try:
        # Check if admin user already exists
        existing = db.query(SysUser).filter(SysUser.username == "admin").first()
        if existing:
            print("✅ 用户 'admin' 已存在!")
            # Check student profile
            student = db.query(SysStudent).filter(SysStudent.user_id == existing.id).first()
            if student:
                print(f"   学生信息: {student.name} (学号: {student.student_number})")
            print(f"   用户名: admin")
            print(f"   角色: {existing.role.value}")
            return
        
        # Create user
        user = SysUser(
            username="admin",
            password_hash=get_password_hash("admin"),
            role=UserRole.STUDENT,
            avatar_url=None
        )
        db.add(user)
        db.flush()
        
        # Create student profile
        student = SysStudent(
            user_id=user.id,
            student_number="TEST001",  # 修正: 使用 student_number 而不是 student_id
            name="测试学生",
            major="计算机科学与技术"
        )
        db.add(student)
        db.commit()
        
        print("✅ 测试账号创建成功!")
        print("="*50)
        print("🎓 登录信息:")
        print("   用户名: admin")
        print("   密码:   admin")
        print("   姓名:   测试学生")
        print("   学号:   TEST001")
        print("="*50)
        
    except Exception as e:
        print(f"❌ 创建失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_account()
