# test_run.py
import sys
import os

from storyboard import generate_storyboard
from visuals import generate_all_storyboard_images
from voice import generate_storyboard_audio
from editor import assemble_video

def main():
    print("--- STARTING END-TO-END TEST ---")
    
    # 1. Take a sample article
    test_article = "The BSE Sensex touched a new lifetime high on Wednesday, tracking a broader global market rally. Tech and banking stocks led the surge, buoyed by positive earnings reports and expectations of interest rate cuts by the US Federal Reserve. Investors are optimistic about the upcoming quarter."
    
    # 2. Generate Storyboard
    print("\\n[1/4] Generating Storyboard...")
    storyboard = generate_storyboard(test_article)
    if not storyboard.get("scenes") or "Error" in storyboard.get("scenes")[0].get("scene_title", ""):
        print("FAIL: Storyboard Generation Failed!")
        print(storyboard)
        sys.exit(1)
        
    print("SUCCESS: Storyboard Created! Sequences:", len(storyboard["scenes"]))
    
    # 3. Generate Images
    print("\\n[2/4] Generating Images...")
    images = generate_all_storyboard_images(storyboard, project_id="e2e_test")
    if not images:
        print("FAIL: Image Generation Failed!")
        sys.exit(1)
        
    print("SUCCESS: Images Available:", len(images))
    
    # 4. Generate Voice Narration
    print("\\n[3/4] Generating Voice Narration...")
    audios = generate_storyboard_audio(storyboard, language_code="hi-IN", project_id="e2e_test")
    if not audios:
        print("FAIL: Voice Generation Failed!")
        sys.exit(1)
        
    print("SUCCESS: Audios Available:", len(audios))
    
    # 5. Assemble Video
    print("\\n[4/4] Assembling Video...")
    try:
        video_path = assemble_video(storyboard, images, audios, project_id="e2e_test")
        print(f"\\nSUCCESS! Video exported to: {video_path}")
    except Exception as e:
        print(f"FAIL: Assembly failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
