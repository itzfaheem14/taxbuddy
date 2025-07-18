import os
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from dotenv import load_dotenv
from pymongo import MongoClient
import redis

# Load environment variables
load_dotenv()

# Initialize extensions
socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16777216))
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
    
    # Initialize CORS
    CORS(app, origins=os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(','))
    
    # Initialize SocketIO
    socketio.init_app(app)
    
    # Database connections
    app.mongodb_client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017/museaika'))
    app.db = app.mongodb_client.get_database()
    
    try:
        app.redis_client = redis.from_url(os.getenv('REDIS_URL', 'redis://localhost:6379'))
        app.redis_client.ping()
    except redis.ConnectionError:
        print("Warning: Redis connection failed. Some features may not work.")
        app.redis_client = None
    
    # Register blueprints
    from app.api.auth import auth_bp
    from app.api.emotion import emotion_bp
    from app.api.music import music_bp
    from app.api.social import social_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(emotion_bp, url_prefix='/api/emotion')
    app.register_blueprint(music_bp, url_prefix='/api/music')
    app.register_blueprint(social_bp, url_prefix='/api/social')
    
    # Create upload directory
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    return app