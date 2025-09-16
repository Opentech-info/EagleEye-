"""
Utility helper functions for the EagleEye backend
"""

import os
import re
import hashlib
import mimetypes
from urllib.parse import urlparse
from datetime import datetime
import json

def is_valid_url(url):
    """Validate if a string is a well-formed URL"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def is_youtube_url(url):
    """Check if URL is a YouTube URL"""
    youtube_domains = ['youtube.com', 'youtu.be', 'www.youtube.com', 'm.youtube.com']
    try:
        domain = urlparse(url).netloc.lower()
        return any(yt_domain in domain for yt_domain in youtube_domains)
    except:
        return False

def extract_video_id(url):
    """Extract video ID from YouTube URL"""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
        r'youtube\.com\/v\/([^&\n?#]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def sanitize_filename(filename):
    """Sanitize filename for safe file system storage"""
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip(' .')
    
    # Limit length
    if len(filename) > 200:
        name, ext = os.path.splitext(filename)
        filename = name[:200-len(ext)] + ext
    
    return filename

def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def format_duration(seconds):
    """Format duration in seconds to HH:MM:SS"""
    if not seconds:
        return "00:00"
    
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"

def generate_file_hash(filepath):
    """Generate MD5 hash of a file"""
    hash_md5 = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except:
        return None

def get_file_info(filepath):
    """Get comprehensive file information"""
    if not os.path.exists(filepath):
        return None
    
    stat = os.stat(filepath)
    mime_type, _ = mimetypes.guess_type(filepath)
    
    return {
        'filename': os.path.basename(filepath),
        'size': stat.st_size,
        'size_formatted': format_file_size(stat.st_size),
        'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
        'mime_type': mime_type,
        'extension': os.path.splitext(filepath)[1].lower(),
        'hash': generate_file_hash(filepath)
    }

def create_response(success=True, data=None, message=None, error=None, status_code=200):
    """Create standardized API response"""
    response = {
        'success': success,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    if data is not None:
        response['data'] = data
    
    if message:
        response['message'] = message
    
    if error:
        response['error'] = error
    
    return response, status_code

def validate_video_quality(quality):
    """Validate video quality parameter"""
    valid_qualities = ['144p', '240p', '360p', '480p', '720p', '1080p', '1440p', '2160p', 'best', 'worst']
    return quality in valid_qualities

def parse_yt_dlp_progress(progress_str):
    """Parse yt-dlp progress string"""
    try:
        # Extract percentage
        percent_match = re.search(r'(\d+\.?\d*)%', progress_str)
        if percent_match:
            return float(percent_match.group(1)) / 100
        return 0.0
    except:
        return 0.0

def clean_old_files(directory, max_age_days=7):
    """Clean old files from directory"""
    if not os.path.exists(directory):
        return
    
    cutoff_time = datetime.now().timestamp() - (max_age_days * 24 * 60 * 60)
    
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            if os.path.getmtime(filepath) < cutoff_time:
                try:
                    os.remove(filepath)
                except:
                    pass

def ensure_directory(path):
    """Ensure directory exists, create if it doesn't"""
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def load_json_file(filepath, default=None):
    """Safely load JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return default or {}

def save_json_file(filepath, data):
    """Safely save JSON file"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except:
        return False

def get_platform_info():
    """Get platform information"""
    import platform
    return {
        'system': platform.system(),
        'release': platform.release(),
        'version': platform.version(),
        'machine': platform.machine(),
        'processor': platform.processor()
    }

def validate_email(email):
    """Validate email address format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def generate_unique_filename(original_filename, directory):
    """Generate unique filename to avoid conflicts"""
    base_name, extension = os.path.splitext(original_filename)
    counter = 1
    
    while os.path.exists(os.path.join(directory, original_filename)):
        original_filename = f"{base_name}_{counter}{extension}"
        counter += 1
    
    return original_filename
