import streamlit as st
from streamlit_pdf_viewer import pdf_viewer

pdf = st.session_state["pdf"] if "pdf" in st.session_state else None

if pdf is not None:
    pdf = pdf.getvalue()
    pdf_viewer(pdf, render_text=True, zoom_level=1.25)
