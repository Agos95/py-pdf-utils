from io import BytesIO

import ocrmypdf
import pdfplumber
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer

from utils.slider import SliderState

_OCR_TEXT_KEY = "_ocr_text"
_OCR_SLIDER_KEY = "_ocr_slider"


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


@st.cache_data
def download_full_text(text: list[str]) -> str:
    full_txt = ""
    for i, page in enumerate(text):
        full_txt += "=" * 50 + f" Page {i + 1} " + "=" * 50 + "\n\n"
        full_txt += page
        full_txt += "\n\n"
    return full_txt


pdf = st.session_state.get("pdf", None)
text: list[str] = st.session_state.get(_OCR_TEXT_KEY, None)
slider: SliderState = st.session_state.get(_OCR_SLIDER_KEY, None)


with st.sidebar:
    st.divider()
    if st.button("Extract Text", disabled=pdf is None):
        pdf = BytesIO(pdf.getvalue())
        if st.session_state.get("_ocr_do_ocr", False):
            buffer = BytesIO()
            ocrmypdf.ocr(pdf, buffer, progress_bar=False, skip_text=True)
            pdf = buffer

        text = extract_text(pdf)
        st.session_state[_OCR_TEXT_KEY] = text
        st.session_state[_OCR_SLIDER_KEY] = SliderState(text)
        st.rerun()
    st.subheader("Configuration", divider=None)
    st.checkbox(
        "Perform OCR",
        value=True,
        help="Extract text using `ocrmypdf` if the pdf is scanned",
        key="_ocr_do_ocr",
    )


@st.fragment
def download_fragment():
    with st.container():
        cols = st.columns(2)
        with cols[0]:
            st.download_button(
                "Page",
                data=text[slider.current_page],
                file_name=f"{pdf.name.rsplit('.', maxsplit=-1)[0]}_page_{slider.current_page + 1}.txt",
                icon=":material/download:",
                use_container_width=True,
                on_click="ignore",
            )
        with cols[1]:
            st.download_button(
                "File",
                data=download_full_text(text),
                file_name=f"{pdf.name.rsplit('.', maxsplit=-1)[0]}.txt",
                icon=":material/download:",
                use_container_width=True,
                on_click="ignore",
            )


@st.fragment
def viewer_fragment():
    controls_cols, downloads_cols = st.columns([0.4, 0.6])
    with controls_cols:
        with st.container():
            cols = st.columns([0.15, 0.7, 0.15])
            with cols[0]:
                if st.button(
                    "", icon=":material/chevron_left:", use_container_width=True
                ):
                    slider.prev_page()
                    st.rerun(scope="fragment")

            with cols[1]:
                st.html(f"<center> Page {slider.current_page + 1}</center>")

            with cols[2]:
                if st.button(
                    "", icon=":material/chevron_right:", use_container_width=True
                ):
                    slider.next_page()
                    st.rerun(scope="fragment")

    if text is not None:
        with downloads_cols:
            download_fragment()

    with st.expander("PDF"):
        pdf_viewer(
            pdf.getvalue(),
            render_text=True,
            pages_to_render=[slider.current_page + 1],
            zoom_level=1.25,
        )
    st.code(text[slider.current_page], language=None)


if text is not None:
    viewer_fragment()
