#!/usr/bin/env python3
"""
Simple Flask app for testing
"""

from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        'message': 'EagleEye Backend is running!',
        'timestamp': datetime.now().isoformat(),
        'status': 'healthy'
    })

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.0'
    })

if __name__ == '__main__':
    print("🦅 Starting EagleEye Simple Backend...")
    print("📡 Server will be available at: http://localhost:5000")
    print("🚀 Starting server...\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
