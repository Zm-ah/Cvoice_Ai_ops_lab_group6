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

## Setup

Install [uv](https://docs.astral.sh/uv/) first. Then:

```bash
git clone https://github.com/Zm-ah/Cvoice_Ai_ops_lab_group6.git
cd Cvoice_Ai_ops_lab_group6

uv sync --all-packages
uv run pre-commit install        # runs ruff automatically before each commit
cp .env.example .env             # then fill in your own keys
```

`uv sync --all-packages` creates one `.venv` in the root and installs both `backend` and `frontend`. Run it again after every `git pull`.

## Run

**Locally** (two terminals):

```bash
# Terminal 1: backend
uv run uvicorn cvoice_backend.api:app --reload

# Terminal 2: frontend
cd frontend
uv run streamlit run src/cvoice_frontend/app.py
```

**With Docker** (starts both):

```bash
docker compose up --build
```

- Backend: http://localhost:8000 (API docs at `/docs`)
- Frontend: http://localhost:8501

## Adding a package

```bash
uv add --package cvoice-backend <package>    # or cvoice-frontend
```

Commit both the `pyproject.toml` and `uv.lock`. Everyone else runs `uv sync --all-packages` after pulling.

## Working agreement

See [docs/working-agreement.md](docs/working-agreement.md).


## Team

- Zakaria
- Maarcus
- Nasser
- Zineb   