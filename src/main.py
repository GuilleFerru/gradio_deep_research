from agents import Agent, WebSearchTool, trace, Runner, gen_trace_id, function_tool
import gradio as gr
from search_manager import SearchManager
from dotenv import load_dotenv
import asyncio

load_dotenv(override=True)

message = "Latest AI Agent frameworks in 2025"


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
    progress_messages.append("Research complete!")
    yield format_progress(progress_messages), formatted_result

def format_search_plan_as_markdown(search_results):
    """Format the search results as Markdown for display in Gradio.
    
    Args:
        search_results: A list of search results returned from search_manager.run()
    """
    if not search_results:
        return "No search results available."
    
    md = "## Search Results\n\n"
    
    for i, result in enumerate(search_results, 1):
        if hasattr(result, 'final_output'):
            md += f"### Result {i}: {result.query}\n\n"
            md += f"{result.final_output}\n\n"
            md += "---\n\n"
        elif isinstance(result, str):
            md += f"### Result {i}\n\n"
            md += f"{result}\n\n"
            md += "---\n\n"
        else:
            md += f"### Result {i}\n\n"
            md += f"Result format not recognized: {type(result)}\n\n"
            md += "---\n\n"
    
    return md


with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
    gr.Markdown("# Deep Research")
    
    query_input = gr.Textbox(label="Query", value=message, lines=2)
    run_button = gr.Button("Run", variant="primary")

    progress_output = gr.Markdown(label="Progress", value="Ready to search...")
    result_output = gr.Markdown(label="Research Results")

    run_button.click(
        fn=main,
        inputs=query_input,
        outputs=[progress_output, result_output],
        api_name="search",
        queue=True  # Importante para manejar múltiples actualizaciones
    )
    
ui.launch(inbrowser=True)







