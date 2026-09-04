import streamlit as st
from streamlit_stl import stl_from_file
from utils.theme import inject_theme
from utils.db import init_db, get_all_items
from utils.embeds import render_embed

st.set_page_config(page_title="Portfolio", page_icon="✳", layout="wide")
inject_theme()
init_db()

st.title("Portfolio")
st.markdown(
    '<p class="muted">Every piece below is interactive &mdash; drag to rotate, '
    "scroll to zoom.</p>",
    unsafe_allow_html=True,
)
st.write("")

items = get_all_items()

if not items:
    st.info("No pieces uploaded yet. Check back soon.")
    st.stop()

if "viewing_id" not in st.session_state:
    st.session_state["viewing_id"] = None

cols_per_row = 2
for i in range(0, len(items), cols_per_row):
    row_items = items[i : i + cols_per_row]
    cols = st.columns(cols_per_row, gap="large")
    for col, item in zip(cols, row_items):
        with col:
            with st.container(border=True):
                if item["image_paths"]:
                    st.image(item["image_paths"][0], use_container_width=True)
                    if len(item["image_paths"]) > 1:
                        st.image(item["image_paths"][1:], width=90)

                st.subheader(item["title"])
                if item["price"] is not None:
                    st.markdown(
                        f'<span class="price-tag">${item["price"]:,.2f}</span>',
                        unsafe_allow_html=True,
                    )
                st.write(item["description"] or "")

                has_3d = item["embed_url"] or item["models"]
                if has_3d:
                    if st.button("View in 3D", key=f"view_{item['id']}"):
                        st.session_state["viewing_id"] = (
                            None
                            if st.session_state["viewing_id"] == item["id"]
                            else item["id"]
                        )

                if st.session_state["viewing_id"] == item["id"]:
                    if item["embed_url"]:
                        render_embed(
                            item["embed_url"], item["embed_provider"], height=380
                        )
                    elif item["models"]:
                        model = item["models"][0]
                        if len(item["models"]) > 1:
                            labels = [
                                f"Model {i+1} ({m['format']})"
                                for i, m in enumerate(item["models"])
                            ]
                            choice = st.selectbox(
                                "Choose a file", labels, key=f"model_pick_{item['id']}"
                            )
                            model = item["models"][labels.index(choice)]

                        if model["format"] == ".stl":
                            stl_from_file(
                                file_path=model["path"],
                                color="#2F5D50",
                                auto_rotate=True,
                                height=380,
                            )
                        else:
                            st.warning(
                                f"Preview for {model['format']} files needs "
                                "streamlit_extras.three_viewer wired in - "
                                "see README."
                            )
