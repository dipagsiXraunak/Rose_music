import yt_dlp

YDL_AUDIO_OPTS = {'format': 'bestaudio/best', 'quiet': True, 'no_warnings': True}
YDL_VIDEO_OPTS = {'format': 'bestvideo+bestaudio/best', 'quiet': True, 'no_warnings': True}

def get_audio_url(query: str) -> tuple:
    with yt_dlp.YoutubeDL(YDL_AUDIO_OPTS) as ydl:
        try:
            info = ydl.extract_info(query, download=False)
            if 'entries' in info: info = info['entries'][0]
            return info['url'], info.get('title', 'Unknown')
        except Exception as e:
            print(f"Audio error: {e}")
            return None, None

def get_video_url(query: str) -> tuple:
    with yt_dlp.YoutubeDL(YDL_VIDEO_OPTS) as ydl:
        try:
            info = ydl.extract_info(query, download=False)
            if 'entries' in info: info = info['entries'][0]
            return info['url'], info.get('title', 'Unknown')
        except Exception as e:
            print(f"Video error: {e}")
            return None, None
