from agents import Agent, WebSearchTool, trace, Runner, gen_trace_id
from planner_agent import planner_agent, WebSearchItem, WebSearchPlan
from search_agent import search_agent
import asyncio


class SearchManager:
    def __init__(self, progress_callback=None):
        """Initialize SearchManager with an optional progress callback function.
        
        Args:
            progress_callback: A function that will be called with status messages
        """
        self.progress_callback = progress_callback
    
    async def log(self, message):
        """Log a message to console and via callback if provided."""
        print(message)
        if self.progress_callback:
            if asyncio.iscoroutinefunction(self.progress_callback):
                await self.progress_callback(message)
            else:
                self.progress_callback(message)
    
    async def run(self, query:str):
        """ Run the deep search process, including web searches and summarization. """
        trace_id = gen_trace_id()
        with trace("DeepSearch trace", trace_id=trace_id):
            await self.log(f"Starting deep search for query: {query}")
            search_plan = await self.plan_searches(query)
            search_results = await self.run_searches(search_plan)
            await self.log("Deep search completed.")
            return search_results
    
    
    async def plan_searches(self, query:str) -> WebSearchPlan:
        """ Plan the searches needed to answer the query. """
        await self.log("Planning searches for query: " + query)
        result = await Runner.run(planner_agent, query)
        await self.log("Search plan generated successfully.")
        return result.final_output_as(WebSearchPlan)
    
    async def run_searches(self, search_plan: WebSearchPlan) -> list[WebSearchItem]:
        """ Run the planned searches and return the results. """
        await self.log("Running searches based on the plan.")
        search_results = []
        search_tasks = [self.search(search_item) for search_item in search_plan.searches]
        search_results = await asyncio.gather(*search_tasks)
        await self.log("All searches completed successfully.")
        return search_results
    
    async def search(self, item: WebSearchItem) -> str:
        """ Perform a single web search and return the result. """
        await self.log(f"Performing search for: {item.query}")
        result = await Runner.run(search_agent, item.query)
        await self.log(f"Search completed for: {item.query}")
        
        # Ensure we're returning the final_output if it exists
        if hasattr(result, 'final_output'):
            return result.final_output
        else:
            return result






