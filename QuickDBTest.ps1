# Quick Database Test
$ErrorActionPreference = "Continue"

Write-Host "Testing MySQL Connection..." -ForegroundColor Cyan

# Activate venv
& ".\.venv\Scripts\Activate.ps1"

# Run Python test
$pythonCode = @"
import pymysql
import sys

try:
    # Test connection
    print('Connecting to MySQL...')
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='password067517'
    )
    print('✅ MySQL connection successful!')
    
    # Create database if not exists
    cursor = conn.cursor()
    cursor.execute('CREATE DATABASE IF NOT EXISTS student_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
    print('✅ Database student_system is ready')
    
    # Test connection to database
    cursor.execute('USE student_system')
    cursor.execute('SHOW TABLES')
    tables = cursor.fetchall()
    print(f'📊 Tables in database: {len(tables)}')
    
    cursor.close()
    conn.close()
    print('✅ All tests passed!')
    sys.exit(0)
    
except pymysql.err.OperationalError as e:
    print(f'❌ Connection failed: {e}')
    sys.exit(1)
except Exception as e:
    print(f'❌ Error: {e}')
    sys.exit(1)
"@

python -c $pythonCode

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Database is ready! You can now start the backend." -ForegroundColor Green
}
else {
    Write-Host ""
    Write-Host "Database connection failed. Please check your MySQL configuration." -ForegroundColor Red
}
