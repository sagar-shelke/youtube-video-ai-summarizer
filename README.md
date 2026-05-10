# AI YouTube Video Summarizer

An AI-powered YouTube video summarizer built using React, FastAPI, Faster-Whisper, Groq LLMs, and modern cloud deployment platforms.

---

# Features

* AI-generated YouTube video summaries
* Faster-Whisper audio transcription
* Groq LLM summarization
* Modern React frontend
* FastAPI backend
* Responsive UI
* Error handling
* Free-tier deployment architecture
* Cloud-hosted backend and frontend

---

# Tech Stack

## Frontend

* React
* Tailwind CSS
* Vite

## Backend

* FastAPI
* Python
* Uvicorn

## AI

* Faster Whisper
* Groq API

## Deployment

* Render
* Vercel
* GitHub

---

# Architecture

```text
YouTube URL
     ↓
yt-dlp Audio Download
     ↓
Faster-Whisper Transcription
     ↓
Groq LLM Summary
     ↓
React Frontend
```

---

# Project Structure

```bash
youtube-video-ai-summarizer
│
├── backend
│   ├── app.py
│   ├── requirements.txt
│   ├── .env
│   └── venv
│
├── frontend
│   ├── src
│   ├── public
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

# Windows Local Setup

## Backend Setup

### 1. Open Backend Folder

```powershell
cd backend
```

### 2. Create Virtual Environment

```powershell
python -m venv venv
```

### 3. Activate Virtual Environment

```powershell
.\venv\Scripts\Activate.ps1
```

If blocked:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate again.

### 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 5. Create `.env`

Create `.env` inside backend folder:

```env
GROQ_API_KEY=your_groq_api_key
```

### 6. Start Backend

```powershell
python -m uvicorn app:app --reload
```

Backend runs on:

```text
http://127.0.0.1:8000
```

Swagger Docs:

```text
http://127.0.0.1:8000/docs
```

---

# Frontend Setup (Windows)

### 1. Open Frontend Folder

```powershell
cd frontend
```

### 2. Install Dependencies

```powershell
npm install
```

### 3. Start Frontend

```powershell
npm run dev
```

Frontend runs on:

```text
http://localhost:5173
```

---

# macOS Local Setup

## Backend Setup

### 1. Open Backend Folder

```bash
cd backend
```

### 2. Create Virtual Environment

```bash
python3.11 -m venv venv
```

### 3. Activate Virtual Environment

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Create `.env`

Create `.env` inside backend folder:

```env
GROQ_API_KEY=your_groq_api_key
```

### 6. Start Backend

```bash
python -m uvicorn app:app --reload
```

Backend runs on:

```text
http://127.0.0.1:8000
```

Swagger Docs:

```text
http://127.0.0.1:8000/docs
```

---

# Frontend Setup (macOS)

### 1. Open Frontend Folder

```bash
cd frontend
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Start Frontend

```bash
npm run dev
```

Frontend runs on:

```text
http://localhost:5173
```

---

# Test API

Open Swagger Docs:

```text
http://127.0.0.1:8000/docs
```

Test request:

```json
{
  "url": "https://www.youtube.com/watch?v=jNQXAC9IVRw"
}
```

---

# Deployment

## Frontend

* Vercel

## Backend

* Render

---

# Environment Variables

## Backend `.env`

```env
GROQ_API_KEY=your_groq_api_key
```

---

# Notes

* Some YouTube videos may fail due to YouTube anti-bot protection.
* Render free tier may sleep after inactivity.
* First request may take 20–60 seconds on free hosting.

---

# Future Improvements

* Timestamp summaries
* PDF export
* Chat with video
* Docker support
* AWS deployment
* Authentication
* Database integration

---

# Resume Project Description

Built a full-stack AI-powered YouTube video summarizer using React, FastAPI, Faster-Whisper, Groq LLM API, and cloud deployment platforms. Implemented audio transcription, AI summarization, REST APIs, responsive UI, and free-tier deployment architecture.

---

# Author

Sagar Shelke
