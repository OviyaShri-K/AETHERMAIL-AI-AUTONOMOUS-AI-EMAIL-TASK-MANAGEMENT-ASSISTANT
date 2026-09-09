@echo off
title AI Email & Task Assistant
color 0b
echo =======================================================================
echo   STARTING AUTONOMOUS AI EMAIL & TASK MANAGEMENT SYSTEM
echo =======================================================================
echo.
echo [1/2] Starting FastAPI Backend on http://localhost:8000...
start cmd /k "cd /d %~dp0backend && uvicorn app.main:app --reload --port 8000"

timeout /t 3 /nobreak >nul

echo [2/2] Starting Next.js Frontend on http://localhost:3000...
start cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo =======================================================================
echo   SYSTEM LAUNCHED SUCCESSFULLY!
echo   Frontend Webpage:   http://localhost:3000
echo   Swagger API Docs:   http://localhost:8000/docs
echo   Active Mail ID:      22ai032@nandhaengg.org
echo   PostgreSQL DB:      ai_email_db (localhost:5432)
echo =======================================================================
echo.
pause
