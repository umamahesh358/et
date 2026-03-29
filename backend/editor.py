import os
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "assets", "video")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def create_text_overlay_image(base_image_path: str, text: str, output_path: str):
    """
    Takes an image, draws the on_screen_text onto it using pure Python (PIL),
    and saves it. This avoids complex ImageMagick installations on Windows!
    """
    try:
        # Open original image created by Phase 3
        img = Image.open(base_image_path).convert("RGBA")
        
        # Create a layer for drawing text and semi-transparent backgrounds
        txt_layer = Image.new("RGBA", img.size, (255, 255, 255, 0))
        d = ImageDraw.Draw(txt_layer)
        
        # Load font
        try:
            # Arial bold is preferred for readability
            font = ImageFont.truetype("arialbd.ttf", 60)
        except:
            try:
                font = ImageFont.truetype("arial.ttf", 60)
            except:
                font = ImageFont.load_default()
                
        width, height = img.size
        
        # Smart Text Wrapping logic
        import textwrap
        # Wrap at 30 chars for 1080p width at 60px font
        wrapped_text = textwrap.fill(text, width=32)
        
        # Calculate dynamic box height based on number of lines
        line_count = wrapped_text.count('\n') + 1
        text_height_est = line_count * 80 # Approx 80px per line
        box_top = height - text_height_est - 100 # 100px padding
        
        # Draw a very dark, high-contrast semi-transparent box
        d.rectangle([(0, box_top), (width, height)], fill=(0, 0, 0, 200)) # 200 is very dark but still 80% opacity
        
        # Draw the wrapped text in pure white
        d.multiline_text((50, box_top + 40), wrapped_text, fill=(255, 255, 255, 255), font=font, spacing=15)
        
        # Combine them safely
        out = Image.alpha_composite(img, txt_layer)
        out = out.convert("RGB")
        out.save(output_path)
        return output_path
    except Exception as e:
        print(f"⚠️ Text Overlay failed on {base_image_path}. Using original image. Error: {e}")
        return base_image_path

def assemble_video(storyboard_json: dict, image_paths: list, audio_paths: list, project_id: str = "latest_news"):
    """
    Combines images and audio using MoviePy into a final MP4 video.
    """
    scenes = storyboard_json.get("scenes", [])
    
    if not image_paths or not audio_paths or len(image_paths) != len(audio_paths):
        print("❌ Error: Mismatch between images and audio files. Cannot assemble video.")
        return None
        
    print(f"\n🎬 Assembling final video for {len(scenes)} scenes...")
    
    clips = []
    
    for i, scene in enumerate(scenes):
        scene_text = scene.get("on_screen_text", "")
        img_path = image_paths[i]
        audio_path = audio_paths[i]
        
        # 1. Overlay the text on the image
        img_with_text = os.path.join(os.path.dirname(img_path), f"text_overlay_scene_{i+1}.jpg")
        final_img = create_text_overlay_image(img_path, scene_text, img_with_text)
        
        # 2. Load the actual audio piece
        audio_clip = AudioFileClip(audio_path)
        duration = audio_clip.duration
        
        # 3. Create a video clip from the image, exactly matching the audio duration
        video_clip = ImageClip(final_img).set_duration(duration)
        video_clip = video_clip.set_audio(audio_clip)
        
        # Add simple fade-in transition between clips (except the first one)
        if i > 0:
            video_clip = video_clip.crossfadein(0.5)
            
        clips.append(video_clip)
        
    # Combine all clips together
    final_video = concatenate_videoclips(clips, method="compose")
    
    # Save video cleanly
    output_filename = f"{project_id}_final_video.mp4"
    final_path = os.path.join(OUTPUT_DIR, output_filename)
    
    # 24 fps is perfectly standard for TikTok/Reels size videos
    print(f"⏳ Rendering video to {final_path}...")
    final_video.write_videofile(final_path, fps=24)
    print(f"✅ Video created successfully: {final_path}")
    
    return final_path

if __name__ == "__main__":
    # Test execution module
    pass
