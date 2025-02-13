import yt_dlp
import os
import subprocess

# Configuration
MAX_VIDEO_DURATION_MINUTES = 90

output_folder = "video_current"
os.makedirs(output_folder, exist_ok=True)

url = "https://www.youtube.com/watch?v=zjkBMFhNj_g"

def get_video_info(url):
    """Get video information without downloading."""
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            duration_minutes = info.get('duration', 0) / 60  # Convert seconds to minutes
            title = info.get('title', 'Unknown Title')
            return duration_minutes, title
        except Exception as e:
            print(f"Error getting video info: {str(e)}")
            return None, None

def main():
    # Check video duration first
    duration_minutes, title = get_video_info(url)
    
    if duration_minutes is None:
        print("Could not get video information. Please check the URL.")
        return
    
    if duration_minutes > MAX_VIDEO_DURATION_MINUTES:
        print(f"\nVideo '{title}' is too long!")
        print(f"Duration: {duration_minutes:.1f} minutes")
        print(f"Maximum allowed: {MAX_VIDEO_DURATION_MINUTES} minutes")
        return

    print(f"\nVideo '{title}' duration: {duration_minutes:.1f} minutes")
    print("Duration check passed, proceeding with download...")

    # Set download options
    ydl_opts = {
        "format": "bv*[height<=720]+ba/b[height<=720]",
        "merge_output_format": "mp4",
        "outtmpl": os.path.join(output_folder, "%(title)s.%(ext)s"),
    }

    # Download the video
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.download([url])

    # If download was successful, launch transcription
    if result == 0:
        print("\nLaunching transcription...")
        subprocess.run(["python", "transcription.py"])
    else:
        print("Download failed. Transcription script will not be launched.")

if __name__ == "__main__":
    main()
