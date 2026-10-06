@echo off
echo ============================================
echo ShopWise AI - Git Setup for Deployment
echo ============================================
echo.

echo [Step 1/3] Initializing Git Repository...
git init

echo.
echo [Step 2/3] Adding all files...
git add .

echo.
echo [Step 3/3] Creating initial commit...
git commit -m "Initial commit - ShopWise AI ready for deployment"

echo.
echo ============================================
echo Git Setup Complete! ✓
echo ============================================
echo.
echo Next Steps:
echo.
echo 1. Create a GitHub repository at: https://github.com/new
echo    Name it: shopwise-ai
echo    Make it Public
echo.
echo 2. Run these commands (replace YOUR_USERNAME):
echo.
echo    git remote add origin https://github.com/YOUR_USERNAME/shopwise-ai.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 3. Follow DEPLOYMENT_GUIDE.md to deploy to Render + Vercel
echo.
echo ============================================
pause
