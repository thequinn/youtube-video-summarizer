import pytest
from unittest.mock import patch, MagicMock
import re
from datetime import datetime

# The setup below is needed to import the tools module from the parent directory
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import tools


@pytest.mark.download
def test_create_download_text(tmp_path, monkeypatch):
    """Test the create_download_text function."""
    # Change to a temporary directory for the test
    monkeypatch.chdir(tmp_path)
    
    # Test with valid summary
    summary = "This is a test summary"
    tools.create_download_text(summary)
    
    # Check that a file was created with the expected naming pattern
    created_files = list(tmp_path.glob("summary_*.txt"))
    assert len(created_files) == 1
    
    # Check file contents
    with open(created_files[0], "r") as f:
        content = f.read()
        assert content == summary
    
    # Test with error summary
    error_summary = "Error: Something went wrong"
    tools.create_download_text(error_summary)
    
    # Should still have only one file (error summary shouldn't create a file)
    assert len(list(tmp_path.glob("summary_*.txt"))) == 1

@pytest.mark.summarize
def test_summarize(mock_openai_client, sample_transcript):
    """Test the summarize function."""
    # Test with different modes
    for mode in ["3", "4", "5"]:
        result = tools.summarize(sample_transcript, mode)
        assert "Key Points" in result or "point" in result.lower()
        assert mock_openai_client.chat.completions.create.called
        
        # Reset the mock for the next call
        mock_openai_client.reset_mock()

@pytest.mark.fetch
@patch('tools.YouTubeTranscriptApi.get_transcript')
def test_fetch_transcript(mock_get_transcript):
    """Test the fetch_transcript function."""
    # Setup mock response
    mock_get_transcript.return_value = [
        {"text": "First segment", "start": 0, "duration": 5},
        {"text": "Second segment", "start": 5, "duration": 5}
    ]
    
    # Test with valid YouTube URL
    valid_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    result = tools.fetch_transcript(valid_url)
    assert result == "First segment Second segment"
    mock_get_transcript.assert_called_once_with("dQw4w9WgXcQ")
    
    # Reset mock
    mock_get_transcript.reset_mock()
    
    # Test with invalid URL format
    invalid_url = "not-a-youtube-url"
    result = tools.fetch_transcript(invalid_url)
    assert result.startswith("Error: Invalid YouTube URL format")
    assert not mock_get_transcript.called
    
    # Test with empty URL
    empty_url = ""
    result = tools.fetch_transcript(empty_url)
    assert result == "Error: YouTube URL is required."
    
    # Test with API error
    mock_get_transcript.side_effect = Exception("API Error")
    result = tools.fetch_transcript(valid_url)
    assert result.startswith("Error fetching transcript")

@pytest.mark.summarize
def test_process_inputs_and_summarize(monkeypatch, sample_transcript):
    """Test the process_inputs_and_summarize function."""
    # Mock the fetch_transcript and summarize functions
    def mock_fetch(url):
        if url == "valid-url":
            return sample_transcript
        return "Error: Invalid URL"
    
    def mock_summarize(text, mode):
        return f"**{mode} Key Points:**\n" + "\n".join([f"{i+1}. Point {i+1}" for i in range(int(mode))])
    
    # During the test, any call to tools.fetch_transcript will instead invoke mock_fetch.
    monkeypatch.setattr("tools.fetch_transcript", mock_fetch)
    monkeypatch.setattr("tools.summarize", mock_summarize)
    
    # Test with valid URL
    summary, button = tools.process_inputs_and_summarize("valid-url", "", "3")
    assert "3 Key Points" in summary
    assert button['interactive']  # Button should be interactive
    
    # Test with invalid URL but valid manual transcript
    summary, button = tools.process_inputs_and_summarize("invalid-url", sample_transcript, "4")
    assert "4 Key Points" in summary
    assert button['interactive']
    
    # Test with no inputs
    summary, button = tools.process_inputs_and_summarize("", "", "5")
    assert summary.startswith("Error")
    assert button is None
