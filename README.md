# YouTube Transcription Tool

A Flask web application that automatically transcribes YouTube videos to text using OpenAI's Whisper model. The tool provides real-time progress tracking, timestamps in transcriptions, and a clean interface for managing transcripts.

## Features

- 🎥 Transcribe YouTube videos using just the URL
- 🔄 Real-time progress tracking with status updates
- ⏱️ Timestamps included in transcriptions
- 💾 Automatic saving and organization of transcripts
- 📥 Easy download of transcription files
- 📚 Sidebar history of all transcribed videos
- 🎯 Clean, intuitive web interface
- 🔍 Video title and URL metadata in transcripts

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- FFmpeg (required for audio processing)
- Git (for cloning the repository)

## Installation

1. **Install FFmpeg**:
   - **Ubuntu/Debian**:
     ```bash
     sudo apt update
     sudo apt install ffmpeg
     ```
   - **macOS** (using Homebrew):
     ```bash
     brew install ffmpeg
     ```
   - **Windows**: Download from [FFmpeg website](https://ffmpeg.org/download.html)

2. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd youtube-transcription-tool
   ```

3. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

4. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Start the application**:
   ```bash
   python app.py
   ```

2. **Access the web interface**:
   - Open your browser and go to `http://localhost:5000`
   - You'll see the main transcription interface

3. **Transcribe a video**:
   - Paste a YouTube URL into the input field
   - Click "Transcribe"
   - Watch the real-time progress:
     1. Getting video information
     2. Downloading audio
     3. Generating transcript

4. **View and Download**:
   - View the transcript directly on the results page
   - Download the transcript as a text file
   - Start a new transcription or return to the main page

## Project Structure
