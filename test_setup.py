#!/usr/bin/env python3
"""
Quick setup verification script for ShopifyPulse
Run this after installation to verify everything is working
"""

import sys
import os

def check_python_version():
    """Check Python version"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print(f"  ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"  ❌ Python {version.major}.{version.minor} (requires 3.9+)")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    print("\nChecking dependencies...")
    required = [
        'flask', 'flask_sqlalchemy', 'requests', 'plotly'
    ]
    missing = []
    for package in required:
        try:
            __import__(package.replace('_', ''))
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} (missing)")
            missing.append(package)
    return len(missing) == 0

def check_file_structure():
    """Check if all required files exist"""
    print("\nChecking file structure...")
    required_files = [
        'app.py', 'requirements.txt', 'README.md',
        'api/__init__.py', 'models/__init__.py',
        'templates/demo.html', 'static/css/dashboard.css'
    ]
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} (missing)")
            missing.append(file)
    return len(missing) == 0

def test_imports():
    """Test if main modules can be imported"""
    print("\nTesting imports...")
    try:
        import app
        print("  ✅ Main app imports successfully")
        return True
    except Exception as e:
        print(f"  ❌ Import error: {e}")
        return False

def main():
    """Run all checks"""
    print("=" * 50)
    print("ShopifyPulse Setup Verification")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("File Structure", check_file_structure),
        ("Module Imports", test_imports),
    ]
    
    results = []
    for name, check_func in checks:
        results.append(check_func())
    
    print("\n" + "=" * 50)
    if all(results):
        print("✅ All checks passed! Ready to run.")
        print("\nNext steps:")
        print("  1. cp .env.example .env")
        print("  2. Edit .env with your settings")
        print("  3. ./start.sh")
        return 0
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
