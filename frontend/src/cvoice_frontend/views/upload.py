"""View: Upload."""
import streamlit as st

from cvoice_frontend import api_client
from cvoice_frontend.api_client import ApiError
from cvoice_frontend.constants import (
    ALLOWED_UPLOAD_TYPES,
    SESSION_PROFILE_ID,
    SESSION_SOURCES,
)

st.title("Upload")
st.write(
    "Upload a CV, and a cover letter if you have one. A longer, more descriptive "
    "CV gives the bot more to work with than a one-pager."
)

uploads = st.file_uploader(
    "Documents",
    type=ALLOWED_UPLOAD_TYPES,
    accept_multiple_files=True,
    help="PDF, TXT or Markdown. A scanned PDF without a text layer will not work.",
)

current_profile = st.session_state.get(SESSION_PROFILE_ID)
replace = False
if current_profile:
    st.caption(f"Active profile: `{current_profile}`")
    replace = st.checkbox(
        "Replace the active profile instead of creating a new one",
        help="Keeps the same profile id and deletes the old passages first.",
    )

if st.button("Upload and index", type="primary", disabled=not uploads):
    files = [(upload.name, upload.getvalue()) for upload in uploads or []]

    with st.spinner("Reading the documents and creating embeddings…"):
        try:
            response = api_client.upload_documents(
                files, profile_id=current_profile if replace else None
            )
        except ApiError as exc:
            st.error(str(exc))
            st.stop()

    st.session_state[SESSION_PROFILE_ID] = response["profile_id"]
    st.session_state[SESSION_SOURCES] = response["sources"]

    st.success(
        f"Indexed {len(response['sources'])} document(s) into "
        f"{response['chunk_count']} searchable passages "
        f"({response['characters']:,} characters)."
    )
    st.caption(f"Profile id: `{response['profile_id']}`")