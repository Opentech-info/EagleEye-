# 🦅 EagleEye - Advanced Media Management Platform

EagleEye is a comprehensive media management platform that allows users to search, download, stream, and manage videos and torrents from various sources including YouTube and torrent sites.

## ✨ Features

### 🎥 Video Management
- **YouTube Search & Download**: Search YouTube videos and download them in various qualities
- **Quality Selection**: Choose from multiple video and audio quality options
- **Batch Downloads**: Download multiple videos simultaneously
- **Progress Tracking**: Real-time download progress with WebSocket updates

### 🌊 Torrent Integration
- **Torrent Search**: Search torrents from 1337x and other popular sites
- **Magnet Links**: Direct magnet link support for easy torrent adding
- **Quality Detection**: Automatic quality detection from torrent titles
- **Popular Torrents**: Browse popular torrents by category

### 👤 User Management
- **User Authentication**: Secure registration and login system
- **Profile Management**: Customizable user profiles with preferences
- **Download History**: Track all your downloads and their status
- **Favorites & History**: Save favorite content and view history

### 🎨 Modern UI/UX
- **Responsive Design**: Works seamlessly on desktop and mobile
- **Dark Theme**: Easy on the eyes with a modern dark interface
- **Real-time Updates**: Live updates for downloads and system status
- **Intuitive Navigation**: Clean and organized user interface

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn

### Method 1: Using the Startup Script (Recommended)

1. **Clone or download the project**
   ```bash
   # If you have git:
   git clone <repository-url>
   cd EagleEye
   
   # Or simply extract the downloaded files
   ```

2. **Run the startup script**
   ```bash
   python start_eagleeye.py
   ```

3. **Follow the on-screen instructions**
   - The script will automatically check and install dependencies
   - Start both backend and frontend servers
   - Open your browser to the application

### Method 2: Manual Setup

#### Backend Setup

1. **Navigate to the backend directory**
   ```bash
   cd backend
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the backend server**
   ```bash
   python run.py
   ```

   The backend will be available at: `http://localhost:5000`

#### Frontend Setup

1. **Navigate to the frontend directory** (in a new terminal)
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies**
   ```bash
   npm install
   ```

3. **Start the frontend development server**
   ```bash
   npm start
   ```

   The frontend will be available at: `http://localhost:3000`

## 📁 Project Structure

```
EagleEye/
├── backend/                 # Flask backend application
│   ├── app.py              # Main Flask application
│   ├── config.py           # Configuration settings
│   ├── run.py              # Backend runner script
│   ├── services/           # Business logic services
│   │   ├── auth_service.py    # User authentication
│   │   ├── youtube_service.py # YouTube functionality
│   │   ├── torrent_service.py # Torrent functionality
│   │   └── media_service.py   # Media streaming
│   ├── utils/              # Utility functions
│   │   └── helpers.py        # Helper functions
│   ├── downloads/          # Downloaded files storage
│   └── instance/           # Database instance
├── frontend/               # React TypeScript frontend
│   ├── src/
│   │   ├── components/     # Reusable React components
│   │   ├── pages/         # Page components
│   │   ├── contexts/      # React contexts for state management
│   │   ├── hooks/         # Custom React hooks
│   │   ├── services/      # API service functions
│   │   └── App.tsx        # Main App component
│   ├── public/            # Static files
│   └── package.json       # Frontend dependencies
├── index.html            # Simple HTML frontend (alternative)
├── test_backend.py       # Backend testing script
├── test_frontend.html    # Frontend testing page
├── start_eagleeye.py     # Automated startup script
└── requirements.txt      # Python dependencies
```

## 🔧 Configuration

### Backend Configuration

Edit `backend/config.py` to customize:

- **Secret Keys**: Change default secret keys for production
- **Database**: Configure database connection (default: SQLite)
- **Upload Settings**: Set upload folder and file size limits
- **External Tools**: Configure paths to external tools like MPV, qBittorrent

### Environment Variables

You can also configure the application using environment variables:

```bash
# Backend
export SECRET_KEY="your-secret-key"
export DATABASE_URL="sqlite:///eagleeye.db"
export JWT_SECRET_KEY="your-jwt-secret"

# Frontend
export REACT_APP_API_URL="http://localhost:5000"
```

## 🧪 Testing

### Backend Tests

Run the backend test script:
```bash
python test_backend.py
```

### Frontend Tests

Open the test page in your browser:
```bash
# Open the test file
open test_frontend.html
```

Or navigate to: `file:///path/to/project/test_frontend.html`

## 📚 API Documentation

### Authentication Endpoints

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - Get user profile (requires auth)

### YouTube Endpoints

- `POST /api/youtube/search` - Search YouTube videos
- `POST /api/youtube/download` - Download YouTube video
- `POST /api/youtube/info` - Get video information
- `POST /api/youtube/formats` - Get available formats

### Torrent Endpoints

- `POST /api/torrent/search` - Search torrents
- `GET /api/torrent/popular` - Get popular torrents
- `POST /api/torrent/launch` - Launch qBittorrent

### Media Endpoints

- `POST /api/media/stream` - Get media stream URL
- `POST /api/media/formats` - Get media formats
- `POST /api/media/playlist` - Get playlist info

### System Endpoints

- `GET /api/health` - Health check
- `GET /api/system/info` - System information

## 🛠️ Development

### Adding New Features

1. **Backend**: Add new service in `backend/services/`
2. **Frontend**: Create new components in `frontend/src/components/`
3. **API**: Add new routes in `backend/app.py`
4. **Database**: Update models in `backend/app.py`

### Code Style

- **Python**: Follow PEP 8 guidelines
- **TypeScript**: Use TypeScript strict mode
- **React**: Use functional components with hooks
- **Comments**: Add meaningful comments for complex logic

## 🐛 Troubleshooting

### Common Issues

**Port Already in Use**
```bash
# Find process using port 5000
netstat -ano | findstr :5000  # Windows
lsof -i :5000                 # macOS/Linux

# Kill the process
taskkill /PID <pid> /F        # Windows
kill -9 <pid>                 # macOS/Linux
```

**Dependencies Not Installing**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Backend Import Errors**
```bash
# Make sure you're in the backend directory
cd backend

# Install dependencies again
pip install -r requirements.txt

# Check Python path
python -c "import sys; print(sys.path)"
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **yt-dlp** for YouTube video downloading
- **React** for the frontend framework
- **Flask** for the backend framework
- **Material-UI** for UI components
- **1337x** for torrent search functionality

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Search existing issues
3. Create a new issue with detailed information
4. Join our community discussions

---

**Built with ❤️ by the EagleEye team**
