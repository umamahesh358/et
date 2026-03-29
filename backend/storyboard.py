import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Initialize the Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Using Llama 3 for fast, structured JSON generation
MODEL_NAME = "llama-3.3-70b-versatile"

def generate_storyboard(article_text: str) -> dict:
    """
    Takes a news article and converts it into a 5-scene storyboard using Groq.
    """
    
    prompt = f"""
    You are an expert video producer. Convert the following news article into a short, engaging 5-scene storyboard for a TikTok/Reels style explainer video.
    
    ARTICLE TEXT:
    {article_text[:3000]}
    
    CRITICAL RULES:
    1. There must be exactly 5 scenes.
    2. Keep each scene VERY short and simple.
    3. The narration text should be conversational and easy to read out loud.
    
    Format your response EXACTLY as a JSON dictionary with a single key "scenes" which contains a list of exactly 5 dictionaries. Each dictionary MUST have these exact keys:
    {{
        "scenes": [
            {{
                "scene_title": "Short title for the scene",
                "narration_text": "The script the AI voice will say out loud (2-3 sentences max).",
                "visual_description": "A simple description of what the background image should look like.",
                "on_screen_text": "A brief, punchy caption to show on the screen (5-7 words max)."
            }},
            ... (4 more scenes)
        ]
    }}
    """
    
    try:
        response = groq_client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful API that returns strictly valid JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},  # Force JSON output
            temperature=0.4  # Slightly higher for creative storyboarding, but still structured
        )
        
        result_text = response.choices[0].message.content
        return json.loads(result_text)
        
    except Exception as e:
        print(f"Error generating storyboard: {e}")
        return {
            "scenes": [
                {
                    "scene_title": "Error",
                    "narration_text": f"Error connecting to AI: {e}",
                    "visual_description": "Blank screen",
                    "on_screen_text": "Error generating storyboard"
                }
            ]
        }

if __name__ == "__main__":
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_groq_api_key_here":
        print("⚠️ Warning: Please set your GROQ_API_KEY in the .env file!")
    else:
        test_article = "The BSE Sensex touched a new lifetime high on Wednesday, tracking a broader global market rally. Tech and banking stocks led the surge, buoyed by positive earnings reports and expectations of interest rate cuts by the US Federal Reserve. Investors are optimistic about the upcoming quarter."
        
        print("Asking Groq AI to generate a 5-scene storyboard...\n")
        storyboard = generate_storyboard(test_article)
        
        print("Generated Storyboard JSON:")
        print(json.dumps(storyboard, indent=2))
