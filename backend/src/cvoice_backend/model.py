"""The language model, defined once and shared by all agents."""

import os

from dotenv import load_dotenv
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from cvoice_backend.constants import LLM_MODEL_NAME, NVIDIA_BASE_URL

load_dotenv()


def nvidia_model(model_name: str = LLM_MODEL_NAME) -> OpenAIChatModel:
    """Return a Nvidia Build model that the agents can use."""
    return OpenAIChatModel(
        model_name=model_name,
        provider=OpenAIProvider(
            base_url=NVIDIA_BASE_URL,
            api_key=os.environ["NVIDIA_API"],
        ),
    )
