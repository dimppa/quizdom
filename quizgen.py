import os
import shutil
from openai import OpenAI

def ensure_directories():
    directories = ["transcript_current", "transcript_archive", "quizzes"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def generate_quiz(transcript_path, quiz_path):
    with open(transcript_path, "r", encoding="utf-8") as f:
        transcript_text = f.read()

    client = OpenAI(
        api_key="paste api key here"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": """You are a quiz generator focused on creating objective, topic-focused questions.
Guidelines:
- Focus on the subject matter and topics discussed, not the speaker/presenter
- Create diverse question types using what, when, where, why, who, and how
- Avoid subjective questions or opinions about the presenter's style/personality
- Ensure questions test understanding of the core concepts and information"""},
                {"role": "user", "content": transcript_text},
                {"role": "user", "content": """Generate a 5-question multiple choice quiz about the topics covered.
Each question should test understanding of different aspects of the subject matter.

FORMAT:
Q1: [Question]
A) [Option]
B) [Option]
C) [Option]
D) [Option]
Answer: [Letter]

Q2...etc"""}
            ]
        )
        
        quiz_text = response.choices[0].message.content
        if "Q1:" in quiz_text:
            quiz_text = "Q1:" + quiz_text.split("Q1:")[1]

        with open(quiz_path, "w", encoding="utf-8") as f:
            f.write(quiz_text)
            
    except Exception as e:
        print(f"Error generating quiz: {str(e)}")
        raise

def process_transcripts():
    transcript_dir = "transcript_current"
    archive_dir = "transcript_archive"
    quiz_dir = "quizzes"
    latest_quiz = None

    for file in os.listdir(transcript_dir):
        if file.endswith("_transcript.txt"):
            transcript_path = os.path.join(transcript_dir, file)
            quiz_path = os.path.join(quiz_dir, file.replace("_transcript.txt", "_quiz.txt"))

            print(f"Generating quiz for {file}...")
            generate_quiz(transcript_path, quiz_path)
            latest_quiz = quiz_path

            shutil.move(transcript_path, os.path.join(archive_dir, file))
            print(f"Quiz for {file} has been generated and saved.")

    if latest_quiz:
        print("\nLaunching quiz interface with the latest quiz...")
        import subprocess
        subprocess.run(['python', 'quiz.py', '--latest'])

if __name__ == "__main__":
    ensure_directories()
    process_transcripts()
