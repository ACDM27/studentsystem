# ====================================
# 学生综合信息服务平台 - 完整项目启动
# ====================================

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "   学生综合信息服务平台 - 一键启动脚本   " -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "技术栈：Vue 3 + FastAPI + MySQL" -ForegroundColor White
Write-Host ""

# 项目根目录
$projectRoot = $PSScriptRoot

# 步骤 1: 检查 MySQL
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "[步骤 1/3] 检查 MySQL 数据库服务" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow

$mysqlServices = @("MySQL80", "MySQL", "MySQL57")
$mysqlRunning = $false

foreach ($service in $mysqlServices) {
    $serviceStatus = Get-Service -Name $service -ErrorAction SilentlyContinue
    if ($serviceStatus) {
        if ($serviceStatus.Status -eq "Running") {
            Write-Host "✓ MySQL 服务正在运行: $service" -ForegroundColor Green
            $mysqlRunning = $true
            break
        }
        else {
            Write-Host "⚠ MySQL 服务已安装但未运行: $service" -ForegroundColor Yellow
            Write-Host "尝试启动服务..." -ForegroundColor Yellow
            Start-Service -Name $service -ErrorAction SilentlyContinue
            if ($?) {
                Write-Host "✓ MySQL 服务已启动" -ForegroundColor Green
                $mysqlRunning = $true
                break
            }
        }
    }
}

if (-not $mysqlRunning) {
    Write-Host "✗ 未找到运行中的 MySQL 服务！" -ForegroundColor Red
    Write-Host ""
    Write-Host "解决方案：" -ForegroundColor Yellow
    Write-Host "1. 检查 MySQL 是否已安装" -ForegroundColor White
    Write-Host "2. 手动启动 MySQL 服务：net start MySQL80" -ForegroundColor White
    Write-Host "3. 或使用 XAMPP/WAMP 等工具启动 MySQL" -ForegroundColor White
    Write-Host ""
    $continue = Read-Host "是否继续？(如果使用其他数据库，输入 Y) [Y/N]"
    if ($continue -ne "Y" -and $continue -ne "y") {
        exit 1
    }
}
Write-Host ""

# 步骤 2: 启动后端
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "[步骤 2/3] 启动后端服务器" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow

Write-Host "后端将在新窗口启动..." -ForegroundColor Cyan
Start-Sleep -Seconds 1

$backendPath = Join-Path $projectRoot "backend"
$backendScript = Join-Path $backendPath "启动后端.ps1"

if (Test-Path $backendScript) {
    Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-File", "`"$backendScript`""
    Write-Host "✓ 后端服务器启动中..." -ForegroundColor Green
    Write-Host "  访问地址: http://localhost:8000" -ForegroundColor Cyan
    Write-Host "  API 文档: http://localhost:8000/docs" -ForegroundColor Cyan
}
else {
    Write-Host "✗ 未找到后端启动脚本！" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "等待后端服务器启动..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# 步骤 3: 启动前端
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "[步骤 3/3] 启动前端服务器" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow

Write-Host "前端将在新窗口启动..." -ForegroundColor Cyan
Start-Sleep -Seconds 1

$frontendPath = Join-Path $projectRoot "frontend"
$frontendScript = Join-Path $frontendPath "启动前端.ps1"

if (Test-Path $frontendScript) {
    Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-File", "`"$frontendScript`""
    Write-Host "✓ 前端服务器启动中..." -ForegroundColor Green
    Write-Host "  访问地址: http://localhost:5173" -ForegroundColor Cyan
}
else {
    Write-Host "✗ 未找到前端启动脚本！" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "            ✓ 项目启动完成！            " -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "服务访问地址：" -ForegroundColor White
Write-Host "  前端应用: http://localhost:5173" -ForegroundColor Cyan
Write-Host "  后端 API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "  API 文档: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "注意事项：" -ForegroundColor Yellow
Write-Host "  - 两个服务器窗口会保持打开状态" -ForegroundColor White
Write-Host "  - 在各自窗口按 Ctrl+C 可停止对应服务" -ForegroundColor White
Write-Host "  - 关闭窗口也会停止服务" -ForegroundColor White
Write-Host ""
Write-Host "测试账号：" -ForegroundColor Yellow
Write-Host "  学号: student001" -ForegroundColor White
Write-Host "  密码: password123" -ForegroundColor White
Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "按任意键关闭此窗口..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
