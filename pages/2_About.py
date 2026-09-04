import streamlit as st
from utils.theme import inject_theme

st.set_page_config(page_title="About", page_icon="✳", layout="wide")
inject_theme()

st.title("About")

st.write("")
st.markdown(
    """
This is placeholder copy &mdash; replace it with your own story.

Say what you make, how you make it, and why someone should care.
A sentence or two on your process (the software, the materials, the
route from idea to finished object) goes a long way toward making the
portfolio feel like a real studio rather than a template.
"""
)

st.write("")
st.subheader("Get in touch")
st.markdown(
    """
Add your real contact details here &mdash; an email address, a form, or a
link to whichever platform you actually want inquiries to land on.
"""
)
