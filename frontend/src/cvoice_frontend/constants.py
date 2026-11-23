"""Shared constants. Define a value here once and reuse it everywhere."""
import os

APP_NAME = "cvoice"
API_URL = os.getenv("API_URL", "http://localhost:8000")
