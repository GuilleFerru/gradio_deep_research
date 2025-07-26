import os
from pydantic import BaseModel, Field
from agents import Agent
from dotenv import load_dotenv

QTY_SEARCHES = 1

load_dotenv(override=True)

model = os.getenv('AI_MODEL', '')
print(f"Using model: {model}")

INSTRUCTION = f"You are a helpful research assistant. Given a query, come up with a set of web searches \
to perform to best answer the query. Output {QTY_SEARCHES} terms to query for."

class WebSearchItem(BaseModel):
    reason: str = Field(description="A reason for the search term, explaining why it is relevant to the query.")
    query: str = Field(description="A search term to use in a web search.")

class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(description="A list of search terms and their reasons for the research query.")



planner_agent = Agent(
    name="planner_agent",
    instructions=INSTRUCTION,
    model=model,
    output_type=WebSearchPlan,
    )

