import pdfplumber
import streamlit as st

_IMPORT_ERROR_MESSAGE = """\
`transformers` is needed to run **Nanonets-OCR-s**.
Install it with `pip install transformers`.
"""

try:
    from transformers import AutoModelForImageTextToText, AutoProcessor, AutoTokenizer
except Exception:
    st.error(_IMPORT_ERROR_MESSAGE)
    st.stop()

_MODEL_NAME = "nanonets/Nanonets-OCR-s"


@st.cache_resource
def get_nanonets_model() -> AutoModelForImageTextToText:
    model = AutoModelForImageTextToText.from_pretrained(
        _MODEL_NAME,
        torch_dtype="auto",
        device_map="auto",
        attn_implementation="flash_attention_2",
    )
    model.eval()
    return model


@st.cache_data
def pdf2img(pdf: bytes):
    pdf: pdfplumber.PDF = pdfplumber.open(pdf)


pdf = st.session_state.get("pdf", None)

with st.sidebar:
    if st.button("Extract Text", disabled=pdf is None):
        pass
