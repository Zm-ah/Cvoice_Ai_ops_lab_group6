"""Entry point. Sets up navigation between the views."""
import streamlit as st

from cvoice_frontend.constants import APP_NAME

st.set_page_config(page_title=APP_NAME, layout="wide")

pages = [
    st.Page("views/upload.py", title="Upload"),
    st.Page("views/profile.py", title="Profile"),
    st.Page("views/chat.py", title="Chat"),
    st.Page("views/voice.py", title="Voice"),
    st.Page("views/job_match.py", title="Job match"),
]

st.navigation(pages).run()
