# cvoice

> Talk to your CV. Upload a resume and cover letter, get a profile summary, and chat or talk with a bot that speaks as the person behind the documents.

<!-- TODO: add a screenshot of the app here -->

## What it does

- **Upload**: a user uploads a CV, a cover letter and similar documents.
- **Profile**: the app shows KPIs (for example years of experience), a job dropdown and a short summary.
- **Persona bot**: a bot answers questions as the person in the profile (chat and voice).
- **Job match** (optional): match a profile against a job ad.

## Architecture

- `backend/`: FastAPI service that serves the models and agents.
- `frontend/`: Streamlit app for the user interface.
- `dockerfiles/` and `docker-compose.yaml`: run everything with Docker.
- `docs/`: working agreement and architecture notes.

## Getting started

```bash
# 1. Copy the environment template and fill in your own keys
cp .env.example .env

# 2. Start backend and frontend together
docker compose up --build
```

- Backend: http://localhost:8000 (docs at `/docs`)
- Frontend: http://localhost:8501

## Local development (without Docker)

```bash
# Backend
cd backend
pip install -e ".[dev]"
uvicorn cvoice_backend.api:app --reload

# Frontend (in a second terminal)
cd frontend
pip install -e ".[dev]"
streamlit run src/cvoice_frontend/app.py
```

## Team

<!-- TODO: add names and GitHub handles -->

## LLM usage

Parts of the code that are LLM generated are marked with a comment.
