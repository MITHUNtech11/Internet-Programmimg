@echo off
title EventFlow - Smart Campus Event Portal
echo ===============================================================
echo Starting EventFlow Backend (FastAPI) and Frontend (Vite)...
echo ===============================================================

start "EventFlow Backend Server (Port 5000)" cmd /k "cd /d "%~dp0" && python server/run.py"
start "EventFlow Frontend Client (Port 5173)" cmd /k "cd /d "%~dp0client" && npm run dev"

echo Both services launched!
echo - Frontend: http://localhost:5173
echo - Backend API & Docs: http://localhost:5000/docs
pause
