@echo off
echo ============================================
echo ShopWise AI - Windows Setup Script
echo ============================================
echo.

echo [1/4] Setting up Backend...
cd backend

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing backend dependencies...
pip install -r requirements.txt

echo.
echo [2/4] Backend setup complete!
echo.

cd ..

echo [3/4] Setting up Frontend...
cd frontend

echo Installing frontend dependencies...
call npm install

echo.
echo [4/4] Frontend setup complete!
echo.

cd ..

echo ============================================
echo Setup Complete! ✓
echo ============================================
echo.
echo Your API keys are already configured in backend/.env
echo.
echo To run the application:
echo.
echo   Terminal 1 (Backend):
echo     cd backend
echo     venv\Scripts\activate
echo     python main.py
echo.
echo   Terminal 2 (Frontend):
echo     cd frontend
echo     npm run dev
echo.
echo Then open: http://localhost:3000
echo.
echo ============================================
pause
