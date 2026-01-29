import yt_dlp
import os

def get_video_info(url):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
        'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
        'source_address': '0.0.0.0', # Force IPv4
        'proxy': os.getenv('PROXY'),
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return info
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"Error fetching video info: {e}")
            return None

def download_video(url, format_id, output_path='downloads'):
    os.makedirs(output_path, exist_ok=True)
    
    ydl_opts = {
        'format': format_id,
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
        'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
        'source_address': '0.0.0.0', # Force IPv4
        'proxy': os.getenv('PROXY'),
    }
    
    if format_id == 'audio':
         ydl_opts['format'] = 'bestaudio/best'
         ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
         ydl_opts['outtmpl'] = f'{output_path}/%(title)s.%(ext)s'

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if format_id == 'audio':
                 # calculate the expected filename after post-processing
                 base, _ = os.path.splitext(filename)
                 filename = f"{base}.mp3"
            return filename
        except Exception as e:
            print(f"Error downloading video: {e}")
            return None
