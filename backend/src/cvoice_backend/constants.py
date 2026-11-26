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


# Nvidia Build: the embedding model used by the vector store
EMBEDDING_MODEL_NAME = "nvidia/nemotron-3.5-embed-8b"
EMBEDDING_DIMENSIONS = 4096

# Name the embedding function is registered under in LanceDB's registry
EMBEDDER_NAME = "nvidia-nemotron"

# Ingestion: how documents are split before they are embedded
CHUNK_SIZE = 900
CHUNK_OVERLAP = 150

# How many chunks a search returns by default
SEARCH_TOP_K = 5

# What the upload endpoint accepts
ALLOWED_SUFFIXES = (".pdf", ".txt", ".md")
MAX_UPLOAD_BYTES = 10 * 1024 * 1024

# Sample CVs used by tests and demos
SAMPLE_PROFILES_PATH = BACKEND_PATH / "src" / "data" / "sample_profiles"