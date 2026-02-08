# 前端启动脚本

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "        学生综合信息服务平台 - 前端启动脚本" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# 1. 检查node_modules
if (-not (Test-Path ".\node_modules")) {
    Write-Host "[1/3] node_modules不存在，正在安装依赖..." -ForegroundColor Yellow
    npm install --force
    if ($LASTEXITCODE -ne 0) {
        Write-Host "依赖安装失败！" -ForegroundColor Red
        exit 1
    }
    Write-Host "依赖安装完成！" -ForegroundColor Green
} else {
    Write-Host "[1/3] node_modules已存在" -ForegroundColor Green
}

# 2. 检查vite
if (-not (Test-Path ".\node_modules\vite")) {
    Write-Host "[2/3] Vite未安装，正在安装..." -ForegroundColor Yellow  
    npm install vite @vitejs/plugin-vue --force
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Vite安装失败！" -ForegroundColor Red
        exit 1
    }
    Write-Host "Vite安装完成！" -ForegroundColor Green
} else {
    Write-Host "[2/3] Vite已安装" -ForegroundColor Green
}

# 3. 启动开发服务器
Write-Host "[3/3] 正在启动前端开发服务器..." -ForegroundColor Yellow
Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  前端服务即将启动在: http://localhost:5173" -ForegroundColor Green
Write-Host "  测试账号: admin / admin" -ForegroundColor Green  
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

npm run dev
