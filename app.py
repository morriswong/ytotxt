from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory, jsonify
import yttotxt
import logging
from pathlib import Path
import os
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure random key
logging.basicConfig(level=logging.DEBUG)

def get_transcribed_files():
    """Get list of all transcribed files with their metadata"""
    downloads_dir = Path('downloads')
    if not downloads_dir.exists():
        return []
    
    files = []
    for video_dir in downloads_dir.iterdir():
        if video_dir.is_dir():
            txt_file = video_dir / f"{video_dir.name}.txt"
            if txt_file.exists():
                with open(txt_file, 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                    title = first_line.replace('Title: ', '') if first_line.startswith('Title: ') else video_dir.name
                files.append({
                    'id': video_dir.name,
                    'title': title,
                    'path': str(txt_file.relative_to(downloads_dir))
                })
    return sorted(files, key=lambda x: x['title'])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        youtube_url = request.form.get('url')
        app.logger.debug(f"Received URL: {youtube_url}")
        if youtube_url:
            try:
                video_id = youtube_url.split("v=")[-1]
                transcript = yttotxt.transcribe_youtube(youtube_url)
                session['transcript'] = transcript
                session['youtube_url'] = youtube_url
                session['video_id'] = video_id
                return redirect(url_for('show_result'))
            except Exception as e:
                app.logger.error(f"Error processing video: {str(e)}")
                flash(f'Error processing video: {str(e)}')
                return redirect(url_for('index'))
    return render_template('index.html', transcribed_files=get_transcribed_files())

@app.route('/result')
def show_result():
    transcript = session.get('transcript')
    youtube_url = session.get('youtube_url')
    video_id = session.get('video_id')
    
    if not all([transcript, youtube_url, video_id]):
        return redirect(url_for('index'))
    
    return render_template('result.html', 
                         transcript=transcript, 
                         youtube_url=youtube_url,
                         transcribed_files=get_transcribed_files())

@app.route('/new', methods=['POST'])
def new_transcription():
    youtube_url = request.form.get('new_url')
    app.logger.debug(f"New URL received: {youtube_url}")
    if youtube_url:
        try:
            video_id = youtube_url.split("v=")[-1]
            transcript = yttotxt.transcribe_youtube(youtube_url)
            session['transcript'] = transcript
            session['youtube_url'] = youtube_url
            session['video_id'] = video_id
            return redirect(url_for('show_result'))
        except Exception as e:
            app.logger.error(f"Error processing new video: {str(e)}")
            flash(f'Error processing video: {str(e)}')
    return redirect(url_for('index'))

@app.route('/clear')
def clear_session():
    session.clear()
    return redirect(url_for('index'))

@app.route('/downloads/<path:filename>')
def download_file(filename):
    return send_from_directory('downloads', filename)

def extract_video_id(url):
    """Extract video ID from various YouTube URL formats"""
    if 'youtu.be' in url:
        # Handle shortened URLs like https://youtu.be/VIDEO_ID
        video_id = url.split('youtu.be/')[-1].split('?')[0]
    else:
        # Handle standard URLs like https://www.youtube.com/watch?v=VIDEO_ID
        video_id = url.split('v=')[-1].split('&')[0]
    return video_id

def is_valid_youtube_url(url):
    """Validate YouTube URL format"""
    youtube_regex = (
        r'(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[a-zA-Z0-9_-]{11}.*'
    )
    return bool(re.match(youtube_regex, url))

@app.route('/transcribe', methods=['POST'])
def transcribe():
    youtube_url = request.form.get('url')
    if not youtube_url:
        return jsonify({
            'status': 'error',
            'message': 'Please enter a YouTube URL'
        }), 400
        
    if not is_valid_youtube_url(youtube_url):
        return jsonify({
            'status': 'error',
            'message': 'Please enter a valid YouTube URL'
        }), 400
        
    try:
        # Get video info first
        video_id = extract_video_id(youtube_url)
        video_info = yttotxt.get_video_info(youtube_url)
        video_title = video_info['title']
        
        # Store info in session
        session['video_id'] = video_id
        session['video_title'] = video_title
        session['youtube_url'] = youtube_url
        session.modified = True
        
        # Process the video
        transcript = yttotxt.transcribe_youtube(youtube_url, None)  # No need for status updates now
        
        # Store final result
        session['transcript'] = transcript
        session.modified = True
        
        return jsonify({
            'status': 'success',
            'redirect': url_for('show_result')
        })
        
    except Exception as e:
        app.logger.error(f"Error processing video: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400
    
    return jsonify({'status': 'error', 'message': 'No URL provided'}), 400

@app.route('/status')
def get_status():
    status = session.get('status', 'idle')
    app.logger.debug(f"Current status: {status}")
    return jsonify({
        'status': status,
        'video_title': session.get('video_title', ''),
        'video_id': session.get('video_id', ''),
        'youtube_url': session.get('youtube_url', '')
    })

@app.route('/delete-all')
def delete_all_transcripts():
    try:
        downloads_dir = Path('downloads')
        if downloads_dir.exists():
            # Delete all contents of downloads directory
            for item in downloads_dir.iterdir():
                if item.is_dir():
                    for subitem in item.iterdir():
                        subitem.unlink()  # Delete files inside subdirectories
                    item.rmdir()  # Delete empty directory
        # Recreate downloads directory
        downloads_dir.mkdir(exist_ok=True)
    except Exception as e:
        flash(f'Error deleting transcripts: {str(e)}')
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Ensure downloads directory exists
    Path('downloads').mkdir(exist_ok=True)
    app.run(debug=True) 