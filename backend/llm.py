import os
import json
from groq import Groq
from dotenv import load_dotenv

# Load API keys from the .env file
load_dotenv()

# Initialize the Groq client securely 
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Use Llama 3 inside Groq (Lightning fast, open-source model)
MODEL_NAME = "llama-3.3-70b-versatile"

def generate_briefing(article_text: str, persona: str = "investor") -> dict:
    """
    Takes raw article text and asks Groq to generate a 4-point smart briefing.
    """
    
    # 1. Our magical prompt that forces the AI to output short, structured beginner-friendly answers
    prompt = f"""
    You are an expert news analyst. Read the following article and provide a clear, simple briefing.
    
    ARTICLE TEXT:
    {article_text[:3000]}  # We limit the text length slightly just to be safe
    
    Answer these 4 questions. Keep each answer to exactly 1 or 2 short sentences max:
    1. What happened?
    2. Why does it matter to a {persona}?
    3. Who are the key players involved?
    4. What should we watch for next?
    
    Format your response EXACTLY as a JSON dictionary holding these exact keys:
    {{
        "what_happened": "...",
        "why_it_matters": "...",
        "who_involved": "...",
        "what_next": "..."
    }}
    """
    
    # 2. Sent the prompt to the AI
    try:
        response = groq_client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful API that returns strictly valid JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},  # This powerful feature FORCES the AI to give us JSON, not text paragraphs!
            temperature=0.3  # Low temperature means the AI acts more factual and less "creative"
        )
        
        # 3. We take the text response and convert it into a real Python dictionary
        result_text = response.choices[0].message.content
        return json.loads(result_text)
        
    except Exception as e:
        print(f"Error generating briefing: {e}")
        return {
            "what_happened": "Error connecting to AI.",
            "why_it_matters": "Ensure your GROQ_API_KEY is correct in the .env file.",
            "who_involved": "N/A",
            "what_next": "N/A"
        }

# Simple runner so you can test this straight from the terminal
if __name__ == "__main__":
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_groq_api_key_here":
        print("⚠️ Warning: You need to paste your real GROQ_API_KEY into the .env file first!")
    else:
        # A tiny fake article for an instant test
        test_article = "The BSE Sensex touched a new lifetime high on Wednesday, tracking a broader global market rally. Tech and banking stocks led the surge, buoyed by positive earnings reports and expectations of interest rate cuts by the US Federal Reserve."
        
        print(f"🧠 Asking Groq AI to generate a briefing...")
        briefing = generate_briefing(test_article, persona="investor")
        
        print("\n✨ Generated Briefing:")
        print(json.dumps(briefing, indent=2))
