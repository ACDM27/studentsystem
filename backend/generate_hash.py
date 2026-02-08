"""
快速修复 student001 密码
"""
import sys
sys.path.insert(0, 'd:\\student_system\\backend')

from auth import get_password_hash

# 生成密码哈希
password = "123456"
hash_value = get_password_hash(password)

print("=" * 70)
print("生成的密码哈希")
print("=" * 70)
print(f"密码: {password}")
print(f"哈希值:")
print(hash_value)
print("\n复制以下 SQL 到 MySQL 中执行:\n")
print(f"UPDATE sys_users SET password_hash = '{hash_value}' WHERE username = 'student001';")
print("\n" + "=" * 70)
