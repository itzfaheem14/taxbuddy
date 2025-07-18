# MuseAIka 🎵🤖

> **AI-Powered Music Emotion Engine** - Discover music that matches your emotions with cutting-edge facial recognition and sentiment analysis.

![MuseAIka Banner](https://via.placeholder.com/1200x400/9c27b0/ffffff?text=MuseAIka+-+AI+Music+Emotion+Engine)

## 🚀 Features

### 🧠 **Emotion-Based AI Music Recommender**
- **Facial Emotion Detection**: Uses OpenCV and Hugging Face Transformers for real-time emotion recognition
- **Text Sentiment Analysis**: Analyzes written mood descriptions using advanced NLP models
- **Personalized Recommendations**: Integrates Spotify API for tailored music suggestions
- **Real-time Mood Tracking**: Charts and visualizes emotional patterns over time

### 🎼 **AI Music Generation**
- **Magenta Integration**: Leverages Google's Magenta and TensorFlow for AI-powered music creation
- **Emotion-driven Composition**: Generates melodies and tracks based on detected emotions
- **Multiple Instruments**: Creates both melody and drum patterns
- **Customizable Parameters**: Adjust tempo, key, and style based on mood

### 🎨 **Beautiful Modern UI**
- **Next.js & Material UI**: Responsive, accessible, and beautiful interface
- **Dark Theme**: Elegant glassmorphism design with purple/pink gradients
- **Real-time Charts**: Interactive mood visualization using Chart.js
- **Smooth Animations**: Framer Motion powered transitions and effects

### 👥 **Social & Collaborative Features**
- **Collaborative Playlists**: Real-time playlist editing with WebSockets
- **Social Sharing**: Share mood-based playlists with friends
- **Group Sessions**: Join collaborative music discovery sessions
- **Voting System**: Community-driven track recommendations

### 🔐 **Secure Authentication**
- **Spotify OAuth 2.0**: Seamless login with Spotify accounts
- **JWT Tokens**: Secure session management
- **Privacy Protection**: User data privacy and security checks

## 🏗️ Architecture

### **Backend Stack**
- **Framework**: Python Flask with SocketIO for WebSockets
- **AI/ML**: TensorFlow, Magenta, OpenCV, Hugging Face Transformers
- **Database**: MongoDB for data storage, Redis for caching
- **APIs**: Spotify Web API integration
- **Authentication**: OAuth 2.0, JWT tokens

### **Frontend Stack**
- **Framework**: Next.js 14 with TypeScript
- **UI Library**: Material UI with custom theming
- **State Management**: Zustand for lightweight state management
- **Real-time**: Socket.IO client for live features
- **Charts**: Chart.js for mood visualization
- **Animation**: Framer Motion for smooth transitions

### **Infrastructure**
- **Containerization**: Docker & Docker Compose
- **Orchestration**: Kubernetes support
- **Monitoring**: Prometheus & Grafana
- **Reverse Proxy**: Nginx for production
- **Error Handling**: Comprehensive fallback systems

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Spotify Developer Account
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/museaika.git
cd museaika
```

### 2. Set Up Environment Variables
```bash
# Copy environment template
cp .env.example .env

# Edit with your Spotify credentials
nano .env
```

Required environment variables:
```env
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SPOTIFY_REDIRECT_URI=http://localhost:3000/callback
SECRET_KEY=your_super_secret_key
JWT_SECRET_KEY=your_jwt_secret_key
```

### 3. Run with Docker Compose
```bash
# Start all services
cd docker
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 4. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **MongoDB**: localhost:27017
- **Redis**: localhost:6379

## 🛠️ Development Setup

### Backend Development
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env

# Run development server
python run.py
```

### Frontend Development
```bash
cd frontend

# Install dependencies
npm install

# Set environment variables
cp .env.local.example .env.local

# Run development server
npm run dev
```

## 📡 API Documentation

### Authentication Endpoints
```
POST /api/auth/spotify/login     # Get Spotify auth URL
POST /api/auth/spotify/callback  # Handle OAuth callback
POST /api/auth/verify           # Verify JWT token
GET  /api/auth/profile          # Get user profile
POST /api/auth/logout           # Logout user
```

### Emotion Detection Endpoints
```
POST /api/emotion/detect-facial    # Detect emotion from image
POST /api/emotion/analyze-text     # Analyze text sentiment
GET  /api/emotion/mood-history     # Get mood history
POST /api/emotion/mood-recommendations # Get mood-based recommendations
```

### Music Endpoints
```
POST /api/music/recommendations    # Get music recommendations
GET  /api/music/search            # Search tracks
POST /api/music/generate/melody   # Generate AI melody
POST /api/music/generate/track    # Generate full AI track
POST /api/music/playlists/create  # Create playlist
GET  /api/music/playlists         # Get user playlists
POST /api/music/mood-playlist     # Create mood-based playlist
```

### Social Endpoints
```
POST /api/social/sessions/create           # Create collaborative session
POST /api/social/sessions/{id}/join        # Join session
POST /api/social/sessions/{id}/add-track   # Add track to session
GET  /api/social/sessions                  # Get user sessions
```

## 🎯 Usage Examples

### Emotion Detection
```javascript
// Facial emotion detection
const response = await emotionService.detectFacialEmotion(imageBase64);
console.log(response.emotion); // 'happy', 'sad', 'angry', etc.

// Text sentiment analysis
const sentiment = await emotionService.analyzeTextSentiment(
  "I'm feeling great today!"
);
console.log(sentiment.emotion); // 'happy'
```

### Music Recommendations
```javascript
// Get emotion-based recommendations
const recommendations = await musicService.getRecommendations({
  emotion: 'happy',
  genres: ['pop', 'dance'],
  limit: 20
});

// Create mood playlist
const playlist = await musicService.createMoodPlaylist({
  emotion: 'sad',
  genres: ['acoustic', 'indie'],
  track_count: 15
});
```

### AI Music Generation
```javascript
// Generate melody
const melody = await musicService.generateMelody('happy', {
  num_steps: 128,
  temperature: 1.0
});

// Generate full track
const track = await musicService.generateTrack('energetic', {
  tempo: 120,
  num_bars: 8,
  key: 'C major'
});
```

## 🔧 Configuration

### Backend Configuration
Edit `backend/.env`:
```env
# Flask Settings
FLASK_ENV=development
SECRET_KEY=your_secret_key

# Database
MONGODB_URI=mongodb://localhost:27017/museaika
REDIS_URL=redis://localhost:6379

# Spotify API
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_REDIRECT_URI=http://localhost:3000/callback

# AI Models
EMOTION_MODEL_PATH=models/emotion_detection
MUSIC_GENERATION_MODEL_PATH=models/music_generation

# Security
JWT_SECRET_KEY=your_jwt_secret
JWT_ACCESS_TOKEN_EXPIRES=3600
```

### Frontend Configuration
Edit `frontend/.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:5000
NEXT_PUBLIC_WS_URL=http://localhost:5000
```

## 🚢 Deployment

### Docker Production Deployment
```bash
# Build production images
docker-compose -f docker-compose.yml -f docker-compose.prod.yml build

# Deploy with production profile
docker-compose --profile production up -d

# Enable monitoring
docker-compose --profile monitoring up -d
```

### Kubernetes Deployment
```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -n museaika

# Access via port-forward
kubectl port-forward svc/museaika-frontend 3000:3000 -n museaika
```

## 📊 Monitoring

### Prometheus Metrics
- API response times and error rates
- Emotion detection accuracy
- Music recommendation performance
- User engagement metrics

### Grafana Dashboards
- Real-time application metrics
- User mood analytics
- System performance monitoring
- Error tracking and alerting

Access monitoring:
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3001 (admin/admin123)

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/ -v --cov=app
```

### Frontend Tests
```bash
cd frontend
npm run test
npm run test:e2e
```

### Integration Tests
```bash
# Run full test suite
npm run test:integration
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow Python PEP 8 style guide for backend
- Use TypeScript and ESLint for frontend
- Write comprehensive tests for new features
- Update documentation for API changes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Spotify Web API** for music data and playback
- **Google Magenta** for AI music generation capabilities
- **Hugging Face** for pre-trained emotion detection models
- **OpenCV** for computer vision and facial recognition
- **Material UI** for beautiful React components
- **Next.js** for the amazing React framework

## 📞 Support

- 📧 Email: support@museaika.com
- 💬 Discord: [MuseAIka Community](https://discord.gg/museaika)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/museaika/issues)
- 📖 Docs: [Full Documentation](https://docs.museaika.com)

## 🗺️ Roadmap

### Version 2.0 (Coming Soon)
- [ ] Mobile app (React Native)
- [ ] Voice emotion detection
- [ ] Multi-language support
- [ ] Advanced AI music composition
- [ ] Social features expansion
- [ ] Playlist sharing marketplace

### Version 2.1 (Future)
- [ ] VR/AR integration
- [ ] Live concert recommendations
- [ ] Artist collaboration tools
- [ ] Music therapy features
- [ ] Enterprise dashboard

---

<div align="center">

**Made with ❤️ and 🎵 by the MuseAIka Team**

[⭐ Star this project](https://github.com/yourusername/museaika) • [🍴 Fork it](https://github.com/yourusername/museaika/fork) • [📱 Try the Demo](https://demo.museaika.com)

</div>