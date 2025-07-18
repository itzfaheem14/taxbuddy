import cv2
import numpy as np
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from PIL import Image
import base64
import io
from typing import Dict, List, Optional

class EmotionDetectionService:
    """Service for detecting emotions from facial expressions and text sentiment analysis."""
    
    def __init__(self):
        # Initialize face detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Initialize text sentiment analysis
        self.text_analyzer = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest",
            tokenizer="cardiffnlp/twitter-roberta-base-sentiment-latest"
        )
        
        # Emotion mapping for music recommendation
        self.emotion_to_music_mapping = {
            'happy': ['pop', 'dance', 'funk', 'disco'],
            'sad': ['blues', 'acoustic', 'indie', 'ambient'],
            'angry': ['rock', 'metal', 'punk', 'electronic'],
            'fear': ['ambient', 'classical', 'chill'],
            'surprise': ['experimental', 'jazz', 'world'],
            'disgust': ['grunge', 'alternative', 'industrial'],
            'neutral': ['pop', 'indie', 'alternative', 'folk']
        }
    
    def detect_facial_emotion(self, image_data: str) -> Dict:
        """
        Detect emotion from facial expression in base64 encoded image.
        
        Args:
            image_data: Base64 encoded image string
            
        Returns:
            Dictionary containing detected emotion and confidence scores
        """
        try:
            # Decode base64 image
            image_bytes = base64.b64decode(image_data.split(',')[1] if ',' in image_data else image_data)
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to OpenCV format
            opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            if len(faces) == 0:
                return {
                    'success': False,
                    'error': 'No face detected in the image',
                    'emotion': 'neutral',
                    'confidence': 0.0
                }
            
            # For now, we'll use a simplified emotion detection
            # In a real implementation, you'd use a trained emotion recognition model
            emotions = ['happy', 'sad', 'angry', 'surprise', 'fear', 'disgust', 'neutral']
            
            # Simulate emotion detection (replace with actual model inference)
            detected_emotion = self._analyze_facial_features(gray, faces[0])
            
            return {
                'success': True,
                'emotion': detected_emotion['emotion'],
                'confidence': detected_emotion['confidence'],
                'face_count': len(faces),
                'music_genres': self.emotion_to_music_mapping.get(detected_emotion['emotion'], ['pop'])
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error processing image: {str(e)}',
                'emotion': 'neutral',
                'confidence': 0.0
            }
    
    def analyze_text_sentiment(self, text: str) -> Dict:
        """
        Analyze sentiment from text input.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary containing sentiment analysis results
        """
        try:
            if not text or len(text.strip()) == 0:
                return {
                    'success': False,
                    'error': 'Empty text provided',
                    'sentiment': 'neutral',
                    'confidence': 0.0
                }
            
            # Analyze sentiment
            result = self.text_analyzer(text)[0]
            
            # Map sentiment labels to emotions
            sentiment_to_emotion = {
                'LABEL_0': 'sad',      # Negative
                'LABEL_1': 'neutral',  # Neutral
                'LABEL_2': 'happy',    # Positive
                'NEGATIVE': 'sad',
                'NEUTRAL': 'neutral',
                'POSITIVE': 'happy'
            }
            
            emotion = sentiment_to_emotion.get(result['label'], 'neutral')
            
            return {
                'success': True,
                'sentiment': result['label'],
                'emotion': emotion,
                'confidence': result['score'],
                'text': text,
                'music_genres': self.emotion_to_music_mapping.get(emotion, ['pop'])
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error analyzing text: {str(e)}',
                'sentiment': 'neutral',
                'confidence': 0.0
            }
    
    def _analyze_facial_features(self, gray_image: np.ndarray, face_coords: tuple) -> Dict:
        """
        Simplified facial feature analysis for emotion detection.
        In a real implementation, this would use a trained emotion recognition model.
        """
        x, y, w, h = face_coords
        face_roi = gray_image[y:y+h, x:x+w]
        
        # Simple heuristic-based emotion detection (placeholder)
        # Calculate basic features
        mean_intensity = np.mean(face_roi)
        std_intensity = np.std(face_roi)
        
        # Simple emotion classification based on image statistics
        if mean_intensity > 120 and std_intensity > 30:
            emotion = 'happy'
            confidence = 0.75
        elif mean_intensity < 80:
            emotion = 'sad'
            confidence = 0.70
        elif std_intensity > 50:
            emotion = 'surprise'
            confidence = 0.65
        else:
            emotion = 'neutral'
            confidence = 0.60
        
        return {
            'emotion': emotion,
            'confidence': confidence
        }
    
    def get_mood_recommendations(self, emotion: str, confidence: float) -> Dict:
        """
        Get music recommendations based on detected emotion.
        
        Args:
            emotion: Detected emotion
            confidence: Confidence score
            
        Returns:
            Dictionary containing music recommendations
        """
        genres = self.emotion_to_music_mapping.get(emotion, ['pop'])
        
        # Adjust recommendations based on confidence
        if confidence < 0.5:
            # Low confidence, add more diverse genres
            genres.extend(['indie', 'alternative'])
        
        return {
            'primary_emotion': emotion,
            'confidence': confidence,
            'recommended_genres': list(set(genres)),
            'mood_description': self._get_mood_description(emotion),
            'energy_level': self._get_energy_level(emotion)
        }
    
    def _get_mood_description(self, emotion: str) -> str:
        """Get human-readable mood description."""
        descriptions = {
            'happy': 'Upbeat and energetic',
            'sad': 'Melancholic and contemplative',
            'angry': 'Intense and powerful',
            'fear': 'Calm and soothing',
            'surprise': 'Unexpected and diverse',
            'disgust': 'Alternative and edgy',
            'neutral': 'Balanced and versatile'
        }
        return descriptions.get(emotion, 'Unknown mood')
    
    def _get_energy_level(self, emotion: str) -> str:
        """Get energy level for the emotion."""
        energy_levels = {
            'happy': 'high',
            'sad': 'low',
            'angry': 'high',
            'fear': 'low',
            'surprise': 'medium',
            'disgust': 'medium',
            'neutral': 'medium'
        }
        return energy_levels.get(emotion, 'medium')