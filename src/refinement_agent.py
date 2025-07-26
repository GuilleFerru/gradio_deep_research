from pydantic import BaseModel, Field
from agents import Agent
import os
from dotenv import load_dotenv

load_dotenv(override=True)
model = os.getenv('AI_MODEL', '')

class RefinementQuestion(BaseModel):
    """A question to refine the user's query."""
    question: str = Field(description="A question to ask the user to refine their query")
    reasoning: str = Field(description="Why this question will help refine the search")

class QueryRefinement(BaseModel):
    """A set of questions to refine the user's query."""
    questions: list[RefinementQuestion] = Field(
        description="Up to 3 questions to refine the query", 
        max_items=3
    )

REFINEMENT_INSTRUCTION = """You are a query refinement assistant. Given an initial search query, 
generate up to 3 questions that would help clarify and focus the search intent.
These questions should help gather more context, specify areas of interest, or clarify ambiguities.
Think about what additional information would make the search more effective.
"""

refinement_agent = Agent(
    name="refinement_agent",
    instructions=REFINEMENT_INSTRUCTION,
    model=model,
    output_type=QueryRefinement,
)