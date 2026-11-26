"""Agent that builds a structured Profile from the uploaded documents."""

from datetime import date

from pydantic_ai import Agent

from cvoice_backend.data_models import Profile
from cvoice_backend.model import nvidia_model
from cvoice_backend.prompts import PROFILE_PROMPT

profile_agent = Agent(
    model=nvidia_model(),
    retries=2,
    instructions=PROFILE_PROMPT,
    output_type=Profile,
)


@profile_agent.instructions
def add_todays_date() -> str:
    """Tell the agent today's date, so it can count years up to 'Present'."""
    return f"Today's date is {date.today()}."


async def build_profile(text: str) -> Profile:
    """Build a Profile from the text of a person's documents."""
    result = await profile_agent.run(text)
    return result.output
