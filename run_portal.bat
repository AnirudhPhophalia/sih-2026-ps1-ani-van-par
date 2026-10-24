@echo off
title AICTE Security Deposit & FDR Management Portal
echo =======================================================================
echo   Launching AICTE FDR Lifecycle Portal & Zero-Trust Governance Engine
echo =======================================================================
echo.
cd /d "%~dp0"

if not exist "venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found at .\venv. Please create it first.
    pause
    exit /b 1
)

echo Starting portal server on http://127.0.0.1:8000 ...
.\venv\Scripts\python.exe run_portal.py
pause
