"""
Gradio UI for Deep Research application
"""
import gradio as gr
from main import main
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Default message for the input box
#DEFAULT_MESSAGE = "Latest AI Agent frameworks in 2025"

# Create Gradio interface
with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue")) as ui:
    with gr.Row(elem_id="header"):
        gr.Markdown("## 🔍 Deep Research Agent", elem_id="title")
    gr.Markdown("*Clarify your query, perform research, then generate an email.*", elem_id="subtitle")
    
    with gr.Tabs():
        with gr.TabItem("Progress Logs"):
                progress_output = gr.Markdown(label="Progress", value="Ready to search...")
                query_input = gr.Textbox(label="Query", placeholder="Enter the topic you want to explore...", lines=1, autofocus=True)
                with gr.Row(elem_id="controls"):
                    run_button = gr.Button("Run Workflow", variant="primary", size="lg")
        with gr.TabItem("Research Result"):
                result_output = gr.Markdown(label="Research Result")
    with gr.Row(elem_id="footer"):
        gr.HTML("<p style='text-align:center;'>Built with ❤️ using Gradio</p>")   

    # Connect the UI to the main function
    run_button.click(
        fn=main,
        inputs=query_input,
        outputs=[progress_output, result_output ],
        api_name="search",
        queue=True 
    )

# Function to launch the UI
def launch_ui(inbrowser=True):
    """Launch the Gradio UI"""
    ui.launch(inbrowser=inbrowser)

# Launch the UI when this script is run directly
if __name__ == "__main__":
    launch_ui()
