import os
import json
from groq import Groq
from dotenv import load_dotenv

# We import our search function from Phase 4 so we can fetch related articles!
from vector_db import search_articles

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Using our reliable fast model
MODEL_NAME = "llama-3.3-70b-versatile"

def answer_question(user_question: str) -> dict:
    """
    RAG Pipeline: Retrieves related articles first, then asks the AI to answer using ONLY those articles.
    """
    # 1. & 2. Search related articles first (Retrieval)
    # We fetch the top 3 most relevant articles to build our "context"
    related_articles = search_articles(user_question, limit=3)
    
    if not related_articles:
        return {
            "answer": "I couldn't find any relevant articles in the database to answer your question.",
            "citations": []
        }
        
    # Build the context block for the AI to read
    context_text = ""
    for idx, article in enumerate(related_articles):
        # We number them so the AI can easily cite them by Source Number
        context_text += f"\n--- Source {idx + 1}: {article['title']} ({article['source']}) ---\n{article['content']}\n"
    
    # 3, 4, & 5. Prompt the AI with strict hallucination-prevention rules
    prompt = f"""
    You are a strict, highly accurate research assistant for ET News Copilot.
    
    USER QUESTION: 
    {user_question}
    
    AVAILABLE CONTEXT (News Articles):
    {context_text}
    
    STRICT RULES:
    1. Answer the user's question using ONLY the facts provided in the Available Context above.
    2. If the context does not contain the answer, say EXACTLY: "I cannot answer this based on the provided articles." Do not guess or make things up.
    3. Keep your answer clear and concise (1-2 short paragraphs).
    4. At the end of every factual sentence you write, include a citation in brackets like [Source 1] based on where you found the fact.
    
    Format your output strictly as JSON with this structure:
    {{
        "answer": "Your detailed answer goes here with [Source 1] citations...",
        "citations": ["Title of Source 1", "Title of Source 2"]
    }}
    """
    
    try:
        response = groq_client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a factual API that strictly outputs valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.0  # Temperature 0.0 means ZERO creativity. It will only copy facts exactly.
        )
        
        result_text = response.choices[0].message.content
        return json.loads(result_text)
        
    except Exception as e:
        print(f"Error answering question: {e}")
        return {
            "answer": "An error occurred while connecting to the AI.",
            "citations": []
        }

if __name__ == "__main__":
    if not os.getenv("GROQ_API_KEY") or os.getenv("GROQ_API_KEY") == "your_groq_api_key_here":
        print("⚠️ Warning: Please add your real GROQ_API_KEY to the .env file first!")
    else:
        # We ask a specific question that we know exists in our Mock Data
        test_q = "How much did electric vehicle sales grow in Q1?"
        print(f"🧠 User asked: '{test_q}'")
        print("🔍 Searching for context and generating answer...\n")
        
        result = answer_question(test_q)
        print("✨ Final RAG Answer:")
        print(json.dumps(result, indent=2))
