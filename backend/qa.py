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

def answer_question(user_question: str, article_text: str = "") -> dict:
    """
    RAG Pipeline: Uses the pasted article as primary context.
    Also fetches related articles from ChromaDB as supplementary context.
    """
    context_parts = []
    citation_titles = []

    # 1. PRIMARY CONTEXT: the article the user actually pasted/linked
    if article_text and len(article_text.strip()) > 50:
        # Truncate to 4000 chars to stay safe within token limits
        trimmed = article_text.strip()[:4000]
        context_parts.append(f"--- Source 1: Your Current Article ---\n{trimmed}")
        citation_titles.append("Your Current Article")

    # 2. SUPPLEMENTARY CONTEXT: ChromaDB related articles
    related_articles = search_articles(user_question, limit=2)
    for idx, article in enumerate(related_articles):
        src_num = len(context_parts) + 1
        context_parts.append(f"--- Source {src_num}: {article['title']} ({article['source']}) ---\n{article['content']}")
        citation_titles.append(article['title'])

    if not context_parts:
        return {
            "answer": "I couldn't find any relevant articles in the database to answer your question. Please paste an article first.",
            "citations": []
        }

    context_text = "\n\n".join(context_parts)

    prompt = f"""
    You are a strict, highly accurate research assistant for ET News Copilot.
    
    USER QUESTION: 
    {user_question}
    
    AVAILABLE CONTEXT (News Articles):
    {context_text}
    
    STRICT RULES:
    1. Answer the user's question using ONLY the facts in the Available Context above.
    2. Prioritise information from "Source 1: Your Current Article" whenever relevant.
    3. If the context does not contain the answer, say EXACTLY: "I cannot answer this based on the provided article." Do not guess.
    4. Keep your answer clear and concise (1-2 short paragraphs).
    5. Include inline citations like [Source 1] after each factual sentence.
    
    Format your output strictly as JSON:
    {{
        "answer": "Your detailed answer with [Source 1] citations...",
        "citations": {json.dumps(citation_titles)}
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
            temperature=0.0
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
