import os
import requests
import urllib.parse
from PIL import Image
from io import BytesIO

# The folder where we will save our beautiful scene images
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "assets", "images")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_scene_image(visual_description: str, scene_index: int, project_id: str = "latest_news") -> str:
    """
    Takes a visual description and uses Hugging Face's Free Inference API (Stable Diffusion)
    to generate an image. 
    """
    hf_token = os.getenv("HF_TOKEN")
    image_filename = f"{project_id}_scene_{scene_index}.jpg"
    image_path = os.path.join(OUTPUT_DIR, image_filename)
        
    if not hf_token:
        print(f"⚠️ Warning: HF_TOKEN not found in .env. Creating dummy fallback image for Scene {scene_index}.")
        # Create a simple vertical color gradient / block as a fallback so testing doesn't halt
        from PIL import Image, ImageDraw
        img = Image.new('RGB', (1080, 1920), color=(30, 30, scene_index * 40 + 50))
        d = ImageDraw.Draw(img)
        img.save(image_path)
        return image_path
        
    # We "clean up" the prompt to enforce a professional news style
    enhanced_prompt = f"{visual_description}. Professional news broadcast style, ultra-realistic, vivid colors, clean, 4k resolution, vertical orientation."
    
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    headers = {"Authorization": f"Bearer {hf_token}"}
    payload = {"inputs": enhanced_prompt}
    
    import time
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            print(f"🎨 Generating image for Scene {scene_index} (Attempt {attempt + 1}/{max_retries})...")
            response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                # Save the image cleanly in our folder structure
                image_filename = f"{project_id}_scene_{scene_index}.jpg"
                image_path = os.path.join(OUTPUT_DIR, image_filename)
                
                with open(image_path, 'wb') as f:
                    f.write(response.content)
                        
                print(f"✅ Saved Scene {scene_index} to {image_path}")
                return image_path
            
            elif response.status_code == 503:
                # The free HuggingFace API often puts models to sleep. A 503 just means it's booting up.
                print(f"⚠️ Hugging Face model is booting up (503). Waiting 15 seconds to try again...")
                time.sleep(15)
                continue
            
            else:
                print(f"❌ HF API Failed completely. Status Code: {response.status_code}. Error: {response.text}")
                break
                
        except Exception as e:
            print(f"❌ Network Error downloading image: {e}")
            break
            
    print(f"⚠️ Hugging Face API unavailable. Fetching high-quality realistic news photo for Scene {scene_index}...")
    # FALLBACK GENERATOR: Fetches a real 1080x1920 photography image to keep the video looking premium
    image_filename = f"{project_id}_scene_{scene_index}.jpg"
    image_path = os.path.join(OUTPUT_DIR, image_filename)
    
    try:
        # We append a random param so each scene gets a unique stock image from the news/corporate bucket
        import random
        r = requests.get(f"https://loremflickr.com/1080/1920/news,corporate?random={random.randint(1, 1000)}", headers={'User-Agent': 'Mozilla/5.0'})
        if r.status_code == 200:
            with open(image_path, 'wb') as f:
                f.write(r.content)
            print(f"✅ Fetched realistic photo placeholder for Scene {scene_index}")
            return image_path
    except Exception as fetch_err:
        print(f"❌ Photo fetch failed: {fetch_err}")
        
    print("⚠️ Failsafe active: Reverting to color block.")
    from PIL import Image, ImageDraw
    img = Image.new('RGB', (1080, 1920), color=(30, 30, scene_index * 40 + 50))
    d = ImageDraw.Draw(img)
    img.save(image_path)
    return image_path

def generate_all_storyboard_images(storyboard_json: dict, project_id: str = "latest_news"):
    """
    Takes the full JSON storyboard output from Phase 2, and generates all 5 images.
    Returns a list of the saved image file paths.
    """
    scenes = storyboard_json.get("scenes", [])
    image_paths = []
    
    print(f"\n🚀 Starting Image Generation for {len(scenes)} scenes...")
    
    for i, scene in enumerate(scenes):
        scene_num = i + 1
        visual_desc = scene.get("visual_description", "A news room background.")
        
        # Generate and save the image
        saved_path = generate_scene_image(visual_desc, scene_num, project_id)
        if saved_path:
            image_paths.append(saved_path)
            
    return image_paths

# Simple runner for instant testing right from the terminal
if __name__ == "__main__":
    # Fake Phase 2 Storyboard Output for testing Phase 3 independently
    test_storyboard = {
      "scenes": [
        {
          "scene_title": "Market High",
          "narration_text": "The stock market just hit an all-time high!",
          "visual_description": "A glowing green upward trend line over an abstract stock market board.",
          "on_screen_text": "Sensex Hits Record High! 🚀"
        },
        {
          "scene_title": "Global Rally",
          "narration_text": "This tracked a huge global market rally happening worldwide.",
          "visual_description": "A stylized spinning 3D earth with glowing connecting lines.",
          "on_screen_text": "Global Market Rally 🌍"
        }
      ]
    }
    
    print("\n🖼️ Testing Visuals Module independently...")
    generated_files = generate_all_storyboard_images(test_storyboard, project_id="test_run")
    
    print("\n✨ Done! Generated these files:")
    for file in generated_files:
        print(f"- {file}")
