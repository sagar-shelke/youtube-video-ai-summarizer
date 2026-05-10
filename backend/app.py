from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv
from faster_whisper import WhisperModel
import yt_dlp
import os
import uuid

# Load env
load_dotenv()

# FastAPI app
app = FastAPI()

# CORS
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

    try:

        # Unique filename
        filename = str(uuid.uuid4())

        # Download audio
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{filename}.%(ext)s',
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([data.url])

        # Find downloaded file
        audio_file = None

        for file in os.listdir():
            if file.startswith(filename):
                audio_file = file
                break

        if not audio_file:
            return {
                "error": "Audio download failed"
            }

        # Transcribe audio
        segments, info = whisper_model.transcribe(audio_file)

        transcript = ""

        for segment in segments:
            transcript += segment.text + " "

        # Limit transcript size
        transcript = transcript[:4000]

        # AI Prompt
        prompt = f'''
        Summarize this YouTube video transcript.

        Provide:
        1. Short Summary
        2. Key Points
        3. Important Insights

        Transcript:
        {transcript}
        '''

        # Groq summary
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

        # Cleanup audio file
        os.remove(audio_file)

        return {
            "summary": summary
        }

    except Exception as e:

        return {
            "error": str(e)
        }