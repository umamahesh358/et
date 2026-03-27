import requests
import os
from dotenv import load_dotenv

load_dotenv()

# We expect the user to have SARVAM_API_KEY in their .env
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

def generate_sarvam_tts(text: str, language_code: str = "hi-IN"):
    """
    Sends text to Sarvam AI and returns the path to the generated audio file.
    """
    url = "https://api.sarvam.ai/text-to-speech"

    if not SARVAM_API_KEY:
        return {"error": "SARVAM_API_KEY not found in environment variables."}

    payload = {
        "inputs": [text],
        "target_language_code": language_code,
        "speaker": "meera",
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
            # We save the output in a temporary file in the backend folder
            output_filename = "output.wav"
            output_path = os.path.join(os.path.dirname(__file__), output_filename)
            
            with open(output_path, "wb") as f:
                f.write(response.content)
            
            return output_path
        else:
            print(f"Sarvam API Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error calling Sarvam API: {e}")
        return None
