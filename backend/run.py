#!/usr/bin/env python3
"""
Simple runner for the EagleEye backend server
"""

import os
import sys
from app import app, socketio

if __name__ == '__main__':
    print("🦅 EagleEye Backend Server Starting...")
    print("📡 Server will run on: http://localhost:5000")
    print("🔗 Health check: http://localhost:5000/api/health")
    print("⚡ Starting SocketIO server...")
    
    # Run the app with SocketIO
    socketio.run(
        app,
        debug=True,
        host='0.0.0.0',
        port=5000,
        allow_unsafe_werkzeug=True
    )
