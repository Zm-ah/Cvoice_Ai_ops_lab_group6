FROM python:3.11-slim

WORKDIR /app

COPY frontend/pyproject.toml ./pyproject.toml
COPY frontend/src ./src
COPY frontend/.streamlit ./.streamlit
RUN pip install --no-cache-dir .

EXPOSE 8501
CMD ["streamlit", "run", "src/cvoice_frontend/app.py", "--server.address=0.0.0.0", "--server.port=8501"]
