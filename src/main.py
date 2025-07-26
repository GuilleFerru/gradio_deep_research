
from agents import Agent, WebSearchTool, trace, Runner, gen_trace_id, function_tool
import gradio as gr
from search_manager import SearchManager
from dotenv import load_dotenv
import asyncio

load_dotenv(override=True)

message = "Latest AI Agent frameworks in 2025"


async def main(query):
    progress_log = ["Starting research process..."]
    
    def update_progress(message):
        progress_log.append(message)
        return "\n".join(progress_log)
    
    # Create an instance of SearchManager with the progress callback
    search_manager = SearchManager(progress_callback=update_progress)
    
    # Run the search and get results
    result = await search_manager.run(query)
    
    # Log the result type for debugging
    print(f"Result type: {type(result)}")
    if isinstance(result, list):
        print(f"List length: {len(result)}")
        if result:
            print(f"First item type: {type(result[0])}")
    
    # Format the final results as Markdown
    formatted_result = format_search_plan_as_markdown(result)
    
    # Return both the progress log and the formatted result
    final_progress = update_progress("Research complete!")
    return final_progress, formatted_result

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

    run_button.click(fn=main, inputs=query_input, outputs=[progress_output, result_output])
    
ui.launch(inbrowser=True)







