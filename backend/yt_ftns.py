import yt_dlp
import json

def get_avatar_url(handle_or_id: str) -> str:
    # Works with handles (e.g., "casey") or channel IDs (e.g., "UC...")
    return f"https://unavatar.io/youtube/{handle_or_id}"

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
                        "date": entry.get('upload_date'),  # still None in flat mode
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

print(search_yt('food'))