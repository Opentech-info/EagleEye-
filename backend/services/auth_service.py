"""
Authentication Service - Handles user registration, login, and profile management
"""

import hashlib
import json
import os
from datetime import datetime
from flask import jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

class AuthService:
    def __init__(self):
        self.users_file = 'users_data.json'
        self.ensure_users_file()
    
    def ensure_users_file(self):
        """Ensure users data file exists"""
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({}, f)
    
    def load_users(self):
        """Load users from JSON file"""
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def save_users(self, users_data):
        """Save users to JSON file"""
        with open(self.users_file, 'w') as f:
            json.dump(users_data, f, indent=2)
    
    def hash_password(self, password):
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, data):
        """Register a new user"""
        try:
            username = data.get('username', '').strip()
            email = data.get('email', '').strip()
            password = data.get('password', '')
            
            # Validation
            if not username or not email or not password:
                return {
                    'success': False,
                    'error': 'Username, email, and password are required'
                }
            
            if len(username) < 3:
                return {
                    'success': False,
                    'error': 'Username must be at least 3 characters long'
                }
            
            if len(password) < 6:
                return {
                    'success': False,
                    'error': 'Password must be at least 6 characters long'
                }
            
            # Check if user already exists
            users = self.load_users()
            
            if username in users:
                return {
                    'success': False,
                    'error': 'Username already exists'
                }
            
            # Check if email already exists
            for user_data in users.values():
                if user_data.get('email') == email:
                    return {
                        'success': False,
                        'error': 'Email already registered'
                    }
            
            # Create new user
            user_data = {
                'username': username,
                'email': email,
                'password_hash': self.hash_password(password),
                'created_at': datetime.utcnow().isoformat(),
                'last_login': None,
                'is_active': True,
                'profile': {
                    'full_name': data.get('full_name', ''),
                    'avatar': None,
                    'preferences': {
                        'default_quality': '720p',
                        'download_location': 'downloads/',
                        'auto_subtitle': False
                    }
                }
            }
            
            users[username] = user_data
            self.save_users(users)
            
            # Create access token
            access_token = create_access_token(identity=username)
            
            return {
                'success': True,
                'message': 'User registered successfully',
                'access_token': access_token,
                'user': {
                    'username': username,
                    'email': email,
                    'created_at': user_data['created_at']
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def login_user(self, data):
        """Login user"""
        try:
            username = data.get('username', '').strip()
            password = data.get('password', '')
            
            if not username or not password:
                return {
                    'success': False,
                    'error': 'Username and password are required'
                }
            
            users = self.load_users()
            
            if username not in users:
                return {
                    'success': False,
                    'error': 'Invalid username or password'
                }
            
            user_data = users[username]
            
            # Check if user is active
            if not user_data.get('is_active', True):
                return {
                    'success': False,
                    'error': 'Account is deactivated'
                }
            
            # Verify password
            if user_data['password_hash'] != self.hash_password(password):
                return {
                    'success': False,
                    'error': 'Invalid username or password'
                }
            
            # Update last login
            user_data['last_login'] = datetime.utcnow().isoformat()
            users[username] = user_data
            self.save_users(users)
            
            # Create access token
            access_token = create_access_token(identity=username)
            
            return {
                'success': True,
                'message': 'Login successful',
                'access_token': access_token,
                'user': {
                    'username': username,
                    'email': user_data['email'],
                    'last_login': user_data['last_login'],
                    'profile': user_data.get('profile', {})
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_user_profile(self, username):
        """Get user profile"""
        try:
            users = self.load_users()
            
            if username not in users:
                return {
                    'success': False,
                    'error': 'User not found'
                }
            
            user_data = users[username]
            
            return {
                'success': True,
                'user': {
                    'username': username,
                    'email': user_data['email'],
                    'created_at': user_data['created_at'],
                    'last_login': user_data.get('last_login'),
                    'profile': user_data.get('profile', {}),
                    'is_active': user_data.get('is_active', True)
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def update_user_profile(self, username, profile_data):
        """Update user profile"""
        try:
            users = self.load_users()
            
            if username not in users:
                return {
                    'success': False,
                    'error': 'User not found'
                }
            
            user_data = users[username]
            
            # Update profile fields
            if 'profile' not in user_data:
                user_data['profile'] = {}
            
            allowed_fields = ['full_name', 'avatar', 'preferences']
            for field in allowed_fields:
                if field in profile_data:
                    user_data['profile'][field] = profile_data[field]
            
            users[username] = user_data
            self.save_users(users)
            
            return {
                'success': True,
                'message': 'Profile updated successfully',
                'profile': user_data['profile']
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
