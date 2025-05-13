import os
import re
from datetime import datetime        
from dotenv import load_dotenv
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi
import gradio as gr

load_dotenv()
key = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=key,
)

# Create a downloadable text file from the summary
def create_download_text(summary):
    if summary and not summary.startswith("Error:"):
        filename =  f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w") as f:
            f.write(summary)  

def summarize(prompt: str, mode: str) -> str:
    prompt = (
        "You are a concise assistant.\n"
        f"Summarize the following transcript in {mode} numbered bullet points.\n"
        f"Start with '**Your Summary:**' as a header, then list each point with a number.\n\n"
        f"{prompt}\n\n"
        "Only output the summary."
    )

    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "http://localhost",  # or your actual app URL
            "X-Title": "YT Summarizer App",
        },
        model="meta-llama/llama-4-maverick:free",
        messages=[{"role": "user", "content": [{"type": "text", "text": prompt}]}],
    )

    #print("completion.choices[0].message.content: ", completion.choices[0].message.content)
    return completion.choices[0].message.content


# Fetch auto-captions; raises error if none
def fetch_transcript(url: str) -> str:
    # Check if the URL is provided
    if not url.strip():
        return "Error: YouTube URL is required."

    # Check if the URL is a valid YouTube URL
    if not re.match(r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$", url):
        return "Error: Invalid YouTube URL format."

    # Extract the video ID from the URL
    match = re.search(r"v=([^&]+)", url)
    if not match:
        return ValueError("Error: Invalid YouTube URL format.")

    vid = match.group(1)

    # Fetch the transcript
    try:
        segments = YouTubeTranscriptApi.get_transcript(vid)
        return " ".join(seg["text"] for seg in segments)
    except Exception as e:
        return f"Error fetching transcript: {str(e)}"
    

def process_inputs_and_summarize(url, manual_transcript, bullet_points):
    transcript = None

    if url:
        transcript = fetch_transcript(url)
        if transcript.startswith("Error:") and manual_transcript:
            transcript = manual_transcript.strip()
    elif manual_transcript:
        transcript = manual_transcript.strip()
        print("transcript: ", transcript)
    else:
        return "Error: YouTube URL or Manual Transcript is required.", None

    mode = int(bullet_points)
    summary = summarize(transcript, mode)

    if summary.startswith("Error:"):
        return summary, None
    if summary.startswith("No transcript is provided"):
        return "Transcript not fetched.  Try again or paste the transcript.", None

    return summary, gr.update(interactive=True)
