import re
import yt_dlp
import whisper
from pathlib import Path
import time

def get_video_info(url):
    """Get video information without downloading"""
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
    
    # Extract clean video ID
    if 'youtu.be' in url:
        video_id = url.split('youtu.be/')[-1].split('?')[0]
    else:
        video_id = url.split('v=')[-1].split('&')[0]
        
    return {
        'title': info_dict['title'],
        'id': video_id
    }

def transcribe_youtube(url, update_status=None):
    try:
        # Get video info
        info_dict = get_video_info(url)
        video_title = info_dict['title']
        video_id = info_dict['id']
        
        # Create directory
        downloads_dir = Path('downloads')
        video_dir = downloads_dir / video_id
        video_dir.mkdir(parents=True, exist_ok=True)
        
        # Start downloading
        if update_status:
            update_status('downloading', video_title)
            
        # Download audio
        ydl_opts = {
            'format': 'm4a/bestaudio/best',
            'noplaylist': True,
            'continue_dl': True,
            'outtmpl': str(video_dir / video_id),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'geobypass': True,
            'keepvideo': False
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(url)
        
        # Start transcribing
        if update_status:
            update_status('transcribing', video_title)
            
        # Transcribe audio
        mp3_path = video_dir / f"{video_id}.mp3"
        model = whisper.load_model("base")
        result = model.transcribe(str(mp3_path))
        
        # Format and save transcript
        transcript_text = '\n'.join([
            f"[{result['segments'][i]['start']} ---> {result['segments'][i]['end']}]  {result['segments'][i]['text']}"
            for i in range(len(result['segments']))
        ])
        
        transcript_with_metadata = f"Title: {video_title}\nURL: {url}\n\nTranscript:\n{transcript_text}"
        
        txt_path = video_dir / f"{video_id}.txt"
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(transcript_with_metadata)
        
        return transcript_with_metadata
        
    except Exception as e:
        if update_status:
            update_status('error', str(e))
        raise e

# If needed, you can uncomment the following lines to run stand-alone:
# if __name__ == "__main__":
#     test_url = "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
#     print(transcribe_youtube(test_url))