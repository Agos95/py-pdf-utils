import streamlit as st

st.set_page_config(
    page_title="PDF Utils", layout="wide", page_icon=":material/service_toolbox:"
)

with st.sidebar:
    pdf = st.file_uploader(
        "Upload PDF", type=["pdf"], key="pdf", label_visibility="collapsed"
    )

pages = [
    st.Page("pages/home.py", title="Home", icon=":material/home:", default=True),
    st.Page("pages/ocr.py", title="Classic OCR", icon=":material/document_scanner:"),
]

pg = st.navigation(pages, position="top")

pg.run()
