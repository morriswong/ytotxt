import re
import yt_dlp
import whisper
from pathlib import Path

def get_video_info(url):
    """Get video information without downloading"""
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
    return {
        'title': info_dict['title'],
        'id': url.split("v=")[-1]
    }

def transcribe_youtube(url, update_status=None):
    try:
        # Get video information
        info_dict = get_video_info(url)
        video_title = info_dict['title']
        video_id = info_dict['id']
        
        if update_status:
            update_status('info', video_title)
        
        # Create directory for this video
        downloads_dir = Path('downloads')
        video_dir = downloads_dir / video_id
        video_dir.mkdir(parents=True, exist_ok=True)
        
        if update_status:
            update_status('downloading', video_title)
        
        # Setup download options
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
        
        # Download the audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download(url)
        
        if update_status:
            update_status('transcribing', video_title)
        
        # Transcribe audio using Whisper
        mp3_path = video_dir / f"{video_id}.mp3"
        model = whisper.load_model("base")
        result = model.transcribe(str(mp3_path), verbose=True, word_timestamps=True)
        
        # Format transcript with timestamps
        transcript_text = '\n'.join([
            f"[{result['segments'][i]['start']} ---> {result['segments'][i]['end']}]  {result['segments'][i]['text']}"
            for i in range(len(result['segments']))
        ])
        
        # Add video title and URL at the beginning of transcript
        transcript_with_metadata = f"Title: {video_title}\nURL: {url}\n\nTranscript:\n{transcript_text}"
        
        # Save the transcript to a text file
        txt_path = video_dir / f"{video_id}.txt"
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(transcript_with_metadata)
        
        if update_status:
            update_status('completed', video_title)
        
        return transcript_with_metadata
    except Exception as e:
        if update_status:
            update_status('error', str(e))
        raise e

# If needed, you can uncomment the following lines to run stand-alone:
# if __name__ == "__main__":
#     test_url = "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
#     print(transcribe_youtube(test_url))