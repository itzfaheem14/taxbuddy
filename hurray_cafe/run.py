#!/usr/bin/env python3
"""
Hurray Cafe - Startup Script
This script provides an easy way to start the Hurray Cafe web application.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def install_requirements():
    """Install required packages"""
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("❌ Error: requirements.txt not found")
        sys.exit(1)
    
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Error: Failed to install dependencies")
        sys.exit(1)

def check_data_file():
    """Check if menu data file exists"""
    data_file = Path("data/menu_categories.json")
    if not data_file.exists():
        print("❌ Error: data/menu_categories.json not found")
        print("Please ensure the menu data file exists")
        sys.exit(1)
    print("✅ Menu data file found")

def start_application():
    """Start the Flask application"""
    print("🚀 Starting Hurray Cafe...")
    print("📍 Application will be available at: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Hurray Cafe stopped")
    except ImportError as e:
        print(f"❌ Error importing app: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

def main():
    """Main function"""
    print("=" * 50)
    print("🍕 Welcome to Hurray Cafe Web Application")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Install requirements
    install_requirements()
    
    # Check data file
    check_data_file()
    
    # Start application
    start_application()

if __name__ == "__main__":
    main()