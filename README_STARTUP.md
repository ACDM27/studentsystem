# Student System - Complete Startup Guide

## 🎯 Quick Start (3 Steps)

### Step 1: Start MySQL Database

```powershell
# Start MySQL service
Start-Service MySQL80

# Or check if it's running
Get-Service MySQL80
```

### Step 2: Start Backend Server

**Open Terminal 1:**
```powershell
cd backend
python main.py
```

**Expected output:**
```
Initializing database...
Database initialized successfully!
Uvicorn running on http://0.0.0.0:8000
```

✅ **Verify:** Visit http://localhost:8000/docs

### Step 3: Start Frontend Server

**Open Terminal 2:**
```powershell
cd frontend
pnpm run dev
```

**Expected output:**
```
VITE v5.4.11  ready in XXX ms
➜  Local:   http://localhost:5173/
```

✅ **Verify:** Visit http://localhost:5173

---

## 🚀 Alternative: Use Startup Scripts

### One-Click Start (Recommended)
```powershell
.\StartAll.ps1
```

This will:
- ✓ Check MySQL status
- ✓ Start backend in new window
- ✓ Start frontend in new window

### Separate Scripts
```powershell
# Backend only
cd backend
.\StartBackend.ps1

# Frontend only
cd frontend
.\StartFrontend.ps1
```

---

## 🔧 First Time Setup

### 1. Install MySQL 8.0+

Download from: https://dev.mysql.com/downloads/mysql/

### 2. Create Database

```sql
CREATE DATABASE student_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Configure Backend

Edit `backend/.env`:
```env
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/student_system
```

### 4. Install Backend Dependencies

```powershell
cd backend

# Activate virtual environment (if exists)
..\.venv\Scripts\Activate.ps1

# Install packages
pip install -r requirements.txt

# Initialize database
python init_db.py
```

### 5. Install Frontend Dependencies

```powershell
cd frontend

# Install pnpm (if not installed)
npm install -g pnpm

# Install dependencies
pnpm install
```

---

## 🐛 Troubleshooting

### ❌ Frontend Error: "Cannot find module 'rollup/parseAst'"

**Solution:** Dependencies already fixed! Just reinstall:

```powershell
cd frontend
Remove-Item -Recurse -Force node_modules, pnpm-lock.yaml
pnpm install
```

**Details:** Vite has been downgraded from 7.0.4 to 5.4.11 (stable version)

### ❌ Backend Error: Database connection failed

**Check:**
1. MySQL service is running
2. Database exists
3. Password in `.env` is correct

```powershell
# Check MySQL
Get-Service MySQL80

# Test connection
mysql -u root -p -e "SHOW DATABASES;"
```

### ❌ Port Already in Use

**Backend (8000):**
```powershell
# Find process
netstat -ano | findstr :8000

# Kill process
taskkill /PID <PID> /F
```

**Frontend (5173):**
```powershell
# Find process
netstat -ano | findstr :5173

# Kill process
taskkill /PID <PID> /F
```

### ❌ PowerShell Script Encoding Error

Use **English version scripts** instead:
- `StartAll.ps1` (instead of 一键启动.ps1)
- `backend\StartBackend.ps1`
- `frontend\StartFrontend.ps1`

---

## 📊 Service Ports

| Service | Port | URL |
|---------|------|-----|
| Frontend | 5173 | http://localhost:5173 |
| Backend | 8000 | http://localhost:8000 |
| API Docs | 8000 | http://localhost:8000/docs |
| MySQL | 3306 | localhost:3306 |

---

## 🔐 Test Account

```
Student ID: student001
Password: password123
```

Or check `backend/init_db.py` for more accounts.

---

## 📚 Tech Stack

### Frontend
- Vue 3.5.17
- Vite 5.4.11 (stable)
- Naive UI 2.42.0
- Element Plus 2.11.8
- TypeScript 5.6.3

### Backend
- FastAPI 0.109.0
- Uvicorn 0.27.0
- SQLAlchemy 2.0.25
- MySQL 8.0+

---

## 🎉 Success Checklist

- [ ] MySQL service running
- [ ] Database `student_system` created
- [ ] Backend `.env` configured
- [ ] Backend dependencies installed
- [ ] Backend running on port 8000
- [ ] Frontend dependencies installed
- [ ] Frontend running on port 5173
- [ ] Can login with test account

---

## 💡 Quick Commands Reference

```powershell
# === One-Click Start ===
.\StartAll.ps1

# === Manual Start ===
# Terminal 1 - Backend
cd backend
python main.py

# Terminal 2 - Frontend
cd frontend
pnpm run dev

# === Stop Services ===
# Press Ctrl+C in each terminal

# === Check Status ===
# Backend health check
curl http://localhost:8000/health

# Frontend (browser)
# Visit http://localhost:5173
```

---

**Last Updated:** 2026-01-22

**Need Help?** Check the detailed documentation:
- `项目运行指南.md` (Chinese detailed guide)
- `frontend/依赖修复说明.md` (Dependency fix details)
