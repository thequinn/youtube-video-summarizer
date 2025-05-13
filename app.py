import gradio as gr
import tools
from datetime import datetime

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

# Create a downloadable text file from the summary
def create_download_text(summary):
    if summary and not summary.startswith("Error:"):
        filename =  f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, "w") as f:
            f.write(summary)      
        return filename
    
    return "error occurred, so I set it to this msg...."

# - - - - - - - - - - - - - - #  - - - - - - - - - - - - - - #
def process_inputs_and_summarize(url, manual_transcript, bullet_points):
    transcript = None

    if url:
        transcript = tools.fetch_transcript(url)
        if transcript.startswith("Error:") and manual_transcript:
            transcript = manual_transcript.strip()
    elif manual_transcript:
        transcript = manual_transcript.strip()
    else:
        return "Error: YouTube URL or Manual Transcript is required.", None

    # Convert bullet_points to integer
    mode = int(bullet_points)
    summary = tools.summarize(transcript, mode)
    if summary.startswith("Error:"):
        return summary, None
    
    #gr.update(value=("testing....."), visible=True)
    return summary, gr.update(interactive=True)

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
        
        # Add dropdown for number of bullet points
        bullet_points = gr.Dropdown(
            choices=["3", "4", "5"],
            value="3",
            label="Number of Bullet Points",
            info="Select how many bullet points you want in the summary"
        )
        
        summary_output = gr.Textbox(label="Summary")
        #filename_output = gr.Textbox(label="Summary Filename")

        with gr.Row():
            with gr.Column(scale=1):
                submit_button = gr.Button("Summarize")
            with gr.Column(scale=1):
                download_button = gr.Button(
                    value = "Download Summary",
                    interactive=False
                )

        submit_button.click(
            fn=process_inputs_and_summarize,
            inputs=[url_input, manual_transcript_input, bullet_points],
            outputs=[summary_output, download_button],
            show_progress=True,
            api_name="summarize",
        )
       
        download_button.click(
            fn=create_download_text,
            inputs=[summary_output],
            outputs=[],
        )

app.launch(share=True, debug=False)  
