"""
Backend Diagnostic Script
检查后端环境和配置
"""
import sys
import os

print("=" * 60)
print("Backend Environment Diagnostic")
print("=" * 60)
print()

# 1. Python version
print("1. Python Version:")
print(f"   {sys.version}")
print()

# 2. Current directory
print("2. Current Directory:")
print(f"   {os.getcwd()}")
print()

# 3. Check imports
print("3. Checking Critical Imports:")
imports_to_check = [
    "fastapi",
    "uvicorn",
    "sqlalchemy",
    "pymysql",
    "pydantic",
    "pydantic_settings",
    "jose",
    "passlib",
]

for module_name in imports_to_check:
    try:
        __import__(module_name)
        print(f"   ✅ {module_name}")
    except ImportError as e:
        print(f"   ❌ {module_name}: {e}")
print()

# 4. Check .env file
print("4. Configuration File:")
if os.path.exists(".env"):
    print("   ✅ .env file exists")
    with open(".env", "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines[:5]:  # Show first 5 lines
            if "PASSWORD" in line.upper() or "KEY" in line.upper():
                # Mask sensitive data
                parts = line.split("=")
                if len(parts) == 2:
                    print(f"   {parts[0]}=***")
            else:
                print(f"   {line.strip()}")
else:
    print("   ❌ .env file not found")
print()

# 5. Test database connection
print("5. Database Connection Test:")
try:
    from config import settings
    print(f"   Database URL configured: {settings.DATABASE_URL.split('@')[0]}@***")
    
    import pymysql
    # Parse URL
    import re
    pattern = r'mysql\+pymysql://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)'
    match = re.match(pattern, settings.DATABASE_URL)
    
    if match:
        db_config = {
            'user': match.group(1),
            'password': match.group(2),
            'host': match.group(3),
            'port': int(match.group(4)),
            'database': match.group(5)
        }
        
        # Test connection
        conn = pymysql.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
        print(f"   ✅ Connected to MySQL database '{db_config['database']}'")
        conn.close()
    else:
        print("   ⚠️  Could not parse database URL")
        
except Exception as e:
    print(f"   ❌ Database connection failed: {e}")
print()

# 6. Check if we can import main app
print("6. FastAPI Application:")
try:
    from main import app
    print("   ✅ FastAPI app imported successfully")
    print(f"   App title: {app.title}")
    print(f"   App version: {app.version}")
except Exception as e:
    print(f"   ❌ Failed to import app: {e}")
    import traceback
    traceback.print_exc()
print()

print("=" * 60)
print("Diagnostic Complete")
print("=" * 60)
