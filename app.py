import streamlit as st
from utils.theme import theme_toggle, inject_theme
from utils.db import init_db, get_all_items
from utils.embeds import render_background_embed
from utils.cards import render_card_thumbnail, render_card_meta

st.set_page_config(page_title="Home", page_icon="✳", layout="wide")
dark = theme_toggle()

BACKGROUND_EMBED_URL = "https://my.spline.design/genkubgreetingrobot-OAZ71uXekfp7swCgDp7ENqC1/"
BACKGROUND_EMBED_PROVIDER = "spline"

inject_theme(dark, translucent=True)
render_background_embed(BACKGROUND_EMBED_URL, BACKGROUND_EMBED_PROVIDER, interactive=False)

init_db()

# ---------- Hero ----------

st.write("")
st.markdown(
    """
    <div class="hero-panel" style="max-width:44ch;">
        <h1>See the piece before it's made</h1>
        <p class="muted" style="font-size:1.05rem;">
            Every piece in this portfolio renders in three dimensions,
            right in your browser. Rotate it, study it from every side,
            then get in touch about having it made.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.write("")
st.page_link("pages/1_Portfolio.py", label="View the full portfolio")

st.write("")
st.write("")

# ---------- Featured work ----------

items = get_all_items()[:6]

if items:
    st.divider()
    st.header("Recent work")
    st.markdown(
        '<p class="muted">A few pieces from the full portfolio.</p>',
        unsafe_allow_html=True,
    )
    st.write("")

    cols_per_row = 3
    for i in range(0, len(items), cols_per_row):
        row_items = items[i : i + cols_per_row]
        cols = st.columns(cols_per_row, gap="large")
        for col, item in zip(cols, row_items):
            with col:
                render_card_thumbnail(item)
                render_card_meta(item)
                if st.button("View", key=f"home_view_{item['id']}"):
                    st.session_state["viewing_id"] = item["id"]
                    st.switch_page("pages/1_Portfolio.py")

st.write("")
st.write("")
st.divider()
st.write("")

# ---------- How this works ----------

st.header("How this works")
c1, c2, c3 = st.columns(3, gap="large")
with c1:
    st.markdown(
        """
        <div class="info-card">
            <h3>Browse</h3>
            <p>Drag to rotate, scroll to zoom — every piece is
            interactive, right here in the browser.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        """
        <div class="info-card">
            <h3>Ask</h3>
            <p>See something you like? Reach out from the About page
            to talk pricing, materials, or timeline.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c3:
    st.markdown(
        """
        <div class="info-card">
            <h3>Commission</h3>
            <p>Pieces here can be adapted, resized, or built from
            scratch around what you actually need.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
