# core_engine.py - Media Extraction and Trimming Engine

import os
import re
import time
import random
from PyQt6.QtCore import QThread, pyqtSignal
import yt_dlp
import urllib.request

def parse_time_to_seconds(time_str):
    """Converts HH:MM:SS or MM:SS or SS string to total seconds (float)."""
    try:
        parts = time_str.strip().split(':')
        if len(parts) == 3: # HH:MM:SS
            return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
        elif len(parts) == 2: # MM:SS
            return float(parts[0]) * 60 + float(parts[1])
        else: # SS
            return float(parts[0])
    except (ValueError, IndexError):
        return 0.0

def format_seconds_to_hhmmss(seconds):
    """Converts seconds (int/float) to HH:MM:SS string."""
    try:
        seconds = int(float(seconds))
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f"{h:02d}:{m:02d}:{s:02d}"
    except (ValueError, TypeError):
        return "00:00:00"

def get_error_message(e):
    """Parses exceptions into user-friendly instructions."""
    error_msg = str(e)
    if "Sign in to confirm you’re not a bot" in error_msg:
        return "YouTube Bot Detection: Access denied. This can happen if the video is age-restricted or YouTube has flagged the current IP. Try a different video or wait a few minutes."
    if "cookie database" in error_msg.lower():
        return "Browser Lock Error: Please CLOSE your web browser (Chrome/Edge/Firefox) so the app can sync your session data."
    return error_msg

def get_standard_ydl_opts(project_root):
    """Returns a robust configuration for standalone distribution."""
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    ]
    
    opts = {
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'concurrent_fragment_downloads': 6,
        'buffersize': 1024 * 512,
        'ffmpeg_location': project_root,
        'user_agent': random.choice(user_agents),
        'source_address': '0.0.0.0',
    }
    
    return opts

class DownloadThread(QThread):
    progress_signal = pyqtSignal(dict)
    finished_signal = pyqtSignal(bool, str)

    def __init__(self, task_data):
        super().__init__()
        self.task_data = task_data
        self.url = task_data.get('url')
        self.save_path = task_data.get('save_path')
        self.title = task_data.get('title', 'video')
        self.category = task_data.get('category', 'Video with Sound')
        self.trim_enabled = task_data.get('trim_enabled', False)
        self.start_time = task_data.get('start_time', '00:00:00')
        self.end_time = task_data.get('end_time', '00:00:00')
        self.cookiefile = task_data.get('cookiefile', None)
        self.format_id = task_data.get('format_id')

    def sanitize_filename(self, title):
        return re.sub(r'[\\/*?:"<>|]', "", title)

    def run(self):
        try:
            project_root = os.path.dirname(os.path.abspath(__file__))
            os.environ["PATH"] = project_root + os.pathsep + os.environ["PATH"]

            base_name = self.sanitize_filename(self.title)
            final_name = base_name
            counter = 1
            existing_files = os.listdir(self.save_path)
            while any(f.startswith(final_name) for f in existing_files):
                final_name = f"{counter} - {base_name}"
                counter += 1
            output_template = os.path.join(self.save_path, f"{final_name}.%(ext)s")
            
            ydl_opts = get_standard_ydl_opts(project_root)
            
            if self.format_id:
                if "Audio Only" in self.category:
                    ydl_opts['format'] = self.format_id
                else:
                    ydl_opts['format'] = f"{self.format_id}+bestaudio/best"
            else:
                ydl_opts['format'] = self._get_format_string()

            ydl_opts.update({
                'outtmpl': output_template,
                'progress_hooks': [self._progress_hook],
            })
            if self.cookiefile:
                ydl_opts['cookiefile'] = self.cookiefile

            if "Audio Only" in self.category:
                ext = "mp3"
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': ext,
                    'preferredquality': '320',
                }]
                ydl_opts['merge_output_format'] = None

            if self.trim_enabled:
                start_val = parse_time_to_seconds(self.start_time)
                end_val = parse_time_to_seconds(self.end_time)
                if end_val > start_val:
                    duration = end_val - start_val
                    ydl_opts['external_downloader'] = 'ffmpeg'
                    ydl_opts['external_downloader_args'] = {
                        'ffmpeg_i': ['-ss', str(start_val), '-t', str(duration)]
                    }
                    ydl_opts['force_keyframes_at_cuts'] = True

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            
            self.finished_signal.emit(True, "Download completed successfully.")
        except Exception as e:
            self.finished_signal.emit(False, get_error_message(e))

    def _progress_hook(self, d):
        if d['status'] == 'downloading':
            p = d.get('_percent_str', '0%').replace('%','')
            try: percent = float(p)
            except: percent = 0.0
            status_data = {'percent': percent, 'speed': d.get('_speed_str', '0B/s'), 'eta': d.get('_eta_str', '00:00'), 'title': self.title}
            self.progress_signal.emit(status_data)

    def _get_format_string(self):
        mapping = {
            'Video with Sound': 'bestvideo+bestaudio/best',
            'Audio Only': 'bestaudio/best',
            'Video-Only (No Sound)': 'bestvideo/best',
        }
        return mapping.get(self.category, 'bestvideo+bestaudio/best')

class InfoFetcherThread(QThread):
    info_signal = pyqtSignal(dict)
    error_signal = pyqtSignal(str)

    def __init__(self, url, cookiefile=None):
        super().__init__()
        self.url = url
        self.cookiefile = cookiefile

    def run(self):
        try:
            project_root = os.path.dirname(os.path.abspath(__file__))
            ydl_opts = get_standard_ydl_opts(project_root)
            if self.cookiefile:
                ydl_opts['cookiefile'] = self.cookiefile
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=False)
                
                video_formats = []
                seen_heights = set()
                audio_formats = []
                seen_audio_keys = set()
                
                if 'formats' in info:
                    for f in info['formats']:
                        if f.get('vcodec') != 'none' and f.get('height'):
                            height = int(f.get('height'))
                            if height not in seen_heights:
                                video_formats.append({
                                    'format_id': f.get('format_id'),
                                    'height': height,
                                    'ext': f.get('ext'),
                                    'note': f.get('format_note') or f.get('resolution') or f"{height}p"
                                })
                                seen_heights.add(height)
                        elif f.get('vcodec') == 'none' and f.get('acodec') != 'none':
                            abr = f.get('abr') or 0
                            ext = f.get('ext')
                            key = f"{abr}_{ext}"
                            if key not in seen_audio_keys:
                                audio_formats.append({
                                    'format_id': f.get('format_id'),
                                    'abr': int(abr) if abr else 0,
                                    'ext': ext,
                                    'note': f.get('format_note') or f"{int(abr)}kbps" if abr else ext
                                })
                                seen_audio_keys.add(key)
                
                video_formats.sort(key=lambda x: x['height'], reverse=True)
                audio_formats.sort(key=lambda x: x['abr'], reverse=True)

                thumb_data = None
                thumb_url = info.get('thumbnail')
                if thumb_url:
                    try: thumb_data = urllib.request.urlopen(thumb_url).read()
                    except: pass
                data = {
                    'title': info.get('title', 'video'),
                    'thumbnail_data': thumb_data,
                    'duration': info.get('duration'),
                    'duration_str': format_seconds_to_hhmmss(info.get('duration', 0)),
                    'uploader': info.get('uploader'),
                    'video_formats': video_formats,
                    'audio_formats': audio_formats
                }
                self.info_signal.emit(data)
        except Exception as e:
            self.error_signal.emit(get_error_message(e))
