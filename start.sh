#!/bin/bash

echo "================================================"
echo "🦅 EagleEye - Advanced Media Management Platform"
echo "================================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python is not installed"
    echo "Please install Python 3.8 or higher"
    echo "Visit: https://python.org"
    exit 1
fi

echo "✅ Python detected"
python3 --version

# Check if Node.js is installed
if ! command -v npm &> /dev/null; then
    echo "❌ Node.js/npm is not installed"
    echo "Please install Node.js 14 or higher"
    echo "Visit: https://nodejs.org"
    exit 1
fi

echo "✅ Node.js/npm detected"
npm --version

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found"
    echo "Please make sure you're running this from the EagleEye project directory"
    exit 1
fi

if [ ! -d "backend" ]; then
    echo "❌ Backend directory not found"
    echo "Please make sure you're running this from the EagleEye project directory"
    exit 1
fi

if [ ! -d "frontend" ]; then
    echo "❌ Frontend directory not found"
    echo "Please make sure you're running this from the EagleEye project directory"
    exit 1
fi

echo
echo "📦 Installing dependencies..."
echo

# Install backend dependencies
echo "Installing backend dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install backend dependencies"
    exit 1
fi
echo "✅ Backend dependencies installed"

# Install frontend dependencies
echo "Installing frontend dependencies..."
cd frontend
npm install
if [ $? -ne 0 ]; then
    echo "❌ Failed to install frontend dependencies"
    echo "Make sure Node.js and npm are installed"
    exit 1
fi
echo "✅ Frontend dependencies installed"

cd ..

echo
echo "🚀 Starting servers..."
echo

# Function to cleanup background processes
cleanup() {
    echo
    echo "🛑 Stopping servers..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
    fi
    echo "✅ All servers stopped"
    echo "👋 Goodbye!"
    exit 0
}

# Set trap to cleanup on script termination
trap cleanup SIGINT SIGTERM

# Start backend
echo "Starting backend server..."
cd backend
python3 run.py &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start frontend
echo "Starting frontend server..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

# Wait a moment for frontend to start
sleep 5

echo
echo "================================================"
echo "🎉 EagleEye is now running!"
echo "================================================"
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend:  http://localhost:5000"
echo "🩺 Health:   http://localhost:5000/api/health"
echo
echo "Press Ctrl+C to stop the servers"
echo "================================================"
echo

# Try to open browser (works on most systems)
if command -v xdg-open &> /dev/null; then
    sleep 2
    xdg-open http://localhost:3000
elif command -v open &> /dev/null; then
    sleep 2
    open http://localhost:3000
fi

# Keep script running
wait
