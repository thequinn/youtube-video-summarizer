---
title: YouTube Video Summarizer
app_file: app.py
---

This app is deployed to Hugging Face Spaces or you can run it locally by following the setup istruction below.
https://huggingface.co/spaces/sassywizard/youtube-video-summarizer

PRD and Code:
- Will add link from my www.notion.so

Sample transcript for testing:
- See test_transcript.txt


> > Environment setup on Mac

1. Setup a virtual env

cd into your project folder

python --version or python3 --version

python3 -m venv my-venv

2.  Activate the virtual env
    source my-env/bin/activate

3.  Install dependencies

pip install gradio python-dotenv openai youtube_transcript_api
or
pip install -r requirements.txt

4. Configure your API key

Create a .env and add the following to the file:

OPENROUTER_API_KEY=sk-…

Note: You need to get your own OpenRouter API key. Using this app is free. 

> > Run the app locally and remotely

1. Activate the virtual env

source my-env/bin/activate

2. Run the app, and gradio will show 2 options to access the app - locall and remote

python3 app.py

3. Open your browser to access either one.


