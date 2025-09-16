"""
EagleEye Flask Backend Application
Main Flask application with all the core functionality
"""

from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS 
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_socketio import SocketIO, emit
import os
import sys
from datetime import datetime, timedelta, timezone
from flask import Flask, render_template_string


# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import configuration
try:
    from config import config
except ImportError:
    # Fallback configuration if config.py is not found
    class Config:
        SECRET_KEY = 'your-secret-key-change-this'
        SQLALCHEMY_DATABASE_URI = 'sqlite:///eagleeye.db'
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        JWT_SECRET_KEY = 'jwt-secret-string-change-this'
        JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
        UPLOAD_FOLDER = 'downloads'

    config = {'development': Config, 'default': Config}

# Import our custom modules
try:
    from services.youtube_service import YouTubeService
    from services.torrent_service import TorrentService
    from services.auth_service import AuthService
    from services.media_service import MediaService
    from utils.helpers import create_response, ensure_directory
except ImportError as e:
    print(f"Warning: Could not import some services: {e}")
    # Create dummy classes for missing services
    class YouTubeService:
        def search_videos(self, query, limit=20):
            return {'success': False, 'error': 'Service not available'}
        def download_video(self, data, user_id):
            return {'success': False, 'error': 'Service not available'}
        def get_video_info(self, url):
            return {'success': False, 'error': 'Service not available'}

    class TorrentService:
        def search_torrents(self, query):
            return {'success': False, 'error': 'Service not available'}
        def get_popular_torrents(self, category):
            return {'success': False, 'error': 'Service not available'}
        def launch_qbittorrent(self):
            return {'success': False, 'error': 'Service not available'}

    class AuthService:
        def register_user(self, data):
            return {'success': False, 'error': 'Service not available'}
        def login_user(self, data):
            return {'success': False, 'error': 'Service not available'}
        def get_user_profile(self, username):
            return {'success': False, 'error': 'Service not available'}

    class MediaService:
        def stream_media(self, data):
            return {'success': False, 'error': 'Service not available'}
        def get_video_formats(self, url):
            return {'success': False, 'error': 'Service not available'}

    def create_response(success=True, data=None, message=None, error=None, status_code=200):
        response = {'success': success, 'timestamp': datetime.now(timezone.utc).isoformat()}
        if data is not None:
            response['data'] = data
        if message:
            response['message'] = message
        if error:
            response['error'] = error
        return response, status_code

    def ensure_directory(path):
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

# Initialize Flask app
def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Ensure required directories exist
    ensure_directory(app.config['UPLOAD_FOLDER'])
    ensure_directory('logs')

    return app

app = create_app()

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

# Initialize services
youtube_service = YouTubeService()
torrent_service = TorrentService()
auth_service = AuthService()
media_service = MediaService()

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)

class Download(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    title = db.Column(db.String(200))
    status = db.Column(db.String(50), default='pending')
    progress = db.Column(db.Float, default=0.0)
    file_path = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = db.Column(db.DateTime)

# Routes
# Note: app is already created above with create_app()
@app.route("/")
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>EagleEye</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.8.1/slick.min.css" rel="stylesheet"/>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.8.1/slick-theme.min.css" rel="stylesheet"/>
        <style>
            body, html {
                margin: 0;
                padding: 0;
                height: 100%;
                font-family: 'Arial', sans-serif;
                overflow-x: hidden;
            }
            .hero {
                position: relative;
                height: 100vh;
                background: url('https://images.unsplash.com/photo-1611254634177-2fdd94a6b9f1?auto=format&fit=crop&w=1950&q=80') center/cover no-repeat;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                color: #fff;
                text-align: center;
            }
            .hero::after {
                content: "";
                position: absolute;
                top:0; left:0; width:100%; height:100%;
                background: linear-gradient(180deg, rgba(0,0,0,0.6), rgba(0,0,0,0.9));
                z-index: 1;
            }
            .hero-content {
                position: relative;
                z-index: 2;
                max-width: 800px;
                animation: fadeIn 1.5s ease-in-out;
            }
            h1 {
                font-size: 4rem;
                font-weight: bold;
                margin: 0 0 20px;
            }
            p {
                font-size: 1.5rem;
                margin-bottom: 30px;
            }
            .btn {
                padding: 15px 30px;
                font-size: 1.2rem;
                font-weight: bold;
                background: #e50914;
                border: none;
                border-radius: 5px;
                color: white;
                cursor: pointer;
                transition: all 0.3s ease;
                text-decoration: none;
            }
            .btn:hover {
                background: #f6121d;
                transform: scale(1.05);
            }
            @keyframes fadeIn {
                from {opacity: 0; transform: translateY(20px);}
                to {opacity: 1; transform: translateY(0);}
            }
            .carousel {
                margin: 50px auto;
                max-width: 1200px;
            }
            .carousel img {
                width: 100%;
                border-radius: 10px;
            }
            .carousel .slick-slide {
                margin: 0 10px;
            }
            .carousel .slick-list {
                margin: 0 -10px;
            }
            h2 {
                color: #fff;
                margin-left: 20px;
                margin-bottom: 20px;
            }
        </style>
    </head>
    <body>
        <div class="hero">
            <div class="hero-content">
                <h1>🦅 EagleEye</h1>
                <p>Unlimited movies, TV shows, and more</p>
                <a href="/api/docs" class="btn">Get Started</a>
            </div>
        </div>

        <h2>Trending Now</h2>
        <div class="carousel">
            <div><img src="https://image.tmdb.org/t/p/w500/5SQD9.jpg" alt="Movie 1"></div>
            <div><img src="https://image.tmdb.org/t/p/w500/6FL.jpg" alt="Movie 2"></div>
            <div><img src="https://image.tmdb.org/t/p/w500/7BonApp.jpg" alt="Movie 3"></div>
            <div><img src="https://image.tmdb.org/t/p/w500/8Aiyaa.jpg" alt="Movie 4"></div>
            <div><img src="https://image.tmdb.org/t/p/w500/9SexLife.jpg" alt="Movie 5"></div>
        </div>

        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.8.1/slick.min.js"></script>
        <script>
            $(document).ready(function(){
                $('.carousel').slick({
                    slidesToShow: 5,
                    slidesToScroll: 1,
                    autoplay: true,
                    autoplaySpeed: 2000,
                    arrows: true,
                    dots: false,
                    responsive: [
                        { breakpoint: 1024, settings: { slidesToShow: 4 }},
                        { breakpoint: 768, settings: { slidesToShow: 3 }},
                        { breakpoint: 480, settings: { slidesToShow: 2 }}
                    ]
                });
            });
        </script>
    </body>
    </html>
    """)


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now(timezone.utc).isoformat()})

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    return auth_service.register_user(data)

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    return auth_service.login_user(data)

@app.route('/api/auth/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()
    return auth_service.get_user_profile(current_user_id)

@app.route('/api/youtube/search', methods=['POST'])
@jwt_required()
def youtube_search():
    data = request.get_json()
    query = data.get('query', '')
    limit = data.get('limit', 20)
    return youtube_service.search_videos(query, limit)

@app.route('/api/youtube/download', methods=['POST'])
def youtube_download():
    data = request.get_json()
    
    # Try to get user ID if authenticated, otherwise allow guest download
    try:
        current_user_id = get_jwt_identity()
    except:
        current_user_id = None
    
    return youtube_service.download_video(data, current_user_id)

@app.route('/api/torrent/search', methods=['POST'])
@jwt_required()
def torrent_search():
    data = request.get_json()
    query = data.get('query', '')
    return torrent_service.search_torrents(query)

@app.route('/api/media/stream', methods=['POST'])
@jwt_required()
def stream_media():
    data = request.get_json()
    return media_service.stream_media(data)

@app.route('/api/downloads', methods=['GET'])
@jwt_required()
def get_downloads():
    current_user_id = get_jwt_identity()
    downloads = Download.query.filter_by(user_id=current_user_id).order_by(Download.created_at.desc()).all()
    return jsonify([{
        'id': d.id,
        'url': d.url,
        'title': d.title,
        'status': d.status,
        'progress': d.progress,
        'created_at': d.created_at.isoformat(),
        'completed_at': d.completed_at.isoformat() if d.completed_at else None
    } for d in downloads])

@app.route('/api/downloads/<int:download_id>', methods=['DELETE'])
@jwt_required()
def delete_download(download_id):
    current_user_id = get_jwt_identity()
    download = Download.query.filter_by(id=download_id, user_id=current_user_id).first()

    if not download:
        return jsonify({'success': False, 'error': 'Download not found'}), 404

    # Delete file if it exists
    if download.file_path and os.path.exists(download.file_path):
        try:
            os.remove(download.file_path)
        except:
            pass

    db.session.delete(download)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Download deleted successfully'})

@app.route('/api/downloads/<int:download_id>/file', methods=['GET'])
@jwt_required()
def download_file(download_id):
    current_user_id = get_jwt_identity()
    download = Download.query.filter_by(id=download_id, user_id=current_user_id).first()

    if not download or not download.file_path:
        return jsonify({'success': False, 'error': 'File not found'}), 404

    if not os.path.exists(download.file_path):
        return jsonify({'success': False, 'error': 'File no longer exists'}), 404

    return send_file(download.file_path, as_attachment=True)

@app.route('/api/youtube/info', methods=['POST'])
def get_video_info():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'success': False, 'error': 'URL is required'}), 400

    return youtube_service.get_video_info(url)

@app.route('/api/media/formats', methods=['POST'])
@jwt_required()
def get_media_formats():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'success': False, 'error': 'URL is required'}), 400

    return media_service.get_video_formats(url)

@app.route('/api/torrent/popular', methods=['GET'])
@jwt_required()
def get_popular_torrents():
    category = request.args.get('category', 'movies')
    return torrent_service.get_popular_torrents(category)

@app.route('/api/torrent/launch', methods=['POST'])
@jwt_required()
def launch_qbittorrent():
    return torrent_service.launch_qbittorrent()

@app.route('/api/system/info', methods=['GET'])
def get_system_info():
    from utils.helpers import get_platform_info
    return jsonify({
        'success': True,
        'platform': get_platform_info(),
        'version': '2.0.0',
        'features': {
            'youtube_download': True,
            'torrent_search': True,
            'media_streaming': True,
            'user_authentication': True
        }
    })

@app.route('/api/youtube/formats', methods=['POST'])
def get_video_formats():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'success': False, 'error': 'URL is required'}), 400

    try:
        video_info = youtube_service.get_video_info(url)
        if video_info.get('success'):
            return jsonify(video_info)
        else:
            return jsonify(video_info), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/youtube/stream/<stream_token>', methods=['GET'])
def stream_video(stream_token):
    """Proxy stream video content to avoid 403 errors"""
    response = youtube_service.stream_video(stream_token)
    
    if response is None:
        return jsonify({'success': False, 'error': 'Stream not found or expired'}), 404
    
    return response

@app.route('/api/youtube/download-with-quality', methods=['POST'])
def download_with_quality():
    data = request.get_json()
    url = data.get('url')
    format_id = data.get('format_id')
    download_type = data.get('type', 'video')  # video, audio

    if not url:
        return jsonify({'success': False, 'error': 'URL is required'}), 400

    try:
        # For now, use the existing download method
        # In a real implementation, you'd modify the download method to accept format_id
        download_data = {
            'url': url,
            'quality': data.get('quality', 'best'),
            'type': download_type
        }

        # This would need JWT authentication in a real app
        result = youtube_service.download_video(download_data, user_id=1)
        return result

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# WebSocket events for real-time updates
@socketio.on('connect')
@jwt_required()
def handle_connect():
    print('Client connected')
    emit('status', {'msg': 'Connected to EagleEye server'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
