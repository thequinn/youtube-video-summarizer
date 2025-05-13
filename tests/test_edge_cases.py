import pytest
from unittest.mock import patch

# The setup below is needed to import the app and tools modules from the parent directory
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import app
import tools

def test_very_long_transcript():
    """Test handling of very long transcripts."""
    long_transcript = "word " * 10000  # Create a very long transcript
    
    with patch('tools.client.chat.completions.create') as mock_create:
        # Setup mock response
        mock_response = type('obj', (object,), {
            'choices': [type('obj', (object,), {
                'message': type('obj', (object,), {
                    'content': "**3 Key Points:**\n1. Long point\n2. Another point\n3. Final point"
                })
            })]
        })
        mock_create.return_value = mock_response
        
        # Test the function with long input
        result = tools.summarize(long_transcript, "3")
        assert "Key Points" in result
        
        # Verify the API was called with the long transcript
        call_args = mock_create.call_args[1]
        assert "messages" in call_args
        assert long_transcript in str(call_args["messages"])

def test_empty_summary_response():
    """Test handling of empty summary from API."""
    with patch('tools.client.chat.completions.create') as mock_create:
        # Setup mock response with empty content
        mock_response = type('obj', (object,), {
            'choices': [type('obj', (object,), {
                'message': type('obj', (object,), {
                    'content': ""
                })
            })]
        })
        mock_create.return_value = mock_response
        
        # Test the function
        result = tools.summarize("Test transcript", "3")
        assert result == ""  # Should return empty string, not error

def test_api_error_handling():
    """Test handling of API errors."""
    with patch('tools.client.chat.completions.create') as mock_create:
        # Setup mock to raise an exception
        mock_create.side_effect = Exception("API Error")
        
        # Test the function
        with pytest.raises(Exception):
            tools.summarize("Test transcript", "3")