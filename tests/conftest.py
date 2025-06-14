import pytest
import os
from unittest.mock import MagicMock

@pytest.fixture
def sample_transcript():
    """Provide a sample transcript for testing."""
    return """This is a sample transcript for testing purposes.
    It contains multiple lines of text that can be summarized.
    The AI should be able to extract key points from this text."""

@pytest.fixture
def mock_openai_client(monkeypatch):
    """Mock the OpenAI client."""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "**3 Key Points:**\n1. First point\n2. Second point\n3. Third point"
    mock_client.chat.completions.create.return_value = mock_response
    
    monkeypatch.setattr("tools.client", mock_client)
    return mock_client

@pytest.fixture(autouse=True)
def timeout_for_tests():
    """Add a timeout to all tests."""
    import signal
    
    def timeout_handler(signum, frame):
        raise Exception("Test timed out!")
    
    # Set a 30-second timeout for each test
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(30)
    
    yield
    
    # Disable the alarm after the test
    signal.alarm(0)
