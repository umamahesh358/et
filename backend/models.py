from pydantic import BaseModel
from typing import List

# These models tell FastAPI exactly what shape our data should take.
# It makes the API predictable and beginner-friendly to debug!

class Article(BaseModel):
    id: str
    title: str
    content: str
    source: str
    date: str
    tags: List[str]

class ArticlesResponse(BaseModel):
    articles: List[Article]
    total: int

# --- New Models for our AI Endpoints ---

class BriefingRequest(BaseModel):
    article_text: str
    persona: str = "investor"

class RelatedRequest(BaseModel):
    query: str
    limit: int = 5

class QARequest(BaseModel):
    question: str

class TTSRequest(BaseModel):
    text: str
    language_code: str = "hi-IN"
