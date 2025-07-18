from flask import Blueprint, request, jsonify, current_app
from flask_socketio import emit, join_room, leave_room, rooms
from app import socketio
import jwt
import os
from datetime import datetime
import json

social_bp = Blueprint('social', __name__)

# In-memory storage for collaborative sessions (use Redis in production)
collaborative_sessions = {}

@social_bp.route('/sessions/create', methods=['POST'])
def create_collaborative_session():
    """Create a new collaborative playlist session."""
    try:
        # Verify authentication
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
        except jwt.InvalidTokenError:
            return jsonify({
                'success': False,
                'error': 'Invalid token'
            }), 401
        
        data = request.get_json()
        
        if not data or 'name' not in data:
            return jsonify({
                'success': False,
                'error': 'Session name is required'
            }), 400
        
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{payload['user_id']}"
        
        session_data = {
            'id': session_id,
            'name': data['name'],
            'description': data.get('description', ''),
            'creator': payload['user_id'],
            'creator_name': payload['display_name'],
            'participants': [payload['user_id']],
            'playlist': [],
            'created_at': datetime.now().isoformat(),
            'is_active': True,
            'emotion_theme': data.get('emotion_theme', 'mixed'),
            'allow_voting': data.get('allow_voting', True),
            'max_participants': data.get('max_participants', 10)
        }
        
        collaborative_sessions[session_id] = session_data
        
        # Store in Redis if available
        if current_app.redis_client:
            try:
                current_app.redis_client.setex(
                    f"collab_session:{session_id}",
                    86400,  # 24 hours
                    json.dumps(session_data, default=str)
                )
            except Exception as e:
                print(f"Warning: Failed to store session in Redis: {e}")
        
        return jsonify({
            'success': True,
            'session': session_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to create session: {str(e)}'
        }), 500

@social_bp.route('/sessions/<session_id>/join', methods=['POST'])
def join_collaborative_session(session_id):
    """Join an existing collaborative session."""
    try:
        # Verify authentication
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
        except jwt.InvalidTokenError:
            return jsonify({
                'success': False,
                'error': 'Invalid token'
            }), 401
        
        # Get session data
        session_data = collaborative_sessions.get(session_id)
        
        if not session_data:
            # Try to get from Redis
            if current_app.redis_client:
                try:
                    session_json = current_app.redis_client.get(f"collab_session:{session_id}")
                    if session_json:
                        session_data = json.loads(session_json.decode('utf-8'))
                        collaborative_sessions[session_id] = session_data
                except Exception as e:
                    print(f"Warning: Failed to get session from Redis: {e}")
        
        if not session_data:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
        
        if not session_data['is_active']:
            return jsonify({
                'success': False,
                'error': 'Session is not active'
            }), 400
        
        user_id = payload['user_id']
        
        # Check if user is already in session
        if user_id not in session_data['participants']:
            # Check max participants limit
            if len(session_data['participants']) >= session_data['max_participants']:
                return jsonify({
                    'success': False,
                    'error': 'Session is full'
                }), 400
            
            session_data['participants'].append(user_id)
            
            # Update session
            collaborative_sessions[session_id] = session_data
            
            # Update in Redis
            if current_app.redis_client:
                try:
                    current_app.redis_client.setex(
                        f"collab_session:{session_id}",
                        86400,
                        json.dumps(session_data, default=str)
                    )
                except Exception as e:
                    print(f"Warning: Failed to update session in Redis: {e}")
        
        return jsonify({
            'success': True,
            'session': session_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to join session: {str(e)}'
        }), 500

@social_bp.route('/sessions/<session_id>/add-track', methods=['POST'])
def add_track_to_session(session_id):
    """Add a track to collaborative session."""
    try:
        # Verify authentication
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
        except jwt.InvalidTokenError:
            return jsonify({
                'success': False,
                'error': 'Invalid token'
            }), 401
        
        data = request.get_json()
        
        if not data or 'track' not in data:
            return jsonify({
                'success': False,
                'error': 'Track data is required'
            }), 400
        
        session_data = collaborative_sessions.get(session_id)
        
        if not session_data:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
        
        user_id = payload['user_id']
        
        if user_id not in session_data['participants']:
            return jsonify({
                'success': False,
                'error': 'Not a participant in this session'
            }), 403
        
        track_data = data['track']
        track_data.update({
            'added_by': user_id,
            'added_by_name': payload['display_name'],
            'added_at': datetime.now().isoformat(),
            'votes': 0,
            'voted_by': []
        })
        
        session_data['playlist'].append(track_data)
        
        # Update session
        collaborative_sessions[session_id] = session_data
        
        # Update in Redis
        if current_app.redis_client:
            try:
                current_app.redis_client.setex(
                    f"collab_session:{session_id}",
                    86400,
                    json.dumps(session_data, default=str)
                )
            except Exception as e:
                print(f"Warning: Failed to update session in Redis: {e}")
        
        # Emit to all participants via WebSocket
        socketio.emit('track_added', {
            'session_id': session_id,
            'track': track_data,
            'playlist_length': len(session_data['playlist'])
        }, room=session_id)
        
        return jsonify({
            'success': True,
            'track': track_data,
            'playlist_length': len(session_data['playlist'])
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to add track: {str(e)}'
        }), 500

@social_bp.route('/sessions', methods=['GET'])
def get_user_sessions():
    """Get user's collaborative sessions."""
    try:
        # Verify authentication
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
        except jwt.InvalidTokenError:
            return jsonify({
                'success': False,
                'error': 'Invalid token'
            }), 401
        
        user_id = payload['user_id']
        user_sessions = []
        
        # Get sessions from memory
        for session_id, session_data in collaborative_sessions.items():
            if user_id in session_data['participants']:
                user_sessions.append(session_data)
        
        # Also check Redis for additional sessions
        if current_app.redis_client:
            try:
                # This is a simplified approach - in production, you'd maintain a user->sessions index
                session_keys = current_app.redis_client.keys("collab_session:*")
                for key in session_keys:
                    session_json = current_app.redis_client.get(key)
                    if session_json:
                        session_data = json.loads(session_json.decode('utf-8'))
                        if (user_id in session_data['participants'] and 
                            session_data['id'] not in [s['id'] for s in user_sessions]):
                            user_sessions.append(session_data)
            except Exception as e:
                print(f"Warning: Failed to get sessions from Redis: {e}")
        
        return jsonify({
            'success': True,
            'sessions': user_sessions
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to get sessions: {str(e)}'
        }), 500

# WebSocket events
@socketio.on('join_session')
def on_join_session(data):
    """Handle user joining a collaborative session via WebSocket."""
    session_id = data.get('session_id')
    if session_id:
        join_room(session_id)
        emit('user_joined', {
            'message': f'User joined session {session_id}'
        }, room=session_id)

@socketio.on('leave_session')
def on_leave_session(data):
    """Handle user leaving a collaborative session via WebSocket."""
    session_id = data.get('session_id')
    if session_id:
        leave_room(session_id)
        emit('user_left', {
            'message': f'User left session {session_id}'
        }, room=session_id)

@socketio.on('vote_track')
def on_vote_track(data):
    """Handle track voting in collaborative session."""
    session_id = data.get('session_id')
    track_index = data.get('track_index')
    user_id = data.get('user_id')
    
    if session_id and track_index is not None and user_id:
        session_data = collaborative_sessions.get(session_id)
        
        if (session_data and session_data['allow_voting'] and 
            0 <= track_index < len(session_data['playlist'])):
            
            track = session_data['playlist'][track_index]
            
            if user_id not in track['voted_by']:
                track['votes'] += 1
                track['voted_by'].append(user_id)
                
                # Update session
                collaborative_sessions[session_id] = session_data
                
                emit('track_voted', {
                    'session_id': session_id,
                    'track_index': track_index,
                    'votes': track['votes']
                }, room=session_id)

@socketio.on('emotion_update')
def on_emotion_update(data):
    """Handle real-time emotion updates in collaborative session."""
    session_id = data.get('session_id')
    emotion = data.get('emotion')
    user_id = data.get('user_id')
    
    if session_id and emotion and user_id:
        emit('emotion_detected', {
            'session_id': session_id,
            'user_id': user_id,
            'emotion': emotion,
            'timestamp': datetime.now().isoformat()
        }, room=session_id)