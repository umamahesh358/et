from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from models import ArticlesResponse, BriefingRequest, RelatedRequest, QARequest, TTSRequest

# Import our AI functions built in Phases 4, 5, 6, 9, and 11
from llm import generate_briefing
from vector_db import search_articles
from qa import answer_question
from insights import generate_insights
from voice import generate_sarvam_tts

# 1. Create the FastAPI app
app = FastAPI(title="ET News Copilot API", description="Backend for the AI-native news experience.")

# 2. Add CORS so our Streamlit frontend can talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow any frontend to connect (useful for local dev)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Helper to find the sample data safely
DATA_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "articles.json")

# 3. Add a simple health check endpoint
@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "ET News Copilot Backend is running properly!"}

# 4. Add an endpoint to return our sample articles we created in Phase 2
@app.get("/api/articles", response_model=ArticlesResponse, tags=["Articles"])
def get_articles():
    try:
        with open(DATA_FILE_PATH, "r", encoding="utf-8") as file:
            articles = json.load(file)
            return {"articles": articles, "total": len(articles)}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Articles data file not found. Have you completed Phase 2?")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Articles data file contains invalid JSON.")

# 5. Briefing Endpoint (Phase 5)
@app.post("/api/briefing", tags=["AI Copilot"])
def api_get_briefing(req: BriefingRequest):
    # This calls our Groq LLM function from llm.py
    return generate_briefing(req.article_text, persona=req.persona)

# 6. Related Articles Endpoint (Phase 4)
@app.post("/api/related", tags=["AI Copilot"])
def api_get_related(req: RelatedRequest):
    # This calls our ChromaDB search from vector_db.py
    results = search_articles(req.query, limit=req.limit)
    return {"related_articles": results}

# 7. Q&A Endpoint (Phase 6)
@app.post("/api/qa", tags=["AI Copilot"])
def api_answer_question(req: QARequest):
    # This calls our RAG system from qa.py
    return answer_question(req.question)

# 8. Global Insights Endpoint (Phase 9)
@app.get("/api/insights", tags=["AI Copilot"])
def api_get_insights():
    # This analyzes all articles for macro trends
    return generate_insights()

# 9. Voice Summary Endpoint (Voice Phase 3)
@app.post("/api/tts", tags=["AI Copilot"])
def api_get_voice_summary(req: TTSRequest):
    
    # Step 1: Translate the summary for a natural spoken version using Sarvam
    from voice import sarvam_translate
    native_text = sarvam_translate(req.text, req.language_code)
    
    # Step 2: Generate the audio
    audio_path = generate_sarvam_tts(native_text, req.language_code)
    
    if audio_path and os.path.exists(audio_path):
        return FileResponse(audio_path, media_type="audio/wav", filename="news_summary.wav")
    else:
        raise HTTPException(status_code=500, detail="Failed to generate audio summary.")



