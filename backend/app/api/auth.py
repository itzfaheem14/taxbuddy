from flask import Blueprint, request, jsonify, redirect, current_app
from app.services.spotify_service import SpotifyService
import jwt
import datetime
import os

auth_bp = Blueprint('auth', __name__)
spotify_service = SpotifyService()

@auth_bp.route('/spotify/login', methods=['GET'])
def spotify_login():
    """Initiate Spotify OAuth login."""
    try:
        auth_url = spotify_service.get_auth_url()
        
        return jsonify({
            'success': True,
            'auth_url': auth_url
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to generate auth URL: {str(e)}'
        }), 500

@auth_bp.route('/spotify/callback', methods=['POST'])
def spotify_callback():
    """Handle Spotify OAuth callback."""
    try:
        data = request.get_json()
        
        if not data or 'code' not in data:
            return jsonify({
                'success': False,
                'error': 'Authorization code is required'
            }), 400
        
        authorization_code = data['code']
        
        # Exchange code for access token
        token_result = spotify_service.get_access_token(authorization_code)
        
        if not token_result['success']:
            return jsonify(token_result), 400
        
        access_token = token_result['access_token']
        
        # Get user profile
        profile_result = spotify_service.get_user_profile(access_token)
        
        if not profile_result['success']:
            return jsonify(profile_result), 400
        
        user_info = profile_result['user']
        
        # Generate JWT token for our application
        jwt_payload = {
            'user_id': user_info['id'],
            'display_name': user_info['display_name'],
            'email': user_info.get('email'),
            'spotify_access_token': access_token,
            'spotify_refresh_token': token_result['refresh_token'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            'iat': datetime.datetime.utcnow()
        }
        
        jwt_token = jwt.encode(
            jwt_payload,
            os.getenv('JWT_SECRET_KEY', 'default-secret'),
            algorithm='HS256'
        )
        
        # Store user session in Redis if available
        if current_app.redis_client:
            try:
                current_app.redis_client.setex(
                    f"user_session:{user_info['id']}",
                    3600,  # 1 hour
                    jwt_token
                )
            except Exception as e:
                print(f"Warning: Failed to store session in Redis: {e}")
        
        return jsonify({
            'success': True,
            'token': jwt_token,
            'user': user_info,
            'expires_in': 3600
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Authentication failed: {str(e)}'
        }), 500

@auth_bp.route('/verify', methods=['POST'])
def verify_token():
    """Verify JWT token and return user info."""
    try:
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                'success': False,
                'error': 'Invalid authorization header'
            }), 401
        
        token = auth_header[7:]  # Remove 'Bearer ' prefix
        
        try:
            payload = jwt.decode(
                token,
                os.getenv('JWT_SECRET_KEY', 'default-secret'),
                algorithms=['HS256']
            )
            
            return jsonify({
                'success': True,
                'user': {
                    'id': payload['user_id'],
                    'display_name': payload['display_name'],
                    'email': payload.get('email')
                },
                'valid': True
            }), 200
            
        except jwt.ExpiredSignatureError:
            return jsonify({
                'success': False,
                'error': 'Token has expired'
            }), 401
            
        except jwt.InvalidTokenError:
            return jsonify({
                'success': False,
                'error': 'Invalid token'
            }), 401
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Token verification failed: {str(e)}'
        }), 500

@auth_bp.route('/profile', methods=['GET'])
def get_profile():
    """Get user profile information."""
    try:
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                'success': False,
                'error': 'Authorization required'
            }), 401
        
        token = auth_header[7:]
        
        try:
            payload = jwt.decode(
                token,
                os.getenv('JWT_SECRET_KEY', 'default-secret'),
                algorithms=['HS256']
            )
            
            # Get fresh profile from Spotify
            spotify_access_token = payload.get('spotify_access_token')
            
            if spotify_access_token:
                profile_result = spotify_service.get_user_profile(spotify_access_token)
                
                if profile_result['success']:
                    return jsonify({
                        'success': True,
                        'user': profile_result['user']
                    }), 200
            
            # Fallback to token data
            return jsonify({
                'success': True,
                'user': {
                    'id': payload['user_id'],
                    'display_name': payload['display_name'],
                    'email': payload.get('email')
                }
            }), 200
            
        except jwt.ExpiredSignatureError:
            return jsonify({
                'success': False,
                'error': 'Token has expired'
            }), 401
            
        except jwt.InvalidTokenError:
            return jsonify({
                'success': False,
                'error': 'Invalid token'
            }), 401
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to get profile: {str(e)}'
        }), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout user and invalidate session."""
    try:
        auth_header = request.headers.get('Authorization')
        
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header[7:]
            
            try:
                payload = jwt.decode(
                    token,
                    os.getenv('JWT_SECRET_KEY', 'default-secret'),
                    algorithms=['HS256']
                )
                
                user_id = payload['user_id']
                
                # Remove session from Redis if available
                if current_app.redis_client:
                    try:
                        current_app.redis_client.delete(f"user_session:{user_id}")
                    except Exception as e:
                        print(f"Warning: Failed to remove session from Redis: {e}")
                
            except jwt.InvalidTokenError:
                pass  # Token already invalid
        
        return jsonify({
            'success': True,
            'message': 'Logged out successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Logout failed: {str(e)}'
        }), 500