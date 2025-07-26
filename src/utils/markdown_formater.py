
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

