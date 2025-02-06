import yt_dlp
import os
import subprocess

output_folder= "video_current"
os.makedirs(output_folder, exist_ok=True)


url = "https://www.youtube.com/watch?v=uqsBx58GxYY"

# Set download options
ydl_opts = {
    "format": "bv*[height<=720]+ba/b[height<=720]",
    "merge_output_format": "mp4",
    "outtmpl": os.path.join(output_folder, "%(title)s.%(ext)s"),
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

def launch_script(script_name):
    """Launch another Python script after a successful download."""
    print(f"Launching {script_name}...")
    subprocess.run(["python", script_name])  # Runs the script

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    result = ydl.download([url])

# Step 3: If the download was successful, launch another script
if result == 0:  # yt-dlp returns 0 if successful
    launch_script("transcription.py")
else:
    print("Download failed. Transcription script will not be launched.")
