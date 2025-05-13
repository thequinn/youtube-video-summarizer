from dotenv import load_dotenv
import os
from openai import OpenAI
import re
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()
key = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=key,
)


def summarize(prompt: str, mode: str) -> str:
    prompt = (
        "You are a concise assistant.\n"
        f"Summarize the following transcript in **{mode}**:\n\n"
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

    return completion.choices[0].message.content


# Fetch auto-captions; raises error if none
def fetch_transcript(url: str) -> str:
    # Check if the URL is provided
    if not url.strip():
        # raise ValueError("Error: YouTube URL is required.")
        return "Error: YouTube URL is required."

    # Check if the URL is a valid YouTube URL
    if not re.match(r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$", url):
        # raise ValueError("Error: Invalid YouTube URL format.")
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
