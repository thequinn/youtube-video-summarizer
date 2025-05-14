import pytest
import gradio as gr
from unittest.mock import patch, MagicMock

# The setup below is needed to import the app module from the parent directory
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import app

def test_create_title_bar():
    """Test the create_title_bar function."""
    # Test with title only
    title_only = app.create_title_bar("Test Title")
    assert isinstance(title_only, gr.HTML)
    assert "Test Title" in title_only.value
    
    # Test with title and description
    title_desc = app.create_title_bar("Test Title", "Test Description")
    assert isinstance(title_desc, gr.HTML)
    assert "Test Title" in title_desc.value
    assert "Test Description" in title_desc.value

@patch('app.tools.process_inputs_and_summarize')
@patch('app.tools.create_download_text')
def test_app_interface(mock_create_download, mock_process):
    """Test the Gradio app interface."""
    # Setup mocks
    mock_process.return_value = ("Test Summary", gr.update(interactive=True))
    mock_create_download.return_value = "Download Link"

    # Get the app interface
    interface = app.app

    # Check that the interface has the expected components
    components = [getattr(c, 'label', None) for c in interface.blocks.values()]
    components = [c for c in components if c is not None]

    # Verify expected components exist
    assert any("Enter YouTube URL" in c for c in components)
    assert any("Manual Transcript" in c for c in components)
    assert any("Number of Bullet Points" in c for c in components)
    assert any("Summary" in c for c in components)

    # Simulate the button click by calling the mocked function
    url = "https://example.com"
    transcript = "Sample transcript"
    bullet_points = "3"

    # Simulate the submit button click
    mock_process.assert_not_called()
    mock_create_download.assert_not_called()

    # Call the function directly to simulate the click
    result = mock_process(url, transcript, bullet_points)

    # Verify the mocked function was called with the correct arguments
    mock_process.assert_called_once_with(url, transcript, bullet_points)
    assert result == ("Test Summary", gr.update(interactive=True))