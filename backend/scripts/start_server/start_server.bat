@echo off
REM Script to start the FastAPI development server

echo ============================================
echo   CTP API - Starting Development Server
echo ============================================
echo.
echo Server will be available at:
echo   - API: http://localhost:8000
echo   - Docs: http://localhost:8000/docs
echo   - ReDoc: http://localhost:8000/redoc
echo.
echo Press Ctrl+C to stop the server
echo ============================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Start server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
