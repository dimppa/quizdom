import os
import shutil
import subprocess
import ollama


def ensure_directories():
    directories = ["transcript_current", "transcript_archive", "quizzes"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


def generate_quiz(transcript_path, quiz_path):
    with open(transcript_path, "r", encoding="utf-8") as f:
        transcript_text = f.read()

    prompt = f"""
    Based on the following transcript, create a quiz with 5 multiple-choice questions.
    Each question should have four answer choices, with one correct answer clearly marked.

    Transcript:
    {transcript_text}

    Format the output as follows:
    Q1: [Question text]
    A) [Option 1]
    B) [Option 2]
    C) [Option 3]
    D) [Option 4]
    Answer: [Correct Option]
    """

    response = ollama.chat(model="deepseek-r1:8b", messages=[{"role": "user", "content": prompt}])
    quiz_text = response["message"]["content"]

    with open(quiz_path, "w", encoding="utf-8") as f:
        f.write(quiz_text)


def process_transcripts():
    transcript_dir = "transcript_current"
    archive_dir = "transcript_archive"
    quiz_dir = "quizzes"

    for file in os.listdir(transcript_dir):
        if file.endswith("_transcript.txt"):
            transcript_path = os.path.join(transcript_dir, file)
            quiz_path = os.path.join(quiz_dir, file.replace("_transcript.txt", "_quiz.txt"))

            print(f"Generating quiz for {file}...")
            generate_quiz(transcript_path, quiz_path)

            # Move transcript to archive
            shutil.move(transcript_path, os.path.join(archive_dir, file))

            print(f"Quiz for {file} has been generated and saved.")


if __name__ == "__main__":
    ensure_directories()
    process_transcripts()
