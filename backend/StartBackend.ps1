# ====================================
# Backend Server Startup Script
# ====================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Starting Backend (FastAPI + MySQL)   " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Navigate to backend directory
Set-Location -Path $PSScriptRoot

# Check for virtual environment
Write-Host "[1/4] Checking Python virtual environment..." -ForegroundColor Yellow
$venvPath = ".venv\Scripts\Activate.ps1"
$parentVenvPath = "..\.venv\Scripts\Activate.ps1"

if (Test-Path $venvPath) {
    Write-Host "[OK] Activating local venv..." -ForegroundColor Green
    & $venvPath
}
elseif (Test-Path $parentVenvPath) {
    Write-Host "[OK] Activating parent venv..." -ForegroundColor Green
    & $parentVenvPath
}
else {
    Write-Host "[WARN] No virtual environment found, using system Python" -ForegroundColor Yellow
}
Write-Host ""

# Check dependencies
Write-Host "[2/4] Checking dependencies..." -ForegroundColor Yellow
$packages = @("fastapi", "uvicorn", "sqlalchemy")
$missingPackages = @()

foreach ($package in $packages) {
    pip show $package 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        $missingPackages += $package
    }
}

if ($missingPackages.Count -gt 0) {
    Write-Host "[WARN] Missing packages: $($missingPackages -join ', ')" -ForegroundColor Yellow
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to install dependencies!" -ForegroundColor Red
        exit 1
    }
}
Write-Host "[OK] All dependencies installed" -ForegroundColor Green
Write-Host ""

# Check configuration
Write-Host "[3/4] Checking configuration..." -ForegroundColor Yellow
if (!(Test-Path ".env")) {
    Write-Host "[ERROR] .env file not found!" -ForegroundColor Red
    Write-Host "Please copy from .env.example and configure" -ForegroundColor Yellow
    exit 1
}
Write-Host "[OK] Configuration file exists" -ForegroundColor Green
Write-Host ""

# Start server
Write-Host "[4/4] Starting server..." -ForegroundColor Yellow
Write-Host "Backend will run at: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API docs available at: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Note: Database will be initialized on first run" -ForegroundColor Gray
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Start the server
python main.py
