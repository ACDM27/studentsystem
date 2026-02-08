# 创建测试账号脚本
Write-Host "正在创建测试账号..." -ForegroundColor Green

# 激活虚拟环境并运行脚本
$pythonPath = ".\.venv\Scripts\python.exe"

if (Test-Path $pythonPath) {
    Write-Host "使用虚拟环境Python: $pythonPath" -ForegroundColor Cyan
    & $pythonPath create_test_account.py
}
else {
    Write-Host "虚拟环境未找到，使用系统Python" -ForegroundColor Yellow
    python create_test_account.py
}

Write-Host "`n按任意键退出..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
