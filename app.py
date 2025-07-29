from io import BytesIO

import pdfplumber
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer

st.set_page_config(page_title="PDF Utils", layout="wide")

pdfplumber_page = st.Page("pages/pdfplumber.py")
ocr_page = st.Page("pages/ocr.py")

pg = st.navigation([pdfplumber_page, ocr_page], position="top")


# with st.sidebar:
#     pdf = st.file_uploader("Upload PDF", type=["pdf"])

# tab_pdf, tab_pdfplumber = st.tabs(["PDF", "PDFPlumber"])

# if pdf is not None:
#     pdf = pdf.getvalue()
#     with tab_pdf:
#         pdf_viewer(pdf, render_text=True)

#     with tab_pdfplumber:
#         if st.button("Extract Text"):
#             doc = pdfplumber.open(BytesIO(pdf))
#             text = ""
#             for page in doc.pages:
#                 text += page.extract_text(layout=True, use_text_flow=False)

#             st.markdown(f"```\n{text}\n```")


pg.run()
