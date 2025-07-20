#!/usr/bin/env python3
"""
Test script for Hurray Cafe application
"""

import json
import requests
import time
import sys

def test_data_file():
    """Test if menu data file is valid JSON"""
    try:
        with open('data/menu_categories.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        categories = data.get('categories', [])
        print(f"✅ Menu data loaded successfully - {len(categories)} categories found")
        
        # Check each category has required fields
        for category in categories:
            required_fields = ['id', 'name', 'image', 'description', 'items']
            for field in required_fields:
                if field not in category:
                    print(f"❌ Category '{category.get('name', 'Unknown')}' missing field: {field}")
                    return False
        
        print("✅ All categories have required fields")
        return True
        
    except FileNotFoundError:
        print("❌ Menu data file not found")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in menu data file: {e}")
        return False

def test_flask_app():
    """Test Flask application endpoints"""
    base_url = "http://localhost:5000"
    
    # Wait for app to start
    print("⏳ Waiting for application to start...")
    time.sleep(3)
    
    try:
        # Test health endpoint
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
        
        # Test categories endpoint
        response = requests.get(f"{base_url}/api/categories", timeout=5)
        if response.status_code == 200:
            categories = response.json()
            print(f"✅ Categories endpoint working - {len(categories)} categories returned")
        else:
            print(f"❌ Categories endpoint failed: {response.status_code}")
            return False
        
        # Test restaurant info endpoint
        response = requests.get(f"{base_url}/api/restaurant-info", timeout=5)
        if response.status_code == 200:
            info = response.json()
            print(f"✅ Restaurant info endpoint working - {info.get('name', 'Unknown')}")
        else:
            print(f"❌ Restaurant info endpoint failed: {response.status_code}")
            return False
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to application. Is it running?")
        return False
    except requests.exceptions.Timeout:
        print("❌ Request timeout")
        return False
    except Exception as e:
        print(f"❌ Error testing endpoints: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 50)
    print("🧪 Testing Hurray Cafe Application")
    print("=" * 50)
    
    # Test data file
    if not test_data_file():
        print("❌ Data file test failed")
        sys.exit(1)
    
    # Test Flask app
    if not test_flask_app():
        print("❌ Flask app test failed")
        print("💡 Make sure to run 'python app.py' first")
        sys.exit(1)
    
    print("=" * 50)
    print("🎉 All tests passed! Application is working correctly.")
    print("🌐 Open http://localhost:5000 in your browser")
    print("=" * 50)

if __name__ == "__main__":
    main()