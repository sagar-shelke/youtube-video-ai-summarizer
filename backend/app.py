from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI
from mangum import Mangum
from dotenv import load_dotenv
import os
import re

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

# Request body model
class VideoRequest(BaseModel):
    url: str

# Extract YouTube video ID
def extract_video_id(url):

    regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"

    match = re.search(regex, url)

    if not match:
        return None

    return match.group(1)

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

        # Extract video ID
        video_id = extract_video_id(data.url)

        if not video_id:

            return {
                "error": "Invalid YouTube URL"
            }

        # Fetch transcript
        api = YouTubeTranscriptApi()

        try:
            transcript = api.fetch(video_id)

        except Exception:
            return {
                "error": "Transcript unavailable for this video. Try another YouTube video."
            }

        # Reduce transcript size for faster AI response
        text = " ".join([item.text for item in transcript[:50]])

        # AI Prompt
        prompt = f"""
        Summarize this YouTube video transcript.

        Provide:
        1. Short Summary
        2. Key Points
        3. Important Insights

        Transcript:
        {text}
        """

        # Groq AI response
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

        return {
            "summary": summary
        }

    except Exception as e:

        return {
            "error": str(e)
        }

# AWS Lambda handler
handler = Mangum(app)