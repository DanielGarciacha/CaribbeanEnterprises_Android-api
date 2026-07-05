@echo off
REM Script to initialize the database with tables and test users

echo ============================================
echo   CTP API - Database Initialization
echo ============================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Change to backend directory
cd /d "%~dp0..\.."

REM Run initialization script
python scripts\init_db\init_db.py

echo.
echo ============================================
pause
