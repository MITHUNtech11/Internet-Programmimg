# EventFlow Startup Script
Write-Host "===============================================================" -ForegroundColor Cyan
Write-Host " Starting EventFlow Production Stack" -ForegroundColor Green
Write-Host "===============================================================" -ForegroundColor Cyan

$baseDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# 1. Start Backend in new window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$baseDir'; python server/run.py"

# 2. Start Frontend in new window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$baseDir\client'; npm run dev"

Write-Host "Services started:" -ForegroundColor Yellow
Write-Host "  -> Frontend Client:  http://localhost:5173" -ForegroundColor White
Write-Host "  -> Backend Swagger:  http://localhost:5000/docs" -ForegroundColor White
