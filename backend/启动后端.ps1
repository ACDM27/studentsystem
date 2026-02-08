# 后端启动脚本

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "        学生综合信息服务平台 - 后端启动脚本" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan  
Write-Host ""

# 1. 检查Python依赖
Write-Host "[1/3] 检查Python依赖..." -ForegroundColor Yellow
$modules = @("fastapi", "uvicorn", "pymysql", "sqlalchemy")
$missing = @()

foreach ($module in $modules) {
    python -c "import $module" 2>$null
    if ($LASTEXITCODE -ne 0) {
        $missing += $module
    }
}

if ($missing.Count -gt 0) {
    Write-Host "缺少依赖: $($missing -join ', ')" -ForegroundColor Yellow
    Write-Host "正在安装..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "依赖安装失败！" -ForegroundColor Red
        exit 1
    }
    Write-Host "依赖安装完成！" -ForegroundColor Green
} else {
    Write-Host "所有依赖已安装" -ForegroundColor Green
}

# 2. 检查MySQL连接
Write-Host "[2/3] 检查MySQL连接..." -ForegroundColor Yellow
python -c "from database import engine; engine.connect(); print('数据库连接成功!')" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "数据库连接失败！请检查MySQL服务是否启动" -ForegroundColor Red
    Write-Host "提示: 运行 Get-Service MySQL* 查看MySQL状态" -ForegroundColor Yellow
    exit 1  
}
Write-Host "数据库连接正常" -ForegroundColor Green

# 3. 启动FastAPI服务器
Write-Host "[3/3] 正在启动后端服务器..." -ForegroundColor Yellow
Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  后端API服务即将启动在: http://localhost:8000" -ForegroundColor Green
Write-Host "  API文档地址: http://localhost:8000/docs" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
