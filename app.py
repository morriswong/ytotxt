from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory, jsonify
import yttotxt
import logging
from pathlib import Path
import os

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

@app.route('/transcribe', methods=['POST'])
def transcribe():
    youtube_url = request.form.get('url')
    if youtube_url:
        try:
            # Start the transcription process
            video_id = youtube_url.split("v=")[-1]
            
            # Get video info first
            video_info = yttotxt.get_video_info(youtube_url)
            video_title = video_info['title']
            
            def update_status(status, title):
                session['status'] = status
                session['video_title'] = title
                
            # Store initial state in session
            session['status'] = 'info'
            session['video_title'] = video_title
            session['youtube_url'] = youtube_url
            session['video_id'] = video_id
            
            # Download and transcribe
            transcript = yttotxt.transcribe_youtube(youtube_url, update_status)
            
            # Store final result
            session['transcript'] = transcript
            
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
    return jsonify({
        'status': session.get('status', 'idle'),
        'video_title': session.get('video_title', ''),
        'youtube_url': session.get('youtube_url', '')
    })

if __name__ == '__main__':
    # Ensure downloads directory exists
    Path('downloads').mkdir(exist_ok=True)
    app.run(debug=True) 