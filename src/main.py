from search_manager import SearchManager
from utils.markdown_formater import format_search_plan_as_markdown
from dotenv import load_dotenv
import asyncio

load_dotenv(override=True)

global_search_manager = None
global_progress_messages = []

async def main(query: str):
    
    global global_search_manager, global_progress_messages


    progress_queue = asyncio.Queue()

    def format_progress(messages: list[str]) -> str:
        """Formats a list of messages as markdown."""
        formatted = "### Progress Log:\n\n"
        for msg in messages:
            formatted += f"- {msg}\n"
        return formatted

    # If no search is active, start a new search session: reset the progress log and create a SearchManager.
    # Otherwise, reuse the existing manager and update its progress callback to write to our new queue.
    if global_search_manager is None:
        
        global_progress_messages = ["Starting research process..."]
        async def update_progress(message: str) -> None:
            await progress_queue.put(message)
        global_search_manager = SearchManager(progress_callback=update_progress)
        
    else:
        
        async def update_progress(message: str) -> None:
            await progress_queue.put(message)
        global_search_manager.progress_callback = update_progress

    search_task = asyncio.create_task(global_search_manager.run(query))

    # If this is the first call in a new session, yield the initial log.
    if len(global_progress_messages) == 1:
        yield format_progress(global_progress_messages), None

    # Drain the queue as messages arrive. Each message is appended to the persistent log and emitted to the UI.
    while not search_task.done():
        try:
            message = await asyncio.wait_for(progress_queue.get(), timeout=5.0)
            global_progress_messages.append(message)
            yield format_progress(global_progress_messages), None
        except asyncio.TimeoutError:
            # Avoid blocking the event loop; yield control briefly.
            await asyncio.sleep(0.1)

    result = await search_task

    # Append any remaining messages to the progress log.
    while not progress_queue.empty():
        try:
            msg = progress_queue.get_nowait()
            global_progress_messages.append(msg)
        except Exception:
            break

    # If refinement is not complete (is_final=False), ask the user for more information and keep the search manager alive. Do not reset state.
    if isinstance(result, dict) and not result.get("is_final", True):
        global_progress_messages.append(
            "**Awaiting additional information from user based on the above question.**"
        )
        yield format_progress(global_progress_messages), None
        return

    # Otherwise, the search is complete. Format the report and clean up
    formatted_result = format_search_plan_as_markdown(result)
    global_progress_messages.append("Research complete")
    global_progress_messages.append("**Check Research Result Tab!!!!**")
    yield format_progress(global_progress_messages), formatted_result

    global_search_manager = None
    global_progress_messages = []

if __name__ == "__main__":
    from gradio_ui import GradioUI
    
    gradio = GradioUI()
    gradio.launch()

