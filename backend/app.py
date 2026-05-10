from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv
from faster_whisper import WhisperModel
import yt_dlp
import os
import uuid

# Load environment variables
load_dotenv()

# FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Groq client
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# Whisper model
whisper_model = WhisperModel("base")

# Request model
class VideoRequest(BaseModel):
    url: str

# Home route
@app.get("/")
def home():

    return {
        "message": "AI YouTube Summarizer API Running"
    }

# Summarize route
@app.post("/summarize")
def summarize_video(data: VideoRequest):

    audio_file = None

    try:

        # Generate unique filename
        filename = str(uuid.uuid4())

        # yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'noplaylist': True,
            'extractaudio': True,
            'audioformat': 'mp3',
            'outtmpl': f'{filename}.%(ext)s',
            'cookiefile': None,
            'nocheckcertificate': True,
            'ignoreerrors': True,
            'no_warnings': True,
        }

        # Download YouTube audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([data.url])

        # Find downloaded audio file
        for file in os.listdir():
            if file.startswith(filename):
                audio_file = file
                break

        if not audio_file:

            return {
                "error": "Failed to download video audio. Try another public YouTube video."
            }

        # Transcribe audio
        segments, info = whisper_model.transcribe(audio_file)

        transcript = ""

        for segment in segments:
            transcript += segment.text + " "

        # Limit transcript size
        transcript = transcript[:4000]

        # AI prompt
        prompt = f"""
        Summarize this YouTube video transcript.

        Provide:
        1. Short Summary
        2. Key Points
        3. Important Insights

        Transcript:
        {transcript}
        """

        # Generate AI summary
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        summary = response.choices[0].message.content

        # Cleanup downloaded audio
        if audio_file and os.path.exists(audio_file):
            os.remove(audio_file)

        return {
            "summary": summary
        }

    except Exception as e:

        # Cleanup if file exists
        if audio_file and os.path.exists(audio_file):
            os.remove(audio_file)

        error_message = str(e)

        # Friendly YouTube blocking message
        if "Sign in to confirm you're not a bot" in error_message:

            return {
                "error": "YouTube blocked this video for cloud access. Please try another public YouTube video."
            }

        # Generic error
        return {
            "error": "Something went wrong while processing the video."
        }