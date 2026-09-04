import streamlit as st
from utils.theme import inject_theme
from utils.db import init_db
from utils.embeds import render_embed

st.set_page_config(page_title="Home", page_icon="✳", layout="wide")
inject_theme()
init_db()

# Swap this for your own Spline scene's public embed URL
# (Spline: Export > Code Export > Public URL). Sketchfab works too -
# just switch the provider argument to "sketchfab" and use a
# sketchfab.com/.../embed URL instead.
FEATURED_EMBED_URL = "https://my.spline.design/replaceme-00000000000000000000000000000000/"
FEATURED_EMBED_PROVIDER = "spline"

left, right = st.columns([0.45, 0.55], gap="large")

with left:
    st.write("")
    st.write("")
    st.title("Objects worth turning around in your hands")
    st.markdown(
        '<p class="muted" style="font-size:1.05rem; max-width:38ch;">'
        "A working studio's collection of 3D pieces &mdash; browse the full "
        "catalog, rotate each one, and get in touch about the pieces you "
        "want made real."
        "</p>",
        unsafe_allow_html=True,
    )
    st.write("")
    st.page_link("pages/1_Portfolio.py", label="View the portfolio")

with right:
    try:
        render_embed(FEATURED_EMBED_URL, FEATURED_EMBED_PROVIDER, height=480)
    except Exception:
        st.info("Add your Spline or Sketchfab embed URL in Home.py to feature a piece here.")
