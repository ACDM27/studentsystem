"""
修复 student001 账号密码
使用正确的 Argon2 哈希
"""
import pymysql
from auth import get_password_hash
from config import settings

def fix_password():
    # 解析数据库连接
    db_url = settings.DATABASE_URL.replace('mysql+pymysql://', '')
    user_pass, host_db = db_url.split('@')
    user, password = user_pass.split(':')
    host_port, database = host_db.split('/')
    host, port = host_port.split(':')
    
    print("=" * 70)
    print("修复 student001 密码")
    print("=" * 70)
    
    try:
        # 连接数据库
        conn = pymysql.connect(
            host=host,
            port=int(port),
            user=user,
            password=password,
            database=database,
            charset='utf8mb4'
        )
        
        cursor = conn.cursor()
        
        # 1. 检查账号是否存在
        print("\n[1] 检查账号...")
        cursor.execute("SELECT id, username, role FROM sys_users WHERE username = %s", ('student001',))
        user_data = cursor.fetchone()
        
        if not user_data:
            print("❌ 账号不存在，请先创建账号")
            return
        
        print(f"✅ 找到账号: ID={user_data[0]}, 用户名={user_data[1]}, 角色={user_data[2]}")
        
        # 2. 生成新的密码哈希
        print("\n[2] 生成新的密码哈希...")
        new_password = "123456"  # 使用您想要的密码
        password_hash = get_password_hash(new_password)
        print(f"✅ 密码哈希已生成")
        print(f"   密码: {new_password}")
        print(f"   哈希前缀: {password_hash[:50]}...")
        
        # 3. 更新密码
        print("\n[3] 更新数据库...")
        cursor.execute(
            "UPDATE sys_users SET password_hash = %s WHERE username = %s",
            (password_hash, 'student001')
        )
        conn.commit()
        print(f"✅ 密码已更新")
        
        # 4. 验证
        print("\n[4] 验证更新...")
        cursor.execute(
            "SELECT username, SUBSTRING(password_hash, 1, 30) as hash_prefix FROM sys_users WHERE username = %s",
            ('student001',)
        )
        result = cursor.fetchone()
        print(f"✅ 验证成功: {result[0]} - {result[1]}...")
        
        # 5. 显示登录信息
        print("\n" + "=" * 70)
        print("✅ 密码修复完成！")
        print("=" * 70)
        print("\n📝 登录信息:")
        print(f"   用户名: student001")
        print(f"   密码:   {new_password}")
        print("\n现在可以使用以上信息登录了！")
        print("=" * 70 + "\n")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_password()
