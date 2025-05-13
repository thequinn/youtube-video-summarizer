import gradio as gr
import tools


# Creates a styled title bar section using HTML and CSS
def create_title_bar(title, description=None):
    html_content = f"""
        <div style="background-color: #f0f0f0; /* Light background */
                padding: 15px;
                margin-bottom: 10px;
                border-bottom: 1px solid #ddd; /* Subtle border */
                border-radius: 5px;">
            <h1 style="color: #2c3e50; /* Darker title color */
                   margin-top: 0;
                   margin-bottom: 5px;
                   font-size: 24px;
                   font-weight: bold;">{title}</h1>
        """
    if description:
        html_content += f"""
        <p style="color: #7f8c8d; /* Gray description color */
                   font-size: 16px;
                   line-height: 1.5;">{description}</p>
        """
    html_content += "</div>"
    return gr.HTML(html_content)

# - - - - - - - - - - - - - - #  - - - - - - - - - - - - - - #
# 未... Understand the simiplified code and thhe remove the version in the next section...

def process_inputs_and_summarize(url, manual_transcript, mode):
    transcript = None

    if url:
        transcript = tools.fetch_transcript(url)
        if transcript.startswith("Error:") and manual_transcript:
            transcript = manual_transcript.strip()
    elif manual_transcript:
        transcript = manual_transcript.strip()
    else:
        return "Error: YouTube URL or Manual Transcript is required."

    mode = 3  # Always summarize with 3 bullet points
    summary = tools.summarize(transcript, mode)
    if summary.startswith("Error:"):
        return summary

    return summary

# - - - - - - - - - - - - - - #  - - - - - - - - - - - - - - #
def process_inputs_and_summarize(url, manual_transcript, mode):

    # If both URL and manual transcript are provided, prioritize the URL unless it return error.
    if url != "" and manual_transcript != "":
        # Try fetching the transcript from the URL
        transcript = tools.fetch_transcript(url)
        if transcript.startswith("Error:"):
            # If fetching from the URL fails, use the manual transcript
            transcript = manual_transcript.strip()
    elif url != "" and manual_transcript == "":
        transcript = tools.fetch_transcript(url)
        if transcript.startswith("Error:"):
            return transcript
    if url == "" and manual_transcript != "":
        transcript = manual_transcript.strip()
    if url == "" and manual_transcript == "":
        return "Error: YouTube URL or Manual Transcript is required."

    # Summarize the transcript
    mode = 3  # 3 bullet points
    summary = tools.summarize(transcript, mode)
    if summary.startswith("Error:"):
        return summary  # Return the error message directly to the UI

    return summary
# - - - - - - - - - - - - - - #  - - - - - - - - - - - - - - #


with gr.Blocks() as app:
    # Styled Title Bar using HTML and CSS
    title_bar = create_title_bar(
        title="YouTube Video Summarizer",
        description="Enter a YouTube video URL or Transcript, get an AI-powered summary"
    )

    with gr.Group():
        url_input = gr.Textbox(label="Enter YouTube URL")
        manual_transcript_input = gr.Textbox(label="Manual Transcript")
        output = gr.Textbox(label="Summary")

        submit_button = gr.Button("Summarize")
        submit_button.click(
            fn=process_inputs_and_summarize,
            inputs=[url_input, manual_transcript_input],
            outputs=output,
            show_progress=True,
            api_name="summarize",
        )

app.launch(share=True)
