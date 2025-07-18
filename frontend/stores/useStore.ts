import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { authService } from '../services/api';

interface User {
  id: string;
  display_name: string;
  email?: string;
  country?: string;
  followers: number;
  images: any[];
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

interface EmotionState {
  emotion: string;
  confidence: number;
  music_genres: string[];
  mood_description: string;
  energy_level: string;
}

interface AppState {
  // Auth state
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  
  // Music state
  currentTrack: Track | null;
  isPlaying: boolean;
  recommendations: Track[];
  playlists: any[];
  
  // Emotion state
  currentEmotion: EmotionState | null;
  moodHistory: any[];
  
  // Social state
  collaborativeSessions: any[];
  currentSession: any | null;
  
  // UI state
  theme: 'dark' | 'light';
  sidebarOpen: boolean;
  
  // Actions
  setUser: (user: User | null) => void;
  setAuthenticated: (authenticated: boolean) => void;
  setLoading: (loading: boolean) => void;
  
  setCurrentTrack: (track: Track | null) => void;
  setIsPlaying: (playing: boolean) => void;
  setRecommendations: (tracks: Track[]) => void;
  setPlaylists: (playlists: any[]) => void;
  
  setCurrentEmotion: (emotion: EmotionState | null) => void;
  setMoodHistory: (history: any[]) => void;
  addMoodEntry: (entry: any) => void;
  
  setCollaborativeSessions: (sessions: any[]) => void;
  setCurrentSession: (session: any | null) => void;
  
  setTheme: (theme: 'dark' | 'light') => void;
  setSidebarOpen: (open: boolean) => void;
  
  // Auth actions
  login: (user: User) => void;
  logout: () => Promise<void>;
  checkAuth: () => Promise<boolean>;
  
  // Reset actions
  reset: () => void;
}

export const useStore = create<AppState>()(
  persist(
    (set, get) => ({
      // Initial state
      user: null,
      isAuthenticated: false,
      isLoading: false,
      
      currentTrack: null,
      isPlaying: false,
      recommendations: [],
      playlists: [],
      
      currentEmotion: null,
      moodHistory: [],
      
      collaborativeSessions: [],
      currentSession: null,
      
      theme: 'dark',
      sidebarOpen: false,
      
      // Basic setters
      setUser: (user) => set({ user }),
      setAuthenticated: (authenticated) => set({ isAuthenticated: authenticated }),
      setLoading: (loading) => set({ isLoading: loading }),
      
      setCurrentTrack: (track) => set({ currentTrack: track }),
      setIsPlaying: (playing) => set({ isPlaying: playing }),
      setRecommendations: (tracks) => set({ recommendations: tracks }),
      setPlaylists: (playlists) => set({ playlists }),
      
      setCurrentEmotion: (emotion) => set({ currentEmotion: emotion }),
      setMoodHistory: (history) => set({ moodHistory: history }),
      addMoodEntry: (entry) => {
        const { moodHistory } = get();
        const newHistory = [entry, ...moodHistory].slice(0, 100); // Keep last 100 entries
        set({ moodHistory: newHistory });
      },
      
      setCollaborativeSessions: (sessions) => set({ collaborativeSessions: sessions }),
      setCurrentSession: (session) => set({ currentSession: session }),
      
      setTheme: (theme) => set({ theme }),
      setSidebarOpen: (open) => set({ sidebarOpen: open }),
      
      // Auth actions
      login: (user) => {
        set({
          user,
          isAuthenticated: true,
          isLoading: false,
        });
      },
      
      logout: async () => {
        set({ isLoading: true });
        
        try {
          await authService.logout();
        } catch (error) {
          console.error('Logout error:', error);
        } finally {
          set({
            user: null,
            isAuthenticated: false,
            isLoading: false,
            currentTrack: null,
            isPlaying: false,
            recommendations: [],
            playlists: [],
            currentEmotion: null,
            collaborativeSessions: [],
            currentSession: null,
          });
        }
      },
      
      checkAuth: async () => {
        if (!authService.isAuthenticated()) {
          set({ isAuthenticated: false, user: null });
          return false;
        }
        
        set({ isLoading: true });
        
        try {
          const response = await authService.verifyToken();
          
          if (response.success && response.user) {
            set({
              user: response.user,
              isAuthenticated: true,
              isLoading: false,
            });
            return true;
          } else {
            set({
              user: null,
              isAuthenticated: false,
              isLoading: false,
            });
            return false;
          }
        } catch (error) {
          console.error('Auth check error:', error);
          set({
            user: null,
            isAuthenticated: false,
            isLoading: false,
          });
          return false;
        }
      },
      
      // Reset all state
      reset: () => {
        set({
          user: null,
          isAuthenticated: false,
          isLoading: false,
          currentTrack: null,
          isPlaying: false,
          recommendations: [],
          playlists: [],
          currentEmotion: null,
          moodHistory: [],
          collaborativeSessions: [],
          currentSession: null,
          sidebarOpen: false,
        });
      },
    }),
    {
      name: 'museaika-store',
      partialize: (state) => ({
        // Only persist certain parts of the state
        theme: state.theme,
        moodHistory: state.moodHistory,
        // Don't persist sensitive data like user info or auth state
      }),
    }
  )
);

// Selectors for common state combinations
export const useAuth = () => {
  const { user, isAuthenticated, isLoading, login, logout, checkAuth } = useStore();
  return { user, isAuthenticated, isLoading, login, logout, checkAuth };
};

export const useMusic = () => {
  const {
    currentTrack,
    isPlaying,
    recommendations,
    playlists,
    setCurrentTrack,
    setIsPlaying,
    setRecommendations,
    setPlaylists,
  } = useStore();
  
  return {
    currentTrack,
    isPlaying,
    recommendations,
    playlists,
    setCurrentTrack,
    setIsPlaying,
    setRecommendations,
    setPlaylists,
  };
};

export const useEmotion = () => {
  const {
    currentEmotion,
    moodHistory,
    setCurrentEmotion,
    setMoodHistory,
    addMoodEntry,
  } = useStore();
  
  return {
    currentEmotion,
    moodHistory,
    setCurrentEmotion,
    setMoodHistory,
    addMoodEntry,
  };
};

export const useSocial = () => {
  const {
    collaborativeSessions,
    currentSession,
    setCollaborativeSessions,
    setCurrentSession,
  } = useStore();
  
  return {
    collaborativeSessions,
    currentSession,
    setCollaborativeSessions,
    setCurrentSession,
  };
};

export const useUI = () => {
  const {
    theme,
    sidebarOpen,
    setTheme,
    setSidebarOpen,
  } = useStore();
  
  return {
    theme,
    sidebarOpen,
    setTheme,
    setSidebarOpen,
  };
};