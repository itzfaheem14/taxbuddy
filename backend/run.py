#!/usr/bin/env python3
"""
MuseAIka Backend Application Runner
"""

import os
from app import create_app, socketio

# Create Flask application
app = create_app()

if __name__ == '__main__':
    # Development server settings
    debug = os.getenv('FLASK_ENV', 'production') == 'development'
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    
    print(f"Starting MuseAIka Backend Server...")
    print(f"Environment: {os.getenv('FLASK_ENV', 'production')}")
    print(f"Host: {host}:{port}")
    print(f"Debug: {debug}")
    
    # Run the application with SocketIO support
    socketio.run(
        app,
        host=host,
        port=port,
        debug=debug,
        allow_unsafe_werkzeug=True  # Allow for development
    )