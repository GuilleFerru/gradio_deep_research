"""
Main functionality for Deep Research application
"""
from agents import Agent, WebSearchTool, trace, Runner, gen_trace_id, function_tool
from search_manager import SearchManager
from utils.markdown_formater import format_search_plan_as_markdown
from dotenv import load_dotenv
import asyncio

# Load environment variables
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


# Entry point when run directly
if __name__ == "__main__":
    # Import here to avoid circular imports
    from gradio_ui import launch_ui
    launch_ui()




