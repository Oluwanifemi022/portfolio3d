import streamlit as st
from utils.theme import theme_toggle, inject_theme
from utils.db import init_db
from utils.embeds import render_background_embed

st.set_page_config(page_title="Home", page_icon="✳", layout="wide")
dark = theme_toggle()

# Paste the real embeddable URL here once you have it from Spline's
# Export > Code Export panel (looks like https://my.spline.design/xxxx/).
# The app.spline.design/community/... browsing link won't work here.
BACKGROUND_EMBED_URL = "<iframe src='https://my.spline.design/genkubgreetingrobot-OAZ71uXekfp7swCgDp7ENqC1/' frameborder='0' width='100%' height='100%'></iframe>"
BACKGROUND_EMBED_PROVIDER = "spline"

inject_theme(dark, translucent=True)
render_background_embed(BACKGROUND_EMBED_URL, BACKGROUND_EMBED_PROVIDER, interactive=False)

init_db()

st.write("")
st.write("")
st.title("Objects worth turning around in your hands")
st.markdown(
    '<p class="muted" style="font-size:1.05rem; max-width:42ch;">'
    "A working studio's collection of 3D pieces &mdash; browse the full "
    "catalog, rotate each one, and get in touch about the pieces you "
    "want made real."
    "</p>",
    unsafe_allow_html=True,
)
st.write("")
st.page_link("pages/1_Portfolio.py", label="View the portfolio")

st.write("")
st.write("")
st.divider()
st.write("")

st.header("How it works")
c1, c2, c3 = st.columns(3, gap="large")
with c1:
    st.subheader("Browse")
    st.write("Every piece in the portfolio is interactive — drag to rotate, scroll to zoom, right there in the browser.")
with c2:
    st.subheader("Ask")
    st.write("See something you like? Reach out from the About page to talk pricing, materials, or a custom commission.")
with c3:
    st.subheader("Commission")
    st.write("Pieces here can be adapted or built from scratch to fit what you actually need.")
