import os
from pydantic import BaseModel, Field
from agents import Agent
from dotenv import load_dotenv

QTY_SEARCHES = 1

load_dotenv(override=True)
model = os.getenv('AI_MODEL', '')

INSTRUCTIONS = (
    "You are a senior researcher tasked with writing a cohesive report for a research query. "
    "You will be provided with the original query, and some initial research done by a research assistant.\n"
    "You should first come up with an outline for the report that describes the structure and "
    "flow of the report. Then, generate the report and return that as your final output.\n"
    "The final output should be in markdown format, in the same language as the query and it should be lengthy and detailed. \n"
    "Aim for 5-10 pages of content, at least 1000 words."
)

class ResearchReport(BaseModel):
    short_summary: str = Field(description="A short summary of the research report.")
    markdown_content: str = Field(description="The full research report in markdown format.")
    follow_up_questions: list[str] = Field(description="A list of follow-up questions that could be asked based on the report.")
    

writer_agent = Agent(
    name="Research Writer",
    instructions=INSTRUCTIONS,
    model=model,
    output_type=ResearchReport
)
