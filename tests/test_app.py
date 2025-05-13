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
    
    # Get the app interface
    interface = app.app
    
    # Check that the interface has the expected components
    components = [c.label for c in interface.blocks.values() if hasattr(c, 'label')]
    
    # Verify expected components exist
    assert any("YouTube URL" in c for c in components)
    assert any("Manual Transcript" in c for c in components)
    assert any("Number of Bullet Points" in c for c in components)
    assert any("Summary" in c for c in components)
    
    # Test the submit button click
    # Note: This is a simplified test as we can't fully test the Gradio interface without running it
    for block in interface.blocks.values():
        if isinstance(block, gr.Button) and block.value == "Summarize":
            # Find the click event handler
            for event in interface.dependencies:
                if event.trigger == block and event.fn.__name__ == "process_inputs_and_summarize":
                    assert event.inputs[0].label == "Enter YouTube URL"
                    assert event.inputs[1].label == "Manual Transcript"
                    assert "Bullet Points" in event.inputs[2].label
                    break