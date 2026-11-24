"""Shared constants. Define a value here once and reuse it everywhere."""

from pathlib import Path

APP_NAME = "cvoice"

# backend/ folder: constants.py -> cvoice_backend -> src -> backend
BACKEND_PATH = Path(__file__).parents[2]

# LanceDB stores its data here
KNOWLEDGE_BASE_PATH = BACKEND_PATH / "knowledge_base"

# Name of the LanceDB table with the document chunks
CHUNKS_TABLE = "chunks"


# Nvidia Build: the language model used by all agents
NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
LLM_MODEL_NAME = "nvidia/nemotron-3.5-super-vl-120b-a12b"
