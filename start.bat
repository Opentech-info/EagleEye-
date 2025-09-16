@echo off
echo ================================================
echo 🦅 EagleEye - Advanced Media Management Platform
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    echo Download from: https://python.org
    pause
    exit /b 1
)

echo ✅ Python detected
python --version

REM Check if we're in the right directory
if not exist "requirements.txt" (
    echo ❌ requirements.txt not found
    echo Please make sure you're running this from the EagleEye project directory
    pause
    exit /b 1
)

if not exist "backend" (
    echo ❌ Backend directory not found
    echo Please make sure you're running this from the EagleEye project directory
    pause
    exit /b 1
)

if not exist "frontend" (
    echo ❌ Frontend directory not found
    echo Please make sure you're running this from the EagleEye project directory
    pause
    exit /b 1
)

echo.
echo 📦 Installing dependencies...
echo.

REM Install backend dependencies
echo Installing backend dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install backend dependencies
    pause
    exit /b 1
)
echo ✅ Backend dependencies installed

REM Install frontend dependencies
echo Installing frontend dependencies...
cd frontend
npm install
if errorlevel 1 (
    echo ❌ Failed to install frontend dependencies
    echo Make sure Node.js and npm are installed
    echo Download from: https://nodejs.org
    pause
    exit /b 1
)
echo ✅ Frontend dependencies installed

cd ..

echo.
echo 🚀 Starting servers...
echo.

REM Start backend in new window
echo Starting backend server...
start "EagleEye Backend" cmd /k "cd backend ; python run.py"

REM Wait a moment for backend to start
timeout /t 5 /nobreak >nul

REM Start frontend in new window
echo Starting frontend server...
start "EagleEye Frontend" cmd /k "cd frontend && npm start"

echo.
echo ================================================
echo 🎉 EagleEye is now running!
echo ================================================
echo 📱 Frontend: http://localhost:3000
echo 🔧 Backend:  http://localhost:5000
echo 🩺 Health:   http://localhost:5000/api/health
echo.
echo Two command windows should have opened for each server.
echo Close them to stop the servers.
echo ================================================
echo.

REM Open browser to frontend
timeout /t 10 /nobreak >nul
start http://localhost:3000

pause
