"""Shared constants. Define a value here once and reuse it everywhere."""
import os

APP_NAME = "cvoice"
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Reading several docs, embedding them takes longer than a normal call.
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "60"))
UPLOAD_TIMEOUT = float(os.getenv("UPLOAD_TIMEOUT", "180"))

ALLOWED_UPLOAD_TYPES = ["pdf", "txt", "md"]

# st.session_state keys, in one place so that a typo cannot create a second key.
SESSION_PROFILE_ID = "profile_id"
SESSION_SOURCES = "profile_sources"