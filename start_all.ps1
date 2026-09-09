# PowerShell Script to Start Both Backend and Frontend
Write-Host "=======================================================================" -ForegroundColor Cyan
Write-Host " 🚀 STARTING AUTONOMOUS AI EMAIL & TASK MANAGEMENT SYSTEM" -ForegroundColor Green
Write-Host "=======================================================================" -ForegroundColor Cyan

$root = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "`n[1/2] Starting FastAPI Backend on http://localhost:8000..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd `"$root\backend`"; uvicorn app.main:app --reload --port 8000"

Start-Sleep -Seconds 2

Write-Host "[2/2] Starting Next.js 14 Frontend on http://localhost:3000..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd `"$root\frontend`"; npm run dev"

Write-Host "`n=======================================================================" -ForegroundColor Cyan
Write-Host " 🎉 SYSTEM RUNNING!" -ForegroundColor Green
Write-Host " 🌐 Frontend Webpage:   http://localhost:3000" -ForegroundColor White
Write-Host " 📖 Swagger API Docs:   http://localhost:8000/docs" -ForegroundColor White
Write-Host " 👤 Active Mail ID:      22ai032@nandhaengg.org" -ForegroundColor White
Write-Host " 🐘 PostgreSQL DB:      ai_email_db (localhost:5432)" -ForegroundColor White
Write-Host "=======================================================================`n" -ForegroundColor Cyan
