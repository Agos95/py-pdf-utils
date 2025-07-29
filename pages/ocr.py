from io import BytesIO

import ocrmypdf
import pdfplumber
import streamlit as st


@st.cache_data
def extract_text(pdf: BytesIO) -> list[str]:
    text = []
    with pdfplumber.open(pdf) as doc:
        for page in doc.pages:
            text.append(
                page.extract_text(
                    layout=True,
                    use_text_flow=False,
                ),
            )
    return text


with st.sidebar:
    st.subheader("Configuration", divider=None)
    do_ocr = st.checkbox(
        "Perform OCR",
        value=True,
        help="Extract text using `ocrmypdf` if the pdf is scanned",
    )


pdf = st.session_state.get("pdf", None)

cols = st.columns(2)
with cols[0]:
    prev_page = st.button("Prev")

with cols[1]:
    next_page = st.button("Next")

if pdf is not None:
    pdf = BytesIO(pdf.getvalue())
    if st.button("Extract Text"):
        if do_ocr:
            buffer = BytesIO()
            ocrmypdf.ocr(pdf, buffer, progress_bar=False, skip_text=True)
            pdf = buffer

        text = extract_text(pdf)

        st.code("\n\n".join(text), language=None)
