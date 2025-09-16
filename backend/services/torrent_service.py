"""
Torrent Service - Handles torrent search and management
"""

import requests
import cloudscraper
from bs4 import BeautifulSoup
from flask import jsonify
import subprocess
import os

class TorrentService:
    def __init__(self):
        self.qbittorrent_path = os.path.join("resources", "qbittorrent.exe")
        
    def search_torrents(self, query, page=1):
        """Search torrents from 1337x"""
        try:
            base_url = "https://www.1337x.to"
            search_url = f"{base_url}/search/{query}/{page}/"
            
            # Use cloudscraper to bypass Cloudflare
            scraper = cloudscraper.create_scraper()
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            response = scraper.get(search_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            torrents = []
            rows = soup.select("table.table-list tbody tr")
            
            if not rows:
                return {
                    'success': True,
                    'results': [],
                    'message': 'No results found'
                }
            
            for row in rows[:20]:  # Limit to 20 results
                try:
                    title_cell = row.select_one("td.name a")
                    if not title_cell:
                        continue
                        
                    title = title_cell.text.strip()
                    detail_page = base_url + title_cell['href']
                    
                    size_cell = row.select_one("td.size")
                    size = size_cell.text.strip() if size_cell else "Unknown"
                    
                    seeders_cell = row.select_one("td.seeds")
                    seeders = int(seeders_cell.text.strip()) if seeders_cell and seeders_cell.text.strip().isdigit() else 0
                    
                    leechers_cell = row.select_one("td.leeches")
                    leechers = int(leechers_cell.text.strip()) if leechers_cell and leechers_cell.text.strip().isdigit() else 0
                    
                    # Determine quality based on title keywords
                    quality = self._determine_quality(title)
                    
                    # Get magnet link
                    magnet_link = self._get_magnet_link(detail_page, scraper)
                    
                    torrents.append({
                        'title': title,
                        'size': size,
                        'seeders': seeders,
                        'leechers': leechers,
                        'quality': quality,
                        'magnet_link': magnet_link,
                        'detail_url': detail_page
                    })
                    
                except Exception as e:
                    continue  # Skip problematic entries
            
            return {
                'success': True,
                'results': torrents,
                'count': len(torrents)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _determine_quality(self, title):
        """Determine video quality from title"""
        title_lower = title.lower()
        
        if any(keyword in title_lower for keyword in ['4k', '2160p', 'uhd']):
            return '4K'
        elif any(keyword in title_lower for keyword in ['1080p', 'fhd']):
            return '1080p'
        elif any(keyword in title_lower for keyword in ['720p', 'hd']):
            return '720p'
        elif any(keyword in title_lower for keyword in ['480p']):
            return '480p'
        elif any(keyword in title_lower for keyword in ['bluray', 'brrip', 'webrip']):
            return 'HD'
        else:
            return 'SD'
    
    def _get_magnet_link(self, detail_url, scraper):
        """Extract magnet link from torrent detail page"""
        try:
            response = scraper.get(detail_url, timeout=10)
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for magnet link
            magnet_link = soup.find("a", href=lambda x: x and x.startswith("magnet:"))
            if magnet_link:
                return magnet_link['href']
            
            # Alternative search patterns
            magnet_patterns = [
                'a[href^="magnet:"]',
                'a:contains("Magnet Download")',
                '.magnet-download a'
            ]
            
            for pattern in magnet_patterns:
                element = soup.select_one(pattern)
                if element and element.get('href'):
                    return element['href']
            
            return None
            
        except Exception as e:
            return None
    
    def launch_qbittorrent(self):
        """Launch qBittorrent application"""
        try:
            if os.path.exists(self.qbittorrent_path):
                subprocess.Popen(self.qbittorrent_path)
                return {
                    'success': True,
                    'message': 'qBittorrent launched successfully'
                }
            else:
                return {
                    'success': False,
                    'error': 'qBittorrent not found. Please install qBittorrent.'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def add_torrent_to_qbittorrent(self, magnet_link):
        """Add torrent to qBittorrent via magnet link"""
        try:
            # This would require qBittorrent Web API setup
            # For now, we'll just return the magnet link for manual addition
            return {
                'success': True,
                'magnet_link': magnet_link,
                'message': 'Use this magnet link in your torrent client'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_popular_torrents(self, category='movies'):
        """Get popular torrents by category"""
        try:
            base_url = "https://www.1337x.to"
            
            category_urls = {
                'movies': f"{base_url}/popular-movies",
                'tv': f"{base_url}/popular-tv",
                'games': f"{base_url}/popular-games",
                'music': f"{base_url}/popular-music",
                'apps': f"{base_url}/popular-applications"
            }
            
            url = category_urls.get(category, category_urls['movies'])
            
            scraper = cloudscraper.create_scraper()
            response = scraper.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            torrents = []
            rows = soup.select("table.table-list tbody tr")
            
            for row in rows[:15]:  # Limit to 15 popular items
                try:
                    title_cell = row.select_one("td.name a")
                    if not title_cell:
                        continue
                        
                    title = title_cell.text.strip()
                    detail_page = base_url + title_cell['href']
                    
                    size_cell = row.select_one("td.size")
                    size = size_cell.text.strip() if size_cell else "Unknown"
                    
                    seeders_cell = row.select_one("td.seeds")
                    seeders = int(seeders_cell.text.strip()) if seeders_cell and seeders_cell.text.strip().isdigit() else 0
                    
                    quality = self._determine_quality(title)
                    
                    torrents.append({
                        'title': title,
                        'size': size,
                        'seeders': seeders,
                        'quality': quality,
                        'detail_url': detail_page,
                        'category': category
                    })
                    
                except Exception as e:
                    continue
            
            return {
                'success': True,
                'results': torrents,
                'category': category,
                'count': len(torrents)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
