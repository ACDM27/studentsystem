# ====================================
# Frontend Server Startup Script
# ====================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Starting Frontend (Vue 3 + Vite)     " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Navigate to frontend directory
Set-Location -Path $PSScriptRoot

# Check Node.js
Write-Host "[1/4] Checking Node.js..." -ForegroundColor Yellow
$nodeVersion = node --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Node.js not installed!" -ForegroundColor Red
    Write-Host "Please download from https://nodejs.org (18+)" -ForegroundColor Yellow
    exit 1
}
Write-Host "[OK] Node.js version: $nodeVersion" -ForegroundColor Green
Write-Host ""

# Check pnpm
Write-Host "[2/4] Checking pnpm..." -ForegroundColor Yellow
$pnpmVersion = pnpm --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[WARN] pnpm not installed, installing..." -ForegroundColor Yellow
    npm install -g pnpm
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to install pnpm!" -ForegroundColor Red
        exit 1
    }
    $pnpmVersion = pnpm --version
}
Write-Host "[OK] pnpm version: $pnpmVersion" -ForegroundColor Green
Write-Host ""

# Check dependencies
Write-Host "[3/4] Checking project dependencies..." -ForegroundColor Yellow
if (!(Test-Path "node_modules")) {
    Write-Host "[WARN] node_modules not found, installing..." -ForegroundColor Yellow
    pnpm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to install dependencies!" -ForegroundColor Red
        exit 1
    }
}
Write-Host "[OK] Dependencies installed" -ForegroundColor Green
Write-Host ""

# Check configuration
Write-Host "[4/4] Starting dev server..." -ForegroundColor Yellow
if (Test-Path ".env") {
    $envContent = Get-Content ".env" -Raw
    if ($envContent -match "VITE_API_URL=(.+)") {
        $apiUrl = $matches[1].Trim()
        Write-Host "Backend API URL: $apiUrl" -ForegroundColor Cyan
    }
}
Write-Host "Frontend will run at: http://localhost:5173" -ForegroundColor Cyan
Write-Host ""
Write-Host "Note: Make sure backend server is running" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Start dev server
pnpm run dev
