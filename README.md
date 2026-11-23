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

```bash
git clone https://github.com/Zm-ah/Cvoice_Ai_ops_lab_group6.git
cd Cvoice_Ai_ops_lab_group6

python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -e "backend[dev]" -e "frontend[dev]"
cp .env.example .env             # then fill in your own keys
```

## Run

**Locally** (two terminals, with the virtual environment activated):

```bash
# Terminal 1: backend
uvicorn cvoice_backend.api:app --reload

# Terminal 2: frontend
cd frontend
streamlit run src/cvoice_frontend/app.py
```

**With Docker** (starts both):

```bash
docker compose up --build
```

- Backend: http://localhost:8000 (API docs at `/docs`)
- Frontend: http://localhost:8501

## Adding a package

1. Add it to `dependencies` in `backend/pyproject.toml` or `frontend/pyproject.toml`.
2. Everyone runs the `pip install -e ...` line from the Setup section again.

## Working agreement

See [docs/working-agreement.md](docs/working-agreement.md).


## Team

- Zakaria
- Maarcus
- Nasser
- Zineb   