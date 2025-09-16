#!/usr/bin/env python3
"""
Simple test script to verify backend functionality
"""

import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_imports():
    """Test if we can import required modules"""
    try:
        print("Testing imports...")
        
        # Test Flask imports
        from flask import Flask
        print("✅ Flask imported successfully")
        
        # Test our services
        from backend.services.auth_service import AuthService
        print("✅ AuthService imported successfully")
        
        from backend.services.youtube_service import YouTubeService
        print("✅ YouTubeService imported successfully")
        
        from backend.utils.helpers import is_valid_url
        print("✅ Helper functions imported successfully")
        
        print("\n🎉 All imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality"""
    try:
        print("\nTesting basic functionality...")
        
        # Test URL validation
        from backend.utils.helpers import is_valid_url
        
        test_urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtu.be/dQw4w9WgXcQ",
            "invalid-url",
            "not-a-url"
        ]
        
        for url in test_urls:
            result = is_valid_url(url)
            status = "✅" if result else "❌"
            print(f"{status} URL validation for '{url}': {result}")
        
        # Test auth service
        from backend.services.auth_service import AuthService
        auth_service = AuthService()
        print("✅ AuthService instantiated successfully")
        
        print("\n🎉 Basic functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Functionality test error: {e}")
        return False

if __name__ == "__main__":
    print("🦅 EagleEye Backend Test Suite")
    print("=" * 40)
    
    # Run tests
    imports_ok = test_imports()
    
    if imports_ok:
        functionality_ok = test_basic_functionality()
        
        if functionality_ok:
            print("\n🎉 All tests passed! Backend is ready.")
            sys.exit(0)
        else:
            print("\n❌ Functionality tests failed.")
            sys.exit(1)
    else:
        print("\n❌ Import tests failed. Please install dependencies.")
        print("Run: pip install -r requirements.txt")
        sys.exit(1)
