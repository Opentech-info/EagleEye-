"""
YouTube Service - Handles YouTube video search, download, and streaming
"""

import os
import yt_dlp
import threading
from flask import jsonify
from datetime import datetime
import tempfile
import subprocess

class YouTubeService:
    def __init__(self):
        self.download_folder = "downloads"
        os.makedirs(self.download_folder, exist_ok=True)
        
    def search_videos(self, query, limit=20):
        """Search YouTube videos with detailed information"""
        try:
            ydl_opts = {
                'quiet': True,
                'skip_download': True,
                'extract_flat': False,  # Get full info for better results
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                search_result = ydl.extract_info(f"ytsearch{limit}:{query}", download=False)
                results = search_result.get('entries', [])

                formatted_results = []
                for entry in results:
                    # Get available formats for quality info
                    formats = entry.get('formats', [])
                    video_qualities = []
                    audio_qualities = []

                    # Extract video qualities
                    for fmt in formats:
                        if fmt.get('vcodec') != 'none' and fmt.get('height'):
                            quality = f"{fmt.get('height')}p"
                            if quality not in video_qualities:
                                video_qualities.append(quality)

                    # Extract audio qualities
                    for fmt in formats:
                        if fmt.get('acodec') != 'none' and fmt.get('vcodec') == 'none':
                            if fmt.get('abr'):
                                quality = f"{fmt.get('abr')}kbps"
                                if quality not in audio_qualities:
                                    audio_qualities.append(quality)

                    # Sort qualities
                    video_qualities.sort(key=lambda x: int(x.replace('p', '')), reverse=True)
                    audio_qualities.sort(key=lambda x: int(x.replace('kbps', '')), reverse=True)

                    # Format duration
                    duration = entry.get('duration')
                    duration_str = "Unknown"
                    if duration:
                        hours = duration // 3600
                        minutes = (duration % 3600) // 60
                        seconds = duration % 60
                        if hours > 0:
                            duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                        else:
                            duration_str = f"{minutes:02d}:{seconds:02d}"

                    # Get best thumbnail
                    thumbnails = entry.get('thumbnails', [])
                    best_thumbnail = None
                    if thumbnails:
                        # Try to get high quality thumbnail
                        for thumb in reversed(thumbnails):
                            if thumb.get('url'):
                                best_thumbnail = thumb['url']
                                break

                    formatted_results.append({
                        'id': entry.get('id'),
                        'title': entry.get('title'),
                        'url': f"https://www.youtube.com/watch?v={entry.get('id')}",
                        'thumbnail': best_thumbnail,
                        'duration': duration,
                        'duration_str': duration_str,
                        'view_count': entry.get('view_count'),
                        'uploader': entry.get('uploader'),
                        'upload_date': entry.get('upload_date'),
                        'description': entry.get('description', '')[:200] + '...' if entry.get('description') else '',
                        'video_qualities': video_qualities,
                        'audio_qualities': audio_qualities,
                        'like_count': entry.get('like_count'),
                        'channel_url': entry.get('channel_url'),
                        'webpage_url': entry.get('webpage_url')
                    })

                return {
                    'success': True,
                    'results': formatted_results,
                    'count': len(formatted_results),
                    'query': query
                }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_video_info(self, url):
        """Get detailed video information"""
        try:
            ydl_opts = {
                'quiet': True,
                'skip_download': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                return {
                    'success': True,
                    'info': {
                        'id': info.get('id'),
                        'title': info.get('title'),
                        'description': info.get('description'),
                        'duration': info.get('duration'),
                        'view_count': info.get('view_count'),
                        'like_count': info.get('like_count'),
                        'uploader': info.get('uploader'),
                        'upload_date': info.get('upload_date'),
                        'thumbnail': info.get('thumbnail'),
                        'formats': self._get_available_formats(info.get('formats', [])),
                        'tags': info.get('tags', []),
                        'categories': info.get('categories', [])
                    }
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _get_available_formats(self, formats):
        """Extract available video and audio formats with detailed quality info"""
        video_formats = []
        audio_formats = []
        seen_video_qualities = set()
        seen_audio_qualities = set()

        for fmt in formats:
            # Video formats (with or without audio)
            if fmt.get('vcodec') != 'none' and fmt.get('height'):
                height = fmt.get('height')
                quality_label = f"{height}p"

                # Add quality labels for common resolutions
                if height >= 4320:
                    quality_label = f"{height}p (8K)"
                elif height >= 2160:
                    quality_label = f"{height}p (4K)"
                elif height >= 1440:
                    quality_label = f"{height}p (2K)"
                elif height >= 1080:
                    quality_label = f"{height}p (Full HD)"
                elif height >= 720:
                    quality_label = f"{height}p (HD)"

                if height not in seen_video_qualities:
                    video_formats.append({
                        'format_id': fmt.get('format_id'),
                        'quality': quality_label,
                        'height': height,
                        'ext': fmt.get('ext'),
                        'filesize': fmt.get('filesize'),
                        'fps': fmt.get('fps'),
                        'vcodec': fmt.get('vcodec'),
                        'acodec': fmt.get('acodec'),
                        'has_audio': fmt.get('acodec') != 'none'
                    })
                    seen_video_qualities.add(height)

            # Audio-only formats
            elif fmt.get('acodec') != 'none' and fmt.get('vcodec') == 'none':
                abr = fmt.get('abr')
                if abr and abr not in seen_audio_qualities:
                    quality_label = f"{abr}kbps"

                    # Add quality labels for audio
                    if abr >= 320:
                        quality_label = f"{abr}kbps (High)"
                    elif abr >= 192:
                        quality_label = f"{abr}kbps (Medium)"
                    elif abr >= 128:
                        quality_label = f"{abr}kbps (Standard)"
                    else:
                        quality_label = f"{abr}kbps (Low)"

                    audio_formats.append({
                        'format_id': fmt.get('format_id'),
                        'quality': quality_label,
                        'abr': abr,
                        'ext': fmt.get('ext'),
                        'filesize': fmt.get('filesize'),
                        'acodec': fmt.get('acodec')
                    })
                    seen_audio_qualities.add(abr)

        # Sort by quality (highest first)
        video_formats.sort(key=lambda x: x['height'], reverse=True)
        audio_formats.sort(key=lambda x: x['abr'], reverse=True)

        return {
            'video_formats': video_formats,
            'audio_formats': audio_formats
        }
    
    def download_video(self, data, user_id=None):
        """Download video with proxy streaming to avoid 403 errors"""
        try:
            url = data.get('url')
            quality = data.get('quality', 'best')
            download_type = data.get('type', 'video+audio')  # video, audio, or video+audio
            
            if not url:
                return {'success': False, 'error': 'URL is required'}
            
            # Create download history record (optional, if user is authenticated)
            if user_id:
                try:
                    from app import db, Download
                    download_record = Download(
                        user_id=user_id,
                        url=url,
                        status='completed',
                        download_type=download_type,
                        quality=quality
                    )
                    db.session.add(download_record)
                    db.session.commit()
                except:
                    # If database operations fail, continue with download
                    pass
            
            # Generate proxy stream URL
            import uuid
            stream_token = str(uuid.uuid4())
            
            # Store stream info in a temporary structure (in production, use Redis or cache)
            if not hasattr(self, '_stream_cache'):
                self._stream_cache = {}
            
            self._stream_cache[stream_token] = {
                'url': url,
                'quality': quality,
                'download_type': download_type,
                'timestamp': datetime.now().timestamp()
            }
            
            # Clean up old cache entries (older than 5 minutes)
            current_time = datetime.now().timestamp()
            self._stream_cache = {
                k: v for k, v in self._stream_cache.items() 
                if current_time - v['timestamp'] < 300
            }
            
            proxy_url = f"/api/youtube/stream/{stream_token}"
            filename = self._generate_filename(url, download_type)
            
            return {
                'success': True,
                'download_url': proxy_url,
                'file_name': filename,
                'message': 'Proxy stream generated'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _download_worker(self, download_id, url, quality, download_type):
        """Background worker for downloading videos"""
        from app import db, Download, socketio
        
        try:
            download_record = Download.query.get(download_id)
            download_record.status = 'downloading'
            db.session.commit()
            
            # Configure yt-dlp options based on download type
            if download_type == 'audio':
                format_selector = 'bestaudio/best'
                outtmpl = f'{self.download_folder}/%(title)s.%(ext)s'
            elif download_type == 'video':
                format_selector = f'bestvideo[height<={quality[:-1]}]+bestaudio/best'
                outtmpl = f'{self.download_folder}/%(title)s.%(ext)s'
            else:  # video+audio
                format_selector = f'bestvideo[height<={quality[:-1]}]+bestaudio/best'
                outtmpl = f'{self.download_folder}/%(title)s.%(ext)s'
            
            def progress_hook(d):
                if d['status'] == 'downloading':
                    try:
                        percent = d.get('_percent_str', '0%').strip('%')
                        progress = float(percent) / 100
                        
                        # Update database
                        download_record.progress = progress
                        db.session.commit()
                        
                        # Emit progress via WebSocket
                        socketio.emit('download_progress', {
                            'download_id': download_id,
                            'progress': progress,
                            'status': 'downloading'
                        })
                    except:
                        pass
                elif d['status'] == 'finished':
                    download_record.status = 'completed'
                    download_record.progress = 1.0
                    download_record.file_path = d['filename']
                    download_record.completed_at = datetime.utcnow()
                    db.session.commit()
                    
                    socketio.emit('download_complete', {
                        'download_id': download_id,
                        'file_path': d['filename']
                    })
            
            ydl_opts = {
                'format': format_selector,
                'outtmpl': outtmpl,
                'progress_hooks': [progress_hook],
                'merge_output_format': 'mp4',
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                download_record.title = info.get('title', 'Unknown')
                db.session.commit()
                
                ydl.download([url])
                
        except Exception as e:
            download_record.status = 'failed'
            db.session.commit()
            
            socketio.emit('download_error', {
                'download_id': download_id,
                'error': str(e)
            })
    
    def _get_direct_stream_url(self, url, quality, download_type):
        """Get direct stream URL for browser download with quality selection"""
        try:
            # Parse quality parameter
            quality_height = None
            if quality != 'best':
                # Extract height from quality (e.g., "4320p" -> 4320)
                quality_height = int(quality.replace('p', ''))
            
            # Configure format selector based on download type and quality
            if download_type == 'audio':
                format_selector = 'bestaudio/best'
                extension = 'mp3'
            elif download_type == 'video':
                if quality_height:
                    format_selector = f'bestvideo[height<={quality_height}]+bestaudio/best'
                else:
                    format_selector = 'bestvideo+bestaudio/best'
                extension = 'mp4'
            else:  # video+audio
                if quality_height:
                    format_selector = f'bestvideo[height<={quality_height}]+bestaudio/best'
                else:
                    format_selector = 'best'
                extension = 'mp4'
            
            ydl_opts = {
                'quiet': True,
                'format': format_selector,
                'skip_download': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                # Get the best format URL
                stream_url = None
                filename = None
                
                if download_type == 'audio':
                    # Find best audio format
                    for fmt in info.get('formats', []):
                        if fmt.get('acodec') != 'none' and fmt.get('vcodec') == 'none':
                            stream_url = fmt.get('url')
                            break
                else:
                    # Find video+audio format or separate streams
                    for fmt in info.get('formats', []):
                        if fmt.get('vcodec') != 'none' and fmt.get('acodec') != 'none':
                            # Combined format
                            stream_url = fmt.get('url')
                            break
                    
                    if not stream_url:
                        # If no combined format, get the best video
                        for fmt in info.get('formats', []):
                            if fmt.get('vcodec') != 'none':
                                stream_url = fmt.get('url')
                                break
                
                # Generate filename
                safe_title = "".join(c for c in info.get('title', 'video') if c.isalnum() or c in (' ', '-', '_')).rstrip()
                filename = f"{safe_title}.{extension}"
                
                if stream_url:
                    return {
                        'success': True,
                        'stream_url': stream_url,
                        'filename': filename,
                        'title': info.get('title')
                    }
                else:
                    return {
                        'success': False,
                        'error': 'No suitable format found'
                    }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def generate_filename(self, url, download_type):
        """Generate safe filename for download"""
        return self._generate_filename(url, download_type)
    
    def _generate_filename(self, url, download_type):
        """Generate safe filename for download"""
        try:
            # Get video title
            ydl_opts = {
                'quiet': True,
                'skip_download': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'video')
                
                # Clean title for filename
                safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
                
                # Add extension based on download type
                if download_type == 'audio':
                    return f"{safe_title}.mp3"
                else:
                    return f"{safe_title}.mp4"
                    
        except Exception:
            # Fallback filename
            return f"youtube_video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    
    def get_stream_info(self, stream_token):
        """Get stream information from cache"""
        if not hasattr(self, '_stream_cache'):
            return None
            
        # Clean up old cache entries first
        current_time = datetime.now().timestamp()
        self._stream_cache = {
            k: v for k, v in self._stream_cache.items() 
            if current_time - v['timestamp'] < 300
        }
        
        return self._stream_cache.get(stream_token)
    
    def stream_video(self, stream_token):
        """Stream video content through proxy to avoid 403 errors"""
        from flask import Response, stream_with_context
        
        stream_info = self.get_stream_info(stream_token)
        if not stream_info:
            return None
        
        url = stream_info['url']
        quality = stream_info['quality']
        download_type = stream_info['download_type']
        
        try:
            # Parse quality parameter
            quality_height = None
            if quality != 'best':
                quality_height = int(quality.replace('p', ''))
            
            # Configure format selector based on download type and quality
            if download_type == 'audio':
                format_selector = 'bestaudio/best'
                extension = 'mp3'
            elif download_type == 'video':
                if quality_height:
                    format_selector = f'bestvideo[height<={quality_height}]+bestaudio/best'
                else:
                    format_selector = 'bestvideo+bestaudio/best'
                extension = 'mp4'
            else:  # video+audio
                if quality_height:
                    format_selector = f'bestvideo[height<={quality_height}]+bestaudio/best'
                else:
                    format_selector = 'best'
                extension = 'mp4'
            
            # yt-dlp options for streaming
            ydl_opts = {
                'format': format_selector,
                'quiet': True,
                'no_warnings': True,
                'outtmpl': '-',
                'noplaylist': True,
            }
            
            def generate():
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url, download=False)
                    
                    # Get the actual stream URL with proper authentication
                    for fmt in info_dict.get('formats', []):
                        if download_type == 'audio':
                            if fmt.get('acodec') != 'none' and fmt.get('vcodec') == 'none':
                                stream_url = fmt.get('url')
                                break
                        else:
                            if fmt.get('vcodec') != 'none' and fmt.get('acodec') != 'none':
                                stream_url = fmt.get('url')
                                break
                    
                    if not stream_url:
                        # Fallback to best available
                        for fmt in info_dict.get('formats', []):
                            if fmt.get('url'):
                                stream_url = fmt.get('url')
                                break
                    
                    if stream_url:
                        # Use requests to stream with proper headers
                        import requests
                        
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                            'Accept': '*/*',
                            'Accept-Language': 'en-US,en;q=0.9',
                            'Accept-Encoding': 'gzip, deflate, br',
                            'Connection': 'keep-alive',
                            'Sec-Fetch-Dest': 'empty',
                            'Sec-Fetch-Mode': 'cors',
                            'Sec-Fetch-Site': 'cross-site',
                        }
                        
                        # Stream the content
                        with requests.get(stream_url, headers=headers, stream=True) as r:
                            r.raise_for_status()
                            for chunk in r.iter_content(chunk_size=8192):
                                yield chunk
            
            filename = self._generate_filename(url, download_type)
            
            response = Response(
                stream_with_context(generate()),
                mimetype='application/octet-stream',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"',
                    'Content-Type': 'application/octet-stream',
                    'Content-Transfer-Encoding': 'binary',
                }
            )
            
            return response
            
        except Exception as e:
            print(f"Streaming error: {e}")
            return None
    
    def get_stream_url(self, video_url):
        """Get direct stream URL for video (legacy method)"""
        try:
            ydl_opts = {
                'quiet': True,
                'format': 'best',
                'skip_download': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                return {
                    'success': True,
                    'stream_url': info.get('url'),
                    'title': info.get('title')
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
