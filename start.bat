@echo off
echo ============================================
echo ShopWise AI - Start Application
echo ============================================
echo.
echo Starting Backend Server...
echo.

cd backend
start cmd /k "venv\Scripts\activate && python main.py"

timeout /t 5 /nobreak >nul

echo Starting Frontend Server...
echo.

cd ..\frontend
start cmd /k "npm run dev"

timeout /t 5 /nobreak >nul

echo.
echo ============================================
echo Application Started! ✓
echo ============================================
echo.
echo Backend running at: http://localhost:8000
echo Frontend running at: http://localhost:3000
echo.
echo Opening browser...
start http://localhost:3000
echo.
echo Press any key to stop all servers...
pause >nul

taskkill /FI "WINDOWTITLE eq *python main.py*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq *npm run dev*" /F >nul 2>&1

echo.
echo Servers stopped.
