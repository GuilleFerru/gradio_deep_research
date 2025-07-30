import gradio as gr
from dotenv import load_dotenv
from utils.custom_css import custom_css

load_dotenv(override=True)

class GradioUI:
    def __init__(self):
        self.demo = None
        self.create_ui()
        
    def create_ui(self):
        from main import main
        
        with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue"), css=custom_css) as self.demo:
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
                gr.HTML("<p style='text-align:center;'>Built with ❤️ using Gradio | GuilleFerru 👨‍💻</p> ")   

            run_button.click(
                fn=main,
                inputs=query_input,
                outputs=[progress_output, result_output],
                api_name="search",
                queue=True 
            )
    
    def launch(self):
        if self.demo:
            self.demo.launch(
                server_port=7860, 
                share=False,
                inbrowser=True,
            )

