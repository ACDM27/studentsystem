from passlib.context import CryptContext
from database import SessionLocal
from models import SysUser, UserRole

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_admin():
    db = SessionLocal()
    try:
        # 检查是否已存在
        existing = db.query(SysUser).filter(SysUser.username == "admin").first()
        if existing:
            print("管理员账号已存在")
            return
        
        # 创建管理员
        hashed_password = pwd_context.hash("admin123")  # 修改为您的密码
        admin_user = SysUser(
            username="admin",
            password_hash=hashed_password,
            role=UserRole.ADMIN
        )
        db.add(admin_user)
        db.commit()
        print("管理员账号创建成功！")
        print("用户名: admin")
        print("密码: admin123")
    except Exception as e:
        print(f"创建失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()