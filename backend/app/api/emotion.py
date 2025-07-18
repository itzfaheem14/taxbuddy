from flask import Blueprint, request, jsonify, current_app
from app.services.emotion_detection import EmotionDetectionService
import logging

emotion_bp = Blueprint('emotion', __name__)
emotion_service = EmotionDetectionService()

@emotion_bp.route('/detect-facial', methods=['POST'])
def detect_facial_emotion():
    """Detect emotion from uploaded facial image."""
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({
                'success': False,
                'error': 'No image data provided'
            }), 400
        
        image_data = data['image']
        
        # Detect emotion
        result = emotion_service.detect_facial_emotion(image_data)
        
        if result['success']:
            # Get mood recommendations
            mood_rec = emotion_service.get_mood_recommendations(
                result['emotion'], 
                result['confidence']
            )
            result.update(mood_rec)
            
            # Store mood data in session or database if needed
            if current_app.redis_client:
                try:
                    # Store recent emotion detection
                    user_id = request.headers.get('User-ID', 'anonymous')
                    current_app.redis_client.lpush(
                        f"emotions:{user_id}", 
                        f"{result['emotion']}:{result['confidence']}"
                    )
                    current_app.redis_client.ltrim(f"emotions:{user_id}", 0, 99)  # Keep last 100
                except Exception as e:
                    logging.warning(f"Failed to store emotion data: {e}")
        
        return jsonify(result), 200 if result['success'] else 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500

@emotion_bp.route('/analyze-text', methods=['POST'])
def analyze_text_sentiment():
    """Analyze sentiment from text input."""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'success': False,
                'error': 'No text provided'
            }), 400
        
        text = data['text']
        
        # Analyze sentiment
        result = emotion_service.analyze_text_sentiment(text)
        
        if result['success']:
            # Get mood recommendations
            mood_rec = emotion_service.get_mood_recommendations(
                result['emotion'], 
                result['confidence']
            )
            result.update(mood_rec)
            
            # Store mood data
            if current_app.redis_client:
                try:
                    user_id = request.headers.get('User-ID', 'anonymous')
                    current_app.redis_client.lpush(
                        f"text_emotions:{user_id}", 
                        f"{result['emotion']}:{result['confidence']}"
                    )
                    current_app.redis_client.ltrim(f"text_emotions:{user_id}", 0, 99)
                except Exception as e:
                    logging.warning(f"Failed to store text emotion data: {e}")
        
        return jsonify(result), 200 if result['success'] else 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500

@emotion_bp.route('/mood-history', methods=['GET'])
def get_mood_history():
    """Get user's mood history."""
    try:
        user_id = request.headers.get('User-ID', 'anonymous')
        
        if not current_app.redis_client:
            return jsonify({
                'success': False,
                'error': 'Mood tracking not available'
            }), 503
        
        # Get recent emotions
        facial_emotions = current_app.redis_client.lrange(f"emotions:{user_id}", 0, 49)
        text_emotions = current_app.redis_client.lrange(f"text_emotions:{user_id}", 0, 49)
        
        # Parse emotions
        facial_data = []
        for emotion_data in facial_emotions:
            emotion_str = emotion_data.decode('utf-8')
            emotion, confidence = emotion_str.split(':')
            facial_data.append({
                'emotion': emotion,
                'confidence': float(confidence),
                'type': 'facial'
            })
        
        text_data = []
        for emotion_data in text_emotions:
            emotion_str = emotion_data.decode('utf-8')
            emotion, confidence = emotion_str.split(':')
            text_data.append({
                'emotion': emotion,
                'confidence': float(confidence),
                'type': 'text'
            })
        
        # Combine and analyze trends
        all_emotions = facial_data + text_data
        
        # Calculate emotion distribution
        emotion_counts = {}
        for item in all_emotions:
            emotion = item['emotion']
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        # Get dominant emotion
        dominant_emotion = max(emotion_counts.items(), key=lambda x: x[1])[0] if emotion_counts else 'neutral'
        
        return jsonify({
            'success': True,
            'mood_history': {
                'facial_emotions': facial_data,
                'text_emotions': text_data,
                'emotion_distribution': emotion_counts,
                'dominant_emotion': dominant_emotion,
                'total_detections': len(all_emotions)
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500

@emotion_bp.route('/mood-recommendations', methods=['POST'])
def get_mood_recommendations():
    """Get music recommendations based on current mood."""
    try:
        data = request.get_json()
        
        if not data or 'emotion' not in data:
            return jsonify({
                'success': False,
                'error': 'No emotion provided'
            }), 400
        
        emotion = data['emotion']
        confidence = data.get('confidence', 0.7)
        
        # Get recommendations
        recommendations = emotion_service.get_mood_recommendations(emotion, confidence)
        
        return jsonify({
            'success': True,
            'recommendations': recommendations
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500