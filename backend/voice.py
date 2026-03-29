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
        "model": "sarvam-translate:v1"
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

def generate_sarvam_tts(text: str, language_code: str = "hi-IN", output_path: str = None):
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
        
        # print(f"Sarvam TTS Status: {response.status_code}") # Disabled debug spam
        
        if response.status_code == 200:
            response_data = response.json()
            import base64
            audios = response_data.get("audios", [])
            if not audios:
                print("❌ Sarvam returned 200 but no audio data")
                return None
            
            audio_bytes = base64.b64decode(audios[0])
            
            # Default to output.wav if no path provided
            if not output_path:
                output_path = os.path.join(os.path.dirname(__file__), "output.wav")
                
            # Ensure the directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, "wb") as f:
                f.write(audio_bytes)
            print(f"✅ Audio saved: {output_path}")
            return output_path
        else:
            print(f"❌ Sarvam API Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error calling Sarvam API: {e}")
        return None

def generate_storyboard_audio(storyboard_json: dict, language_code: str = "en-IN", project_id: str = "latest_news"):
    """
    Takes the JSON storyboard directly, translates the text if needed, and generates audio for each scene.
    Saves outputs tightly synchronized: scene_1_audio.wav, scene_2_audio.wav, etc.
    """
    scenes = storyboard_json.get("scenes", [])
    audio_paths = []
    
    print(f"\n🎧 Starting Audio Generation for {len(scenes)} scenes in {language_code}...")
    
    # Storage folder
    assets_dir = os.path.join(os.path.dirname(__file__), "assets", "audio")
    os.makedirs(assets_dir, exist_ok=True)
    
    for i, scene in enumerate(scenes):
        scene_num = i + 1
        original_text = scene.get("narration_text", "")
        
        # Translate the narration first
        script_to_speak = sarvam_translate(original_text, language_code)
        
        # Determine strict output path
        output_filename = f"{project_id}_scene_{scene_num}_audio.wav"
        output_path = os.path.join(assets_dir, output_filename)
        
        # Generate Audio
        saved_path = generate_sarvam_tts(script_to_speak, language_code, output_path=output_path)
        
        if saved_path:
            audio_paths.append(saved_path)
            
    return audio_paths

if __name__ == "__main__":
    test_storyboard = {
      "scenes": [
        {
          "scene_title": "Market High",
          "narration_text": "The stock market just hit an all-time high! It is a great day for investors.",
        },
        {
          "scene_title": "Global Rally",
          "narration_text": "This amazing surge was directly caused by the worldwide tech rally.",
        }
      ]
    }
    
    print("\n🎤 Testing Voice Module independently...")
    generated_audio = generate_storyboard_audio(test_storyboard, language_code="hi-IN", project_id="test_run")
    
    print("\n✨ Done! Generated these audio files:\n", generated_audio)
