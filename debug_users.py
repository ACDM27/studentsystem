from backend.database import SessionLocal
from backend.models import SysUser, UserRole

def check_users():
    db = SessionLocal()
    try:
        users = db.query(SysUser).all()
        print(f"Total users: {len(users)}")
        for user in users:
            print(f"ID: {user.id}, Username: {user.username}, Role: {user.role}, Has Student Profile: {user.student is not None}")
    finally:
        db.close()

if __name__ == "__main__":
    check_users()
