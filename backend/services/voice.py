import requests
import os
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

def generate_voice_summary(text: str, language_code: str = "hi-IN") -> str:
    """
    Takes a news summary and language code, sends it to Sarvam TTS, 
    and returns the path to the saved audio file.
    """
    if not SARVAM_API_KEY:
        print("❌ Error: SARVAM_API_KEY is missing from .env file!")
        return None

    print(f"🎙️ Generating {language_code} audio for text: '{text[:30]}...'")

    url = "https://api.sarvam.ai/text-to-speech"
    
    payload = {
        "inputs": [text],
        "target_language_code": language_code,
        "speaker": "anushka", # Updated to a valid professional speaker
        "pitch": 0,
        "pace": 1.0,
        "loudness": 1.0,
        "speech_sample_rate": 22050,
        "enable_preprocessing": True
    }

    headers = {
        "api-subscription-key": SARVAM_API_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            # We save the file in the same directory as this script
            output_path = os.path.join(os.path.dirname(__file__), "test_audio.wav")
            
            with open(output_path, "wb") as f:
                f.write(response.content)
            
            print(f"✅ Success! Audio saved to: {output_path}")
            return output_path
        else:
            print(f"❌ Sarvam API Error {response.status_code}: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Connection Error sending to Sarvam: {e}")
        return None

# --- Simple Local Test Block ---
# If you run this file directly, it will test the function.
if __name__ == "__main__":
    sample_text = "The stock market went up today, driving huge profits for technology companies."
    # Let's test English first
    result = generate_voice_summary(sample_text, "en-IN")
    if result:
        print("Testing complete. Check the audio file!")
