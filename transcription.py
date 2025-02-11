import os
import shutil
import subprocess
import whisper
from moviepy import VideoFileClip


def ensure_directories():
    directories = ["video_current", "transcript_current", "video_archive"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


def extract_audio(video_path, audio_path):
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path, codec='mp3')
    clip.close()


def transcribe_audio(audio_path, transcript_path):
    model = whisper.load_model("base")  # You can change to "medium" or "large" for better accuracy
    result = model.transcribe(audio_path)
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(result["text"])


def process_videos():
    video_dir = "video_current"
    archive_dir = "video_archive"
    transcript_dir = "transcript_current"
    processed_any = False

    for file in os.listdir(video_dir):
        if file.endswith(".mp4") or file.endswith(".mkv") or file.endswith(".avi"):
            video_path = os.path.join(video_dir, file)
            base_name = os.path.splitext(file)[0]
            audio_path = os.path.join(video_dir, base_name + ".mp3")
            transcript_path = os.path.join(transcript_dir, base_name + "_transcript.txt")

            print(f"Processing {file}...")
            extract_audio(video_path, audio_path)
            transcribe_audio(audio_path, transcript_path)

            # Move video and audio files to archive
            shutil.move(video_path, os.path.join(archive_dir, file))
            shutil.move(audio_path, os.path.join(archive_dir, os.path.basename(audio_path)))

            print(f"Completed processing {file}.")
            processed_any = True

    # Only launch quizgen.py after all videos are processed
    if processed_any:
        print("\nLaunching quiz generation...")
        subprocess.run(["python", "quizgen.py"])


if __name__ == "__main__":
    ensure_directories()
    process_videos()
