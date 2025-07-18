import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import os
from typing import Dict, List, Optional
import random

class SpotifyService:
    """Service for Spotify API integration including authentication and music recommendations."""
    
    def __init__(self):
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')
        
        # Initialize client credentials flow for app-only requests
        self.client_credentials_manager = SpotifyClientCredentials(
            client_id=self.client_id,
            client_secret=self.client_secret
        )
        self.sp_client = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)
        
    def get_auth_url(self) -> str:
        """Get Spotify authorization URL for user login."""
        scope = "user-read-private user-read-email playlist-read-private playlist-modify-public playlist-modify-private user-read-playback-state user-modify-playback-state user-read-currently-playing"
        
        sp_oauth = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=scope
        )
        
        return sp_oauth.get_authorize_url()
    
    def get_access_token(self, authorization_code: str) -> Dict:
        """Exchange authorization code for access token."""
        try:
            sp_oauth = SpotifyOAuth(
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri=self.redirect_uri
            )
            
            token_info = sp_oauth.get_access_token(authorization_code)
            
            if token_info:
                return {
                    'success': True,
                    'access_token': token_info['access_token'],
                    'refresh_token': token_info['refresh_token'],
                    'expires_in': token_info['expires_in']
                }
            else:
                return {'success': False, 'error': 'Failed to get access token'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_user_profile(self, access_token: str) -> Dict:
        """Get user profile information."""
        try:
            sp = spotipy.Spotify(auth=access_token)
            user_info = sp.current_user()
            
            return {
                'success': True,
                'user': {
                    'id': user_info['id'],
                    'display_name': user_info.get('display_name', ''),
                    'email': user_info.get('email', ''),
                    'country': user_info.get('country', ''),
                    'followers': user_info['followers']['total'],
                    'images': user_info.get('images', [])
                }
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_recommendations_by_emotion(self, emotion: str, genres: List[str], limit: int = 20) -> Dict:
        """Get music recommendations based on emotion and genres."""
        try:
            # Emotion-based audio features
            emotion_features = self._get_emotion_audio_features(emotion)
            
            # Get available genres from Spotify
            available_genres = self.sp_client.recommendation_genre_seeds()['genres']
            valid_genres = [genre for genre in genres if genre in available_genres]
            
            if not valid_genres:
                valid_genres = ['pop']  # Fallback to pop
            
            # Limit to 5 genres (Spotify API limit)
            seed_genres = valid_genres[:5]
            
            recommendations = self.sp_client.recommendations(
                seed_genres=seed_genres,
                limit=limit,
                **emotion_features
            )
            
            tracks = []
            for track in recommendations['tracks']:
                tracks.append({
                    'id': track['id'],
                    'name': track['name'],
                    'artist': ', '.join([artist['name'] for artist in track['artists']]),
                    'album': track['album']['name'],
                    'preview_url': track['preview_url'],
                    'external_url': track['external_urls']['spotify'],
                    'image': track['album']['images'][0]['url'] if track['album']['images'] else None,
                    'duration_ms': track['duration_ms'],
                    'popularity': track['popularity']
                })
            
            return {
                'success': True,
                'tracks': tracks,
                'emotion': emotion,
                'genres_used': seed_genres,
                'audio_features': emotion_features
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def search_tracks(self, query: str, limit: int = 20) -> Dict:
        """Search for tracks on Spotify."""
        try:
            results = self.sp_client.search(q=query, type='track', limit=limit)
            
            tracks = []
            for track in results['tracks']['items']:
                tracks.append({
                    'id': track['id'],
                    'name': track['name'],
                    'artist': ', '.join([artist['name'] for artist in track['artists']]),
                    'album': track['album']['name'],
                    'preview_url': track['preview_url'],
                    'external_url': track['external_urls']['spotify'],
                    'image': track['album']['images'][0]['url'] if track['album']['images'] else None,
                    'duration_ms': track['duration_ms'],
                    'popularity': track['popularity']
                })
            
            return {'success': True, 'tracks': tracks}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def create_playlist(self, access_token: str, name: str, description: str, track_ids: List[str]) -> Dict:
        """Create a new playlist for the user."""
        try:
            sp = spotipy.Spotify(auth=access_token)
            user = sp.current_user()
            
            # Create playlist
            playlist = sp.user_playlist_create(
                user=user['id'],
                name=name,
                description=description,
                public=False
            )
            
            # Add tracks to playlist
            if track_ids:
                track_uris = [f"spotify:track:{track_id}" for track_id in track_ids]
                sp.playlist_add_items(playlist['id'], track_uris)
            
            return {
                'success': True,
                'playlist': {
                    'id': playlist['id'],
                    'name': playlist['name'],
                    'description': playlist['description'],
                    'external_url': playlist['external_urls']['spotify'],
                    'track_count': len(track_ids)
                }
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_user_playlists(self, access_token: str) -> Dict:
        """Get user's playlists."""
        try:
            sp = spotipy.Spotify(auth=access_token)
            playlists = sp.current_user_playlists()
            
            user_playlists = []
            for playlist in playlists['items']:
                user_playlists.append({
                    'id': playlist['id'],
                    'name': playlist['name'],
                    'description': playlist['description'],
                    'track_count': playlist['tracks']['total'],
                    'public': playlist['public'],
                    'external_url': playlist['external_urls']['spotify'],
                    'image': playlist['images'][0]['url'] if playlist['images'] else None
                })
            
            return {'success': True, 'playlists': user_playlists}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _get_emotion_audio_features(self, emotion: str) -> Dict:
        """Get audio features based on emotion for Spotify recommendations."""
        emotion_features = {
            'happy': {
                'target_valence': 0.8,
                'target_energy': 0.7,
                'target_danceability': 0.7,
                'min_tempo': 120,
                'max_tempo': 140
            },
            'sad': {
                'target_valence': 0.2,
                'target_energy': 0.3,
                'target_danceability': 0.3,
                'min_tempo': 60,
                'max_tempo': 90
            },
            'angry': {
                'target_valence': 0.3,
                'target_energy': 0.9,
                'target_danceability': 0.6,
                'min_tempo': 140,
                'max_tempo': 180
            },
            'fear': {
                'target_valence': 0.4,
                'target_energy': 0.2,
                'target_danceability': 0.2,
                'min_tempo': 70,
                'max_tempo': 100
            },
            'surprise': {
                'target_valence': 0.6,
                'target_energy': 0.6,
                'target_danceability': 0.5,
                'min_tempo': 100,
                'max_tempo': 130
            },
            'disgust': {
                'target_valence': 0.3,
                'target_energy': 0.7,
                'target_danceability': 0.4,
                'min_tempo': 110,
                'max_tempo': 150
            },
            'neutral': {
                'target_valence': 0.5,
                'target_energy': 0.5,
                'target_danceability': 0.5,
                'min_tempo': 90,
                'max_tempo': 120
            }
        }
        
        return emotion_features.get(emotion, emotion_features['neutral'])