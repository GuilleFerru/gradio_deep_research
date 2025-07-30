from agents import Agent, WebSearchTool, trace, Runner, gen_trace_id
from refinement_agent import refinement_agent, RefinementQuestion, RefinedQuery
from planner_agent import planner_agent, WebSearchItem, WebSearchPlan
from writer_agent import writer_agent, ResearchReport
from search_agent import search_agent
import asyncio

class SearchManager:
    
    def __init__(self, progress_callback=None):
        self.progress_callback = progress_callback
        self.refinement_original_query: str | None = None  # Stores the original query
        self.refinement_qas: list[dict[str, str]] = []     # Stores Q/A pairs for refinement
        self.pending_question: bool = False                # Indicates if waiting for user answer
        self.questions_asked: int = 0                     # Number of questions asked
        self.last_question: str | None = None              # Last question asked
        self.current_trace_id: str | None = None            # Save the first trace in openai traces

    async def log(self, message):
        print(message)
        if self.progress_callback:
            try:
                if asyncio.iscoroutinefunction(self.progress_callback):
                    await self.progress_callback(message)
                else:
                    self.progress_callback(message)
            except Exception as e:
                print(f"Error sending log to server: {e}")

    async def run(self, query: str):
        
        if self.current_trace_id is None:
            self.current_trace_id = gen_trace_id()
        trace_id = self.current_trace_id

        with trace("DeepSearch trace", trace_id=trace_id):
            await self.log(f"Starting deep search for query: {query}")
            refinement_result = await self.query_refinement(query)
            if isinstance(refinement_result, dict) and not refinement_result.get("is_final", True):
                return refinement_result
            if isinstance(refinement_result, dict):
                refined_query_text = refinement_result.get("query", query)
            else:
                refined_query_text = query
            search_plan = await self.plan_searches(refined_query_text)
            search_results = await self.run_searches(search_plan)
            report = await self.write_report(refined_query_text, search_results)
            return report

    async def query_refinement(self, query: str):
        # Register the original query or pair the answer to the last question
        if not self.pending_question:
            if self.refinement_original_query is None:
                self.refinement_original_query = query
        else:
            if self.last_question is not None:
                self.refinement_qas.append({
                    "question": self.last_question,
                    "answer": query,
                })
            self.pending_question = False
            self.last_question = None

        # Build context with the original query and all stored Q/A pairs
        context_lines = [f"Original query: {self.refinement_original_query}"]
        for qa in self.refinement_qas:
            context_lines.append(f"Question: {qa['question']}")
            context_lines.append(f"Answer: {qa['answer']}")
        context = "\n".join(context_lines)

        # Call the refinement agent with the context
        await self.log("Refining query with context:\n" + context)
        result = await Runner.run(refinement_agent, context)

        # Check if we already have a RefinedQuery (final case after handoff)
        refined_query_text = None
        try:
            refined_query_output = result.final_output_as(RefinedQuery)
            refined_query_text = refined_query_output.query
            is_final = True
            refined_question = None
            question = None
        except Exception:
            # If not RefinedQuery, try to interpret as RefinementQuestion
            try:
                refined_question = result.final_output_as(RefinementQuestion)
                question = refined_question.question[0] if refined_question.question else None
                is_final = bool(refined_question.is_final)
            except Exception:
                refined_question = None
                question = None
                is_final = True

        # If not final and can still ask, return the new question
        if not is_final:
            if self.questions_asked >= 3:
                # Force final if 2 questions have already been asked
                try:
                    refined_query_output = result.final_output_as(RefinedQuery)
                    refined_query_text = refined_query_output.query
                except Exception:
                    refined_query_text = context
                self._reset_refinement_state()
                return {"is_final": True, "query": refined_query_text}
            await self.log("Query refinement is not final, asking for more information.")
            await self.log(f"**Question: {question}**")
            self.pending_question = True
            self.last_question = question
            self.questions_asked += 1
            return {"is_final": False, "question": question}

        # If final, get the refined query (if not already available)
        if refined_query_text is None:
            try:
                refined_query_output = result.final_output_as(RefinedQuery)
                refined_query_text = refined_query_output.query
            except Exception:
                refined_query_text = context
        await self.log("Final query refinement completed.")
        self._reset_refinement_state()
        return {"is_final": True, "query": refined_query_text}

    def _reset_refinement_state(self) -> None:
        self.refinement_original_query = None
        self.refinement_answers = []
        self.pending_question = False
        self.questions_asked = 0
        self.refinement_qas = []
        self.last_question = None
        self.current_trace_id = None

    async def plan_searches(self, query:str) -> WebSearchPlan:
        await self.log(f"**Planning searches for query: {query}**")
        result = await Runner.run(planner_agent, query)
        await self.log("Search plan generated successfully.")
        return result.final_output_as(WebSearchPlan)

    async def run_searches(self, search_plan: WebSearchPlan) -> list[WebSearchItem]:
        await self.log("Running searches based on the plan.")
        search_tasks = [self.search(search_item) for search_item in search_plan.searches]
        search_results = await asyncio.gather(*search_tasks)
        await self.log("**All searches completed successfully.**")
        return search_results

    async def search(self, item: WebSearchItem) -> str:
        await self.log("Performing search")
        result = await Runner.run(search_agent, item.query)
        await self.log("Search completed.")
        if hasattr(result, 'final_output'):
            return result.final_output
        else:
            return result

    async def write_report(self, query:str,search_results:list[str])-> ResearchReport:
        await self.log("Running final report.")
        input = f"Original query ={query}, search results ={search_results}"
        result = await Runner.run(writer_agent, input)
        return result.final_output_as(ResearchReport)