from flask import Flask, render_template, jsonify, request, send_from_directory
import json
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load menu data
def load_menu_data():
    """Load menu data from JSON file"""
    try:
        with open('data/menu_categories.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        logger.error("Menu data file not found")
        return {"categories": [], "restaurant_info": {}}
    except json.JSONDecodeError:
        logger.error("Invalid JSON in menu data file")
        return {"categories": [], "restaurant_info": {}}

# Routes
@app.route('/')
def index():
    """Main page route"""
    return render_template('index.html')

@app.route('/api/categories')
def get_categories():
    """API endpoint to get all menu categories"""
    try:
        menu_data = load_menu_data()
        return jsonify(menu_data.get('categories', []))
    except Exception as e:
        logger.error(f"Error loading categories: {e}")
        return jsonify({"error": "Failed to load categories"}), 500

@app.route('/api/categories/<int:category_id>')
def get_category(category_id):
    """API endpoint to get a specific category by ID"""
    try:
        menu_data = load_menu_data()
        categories = menu_data.get('categories', [])
        
        category = next((cat for cat in categories if cat['id'] == category_id), None)
        
        if category:
            return jsonify(category)
        else:
            return jsonify({"error": "Category not found"}), 404
    except Exception as e:
        logger.error(f"Error loading category {category_id}: {e}")
        return jsonify({"error": "Failed to load category"}), 500

@app.route('/api/restaurant-info')
def get_restaurant_info():
    """API endpoint to get restaurant information"""
    try:
        menu_data = load_menu_data()
        return jsonify(menu_data.get('restaurant_info', {}))
    except Exception as e:
        logger.error(f"Error loading restaurant info: {e}")
        return jsonify({"error": "Failed to load restaurant info"}), 500

@app.route('/api/search')
def search_items():
    """API endpoint to search for items"""
    try:
        query = request.args.get('q', '').lower()
        if not query:
            return jsonify([])
        
        menu_data = load_menu_data()
        categories = menu_data.get('categories', [])
        
        results = []
        for category in categories:
            for item in category.get('items', []):
                if (query in item['name'].lower() or 
                    query in item['description'].lower() or
                    query in category['name'].lower()):
                    results.append({
                        'category': category['name'],
                        'item': item
                    })
        
        return jsonify(results)
    except Exception as e:
        logger.error(f"Error searching items: {e}")
        return jsonify({"error": "Failed to search items"}), 500

@app.route('/api/order', methods=['POST'])
def place_order():
    """API endpoint to place an order"""
    try:
        data = request.get_json()
        
        if not data or 'items' not in data:
            return jsonify({"error": "Invalid order data"}), 400
        
        # Here you would typically save the order to a database
        # For now, we'll just log it and return a success response
        
        order_id = datetime.now().strftime("%Y%m%d%H%M%S")
        logger.info(f"New order received - ID: {order_id}, Items: {data['items']}")
        
        return jsonify({
            "success": True,
            "order_id": order_id,
            "message": "Order placed successfully!",
            "estimated_time": "20-30 minutes"
        })
    except Exception as e:
        logger.error(f"Error placing order: {e}")
        return jsonify({"error": "Failed to place order"}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Hurray Cafe API"
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

# Static file serving
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    # Check if data directory exists
    if not os.path.exists('data'):
        os.makedirs('data')
        logger.info("Created data directory")
    
    # Check if menu data file exists
    if not os.path.exists('data/menu_categories.json'):
        logger.warning("Menu data file not found. Please ensure data/menu_categories.json exists.")
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)