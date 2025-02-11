# quizdom
Generate multiple choice quizes from educational youtube videos. Improve knowledge retention and understanding of topics by getting tested on what you watch.

## Outline
1. paste youtube url in main.py
2. main.py downloads the video using yt-dlp and deposits it in video_current
3. main.py verifies download and launches transcript.py
4. transcript.py takes the video from video_current and extracts the audio using moviepy -> transcribes the video using whisper -> deposits transcript in transcript_current and moves video+audio files from video_current to video_archive
5. transcript.py launches quiz.py
6. quizgen.py takes the transcript from transcript_current and sends a prompt to gpt-4o via openai api to generate a quiz with 5 multiple choice questions + answer key -> deposits quiz in quizzes and moves transcript from transcript_current to transcript_archive. Or use quizgen_ollama.py to do the same locally.
8. quiz.py parses the quizes and opens it in terminal in interactable format with randomised order of questions and answers. Also possible to access previous quizes by running quiz.py directly.

## Libraries
- yt-dlp
- moviepy
- whisper
- OpenAi
- argprase
- datetime
- random
- shutil
- os
- ollama + deepseek-r1:14b (if generating quiz locally)

## Ongoing development
### Access to YouTube watch history
Tried setting this up with my personal google account, couldn't figure it out. You can manually export your YouTube watch history by requesting it from Google Takeout but so far I haven't figured out/found any API or tool that would automate this. Came across this tool but didn't have time to verify if it's legit: https://gandalf.network/

Resources:
  - https://stackoverflow.com/questions/63213016/how-can-i-get-my-watch-history-with-youtube-data-api-v3
  - https://www.reddit.com/r/youtube/comments/ijq4pq/is_there_a_way_to_get_watch_history_via_youtube/
  - https://blog.viktomas.com/posts/youtube-usage/
  - https://www.reddit.com/r/DataHoarder/comments/199411o/google_takeout_is_getting_an_official_api/

### Improving prompt to get better questions
Played around with the prompt and went from deepseek-r1:8b to deepseek-r1:14b, marginal improvement. Ditched this setup, implemented gpt-4o via api and the result is dramatically better. Quizes are generated faster and the questions are significantly better. For obvious reasons keeping this public repository with the local llm setup.

### Building an interactive quiz with grading
Looking into this.
