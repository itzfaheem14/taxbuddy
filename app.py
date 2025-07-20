#!/usr/bin/env python3
"""
Hurray Cafe - Flask Backend Server
A modern cafe menu application with ordering functionality
"""

from flask import Flask, jsonify, request, send_from_directory, render_template_string
from flask_cors import CORS
import json
import os
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
app.config['SECRET_KEY'] = 'hurray-cafe-secret-key-2024'
app.config['DEBUG'] = True

# In-memory storage (in production, you'd use a proper database)
orders = []
cart_sessions = {}

def load_menu_data():
    """Load menu data from JSON file"""
    try:
        with open('menu_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Warning: menu_data.json not found")
        return {"categories": []}

@app.route('/')
def index():
    """Serve the main application"""
    try:
        with open('index.html', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Hurray Cafe - File Not Found</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body class="bg-gray-100 flex items-center justify-center min-h-screen">
            <div class="text-center p-8">
                <h1 class="text-3xl font-bold text-gray-800 mb-4">Welcome to Hurray Cafe!</h1>
                <p class="text-gray-600 mb-4">The frontend files are not found. Please ensure index.html exists.</p>
                <p class="text-sm text-gray-500">Backend server is running on Flask</p>
            </div>
        </body>
        </html>
        """

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    try:
        return send_from_directory('.', filename)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

@app.route('/api/menu')
def get_menu():
    """Get complete menu data"""
    menu_data = load_menu_data()
    return jsonify(menu_data)

@app.route('/api/categories')
def get_categories():
    """Get all menu categories"""
    menu_data = load_menu_data()
    categories = [
        {
            "id": cat["id"],
            "name": cat["name"],
            "image": cat["image"],
            "description": cat["description"],
            "item_count": len(cat.get("items", []))
        }
        for cat in menu_data.get("categories", [])
    ]
    return jsonify({"categories": categories})

@app.route('/api/categories/<category_id>')
def get_category(category_id):
    """Get specific category with all items"""
    menu_data = load_menu_data()
    category = next(
        (cat for cat in menu_data.get("categories", []) if cat["id"] == category_id),
        None
    )
    
    if not category:
        return jsonify({"error": "Category not found"}), 404
    
    return jsonify(category)

@app.route('/api/items/<item_id>')
def get_item(item_id):
    """Get specific menu item"""
    menu_data = load_menu_data()
    
    for category in menu_data.get("categories", []):
        for item in category.get("items", []):
            if item["id"] == item_id:
                item_with_category = item.copy()
                item_with_category["category_name"] = category["name"]
                item_with_category["category_id"] = category["id"]
                return jsonify(item_with_category)
    
    return jsonify({"error": "Item not found"}), 404

@app.route('/api/cart', methods=['GET', 'POST'])
def handle_cart():
    """Handle cart operations"""
    session_id = request.headers.get('X-Session-ID', str(uuid.uuid4()))
    
    if request.method == 'GET':
        # Get cart contents
        cart = cart_sessions.get(session_id, [])
        total = sum(item.get('price', 0) * item.get('quantity', 0) for item in cart)
        return jsonify({
            "session_id": session_id,
            "items": cart,
            "total": round(total, 2),
            "item_count": sum(item.get('quantity', 0) for item in cart)
        })
    
    elif request.method == 'POST':
        # Add item to cart
        data = request.get_json()
        
        if not data or 'item_id' not in data:
            return jsonify({"error": "Item ID required"}), 400
        
        # Get item details from menu
        menu_data = load_menu_data()
        item_found = None
        category_name = None
        
        for category in menu_data.get("categories", []):
            for item in category.get("items", []):
                if item["id"] == data["item_id"]:
                    item_found = item
                    category_name = category["name"]
                    break
            if item_found:
                break
        
        if not item_found:
            return jsonify({"error": "Item not found"}), 404
        
        # Initialize cart if not exists
        if session_id not in cart_sessions:
            cart_sessions[session_id] = []
        
        cart = cart_sessions[session_id]
        quantity = data.get('quantity', 1)
        
        # Check if item already in cart
        existing_item = next(
            (item for item in cart if item['id'] == data['item_id']),
            None
        )
        
        if existing_item:
            existing_item['quantity'] += quantity
        else:
            cart_item = item_found.copy()
            cart_item['quantity'] = quantity
            cart_item['category_name'] = category_name
            cart_item['added_at'] = datetime.now().isoformat()
            cart.append(cart_item)
        
        return jsonify({
            "message": "Item added to cart",
            "session_id": session_id,
            "item": item_found["name"],
            "quantity": quantity
        })

@app.route('/api/cart/<session_id>', methods=['DELETE'])
def clear_cart(session_id):
    """Clear cart for session"""
    if session_id in cart_sessions:
        del cart_sessions[session_id]
    return jsonify({"message": "Cart cleared"})

@app.route('/api/cart/<session_id>/items/<item_id>', methods=['DELETE', 'PUT'])
def modify_cart_item(session_id, item_id):
    """Remove or update item in cart"""
    if session_id not in cart_sessions:
        return jsonify({"error": "Cart not found"}), 404
    
    cart = cart_sessions[session_id]
    item_index = next(
        (i for i, item in enumerate(cart) if item['id'] == item_id),
        None
    )
    
    if item_index is None:
        return jsonify({"error": "Item not found in cart"}), 404
    
    if request.method == 'DELETE':
        # Remove item from cart
        removed_item = cart.pop(item_index)
        return jsonify({
            "message": "Item removed from cart",
            "item": removed_item["name"]
        })
    
    elif request.method == 'PUT':
        # Update item quantity
        data = request.get_json()
        new_quantity = data.get('quantity', 1)
        
        if new_quantity <= 0:
            removed_item = cart.pop(item_index)
            return jsonify({
                "message": "Item removed from cart",
                "item": removed_item["name"]
            })
        else:
            cart[item_index]['quantity'] = new_quantity
            return jsonify({
                "message": "Item quantity updated",
                "item": cart[item_index]["name"],
                "quantity": new_quantity
            })

@app.route('/api/orders', methods=['GET', 'POST'])
def handle_orders():
    """Handle order operations"""
    if request.method == 'GET':
        # Get all orders (in production, you'd filter by user)
        return jsonify({"orders": orders})
    
    elif request.method == 'POST':
        # Create new order
        data = request.get_json()
        session_id = data.get('session_id')
        
        if not session_id or session_id not in cart_sessions:
            return jsonify({"error": "Valid cart session required"}), 400
        
        cart = cart_sessions[session_id]
        if not cart:
            return jsonify({"error": "Cart is empty"}), 400
        
        # Create order
        order = {
            "id": str(uuid.uuid4()),
            "session_id": session_id,
            "items": cart.copy(),
            "total": sum(item.get('price', 0) * item.get('quantity', 0) for item in cart),
            "status": "pending",
            "customer_info": {
                "name": data.get('customer_name', 'Guest'),
                "phone": data.get('customer_phone', ''),
                "email": data.get('customer_email', ''),
                "notes": data.get('notes', '')
            },
            "created_at": datetime.now().isoformat(),
            "estimated_time": "15-20 minutes"
        }
        
        orders.append(order)
        
        # Clear cart after order
        del cart_sessions[session_id]
        
        return jsonify({
            "message": "Order placed successfully",
            "order_id": order["id"],
            "total": round(order["total"], 2),
            "estimated_time": order["estimated_time"]
        })

@app.route('/api/orders/<order_id>')
def get_order(order_id):
    """Get specific order details"""
    order = next((o for o in orders if o["id"] == order_id), None)
    
    if not order:
        return jsonify({"error": "Order not found"}), 404
    
    return jsonify(order)

@app.route('/api/orders/<order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    """Update order status"""
    data = request.get_json()
    new_status = data.get('status')
    
    if new_status not in ['pending', 'preparing', 'ready', 'completed', 'cancelled']:
        return jsonify({"error": "Invalid status"}), 400
    
    order = next((o for o in orders if o["id"] == order_id), None)
    
    if not order:
        return jsonify({"error": "Order not found"}), 404
    
    order["status"] = new_status
    order["updated_at"] = datetime.now().isoformat()
    
    return jsonify({
        "message": "Order status updated",
        "order_id": order_id,
        "status": new_status
    })

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "service": "Hurray Cafe API"
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    print("🎉 Starting Hurray Cafe Server...")
    print("📱 Access the app at: http://localhost:5000")
    print("🔧 API endpoints available at: http://localhost:5000/api/")
    print("📊 Health check: http://localhost:5000/api/health")
    
    # Create menu_data.json if it doesn't exist
    if not os.path.exists('menu_data.json'):
        print("⚠️  menu_data.json not found. Please ensure it exists for full functionality.")
    
    app.run(host='0.0.0.0', port=5000, debug=True)