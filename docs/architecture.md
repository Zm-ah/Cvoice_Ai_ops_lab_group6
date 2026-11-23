# Architecture

<!-- TODO: add the architecture diagram and a short description of each part -->

## Overview

- Frontend (Streamlit) talks to the backend (FastAPI) over HTTP.
- The backend ingests documents, stores chunks in a vector store, and runs agents.

## Components

| Part | Responsibility |
|---|---|
| `ingestion.py` | PDF to text, split into chunks |
| `vector_store.py` | Store and search chunks |
| `agents/profile_agent.py` | Build a structured profile |
| `agents/persona_agent.py` | Answer as the person |
| `agents/match_agent.py` | Match a profile against a job ad |
| `voice.py` | Speech to text and text to speech |
