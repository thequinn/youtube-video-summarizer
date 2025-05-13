import pytest
from unittest.mock import patch
import re

# The setup below is needed to import the tools module from the parent directory
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import tools


@pytest.mark.integration
def test_end_to_end_flow(monkeypatch, tmp_path):
    """Test the entire flow from URL to summary file."""
    # Setup: Change to temp directory and mock external dependencies
    monkeypatch.chdir(tmp_path)
    
    # Mock transcript API
    transcript_text = "This is a test transcript for integration testing."
    
    def mock_get_transcript(video_id):
        return [{"text": transcript_text, "start": 0, "duration": 5}]
    
    # Mock OpenAI API
    summary_text = "**3 Key Points:**\n1. Test point one\n2. Test point two\n3. Test point three"
    
    def mock_create_completion(**kwargs):
        mock_response = type('obj', (object,), {
            'choices': [type('obj', (object,), {
                'message': type('obj', (object,), {
                    'content': summary_text
                })
            })]
        })
        return mock_response
    
    # Apply mocks
    monkeypatch.setattr("youtube_transcript_api.YouTubeTranscriptApi.get_transcript", mock_get_transcript)
    monkeypatch.setattr("tools.client.chat.completions.create", mock_create_completion)
    
    # Execute the flow
    url = "https://www.youtube.com/watch?v=test123"
    summary, button_state = tools.process_inputs_and_summarize(url, "", "3")
    
    # Verify summary
    assert summary == summary_text
    assert button_state.interactive
    
    # Test file creation
    filename = tools.create_download_text(summary)
    assert os.path.exists(filename)
    
    # Check file contents
    with open(filename, "r") as f:
        content = f.read()
        assert content == summary_text