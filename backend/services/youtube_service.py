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
    
    def download_video(self, data, user_id):
        """Download video with progress tracking"""
        try:
            url = data.get('url')
            quality = data.get('quality', 'best')
            download_type = data.get('type', 'video')  # video, audio, or video+audio
            
            if not url:
                return {'success': False, 'error': 'URL is required'}
            
            # Create download record
            from app import db, Download
            download_record = Download(
                user_id=user_id,
                url=url,
                status='starting'
            )
            db.session.add(download_record)
            db.session.commit()
            
            # Start download in background thread
            thread = threading.Thread(
                target=self._download_worker,
                args=(download_record.id, url, quality, download_type)
            )
            thread.start()
            
            return {
                'success': True,
                'download_id': download_record.id,
                'message': 'Download started'
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
    
    def get_stream_url(self, video_url):
        """Get direct stream URL for video"""
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
