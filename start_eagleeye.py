#!/usr/bin/env python3
"""
EagleEye Project Startup Script
This script helps you get the EagleEye project running quickly
"""

import os
import sys
import subprocess
import time
import threading
from pathlib import Path

def print_header():
    print("=" * 60)
    print("🦅 EagleEye - Advanced Media Management Platform")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    print("📦 Checking dependencies...")
    
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment detected")
    else:
        print("⚠️  No virtual environment detected. It's recommended to use one.")
    
    # Check if requirements.txt exists
    if os.path.exists('requirements.txt'):
        print("✅ requirements.txt found")
        
        # Try to install dependencies if needed
        try:
            import flask
            print("✅ Flask is installed")
        except ImportError:
            print("📥 Installing backend dependencies...")
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
            print("✅ Backend dependencies installed")
    else:
        print("❌ requirements.txt not found")
        return False
    
    return True

def check_frontend_dependencies():
    """Check if frontend dependencies are installed"""
    print("\n📦 Checking frontend dependencies...")
    
    if os.path.exists('frontend/package.json'):
        print("✅ frontend/package.json found")
        
        # Check if node_modules exists
        if os.path.exists('frontend/node_modules'):
            print("✅ Frontend dependencies already installed")
        else:
            print("📥 Installing frontend dependencies...")
            try:
                subprocess.run(['npm', 'install'], cwd='frontend', check=True)
                print("✅ Frontend dependencies installed")
            except (subprocess.CalledProcessError, FileNotFoundError):
                print("❌ Failed to install frontend dependencies")
                print("   Make sure Node.js and npm are installed")
                return False
    else:
        print("❌ frontend/package.json not found")
        return False
    
    return True

def start_backend():
    """Start the backend server"""
    print("\n🚀 Starting backend server...")
    
    try:
        # Change to backend directory
        os.chdir('backend')
        
        # Start the backend server
        backend_process = subprocess.Popen([
            sys.executable, 'run.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait a bit for the server to start
        time.sleep(3)
        
        # Check if the server is running
        try:
            import requests
            response = requests.get('http://localhost:5000/api/health', timeout=5)
            if response.status_code == 200:
                print("✅ Backend server started successfully")
                print("   📡 Backend running on: http://localhost:5000")
                return backend_process
        except:
            pass
        
        print("❌ Backend server failed to start")
        return None
        
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return None

def start_frontend():
    """Start the frontend development server"""
    print("\n🚀 Starting frontend development server...")
    
    try:
        # Change to frontend directory
        os.chdir('frontend')
        
        # Start the frontend server
        frontend_process = subprocess.Popen([
            'npm', 'start'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait a bit for the server to start
        time.sleep(5)
        
        print("✅ Frontend server starting...")
        print("   🌐 Frontend will be available at: http://localhost:3000")
        return frontend_process
        
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")
        return None

def main():
    """Main startup function"""
    print_header()
    
    # Check requirements
    if not check_python_version():
        return
    
    if not check_dependencies():
        return
    
    if not check_frontend_dependencies():
        return
    
    # Start servers
    backend_process = start_backend()
    if not backend_process:
        return
    
    frontend_process = start_frontend()
    if not frontend_process:
        backend_process.terminate()
        return
    
    print("\n" + "=" * 60)
    print("🎉 EagleEye is now running!")
    print("=" * 60)
    print("📱 Frontend: http://localhost:3000")
    print("🔧 Backend:  http://localhost:5000")
    print("🩺 Health:   http://localhost:5000/api/health")
    print()
    print("Press Ctrl+C to stop the servers")
    print("=" * 60)
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            if backend_process.poll() is not None:
                print("❌ Backend server stopped unexpectedly")
                break
            
            if frontend_process.poll() is not None:
                print("❌ Frontend server stopped unexpectedly")
                break
                
    except KeyboardInterrupt:
        print("\n🛑 Stopping servers...")
        
        # Terminate processes
        if backend_process:
            backend_process.terminate()
        
        if frontend_process:
            frontend_process.terminate()
        
        print("✅ All servers stopped")
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()
