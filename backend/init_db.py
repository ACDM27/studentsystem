"""
Database Initialization and Seed Script
Creates initial data for testing
"""

from sqlalchemy.orm import Session
from database import SessionLocal, init_db
from models import SysUser, SysTeacher, SysStudent, UserRole
from auth import get_password_hash


def seed_database():
    """Seed database with initial test data"""
    db: Session = SessionLocal()
    
    try:
        print("Starting database seeding...")
        
        # Check if data already exists
        existing_users = db.query(SysUser).count()
        if existing_users > 0:
            print("Database already contains data. Skipping seed.")
            return
        
        # Create admin user (系统管理员)
        admin_user = SysUser(
            username="sysadmin",
            password_hash=get_password_hash("admin123"),
            role=UserRole.ADMIN,
            avatar_url=None
        )
        db.add(admin_user)
        
        # Create test student: admin/admin (便于测试)
        test_user = SysUser(
            username="admin",
            password_hash=get_password_hash("admin"),
            role=UserRole.STUDENT,
            avatar_url=None
        )
        db.add(test_user)
        db.flush()  # Get user ID
        
        test_student = SysStudent(
            user_id=test_user.id,
            student_number="TEST001",
            name="测试学生",
            major="计算机科学与技术"
        )
        db.add(test_student)
        
        # Create teachers
        teachers = [
            SysTeacher(name="李教授", title="教授", department="计算机学院"),
            SysTeacher(name="王讲师", title="讲师", department="软件学院"),
            SysTeacher(name="张副教授", title="副教授", department="人工智能学院"),
        ]
        for teacher in teachers:
            db.add(teacher)
        
        # Create student users
        student_user1 = SysUser(
            username="student001",
            password_hash=get_password_hash("password123"),
            role=UserRole.STUDENT,
            avatar_url=None
        )
        db.add(student_user1)
        db.flush()  # Get user ID
        
        # Create student profile
        student1 = SysStudent(
            user_id=student_user1.id,
            student_number="2021001",
            name="张三",
            major="计算机科学与技术"
        )
        db.add(student1)
        
        # Create another student
        student_user2 = SysUser(
            username="student002",
            password_hash=get_password_hash("password123"),
            role=UserRole.STUDENT,
            avatar_url=None
        )
        db.add(student_user2)
        db.flush()
        
        student2 = SysStudent(
            user_id=student_user2.id,
            student_number="2021002",
            name="李四",
            major="软件工程"
        )
        db.add(student2)
        
        db.commit()
        print("Database seeded successfully!")
        print("\n" + "="*60)
        print("测试账号信息：")
        print("="*60)
        print("🎓 学生测试账号（推荐使用）:")
        print("   用户名: admin")
        print("   密码:   admin")
        print("   姓名:   测试学生")
        print()
        print("🔧 系统管理员账号:")
        print("   用户名: sysadmin")
        print("   密码:   admin123")
        print()
        print("👨‍🎓 其他学生账号:")
        print("   用户名: student001  密码: password123  (张三)")
        print("   用户名: student002  密码: password123  (李四)")
        print("="*60)
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("Initializing database tables...")
    init_db()
    print("Database tables created!")
    
    seed_database()
