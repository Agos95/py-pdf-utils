import streamlit as st

from utils.slider import SliderState

images = [
    "https://placehold.co/600x400/FF0000/FFFFFF?text=Red",
    "https://placehold.co/600x400/00FF00/000000?text=Green",
    "https://placehold.co/600x400/0000FF/FFFFFF?text=Blue",
    "https://placehold.co/600x400/FFD700/000000?text=Gold",
    "https://placehold.co/600x400/C0C0C0/000000?text=Silver",
    "https://placehold.co/600x400/800080/FFFFFF?text=Purple",
    "https://placehold.co/600x400/FFA500/000000?text=Orange",
]

if "_slider" not in st.session_state:
    st.session_state["_slider"] = SliderState(images)


@st.fragment
def viewer():
    slider: SliderState = st.session_state["_slider"]

    # --- Navigation Buttons ---
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if st.button("⬅️ Previous", key="prev_button"):
            slider.prev_page()

    with col3:
        if st.button("Next ➡️", key="next_button"):
            slider.next_page()

    with col2:
        st.markdown(f"Page {slider.current_page}")

    st.image(images[slider.current_page])


viewer()
