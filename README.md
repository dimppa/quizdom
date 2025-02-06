# quizdom
Generate multiple choice quizes from educational youtube videos. Improve knowledge retention and understanding of topics by getting tested on what you watch.

## Outline
1. paste youtube url in main.py
2. main.py downloads the video using yt-dlp and deposits it in video_current
3. main.py verifies download and launches transcript.py
4. transcript.py takes the video from video_current and extracts the audio using moviepy -> transcribes the video using whisper -> deposits transcript in transcript_current and moves video+audio files from video_current to video_archive
5. transcript.py launches quiz.py
6. quiz.py takes the transcript from transcript_current and sends a prompt to ollama to generate a quiz with 5 multiple choice questions + answer key -> deposits quiz in quizzes and moves transcript from transcript_current to transcript_archive
7. ready quiz in quizzes

## Libraries
- yt-dlp
- moviepy
- whisper
- ollama + deepseek-r1:8b
- shutil
- os
