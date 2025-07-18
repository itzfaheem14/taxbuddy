from flask import Blueprint, request, jsonify, current_app, send_file
from app.services.spotify_service import SpotifyService
from app.services.music_generation import MusicGenerationService
import tempfile
import base64
import io

music_bp = Blueprint('music', __name__)
spotify_service = SpotifyService()
music_gen_service = MusicGenerationService()

@music_bp.route('/recommendations', methods=['POST'])
def get_recommendations():
    """Get music recommendations based on emotion and preferences."""
    try:
        data = request.get_json()
        
        if not data or 'emotion' not in data:
            return jsonify({
                'success': False,
                'error': 'Emotion is required'
            }), 400
        
        emotion = data['emotion']
        genres = data.get('genres', [])
        limit = data.get('limit', 20)
        
        # Get recommendations from Spotify
        result = spotify_service.get_recommendations_by_emotion(emotion, genres, limit)
        
        return jsonify(result), 200 if result['success'] else 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500

@music_bp.route('/search', methods=['GET'])
def search_music():
    """Search for music tracks."""
    try:
        query = request.args.get('q')
        limit = request.args.get('limit', 20, type=int)
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Search query is required'
            }), 400
        
        result = spotify_service.search_tracks(query, limit)
        
        return jsonify(result), 200 if result['success'] else 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500

@music_bp.route('/generate/melody', methods=['POST'])
def generate_melody():
    """Generate AI melody based on emotion."""
    try:
        data = request.get_json()
        
        if not data or 'emotion' not in data:
            return jsonify({
                'success': False,
                'error': 'Emotion is required'
            }), 400
        
        emotion = data['emotion']
        num_steps = data.get('num_steps', 128)
        temperature = data.get('temperature', 1.0)
        
        # Generate melody
        result = music_gen_service.generate_melody_by_emotion(emotion, num_steps, temperature)
        
        if result['success']:
            # Convert audio data to base64 for JSON response
            audio_data = result['audio_data']
            audio_bytes = io.BytesIO()
            
            # Convert numpy array to bytes
            audio_data_int16 = (audio_data * 32767).astype('int16')
            audio_bytes.write(audio_data_int16.tobytes())
            audio_bytes.seek(0)
            
            # Encode as base64
            audio_b64 = base64.b64encode(audio_bytes.read()).decode('utf-8')
            
            result['audio_data_b64'] = audio_b64
            # Remove numpy array from response
            del result['audio_data']
            del result['sequence']  # Remove complex objects
        
        return jsonify(result), 200 if result['success'] else 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500

@music_bp.route('/generate/track', methods=['POST'])
def generate_full_track():
    """Generate a full AI track with melody and drums."""
    try:
        data = request.get_json()
        
        if not data or 'emotion' not in data:
            return jsonify({
                'success': False,
                'error': 'Emotion is required'
            }), 400
        
        emotion = data['emotion']
        style_params = data.get('style_params', {})
        
        # Generate full track
        result = music_gen_service.create_full_track(emotion, style_params)
        
        if result['success']:
            # Save audio to temporary file
            audio_data = result['audio_data']
            temp_file = music_gen_service.save_audio(audio_data, f'generated_track_{emotion}.wav')
            
            # Convert audio to base64 for JSON response
            audio_bytes = io.BytesIO()
            audio_data_int16 = (audio_data * 32767).astype('int16')
            audio_bytes.write(audio_data_int16.tobytes())
            audio_bytes.seek(0)
            
            audio_b64 = base64.b64encode(audio_bytes.read()).decode('utf-8')
            
            result['audio_data_b64'] = audio_b64
            result['temp_file_path'] = temp_file
            
            # Remove complex objects from response
            del result['audio_data']
            del result['sequence']
        
        return jsonify(result), 200 if result['success'] else 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500

@music_bp.route('/playlists/create', methods=['POST'])
def create_playlist():
    """Create a new Spotify playlist."""
    try:
        data = request.get_json()
        access_token = request.headers.get('Authorization')
        
        if not access_token:
            return jsonify({
                'success': False,
                'error': 'Access token required'
            }), 401
        
        # Remove 'Bearer ' prefix if present
        if access_token.startswith('Bearer '):
            access_token = access_token[7:]
        
        if not data or 'name' not in data:
            return jsonify({
                'success': False,
                'error': 'Playlist name is required'
            }), 400
        
        name = data['name']
        description = data.get('description', 'Created by MuseAIka')
        track_ids = data.get('track_ids', [])
        
        result = spotify_service.create_playlist(access_token, name, description, track_ids)
        
        return jsonify(result), 200 if result['success'] else 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500

@music_bp.route('/playlists', methods=['GET'])
def get_user_playlists():
    """Get user's Spotify playlists."""
    try:
        access_token = request.headers.get('Authorization')
        
        if not access_token:
            return jsonify({
                'success': False,
                'error': 'Access token required'
            }), 401
        
        # Remove 'Bearer ' prefix if present
        if access_token.startswith('Bearer '):
            access_token = access_token[7:]
        
        result = spotify_service.get_user_playlists(access_token)
        
        return jsonify(result), 200 if result['success'] else 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500

@music_bp.route('/mood-playlist', methods=['POST'])
def create_mood_playlist():
    """Create a playlist based on detected mood."""
    try:
        data = request.get_json()
        access_token = request.headers.get('Authorization')
        
        if not access_token:
            return jsonify({
                'success': False,
                'error': 'Access token required'
            }), 401
        
        if access_token.startswith('Bearer '):
            access_token = access_token[7:]
        
        if not data or 'emotion' not in data:
            return jsonify({
                'success': False,
                'error': 'Emotion is required'
            }), 400
        
        emotion = data['emotion']
        genres = data.get('genres', [])
        track_count = data.get('track_count', 20)
        
        # Get recommendations
        recommendations = spotify_service.get_recommendations_by_emotion(emotion, genres, track_count)
        
        if not recommendations['success']:
            return jsonify(recommendations), 400
        
        # Extract track IDs
        track_ids = [track['id'] for track in recommendations['tracks']]
        
        # Create playlist
        playlist_name = f"My {emotion.title()} Mood - {genres[0] if genres else 'Mixed'}"
        playlist_description = f"AI-generated playlist based on {emotion} emotion. Created by MuseAIka."
        
        playlist_result = spotify_service.create_playlist(
            access_token, 
            playlist_name, 
            playlist_description, 
            track_ids
        )
        
        if playlist_result['success']:
            return jsonify({
                'success': True,
                'playlist': playlist_result['playlist'],
                'tracks': recommendations['tracks'],
                'emotion': emotion,
                'genres_used': recommendations['genres_used']
            }), 200
        else:
            return jsonify(playlist_result), 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500

@music_bp.route('/audio-features', methods=['GET'])
def get_audio_features():
    """Get audio features for emotion mapping (for debugging/info)."""
    try:
        emotion = request.args.get('emotion', 'neutral')
        
        # Get emotion-based audio features
        features = spotify_service._get_emotion_audio_features(emotion)
        
        return jsonify({
            'success': True,
            'emotion': emotion,
            'audio_features': features
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500