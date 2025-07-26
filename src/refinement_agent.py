from pydantic import BaseModel, Field
from agents import Agent
import os
from dotenv import load_dotenv
from planner_agent import planner_agent
from typing import Optional

load_dotenv(override=True)
model = os.getenv('AI_MODEL', '')

class RefinementQuestion(BaseModel):
    """A question to refine the user's query."""
    question: str = Field(description="A specific question to ask the user to refine their query")
    reason: str = Field(description="Why this question will help refine the search")
    iteration: int = Field(description="The current refinement iteration (1 or 2)", default=1)

class RefinedQuery(BaseModel):
    """The final refined query after the refinement process."""
    original_query: str = Field(description="The original query provided by the user")
    refined_query: str = Field(description="The improved query after refinement")
    reasoning: str = Field(description="Explanation of how the refinements improved the query")
    is_final: bool = Field(description="Whether this is the final refinement or another question is needed", default=False)
    next_question: Optional[RefinementQuestion] = Field(description="The next question to ask if not final", default=None)

REFINEMENT_INSTRUCTION = """You are an interactive query refinement assistant. Your goal is to help users improve their search queries through targeted questions.

Process:
1. Analyze the current query
2. Either:
   a. Ask ONE specific question to gather important missing information
   b. If you've already asked 2 questions OR the query is sufficiently refined, finalize the query

If this is the first or second interaction:
- Formulate a single focused question that addresses the most critical gap in the query
- Explain why this question will improve search results
- Set is_final to false and include your question in next_question

If you've already asked 2 questions OR the query is sufficiently detailed:
- Create a final refined_query that incorporates all the information gathered
- Explain how your refinements improve the search
- Set is_final to true and next_question to null

After your refinement process is complete, the final query will be handed off to the planner agent.
"""

refinement_agent = Agent(
    name="refinement_agent",
    instructions=REFINEMENT_INSTRUCTION,
    model=model,
    output_type=RefinedQuery,
)