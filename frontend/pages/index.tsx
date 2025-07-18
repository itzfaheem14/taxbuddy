import { useState, useEffect, useRef } from 'react';
import {
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Box,
  Avatar,
  Chip,
  IconButton,
  Fab,
  Dialog,
  DialogTitle,
  DialogContent,
  TextField,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Divider,
  LinearProgress,
} from '@mui/material';
import {
  CameraAlt,
  TextFields,
  PlayArrow,
  Pause,
  SkipNext,
  SkipPrevious,
  Favorite,
  Share,
  QueueMusic,
  TrendingUp,
  Face,
  Psychology,
  MusicNote,
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';
import Webcam from 'react-webcam';
import confetti from 'canvas-confetti';
import toast from 'react-hot-toast';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import { Bar } from 'react-chartjs-2';

// Services
import { emotionService, musicService, authService } from '../services/api';
import { useStore } from '../stores/useStore';

// Register Chart.js components
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

interface Track {
  id: string;
  name: string;
  artist: string;
  album: string;
  image?: string;
  preview_url?: string;
  external_url: string;
  duration_ms: number;
}

interface EmotionResult {
  emotion: string;
  confidence: number;
  music_genres: string[];
  mood_description: string;
  energy_level: string;
}

const emotionColors = {
  happy: '#FFD700',
  sad: '#4169E1',
  angry: '#DC143C',
  fear: '#9370DB',
  surprise: '#FF6347',
  disgust: '#32CD32',
  neutral: '#778899',
};

const emotionEmojis = {
  happy: '😊',
  sad: '😢',
  angry: '😡',
  fear: '😨',
  surprise: '😲',
  disgust: '🤢',
  neutral: '😐',
};

export default function HomePage() {
  const [currentEmotion, setCurrentEmotion] = useState<EmotionResult | null>(null);
  const [recommendations, setRecommendations] = useState<Track[]>([]);
  const [loading, setLoading] = useState(false);
  const [cameraOpen, setCameraOpen] = useState(false);
  const [textAnalysisOpen, setTextAnalysisOpen] = useState(false);
  const [userText, setUserText] = useState('');
  const [currentTrack, setCurrentTrack] = useState<Track | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [moodHistory, setMoodHistory] = useState<any[]>([]);
  
  const webcamRef = useRef<Webcam>(null);
  const audioRef = useRef<HTMLAudioElement>(null);
  
  const { user, isAuthenticated } = useStore();

  useEffect(() => {
    loadMoodHistory();
  }, []);

  const loadMoodHistory = async () => {
    try {
      const response = await emotionService.getMoodHistory();
      if (response.success) {
        setMoodHistory(response.mood_history?.facial_emotions || []);
      }
    } catch (error) {
      console.error('Failed to load mood history:', error);
    }
  };

  const capturePhoto = async () => {
    if (!webcamRef.current) return;
    
    const imageSrc = webcamRef.current.getScreenshot();
    if (!imageSrc) return;

    setLoading(true);
    try {
      const response = await emotionService.detectFacialEmotion(imageSrc);
      
      if (response.success) {
        setCurrentEmotion(response);
        setCameraOpen(false);
        
        // Trigger confetti for successful detection
        confetti({
          particleCount: 100,
          spread: 70,
          origin: { y: 0.6 }
        });
        
        // Get music recommendations
        await getMusicRecommendations(response.emotion, response.music_genres);
        
        toast.success(`Detected ${response.emotion} emotion!`);
      } else {
        toast.error(response.error || 'Failed to detect emotion');
      }
    } catch (error) {
      toast.error('Failed to analyze image');
    } finally {
      setLoading(false);
    }
  };

  const analyzeText = async () => {
    if (!userText.trim()) return;

    setLoading(true);
    try {
      const response = await emotionService.analyzeTextSentiment(userText);
      
      if (response.success) {
        setCurrentEmotion(response);
        setTextAnalysisOpen(false);
        setUserText('');
        
        // Get music recommendations
        await getMusicRecommendations(response.emotion, response.music_genres);
        
        toast.success(`Detected ${response.emotion} sentiment!`);
      } else {
        toast.error(response.error || 'Failed to analyze text');
      }
    } catch (error) {
      toast.error('Failed to analyze text');
    } finally {
      setLoading(false);
    }
  };

  const getMusicRecommendations = async (emotion: string, genres: string[]) => {
    try {
      const response = await musicService.getRecommendations({
        emotion,
        genres,
        limit: 20
      });
      
      if (response.success) {
        setRecommendations(response.tracks);
      }
    } catch (error) {
      console.error('Failed to get recommendations:', error);
    }
  };

  const playTrack = (track: Track) => {
    if (!track.preview_url) {
      toast.error('Preview not available for this track');
      return;
    }

    if (currentTrack?.id === track.id && isPlaying) {
      // Pause current track
      audioRef.current?.pause();
      setIsPlaying(false);
    } else {
      // Play new track
      if (audioRef.current) {
        audioRef.current.src = track.preview_url;
        audioRef.current.play();
        setCurrentTrack(track);
        setIsPlaying(true);
      }
    }
  };

  const createMoodPlaylist = async () => {
    if (!isAuthenticated || !currentEmotion) {
      toast.error('Please login and detect your mood first');
      return;
    }

    try {
      const trackIds = recommendations.slice(0, 15).map(track => track.id);
      const response = await musicService.createMoodPlaylist({
        emotion: currentEmotion.emotion,
        genres: currentEmotion.music_genres,
        track_count: 15
      });

      if (response.success) {
        toast.success('Mood playlist created successfully!');
      }
    } catch (error) {
      toast.error('Failed to create playlist');
    }
  };

  // Chart data for mood history
  const chartData = {
    labels: moodHistory.slice(0, 10).map((_, index) => `${index + 1}`),
    datasets: [
      {
        label: 'Emotion Confidence',
        data: moodHistory.slice(0, 10).map(item => item.confidence * 100),
        backgroundColor: moodHistory.slice(0, 10).map(item => 
          emotionColors[item.emotion as keyof typeof emotionColors] || '#778899'
        ),
        borderColor: '#9c27b0',
        borderWidth: 2,
        borderRadius: 8,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: true,
        text: 'Recent Mood History',
        color: '#fff',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        ticks: {
          color: '#b0b0b0',
        },
        grid: {
          color: 'rgba(156, 39, 176, 0.1)',
        },
      },
      x: {
        ticks: {
          color: '#b0b0b0',
        },
        grid: {
          color: 'rgba(156, 39, 176, 0.1)',
        },
      },
    },
  };

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      {/* Header */}
      <Box textAlign="center" mb={6}>
        <motion.div
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <Typography variant="h1" component="h1" gutterBottom className="glow">
            <MusicNote sx={{ fontSize: '3rem', mr: 2, color: 'primary.main' }} />
            MuseAIka
          </Typography>
          <Typography variant="h6" color="text.secondary" mb={4}>
            AI-Powered Music Emotion Engine
          </Typography>
          
          {/* Music visualization bars */}
          <Box display="flex" justifyContent="center" gap={1} mb={4}>
            {[1, 2, 3, 4, 5].map((bar) => (
              <Box
                key={bar}
                className="music-bar"
                sx={{
                  width: 4,
                  backgroundColor: 'primary.main',
                  borderRadius: 2,
                }}
              />
            ))}
          </Box>
        </motion.div>
      </Box>

      <Grid container spacing={4}>
        {/* Left Column - Emotion Detection */}
        <Grid item xs={12} md={6}>
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            <Card className="glass glow">
              <CardContent>
                <Typography variant="h5" gutterBottom>
                  <Face sx={{ mr: 2, color: 'primary.main' }} />
                  Emotion Detection
                </Typography>
                
                {currentEmotion && (
                  <Box mb={3}>
                    <Card sx={{ p: 2, textAlign: 'center', background: 'rgba(156, 39, 176, 0.1)' }}>
                      <Typography variant="h3" component="div" mb={1}>
                        {emotionEmojis[currentEmotion.emotion as keyof typeof emotionEmojis]}
                      </Typography>
                      <Typography variant="h6" gutterBottom>
                        {currentEmotion.emotion.toUpperCase()}
                      </Typography>
                      <LinearProgress 
                        variant="determinate" 
                        value={currentEmotion.confidence * 100}
                        sx={{ 
                          height: 8, 
                          borderRadius: 4,
                          backgroundColor: 'rgba(255,255,255,0.1)',
                          '& .MuiLinearProgress-bar': {
                            backgroundColor: emotionColors[currentEmotion.emotion as keyof typeof emotionColors]
                          }
                        }}
                      />
                      <Typography variant="body2" color="text.secondary" mt={1}>
                        {currentEmotion.mood_description} • {Math.round(currentEmotion.confidence * 100)}% confident
                      </Typography>
                      <Box mt={2}>
                        {currentEmotion.music_genres.map((genre) => (
                          <Chip 
                            key={genre} 
                            label={genre} 
                            size="small" 
                            sx={{ m: 0.5 }}
                            color="primary"
                          />
                        ))}
                      </Box>
                    </Card>
                  </Box>
                )}

                <Box display="flex" gap={2} mb={3}>
                  <Button
                    fullWidth
                    variant="contained"
                    startIcon={<CameraAlt />}
                    onClick={() => setCameraOpen(true)}
                    disabled={loading}
                    className="glow"
                  >
                    Capture Emotion
                  </Button>
                  <Button
                    fullWidth
                    variant="outlined"
                    startIcon={<TextFields />}
                    onClick={() => setTextAnalysisOpen(true)}
                    disabled={loading}
                  >
                    Analyze Text
                  </Button>
                </Box>

                {/* Mood History Chart */}
                {moodHistory.length > 0 && (
                  <Box mt={4}>
                    <Bar data={chartData} options={chartOptions} />
                  </Box>
                )}
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        {/* Right Column - Music Recommendations */}
        <Grid item xs={12} md={6}>
          <motion.div
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
          >
            <Card className="glass glow">
              <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
                  <Typography variant="h5">
                    <Psychology sx={{ mr: 2, color: 'secondary.main' }} />
                    Music Recommendations
                  </Typography>
                  {recommendations.length > 0 && (
                    <Button
                      variant="contained"
                      color="secondary"
                      startIcon={<QueueMusic />}
                      onClick={createMoodPlaylist}
                      disabled={!isAuthenticated}
                      size="small"
                    >
                      Create Playlist
                    </Button>
                  )}
                </Box>

                {loading ? (
                  <Box textAlign="center" py={4}>
                    <div className="pulse">
                      <MusicNote sx={{ fontSize: '4rem', color: 'primary.main' }} />
                    </div>
                    <Typography>Analyzing your emotions...</Typography>
                  </Box>
                ) : recommendations.length > 0 ? (
                  <List sx={{ maxHeight: 600, overflowY: 'auto' }}>
                    {recommendations.map((track, index) => (
                      <motion.div
                        key={track.id}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.3, delay: index * 0.1 }}
                      >
                        <ListItem
                          sx={{
                            mb: 1,
                            borderRadius: 2,
                            backgroundColor: currentTrack?.id === track.id 
                              ? 'rgba(156, 39, 176, 0.2)' 
                              : 'rgba(255, 255, 255, 0.05)',
                            '&:hover': {
                              backgroundColor: 'rgba(156, 39, 176, 0.1)',
                            }
                          }}
                        >
                          <ListItemAvatar>
                            <Avatar 
                              src={track.image} 
                              variant="rounded"
                              sx={{ width: 56, height: 56 }}
                            >
                              <MusicNote />
                            </Avatar>
                          </ListItemAvatar>
                          <ListItemText
                            primary={track.name}
                            secondary={`${track.artist} • ${track.album}`}
                            sx={{ ml: 2 }}
                          />
                          <Box display="flex" gap={1}>
                            <IconButton
                              onClick={() => playTrack(track)}
                              color={currentTrack?.id === track.id && isPlaying ? 'secondary' : 'primary'}
                              disabled={!track.preview_url}
                            >
                              {currentTrack?.id === track.id && isPlaying ? <Pause /> : <PlayArrow />}
                            </IconButton>
                            <IconButton size="small">
                              <Favorite />
                            </IconButton>
                            <IconButton 
                              size="small"
                              onClick={() => window.open(track.external_url, '_blank')}
                            >
                              <Share />
                            </IconButton>
                          </Box>
                        </ListItem>
                      </motion.div>
                    ))}
                  </List>
                ) : (
                  <Box textAlign="center" py={6}>
                    <MusicNote sx={{ fontSize: '4rem', color: 'text.secondary', mb: 2 }} />
                    <Typography variant="h6" color="text.secondary">
                      Detect your emotion to get personalized music recommendations
                    </Typography>
                  </Box>
                )}
              </CardContent>
            </Card>
          </motion.div>
        </Grid>
      </Grid>

      {/* Camera Dialog */}
      <Dialog 
        open={cameraOpen} 
        onClose={() => setCameraOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Capture Your Emotion</DialogTitle>
        <DialogContent>
          <Box textAlign="center">
            <Webcam
              ref={webcamRef}
              audio={false}
              screenshotFormat="image/jpeg"
              width="100%"
              videoConstraints={{
                width: 640,
                height: 480,
                facingMode: "user"
              }}
              style={{ borderRadius: 8 }}
            />
            <Box mt={2} display="flex" gap={2} justifyContent="center">
              <Button
                variant="contained"
                onClick={capturePhoto}
                disabled={loading}
                startIcon={<CameraAlt />}
              >
                {loading ? 'Analyzing...' : 'Capture Photo'}
              </Button>
              <Button variant="outlined" onClick={() => setCameraOpen(false)}>
                Cancel
              </Button>
            </Box>
          </Box>
        </DialogContent>
      </Dialog>

      {/* Text Analysis Dialog */}
      <Dialog 
        open={textAnalysisOpen} 
        onClose={() => setTextAnalysisOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Analyze Text Sentiment</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            multiline
            rows={4}
            placeholder="How are you feeling today? Describe your mood..."
            value={userText}
            onChange={(e) => setUserText(e.target.value)}
            sx={{ mt: 2 }}
          />
          <Box mt={3} display="flex" gap={2} justifyContent="flex-end">
            <Button variant="outlined" onClick={() => setTextAnalysisOpen(false)}>
              Cancel
            </Button>
            <Button
              variant="contained"
              onClick={analyzeText}
              disabled={loading || !userText.trim()}
            >
              {loading ? 'Analyzing...' : 'Analyze'}
            </Button>
          </Box>
        </DialogContent>
      </Dialog>

      {/* Hidden audio element for track preview */}
      <audio
        ref={audioRef}
        onEnded={() => setIsPlaying(false)}
        onPause={() => setIsPlaying(false)}
        onPlay={() => setIsPlaying(true)}
      />
    </Container>
  );
}