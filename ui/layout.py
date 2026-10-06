import streamlit as st

def render_header():
    st.title("Smart Time Format Validator")
    st.caption(
        "Two-layer pattern recognition: strict formal automaton (Layer 1) "
        "+ lexical normalization (Layer 2)."
    )