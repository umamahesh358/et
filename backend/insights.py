import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Using our reliable fast model
MODEL_NAME = "llama-3.3-70b-versatile"

DATA_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "articles.json")

def generate_insights() -> dict:
    """
    Reads the mock articles and asks the AI to find macroscopic themes across all of them.
    This demonstrates basic 'trend analysis' for the hackathon.
    """
    # 1. Load a few diverse articles to analyze 
    # (We limit it to a mix of 5 articles to save API tokens and keep it fast)
    try:
        with open(DATA_FILE_PATH, "r", encoding="utf-8") as f:
            all_articles = json.load(f)
            # Pick a spread of articles to ensure diversity in topics
            articles = all_articles[:2] + all_articles[-3:]
    except Exception:
        return {"error": "Could not load articles"}
        
    # Build text block
    articles_text = ""
    for a in articles:
        articles_text += f"\nTitle: {a['title']}\nContent: {a['content']}\n"
    
    # 2, 3, & 4. Prompt to extract repeated themes and a single "why it matters"
    prompt = f"""
    You are a big-data analyst. Read these {len(articles)} short news articles and find the hidden connections.
    
    ARTICLES:
    {articles_text}
    
    Format EXACTLY as JSON with these keys:
    {{
        "trending_topics": ["One or two word topic 1", "Topic 2", "Topic 3"],
        "why_it_matters": "One very simple, beginner-friendly sentence explaining the massive overall trend reshaping these industries."
    }}
    """
    
    try:
        response = groq_client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You politely output strictly valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Error generating insights: {e}")
        return {
            "trending_topics": ["Error loading topics"],
            "why_it_matters": "An error occurred connecting to the AI."
        }
