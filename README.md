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
youtube-transcription-tool/
├── app.py # Flask application and route handlers
├── yttotxt.py # Core transcription and YouTube download logic
├── requirements.txt # Python package dependencies
├── templates/ # HTML templates
│ ├── index.html # Main page template
│ └── result.html # Results page template
└── downloads/ # Storage for downloaded files and transcripts


## How It Works

1. **Video Processing**:
   - Extracts video information using yt-dlp
   - Downloads only the audio stream for efficiency
   - Converts audio to required format using FFmpeg

2. **Transcription**:
   - Uses OpenAI's Whisper model for speech recognition
   - Processes audio in chunks for memory efficiency
   - Generates timestamps for each segment

3. **File Management**:
   - Creates unique directories for each video
   - Saves transcripts with metadata
   - Organizes downloads by video ID

## Dependencies

- **Flask**: Web framework for the application
- **yt-dlp**: Advanced YouTube video downloader
- **whisper**: OpenAI's speech recognition model
- **FFmpeg**: Audio processing library

## Development

To contribute to the project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Troubleshooting

Common issues and solutions:

- **FFmpeg not found**: Ensure FFmpeg is installed and in your system PATH
- **Memory errors**: Try using a smaller model in `yttotxt.py` (e.g., "tiny" or "base")
- **Download errors**: Check your internet connection and video availability

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) for the transcription model
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for YouTube video downloading
- [Flask](https://flask.palletsprojects.com/) for the web framework

## Support

If you encounter any issues or have questions:
1. Check the troubleshooting section
2. Open an issue on GitHub
3. Provide detailed information about your problem

---

Made with ❤️ for the open-source community