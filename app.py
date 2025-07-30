from io import BytesIO

import pdfplumber
import streamlit as st

from utils.session_state_keys import PDF_FILE_KEY, UPLOADED_FILE_KEY

st.set_page_config(
    page_title="PDF Utils",
    layout="wide",
    page_icon=":material/service_toolbox:",
    initial_sidebar_state="expanded",
)


def clear_session_state():
    keys = [k for k in st.session_state.keys() if k.startswith("_")]
    for k in keys:
        del st.session_state[k]


with st.sidebar:
    pdf = st.file_uploader(
        "Upload PDF",
        type=["pdf"],
        key=UPLOADED_FILE_KEY,
        label_visibility="collapsed",
        on_change=clear_session_state,
    )
    if pdf is not None:
        st.session_state[PDF_FILE_KEY] = pdfplumber.open(BytesIO(pdf.getvalue()))

    st.divider()

pages = [
    st.Page("pages/home.py", title="Home", icon=":material/home:", default=True),
    st.Page("pages/ocr.py", title="Classic OCR", icon=":material/document_scanner:"),
]

pg = st.navigation(pages, position="top")

pg.run()
