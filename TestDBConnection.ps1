# 测试数据库连接
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Testing MySQL Database Connection" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 激活虚拟环境并运行测试
$venvPath = Join-Path $PSScriptRoot ".venv\Scripts\Activate.ps1"

if (Test-Path $venvPath) {
    Write-Host "[1/2] Activating virtual environment..." -ForegroundColor Yellow
    & $venvPath
    Write-Host "[OK] Virtual environment activated" -ForegroundColor Green
    Write-Host ""
}
else {
    Write-Host "[WARN] Virtual environment not found, using system Python" -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "[2/2] Running database connection test..." -ForegroundColor Yellow
Write-Host ""

# 切换到 backend 目录并运行测试
Set-Location -Path (Join-Path $PSScriptRoot "backend")
python test_db_connection.py

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Test Complete" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
