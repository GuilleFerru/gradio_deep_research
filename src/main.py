from agents import Agent, WebSearchTool, trace, Runner, gen_trace_id, function_tool
import gradio as gr
from search_manager import SearchManager
from dotenv import load_dotenv
import asyncio

load_dotenv(override=True)


async def main(query):
    # Create a queue for communication between callbacks and main function
    progress_queue = asyncio.Queue()
    progress_messages = ["Starting research process..."]
    
    # Format progress messages as markdown with each message on its own line
    def format_progress(messages):
        formatted = "### Progress Log:\n\n"
        for i, msg in enumerate(messages):
            formatted += f"- {msg}\n"
        return formatted
    
    # Initial state
    yield format_progress(progress_messages), None
    
    # Define progress callback to add messages to the queue
    async def update_progress(message):
        await progress_queue.put(message)
    
    # Create SearchManager with our callback
    search_manager = SearchManager(progress_callback=update_progress)
    
    # Start the search process in a separate task
    search_task = asyncio.create_task(search_manager.run(query))
    
    # Process progress messages while waiting for the search to complete
    while not search_task.done():
        # Check for new progress messages (with timeout to prevent blocking)
        try:
            message = await asyncio.wait_for(progress_queue.get(), timeout=0.1)
            progress_messages.append(message)
            # Update UI with current progress
            yield format_progress(progress_messages), None
        except asyncio.TimeoutError:
            # No new message in the queue, continue checking
            await asyncio.sleep(0.1)
    
    # Get the search result once it's complete
    result = await search_task
    
    # Format final results
    formatted_result = format_search_plan_as_markdown(result)
    
    # Yield the final state with both progress and results
    progress_messages.append("Research complete")
    progress_messages.append("Check Research Result Tab!!!!")
    yield format_progress(progress_messages), formatted_result

def format_search_plan_as_markdown(result):
    """Format the research report as Markdown for display in Gradio.
    
    Args:
        result: Could be a ResearchReport object or other types
    """
    if not result:
        return "No research results available."
    
    # Handle ResearchReport type (from writer_agent)
    if hasattr(result, 'markdown_content') and hasattr(result, 'short_summary'):
        # This is a ResearchReport object
        md = f"# Research Report\n\n"
        md += f"## Summary\n\n{result.short_summary}\n\n"
        md += f"---\n\n"
        md += f"{result.markdown_content}\n\n"
        
        if hasattr(result, 'follow_up_questions') and result.follow_up_questions:
            md += f"\n\n## Follow-up Questions\n\n"
            for i, question in enumerate(result.follow_up_questions, 1):
                md += f"{i}. {question}\n"
        
        return md
    
    # Handle list of search results (from previous implementation)
    elif isinstance(result, list):
        md = "## Search Results\n\n"
        
        for i, item in enumerate(result, 1):
            if hasattr(item, 'final_output'):
                md += f"### Result {i}: {item.query if hasattr(item, 'query') else ''}\n\n"
                md += f"{item.final_output}\n\n"
                md += "---\n\n"
            elif isinstance(item, str):
                md += f"### Result {i}\n\n"
                md += f"{item}\n\n"
                md += "---\n\n"
            else:
                md += f"### Result {i}\n\n"
                md += f"Result format not recognized: {type(item)}\n\n"
                md += "---\n\n"
        
        return md
    
    # Handle string or other formats
    elif isinstance(result, str):
        return result
    else:
        return f"Unsupported result type: {type(result)}"


with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue")) as ui:
    with gr.Row(elem_id="header"):
        gr.Markdown("## 🔍 Deep Research Agent", elem_id="title")
    gr.Markdown("*Clarify your query, perform research, then generate an email.*", elem_id="subtitle")
    
    with gr.Tabs():
        with gr.TabItem("Progress Logs"):
                progress_output = gr.Markdown(label="Progress", value="Ready to search...")
                query_input = gr.Textbox(label="Query",  placeholder="Enter the topic you want to explore...", lines=1)
                with gr.Row(elem_id="controls"):
                    run_button = gr.Button("Run Workflow", variant="primary", size="lg")
        with gr.TabItem("Research Result"):
                result_output = gr.Markdown(label="Research Result")
                
    with gr.Row(elem_id="footer"):
        gr.HTML("<p style='text-align:center;'>Built with ❤️ using Gradio</p>")   


    run_button.click(
        fn=main,
        inputs=query_input,
        outputs=[progress_output, result_output],
        api_name="search",
        queue=True  # Importante para manejar múltiples actualizaciones
    )
    
ui.launch(inbrowser=True)




