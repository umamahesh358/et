import requests
import os
from dotenv import load_dotenv

load_dotenv()

# We expect the user to have SARVAM_API_KEY in their .env
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

def sarvam_translate(text: str, target_language_code: str) -> str:
    """
    Sends text to Sarvam AI Translate API, completely replacing Groq.
    """
    if target_language_code == "en-IN":
        return text
        
    if not SARVAM_API_KEY:
        print("Error: SARVAM_API_KEY not found in environment variables.")
        return text

    url = "https://api.sarvam.ai/translate"
    payload = {
        "input": text,
        "source_language_code": "en-IN",
        "target_language_code": target_language_code,
        "speaker_gender": "Female",
        "mode": "formal",
        "model": "sarvam-translate"
    }
    
    headers = {
        "api-subscription-key": SARVAM_API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            # Sarvam translate API response typically has a "translated_text" key
            return data.get("translated_text", text)
        else:
            print(f"Translation Error {response.status_code}: {response.text}")
            return text
    except Exception as e:
        print(f"Translation Exception: {e}")
        return text

def generate_sarvam_tts(text: str, language_code: str = "hi-IN"):
    """
    Sends text to Sarvam AI and returns the path to the generated audio file.
    """
    url = "https://api.sarvam.ai/text-to-speech"

    if not SARVAM_API_KEY:
        print("Error: SARVAM_API_KEY not found in environment variables.")
        return None

    # Payload for Sarvam AI TTS API
    # Valid speakers for bulbul:v2: anushka, abhilash, manisha, vidya, arya, karun, hitesh
    payload = {
        "inputs": [text],
        "target_language_code": language_code,
        "model": "bulbul:v2",
        "speaker": "anushka",  # Female voice, compatible with bulbul:v2
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
        print(f"🎙️ Calling Sarvam TTS: lang={language_code}, text_len={len(text)}, text='{text[:60]}...'")
        response = requests.post(url, json=payload, headers=headers)
        
        print(f"Sarvam TTS Status: {response.status_code}")
        print(f"Sarvam TTS Response: {response.text[:500]}")
        
        if response.status_code == 200:
            response_data = response.json()
            # Sarvam returns base64-encoded audio in "audios" list
            import base64
            audios = response_data.get("audios", [])
            if not audios:
                print("❌ Sarvam returned 200 but no audio data in response")
                return None
            
            audio_bytes = base64.b64decode(audios[0])
            output_path = os.path.join(os.path.dirname(__file__), "output.wav")
            with open(output_path, "wb") as f:
                f.write(audio_bytes)
            print(f"✅ Audio saved to: {output_path}")
            return output_path
        else:
            print(f"❌ Sarvam API Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error calling Sarvam API: {e}")
        return None
