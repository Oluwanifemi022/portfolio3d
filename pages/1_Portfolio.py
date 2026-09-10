import streamlit as st
from streamlit_stl import stl_from_file
from streamlit_extras.three_viewer import three_viewer
from utils.theme import theme_toggle, inject_theme
from utils.db import init_db, get_all_items, get_categories
from utils.storage import get_local_model_path
from utils.embeds import render_embed, remove_background_embed
from utils.cards import render_card_thumbnail, render_card_meta

st.set_page_config(page_title="Portfolio", page_icon="✳", layout="wide")
dark = theme_toggle()
inject_theme(dark)
remove_background_embed()  # Home's background shouldn't follow onto this page
init_db()

st.title("Portfolio")
st.markdown(
    '<p class="muted">Every piece below is interactive &mdash; drag to rotate, '
    "scroll to zoom.</p>",
    unsafe_allow_html=True,
)
st.write("")

categories = get_categories()
category_options = {"All": None}
category_options.update({c["name"]: c["id"] for c in categories})

if len(category_options) > 1:
    selected_label = st.selectbox("Filter by category", list(category_options.keys()))
    selected_id = category_options[selected_label]
else:
    selected_id = None

items = get_all_items(category_id=selected_id)

if not items:
    st.info("No pieces uploaded yet. Check back soon.")
    st.stop()

if "viewing_id" not in st.session_state:
    st.session_state["viewing_id"] = None

cols_per_row = 3
for i in range(0, len(items), cols_per_row):
    row_items = items[i : i + cols_per_row]
    cols = st.columns(cols_per_row, gap="large")
    for col, item in zip(cols, row_items):
        with col:
            with st.container(border=True):
                render_card_thumbnail(item)
                render_card_meta(item, max_description_chars=110)

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
                            item["embed_url"], item["embed_provider"], height=360
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
                            local_path = get_local_model_path(model["path"])
                            stl_from_file(
                                file_path=local_path,
                                color="#2F5D50",
                                auto_rotate=True,
                                height=360,
                            )
                        else:
                            local_path = get_local_model_path(model["path"])
                            three_viewer(
                                local_path,
                                file_format=model["format"],
                                height=360,
                                key=f"three_viewer_{item['id']}_{model['path']}",
                            )
