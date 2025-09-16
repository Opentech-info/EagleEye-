"""
Media Service - Handles media streaming and playback
"""

import os
import subprocess
import tempfile
import yt_dlp
from flask import jsonify

class MediaService:
    def __init__(self):
        self.mpv_path = os.path.join("resources", "mpv.exe")
        
    def stream_media(self, data):
        """Get streaming URL for media"""
        try:
            url = data.get('url')
            media_type = data.get('type', 'video')  # video or audio
            
            if not url:
                return {
                    'success': False,
                    'error': 'URL is required'
                }
            
            if media_type == 'audio':
                return self._get_audio_stream(url)
            else:
                return self._get_video_stream(url)
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _get_video_stream(self, url):
        """Get video streaming URL"""
        try:
            ydl_opts = {
                'quiet': True,
                'format': 'best[height<=720]',  # Limit to 720p for streaming
                'skip_download': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                return {
                    'success': True,
                    'stream_url': info.get('url'),
                    'title': info.get('title'),
                    'duration': info.get('duration'),
                    'thumbnail': info.get('thumbnail'),
                    'type': 'video'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _get_audio_stream(self, url):
        """Get audio streaming URL"""
        try:
            ydl_opts = {
                'quiet': True,
                'format': 'bestaudio',
                'skip_download': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                return {
                    'success': True,
                    'stream_url': info.get('url'),
                    'title': info.get('title'),
                    'duration': info.get('duration'),
                    'thumbnail': info.get('thumbnail'),
                    'type': 'audio'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_video_formats(self, url):
        """Get available video formats"""
        try:
            ydl_opts = {
                'quiet': True,
                'skip_download': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info.get('formats', [])
                
                # Process formats
                video_formats = []
                audio_formats = []
                
                for fmt in formats:
                    if fmt.get('vcodec') != 'none' and fmt.get('acodec') != 'none':
                        # Video + Audio format
                        video_formats.append({
                            'format_id': fmt.get('format_id'),
                            'quality': f"{fmt.get('height', 'Unknown')}p",
                            'ext': fmt.get('ext'),
                            'filesize': fmt.get('filesize'),
                            'fps': fmt.get('fps'),
                            'vcodec': fmt.get('vcodec'),
                            'acodec': fmt.get('acodec')
                        })
                    elif fmt.get('acodec') != 'none' and fmt.get('vcodec') == 'none':
                        # Audio only format
                        audio_formats.append({
                            'format_id': fmt.get('format_id'),
                            'quality': f"{fmt.get('abr', 'Unknown')}kbps",
                            'ext': fmt.get('ext'),
                            'filesize': fmt.get('filesize'),
                            'acodec': fmt.get('acodec')
                        })
                
                return {
                    'success': True,
                    'video_formats': video_formats,
                    'audio_formats': audio_formats,
                    'title': info.get('title')
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def launch_mpv(self, stream_url):
        """Launch MPV player with stream URL"""
        try:
            if os.path.exists(self.mpv_path):
                subprocess.Popen([self.mpv_path, stream_url])
                return {
                    'success': True,
                    'message': 'MPV player launched'
                }
            else:
                return {
                    'success': False,
                    'error': 'MPV player not found'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_playlist_info(self, url):
        """Get playlist information"""
        try:
            ydl_opts = {
                'quiet': True,
                'skip_download': True,
                'extract_flat': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                if 'entries' in info:
                    # It's a playlist
                    entries = []
                    for entry in info['entries'][:50]:  # Limit to 50 entries
                        entries.append({
                            'id': entry.get('id'),
                            'title': entry.get('title'),
                            'url': entry.get('url') or entry.get('webpage_url'),
                            'duration': entry.get('duration'),
                            'uploader': entry.get('uploader')
                        })
                    
                    return {
                        'success': True,
                        'is_playlist': True,
                        'title': info.get('title'),
                        'entries': entries,
                        'entry_count': len(entries)
                    }
                else:
                    # Single video
                    return {
                        'success': True,
                        'is_playlist': False,
                        'title': info.get('title'),
                        'url': url
                    }
                    
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_subtitle_info(self, url):
        """Get available subtitles for a video"""
        try:
            ydl_opts = {
                'quiet': True,
                'skip_download': True,
                'writesubtitles': True,
                'writeautomaticsub': True,
                'listsubtitles': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                subtitles = info.get('subtitles', {})
                auto_subtitles = info.get('automatic_captions', {})
                
                available_subs = []
                
                # Manual subtitles
                for lang, subs in subtitles.items():
                    for sub in subs:
                        available_subs.append({
                            'language': lang,
                            'ext': sub.get('ext'),
                            'url': sub.get('url'),
                            'type': 'manual'
                        })
                
                # Auto-generated subtitles
                for lang, subs in auto_subtitles.items():
                    for sub in subs:
                        available_subs.append({
                            'language': lang,
                            'ext': sub.get('ext'),
                            'url': sub.get('url'),
                            'type': 'auto'
                        })
                
                return {
                    'success': True,
                    'subtitles': available_subs,
                    'title': info.get('title')
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
