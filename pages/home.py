from typing import TYPE_CHECKING

import streamlit as st
from streamlit_pdf_viewer import pdf_viewer

from utils.session_state_keys import UPLOADED_FILE_KEY

if TYPE_CHECKING:
    from streamlit.runtime.uploaded_file_manager import UploadedFile

pdf: "UploadedFile" = st.session_state.get(UPLOADED_FILE_KEY, None)

if pdf is not None:
    pdf_viewer(pdf.getvalue(), render_text=True, zoom_level=1.25)
