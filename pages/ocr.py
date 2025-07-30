from io import BytesIO
from typing import TYPE_CHECKING

import ocrmypdf
import pdfplumber
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer

from utils.session_state_keys import PDF_FILE_KEY, UPLOADED_FILE_KEY
from utils.slider import SliderState

if TYPE_CHECKING:
    from streamlit.runtime.uploaded_file_manager import UploadedFile

_OCR_TEXT_KEY = "_ocr_text"
_OCR_SLIDER_KEY = "_ocr_slider"


@st.cache_data(hash_funcs={pdfplumber.PDF: lambda x: x.stream})
def extract_text(pdf: pdfplumber.PDF) -> list[str]:
    text = []
    for page in pdf.pages:
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


pdf: pdfplumber.PDF = st.session_state.get(PDF_FILE_KEY, None)
uploaded_file: "UploadedFile" = st.session_state.get(UPLOADED_FILE_KEY, None)
text: list[str] = st.session_state.get(_OCR_TEXT_KEY, None)
slider: SliderState = st.session_state.get(_OCR_SLIDER_KEY, None)


with st.sidebar:
    if st.button("Extract Text", disabled=pdf is None):
        if st.session_state.get("_ocr_do_ocr", False):
            buffer = BytesIO()
            ocrmypdf.ocr(
                BytesIO(uploaded_file.getvalue()),
                buffer,
                progress_bar=False,
                skip_text=True,
            )
            pdf: pdfplumber.PDF = pdfplumber.open(buffer)

        text = extract_text(pdf)
        st.session_state[_OCR_TEXT_KEY] = text
        st.session_state[_OCR_SLIDER_KEY] = SliderState(text)
        st.rerun()
    # config
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
                file_name=f"{uploaded_file.name.rsplit('.', maxsplit=-1)[0]}_page_{slider.current_page + 1}.txt",
                icon=":material/download:",
                use_container_width=True,
                on_click="ignore",
            )
        with cols[1]:
            st.download_button(
                "File",
                data=download_full_text(text),
                file_name=f"{uploaded_file.name.rsplit('.', maxsplit=-1)[0]}.txt",
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
            uploaded_file.getvalue(),
            render_text=True,
            pages_to_render=[slider.current_page + 1],
            zoom_level=1.25,
        )
    st.code(text[slider.current_page], language=None)


if text is not None:
    viewer_fragment()
