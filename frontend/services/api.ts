import axios, { AxiosResponse } from 'axios';
import Cookies from 'js-cookie';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include auth token
api.interceptors.request.use(
  (config) => {
    const token = Cookies.get('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      Cookies.remove('auth_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Types
interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

interface EmotionDetectionResponse {
  success: boolean;
  emotion: string;
  confidence: number;
  music_genres: string[];
  mood_description: string;
  energy_level: string;
  error?: string;
}

interface MusicRecommendationRequest {
  emotion: string;
  genres: string[];
  limit?: number;
}

interface Track {
  id: string;
  name: string;
  artist: string;
  album: string;
  image?: string;
  preview_url?: string;
  external_url: string;
  duration_ms: number;
  popularity: number;
}

interface MusicRecommendationResponse {
  success: boolean;
  tracks: Track[];
  emotion: string;
  genres_used: string[];
  audio_features: any;
  error?: string;
}

interface User {
  id: string;
  display_name: string;
  email?: string;
  country?: string;
  followers: number;
  images: any[];
}

interface AuthResponse {
  success: boolean;
  token?: string;
  user?: User;
  expires_in?: number;
  error?: string;
}

// Auth Service
export const authService = {
  // Get Spotify login URL
  getSpotifyAuthUrl: async (): Promise<{ success: boolean; auth_url?: string; error?: string }> => {
    try {
      const response = await api.get('/api/auth/spotify/login');
      return response.data;
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || 'Failed to get auth URL'
      };
    }
  },

  // Handle Spotify callback
  handleSpotifyCallback: async (code: string): Promise<AuthResponse> => {
    try {
      const response = await api.post('/api/auth/spotify/callback', { code });
      
      if (response.data.success && response.data.token) {
        // Store token in cookie
        Cookies.set('auth_token', response.data.token, { 
          expires: 1, // 1 day
          secure: process.env.NODE_ENV === 'production',
          sameSite: 'strict'
        });
      }
      
      return response.data;
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || 'Authentication failed'
      };
    }
  },

  // Verify token
  verifyToken: async (): Promise<{ success: boolean; user?: User; valid?: boolean; error?: string }> => {
    try {
      const response = await api.post('/api/auth/verify');
      return response.data;
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || 'Token verification failed'
      };
    }
  },

  // Get user profile
  getProfile: async (): Promise<{ success: boolean; user?: User; error?: string }> => {
    try {
      const response = await api.get('/api/auth/profile');
      return response.data;
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || 'Failed to get profile'
      };
    }
  },

  // Logout
  logout: async (): Promise<{ success: boolean; message?: string }> => {
    try {
      const response = await api.post('/api/auth/logout');
      Cookies.remove('auth_token');
      return response.data;
    } catch (error: any) {
      // Remove token even if API call fails
      Cookies.remove('auth_token');
      return {
        success: true,
        message: 'Logged out'
      };
    }
  },

  // Check if user is authenticated
  isAuthenticated: (): boolean => {
    return !!Cookies.get('auth_token');
  },
};

// Emotion Service
export const emotionService = {
  // Detect facial emotion from image
  detectFacialEmotion: async (imageData: string): Promise<EmotionDetectionResponse> => {
    try {
      const response = await api.post('/api/emotion/detect-facial', {
        image: imageData
      });
      return response.data;
    } catch (error: any) {
      return {
        success: false,
        emotion: 'neutral',
        confidence: 0,
        music_genres: [],
        mood_description: '',
        energy_level: 'medium',
        error: error.response?.data?.error || 'Failed to detect emotion'
      };
    }
  },

  // Analyze text sentiment
  analyzeTextSentiment: async (text: string): Promise<EmotionDetectionResponse> => {
    try {
      const response = await api.post('/api/emotion/analyze-text', {
        text
      });
      return response.data;
    } catch (error: any) {
      return {
        success: false,
        emotion: 'neutral',
        confidence: 0,
        music_genres: [],
        mood_description: '',
        energy_level: 'medium',
        error: error.response?.data?.error || 'Failed to analyze text'
      };
    }
  },

  // Get mood history
  getMoodHistory: async (): Promise<{ success: boolean; mood_history?: any; error?: string }> => {
    try {
      const response = await api.get('/api/emotion/mood-history');
      return response.data;
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || 'Failed to get mood history'
      };
    }
  },

  // Get mood recommendations
  getMoodRecommendations: async (emotion: string, confidence: number = 0.7): Promise<any> => {
    try {
      const response = await api.post('/api/emotion/mood-recommendations', {
        emotion,
        confidence
      });
      return response.data;
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || 'Failed to get recommendations'
      };
    }
  },
};

// Music Service
export const musicService = {
  // Get music recommendations
  getRecommendations: async (request: MusicRecommendationRequest): Promise<MusicRecommendationResponse> => {
    try {
      const response = await api.post('/api/music/recommendations', request);
      return response.data;
    } catch (error: any) {
      return {
        success: false,
        tracks: [],
        emotion: request.emotion,
        genres_used: [],
        audio_features: {},
        error: error.response?.data?.error || 'Failed to get recommendations'
      };
    }
  },

  // Search music
  searchMusic: async (query: string, limit: number = 20): Promise<{ success: boolean; tracks: Track[]; error?: string }> => {
    try {
      const response = await api.get('/api/music/search', {
        params: { q: query, limit }
      });
      return response.data;
    } catch (error: any) {
      return {
        success: false,
        tracks: [],
        error: error.response?.data?.error || 'Failed to search music'
      };
    }
  },

  // Generate AI melody
  generateMelody: async (emotion: string, options: any = {}): Promise<any> => {
    try {
      const response = await api.post('/api/music/generate/melody', {
        emotion,
        ...options
      });
      return response.data;
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || 'Failed to generate melody'
      };
    }
  },

  // Generate full AI track
  generateTrack: async (emotion: string, styleParams: any = {}): Promise<any> => {
    try {
      const response = await api.post('/api/music/generate/track', {
        emotion,
        style_params: styleParams
      });
      return response.data;
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || 'Failed to generate track'
      };
    }
  },

  // Create playlist
  createPlaylist: async (name: string, description: string, trackIds: string[]): Promise<any> => {
    try {
      const response = await api.post('/api/music/playlists/create', {
        name,
        description,
        track_ids: trackIds
      });
      return response.data;
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || 'Failed to create playlist'
      };
    }
  },

  // Create mood playlist
  createMoodPlaylist: async (request: { emotion: string; genres: string[]; track_count?: number }): Promise<any> => {
    try {
      const response = await api.post('/api/music/mood-playlist', request);
      return response.data;
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || 'Failed to create mood playlist'
      };
    }
  },

  // Get user playlists
  getUserPlaylists: async (): Promise<{ success: boolean; playlists: any[]; error?: string }> => {
    try {
      const response = await api.get('/api/music/playlists');
      return response.data;
    } catch (error: any) {
      return {
        success: false,
        playlists: [],
        error: error.response?.data?.error || 'Failed to get playlists'
      };
    }
  },

  // Get audio features for emotion
  getAudioFeatures: async (emotion: string): Promise<any> => {
    try {
      const response = await api.get('/api/music/audio-features', {
        params: { emotion }
      });
      return response.data;
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || 'Failed to get audio features'
      };
    }
  },
};

// Social Service
export const socialService = {
  // Create collaborative session
  createSession: async (sessionData: any): Promise<any> => {
    try {
      const response = await api.post('/api/social/sessions/create', sessionData);
      return response.data;
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || 'Failed to create session'
      };
    }
  },

  // Join collaborative session
  joinSession: async (sessionId: string): Promise<any> => {
    try {
      const response = await api.post(`/api/social/sessions/${sessionId}/join`);
      return response.data;
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || 'Failed to join session'
      };
    }
  },

  // Add track to session
  addTrackToSession: async (sessionId: string, track: Track): Promise<any> => {
    try {
      const response = await api.post(`/api/social/sessions/${sessionId}/add-track`, {
        track
      });
      return response.data;
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || 'Failed to add track'
      };
    }
  },

  // Get user sessions
  getUserSessions: async (): Promise<{ success: boolean; sessions: any[]; error?: string }> => {
    try {
      const response = await api.get('/api/social/sessions');
      return response.data;
    } catch (error: any) {
      return {
        success: false,
        sessions: [],
        error: error.response?.data?.error || 'Failed to get sessions'
      };
    }
  },
};

export { api };
export default api;