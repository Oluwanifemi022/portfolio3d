import streamlit as st
from utils.theme import theme_toggle, inject_theme
from utils.db import init_db, get_gallery_images
from utils.storage import get_display_url
from utils.embeds import remove_background_embed

st.set_page_config(page_title="Gallery", page_icon="✳", layout="wide")
dark = theme_toggle()
inject_theme(dark)
remove_background_embed()
init_db()

st.title("Gallery")
st.markdown(
    '<p class="muted">Process shots, references, and pieces that don\'t need a '
    "full writeup — just a look.</p>",
    unsafe_allow_html=True,
)
st.write("")

images = get_gallery_images()

if not images:
    st.info("Nothing in the gallery yet.")
    st.stop()

cols_per_row = 4
for i in range(0, len(images), cols_per_row):
    row = images[i : i + cols_per_row]
    cols = st.columns(cols_per_row, gap="small")
    for col, img in zip(cols, row):
        with col:
            url = get_display_url(img["path"])
            st.markdown(
                f'<div class="thumb" style="height:220px;">'
                f'<img src="{url}" alt="{img.get("caption") or "Gallery image"}" />'
                f"</div>",
                unsafe_allow_html=True,
            )
            if img.get("caption"):
                st.markdown(
                    f'<p class="muted" style="margin-top:-0.4rem;">{img["caption"]}</p>',
                    unsafe_allow_html=True,
                )
