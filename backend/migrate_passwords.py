"""
数据库密码迁移脚本
从 Bcrypt 迁移到 Argon2id
"""
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from config import settings
from models import SysUser

# 旧的 Bcrypt 上下文
bcrypt_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__default_rounds=12,
    bcrypt__truncate_error=False
)

# 新的 Argon2 上下文
argon2_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__memory_cost=65536,
    argon2__time_cost=3,
    argon2__parallelism=4,
    argon2__hash_len=32,
)


def is_bcrypt_hash(password_hash: str) -> bool:
    """检查是否是 Bcrypt 哈希"""
    return password_hash.startswith('$2b$') or password_hash.startswith('$2a$')


def migrate_passwords(dry_run=True):
    """
    迁移所有用户密码从 Bcrypt 到 Argon2
    
    参数:
        dry_run: 如果为 True，只显示需要迁移的用户，不实际修改
    """
    print("=" * 70)
    print("密码哈希迁移工具 - Bcrypt → Argon2id")
    print("=" * 70)
    
    # 创建数据库连接
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        # 查询所有用户
        users = db.query(SysUser).all()
        total_users = len(users)
        bcrypt_users = 0
        argon2_users = 0
        
        print(f"\n总用户数: {total_users}")
        
        # 检查每个用户的密码哈希类型
        for user in users:
            if is_bcrypt_hash(user.password_hash):
                bcrypt_users += 1
                print(f"  [Bcrypt] 用户: {user.username} (ID: {user.id})")
            else:
                argon2_users += 1
        
        print(f"\n统计:")
        print(f"  - Bcrypt 密码: {bcrypt_users}")
        print(f"  - Argon2 密码: {argon2_users}")
        
        if bcrypt_users == 0:
            print("\n✅ 所有用户已使用 Argon2，无需迁移！")
            return
        
        print(f"\n需要迁移 {bcrypt_users} 个用户的密码")
        
        if dry_run:
            print("\n⚠️  这是模拟运行，不会实际修改数据库")
            print("要执行实际迁移，请运行: python migrate_passwords.py --execute")
            return
        
        # 实际迁移需要用户确认
        print("\n" + "!" * 70)
        print("警告: 此操作将修改数据库中的密码哈希！")
        print("!" * 70)
        confirm = input("\n是否继续？(yes/no): ")
        
        if confirm.lower() != 'yes':
            print("迁移已取消")
            return
        
        # 执行迁移方式 1: 使用默认密码重新哈希
        print("\n选择迁移方式:")
        print("1. 为所有用户设置统一的默认密码 (推荐)")
        print("2. 保留原密码（需要用户下次登录时更新）")
        
        choice = input("\n请选择 (1 或 2): ")
        
        if choice == "1":
            default_password = input("请输入默认密码 (最少6个字符): ")
            if len(default_password) < 6:
                print("❌ 密码太短！")
                return
            
            migrated = 0
            for user in users:
                if is_bcrypt_hash(user.password_hash):
                    # 使用 Argon2 重新哈希默认密码
                    user.password_hash = argon2_context.hash(default_password)
                    migrated += 1
                    print(f"✅ 已迁移: {user.username}")
            
            db.commit()
            print(f"\n🎉 成功迁移 {migrated} 个用户！")
            print(f"   默认密码: {default_password}")
            print("   请通知用户在首次登录后更改密码！")
        
        elif choice == "2":
            print("\n⚠️  此方式需要实现渐进式迁移逻辑")
            print("在 auth.py 中添加以下代码：")
            print("""
def verify_password(plain_password: str, hashed_password: str) -> bool:
    # 检测是否是旧的 bcrypt 哈希
    if hashed_password.startswith('$2b$') or hashed_password.startswith('$2a$'):
        # 使用 bcrypt 验证
        if bcrypt_context.verify(plain_password, hashed_password):
            # ⚠️ 在实际使用时，这里应该更新数据库中的哈希
            # user.password_hash = argon2_context.hash(plain_password)
            # db.commit()
            return True
        return False
    # 使用 Argon2 验证
    return argon2_context.verify(plain_password, hashed_password)
            """)
        
        else:
            print("❌ 无效的选择")
    
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        db.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='迁移密码哈希从 Bcrypt 到 Argon2')
    parser.add_argument('--execute', action='store_true', help='执行实际迁移（默认为模拟运行）')
    
    args = parser.parse_args()
    
    migrate_passwords(dry_run=not args.execute)
