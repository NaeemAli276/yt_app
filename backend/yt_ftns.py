import yt_dlp
import json

def get_avatar_url(handle_or_id: str) -> str:
    # Works with handles (e.g., "casey") or channel IDs (e.g., "UC...")
    return f"https://unavatar.io/youtube/{handle_or_id}"

def get_audio_format_sizes(url):
    # Configure yt-dlp to only extract info without downloading
    ydl_opts = {
        'skip_download': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Extract metadata dictionary
        info = ydl.extract_info(url, download=False)
        
        # Formats list contains both video and audio streams
        formats = info.get('formats', [])
        
        print(f"Audio formats for: {info.get('title')}\n")
        print(f"{'Format ID':<10} {'Extension':<10} {'Bitrate':<10} {'Estimated Size':<15}")
        print("-" * 50)
        
        for fmt in formats:
            # vcodec='none' filters for audio-only streams
            if fmt.get('vcodec') == 'none':
                format_id = fmt.get('format_id')
                ext = fmt.get('ext')
                abr = fmt.get('abr')  # Audio Bitrate in kbps
                
                # Sizes can be exact ('filesize') or estimated ('filesize_approx')
                filesize = fmt.get('filesize') or fmt.get('filesize_approx')
                
                if filesize:
                    # Convert bytes to Megabytes (MB)
                    size_mb = f"{filesize / (1024 * 1024):.2f} MB"
                else:
                    size_mb = "Unknown"
                
                print(f"{format_id:<10} {ext:<10} {f'{abr}k':<10} {size_mb:<15}")
        info = ydl.extract_info(url, download=False)
        formats = info.get('formats', [])
        
        print(f"--- Audio Preview for: {info.get('title')} ---\n")
        
        for fmt in formats:
            # Check for audio-only formats
            if fmt.get('vcodec') == 'none' and fmt.get('acodec') != 'none':
                fmt_id = fmt.get('format_id')
                ext = fmt.get('ext')
                abr = fmt.get('abr')
                
                # Fetch exact or estimated size
                bytes_size = fmt.get('filesize') or fmt.get('filesize_approx')
                size_str = f"{bytes_size / (1024 * 1024):.2f} MB" if bytes_size else "Unknown"
                
                print(f"ID: {fmt_id:<5} | Format: {ext:<5} | Quality: {abr:>3.0f}kbps | Size: {size_str}")

        # Extract metadata dictionary
        info = ydl.extract_info(url, download=False)
        
        # Formats list contains both video and audio streams
        formats = info.get('formats', [])
        
        print(f"Audio formats for: {info.get('title')}\n")
        print(f"{'Format ID':<10} {'Extension':<10} {'Bitrate':<10} {'Estimated Size':<15}")
        print("-" * 50)
        
        for fmt in formats:
            # vcodec='none' filters for audio-only streams
            if fmt.get('vcodec') == 'none':
                format_id = fmt.get('format_id')
                ext = fmt.get('ext')
                abr = fmt.get('abr')  # Audio Bitrate in kbps
                
                # Sizes can be exact ('filesize') or estimated ('filesize_approx')
                filesize = fmt.get('filesize') or fmt.get('filesize_approx')
                
                if filesize:
                    # Convert bytes to Megabytes (MB)
                    size_mb = f"{filesize / (1024 * 1024):.2f} MB"
                else:
                    size_mb = "Unknown"
                
                return(f"{format_id:<10} {ext:<10} {f'{abr}k':<10} {size_mb:<15}")

def search_yt(query: str) -> str:
    max_results = 10

    if query == '':
        return json.dumps([])

    search_query = f"ytsearch{max_results}:{query}"

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
        # 'extract_flat': True, 
        'approximate_date': True
    }

    search_results = []

    with yt_dlp.YoutubeDL(params=ydl_opts) as ydl:
        raw_info = ydl.extract_info(search_query, download=False)

        if raw_info and 'entries' in raw_info:
            for entry in raw_info['entries']:
                if entry:
                    search_results.append({
                        "id": entry.get('id'),
                        "title": entry.get('title'),
                        "uploader_name": entry.get('uploader'),
                        "uploader_uri": get_avatar_url(entry.get('uploader_id')),
                        "duration": entry.get('duration'),  # seconds, not string
                        "url": entry.get('url') or f"https://www.youtube.com/watch?v={entry.get('id')}",
                        "views": entry.get('view_count'),
                        "thumbnail": f"https://i.ytimg.com/vi/{entry.get('id')}/hqdefault.jpg",
                        "date": entry.get('upload_date'),  # still None in flat mode,
                        # "audio_formats": get_audio_format_sizes(url=f"https://www.youtube.com/watch?v={entry.get('id')}")
                    })

    return json.dumps(search_results, indent=4)
    
def download_song_selected_song(url):

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '~/Music/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3'
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])