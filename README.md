---
title: YouTube Video Summarizer
app_file: app.py
---

YouTube Video Summarizer

This project is a web application that summarizes YouTube videos using AI. Key features:

Takes a YouTube URL or manual transcript as input
Extracts video transcripts automatically using YouTube's API
Generates concise summaries with customizable bullet points (3-5)
Uses OpenRouter API (with Meta's Llama-4-Maverick model) for summarization
Built with Gradio for the user interface
Includes download functionality for saving summaries as text files
Deployed on Hugging Face Spaces
The app is designed to be simple to use while providing powerful AI-based summarization capabilities for YouTube content.

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

> > Running tests

# Run all tests

pytest

# Run with verbose output

pytest -v

# Run only unit tests (skip integration tests)

pytest -m "not integration"

# Run only integration tests (skip unit tests)

pytest -m "integration"

# Run with coverage report

pytest --cov=tools --cov=app --cov-report=term-missing

# Run a specific test file, -v for verbose

pytest tests/test_tools.py -v

Best Practices for Testing This Project

- Mock External Dependencies: Always mock YouTube API and OpenAI API calls
- Test File Operations: Use tmp_path fixture for file operations
- Parameterize Tests: Use @pytest.mark.parametrize for testing different bullet point counts
- Test Error Handling: Ensure your app gracefully handles errors
- Separate Unit and Integration Tests: Use markers to separate test types
- Test UI Components: Test Gradio components where possible
- Use Coverage Reports: Aim for high test coverage of your core functions
