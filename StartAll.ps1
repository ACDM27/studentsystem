# ====================================
# Student System - Quick Start
# ====================================

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "   Student System - Quick Start Script   " -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Tech Stack: Vue 3 + FastAPI + MySQL" -ForegroundColor White
Write-Host ""

# Project root directory
$projectRoot = $PSScriptRoot

# Step 1: Check MySQL
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "[Step 1/3] Checking MySQL Service" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow

$mysqlServices = @("MySQL80", "MySQL", "MySQL57")
$mysqlRunning = $false

foreach ($service in $mysqlServices) {
    $serviceStatus = Get-Service -Name $service -ErrorAction SilentlyContinue
    if ($serviceStatus) {
        if ($serviceStatus.Status -eq "Running") {
            Write-Host "[OK] MySQL service is running: $service" -ForegroundColor Green
            $mysqlRunning = $true
            break
        }
        else {
            Write-Host "[WARN] MySQL service found but not running: $service" -ForegroundColor Yellow
            Write-Host "Attempting to start service..." -ForegroundColor Yellow
            Start-Service -Name $service -ErrorAction SilentlyContinue
            if ($?) {
                Write-Host "[OK] MySQL service started" -ForegroundColor Green
                $mysqlRunning = $true
                break
            }
        }
    }
}

if (-not $mysqlRunning) {
    Write-Host "[ERROR] No running MySQL service found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Solutions:" -ForegroundColor Yellow
    Write-Host "1. Check if MySQL is installed" -ForegroundColor White
    Write-Host "2. Start MySQL manually: net start MySQL80" -ForegroundColor White
    Write-Host "3. Or use XAMPP/WAMP to start MySQL" -ForegroundColor White
    Write-Host ""
    $continue = Read-Host "Continue anyway? (Y/N)"
    if ($continue -ne "Y" -and $continue -ne "y") {
        exit 1
    }
}
Write-Host ""

# Step 2: Start Backend
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "[Step 2/3] Starting Backend Server" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow

Write-Host "Backend will start in a new window..." -ForegroundColor Cyan
Start-Sleep -Seconds 1

$backendPath = Join-Path $projectRoot "backend"
$backendScript = Join-Path $backendPath "StartBackend.ps1"

# If English script doesn't exist, try to start directly
if (-not (Test-Path $backendScript)) {
    $backendScript = Join-Path $backendPath "main.py"
    if (Test-Path $backendScript) {
        Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-Command", "cd '$backendPath'; python main.py"
        Write-Host "[OK] Backend server starting..." -ForegroundColor Green
    }
    else {
        Write-Host "[ERROR] Backend script not found!" -ForegroundColor Red
        exit 1
    }
}
else {
    Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-File", "`"$backendScript`""
    Write-Host "[OK] Backend server starting..." -ForegroundColor Green
}

Write-Host "  URL: http://localhost:8000" -ForegroundColor Cyan
Write-Host "  API Docs: http://localhost:8000/docs" -ForegroundColor Cyan

Write-Host ""
Write-Host "Waiting for backend to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Step 3: Start Frontend
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "[Step 3/3] Starting Frontend Server" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow

Write-Host "Frontend will start in a new window..." -ForegroundColor Cyan
Start-Sleep -Seconds 1

$frontendPath = Join-Path $projectRoot "frontend"
$frontendScript = Join-Path $frontendPath "StartFrontend.ps1"

# If English script doesn't exist, try to start directly
if (-not (Test-Path $frontendScript)) {
    Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-Command", "cd '$frontendPath'; pnpm run dev"
    Write-Host "[OK] Frontend server starting..." -ForegroundColor Green
}
else {
    Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-File", "`"$frontendScript`""
    Write-Host "[OK] Frontend server starting..." -ForegroundColor Green
}

Write-Host "  URL: http://localhost:5173" -ForegroundColor Cyan

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "            Startup Complete!            " -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Service URLs:" -ForegroundColor White
Write-Host "  Frontend: http://localhost:5173" -ForegroundColor Cyan
Write-Host "  Backend:  http://localhost:8000" -ForegroundColor Cyan
Write-Host "  API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Test Account:" -ForegroundColor Yellow
Write-Host "  Student ID: student001" -ForegroundColor White
Write-Host "  Password:   password123" -ForegroundColor White
Write-Host ""
Write-Host "Note:" -ForegroundColor Yellow
Write-Host "  - Two server windows will remain open" -ForegroundColor White
Write-Host "  - Press Ctrl+C in each window to stop servers" -ForegroundColor White
Write-Host "  - Closing windows will also stop servers" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to close this window..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
