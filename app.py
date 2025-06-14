import gradio as gr
import tools  # Customized tools

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
            fn=tools.process_inputs_and_summarize,
            inputs=[url_input, manual_transcript_input, bullet_points],
            outputs=[summary_output, download_button],
            show_progress=True,
            api_name="summarize",
        )
       
        download_button.click(
            fn=tools.create_download_text,
            inputs=[summary_output],
            #outputs=[],
            show_progress=True,
            api_name="create_download_text",
        )

if __name__ == "__main__":
    app.launch(share=True, debug=False)
