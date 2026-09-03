import streamlit as st
from streamlit_stl import stl_from_file
from utils.db import init_db, get_all_items

st.set_page_config(page_title="3D Portfolio", page_icon="🎨", layout="wide")

init_db()

st.title("🎨 3D Portfolio")
st.caption("Browse the collection. Click a piece to view it in 3D.")

items = get_all_items()

if not items:
    st.info("No pieces uploaded yet. Check back soon.")
    st.stop()

# Track which item is currently expanded for 3D viewing
if "viewing_id" not in st.session_state:
    st.session_state["viewing_id"] = None

cols_per_row = 3
for i in range(0, len(items), cols_per_row):
    row_items = items[i : i + cols_per_row]
    cols = st.columns(cols_per_row)
    for col, item in zip(cols, row_items):
        with col:
            if item["image_path"]:
                st.image(item["image_path"], use_container_width=True)
            st.subheader(item["title"])
            if item["price"] is not None:
                st.write(f"**${item['price']:,.2f}**")
            st.write(item["description"] or "")

            if st.button("View in 3D", key=f"view_{item['id']}"):
                st.session_state["viewing_id"] = (
                    None
                    if st.session_state["viewing_id"] == item["id"]
                    else item["id"]
                )

            if st.session_state["viewing_id"] == item["id"] and item["model_path"]:
                st.caption("Drag to rotate · scroll to zoom")
                # streamlit-stl currently renders .stl files. For other
                # formats (glb/obj/fbx) swap in three_viewer from
                # streamlit_extras - see README for the one-line change.
                if item["model_format"] == ".stl":
                    stl_from_file(
                        file_path=item["model_path"],
                        color="#c9c9c9",
                        auto_rotate=True,
                        height=400,
                    )
                else:
                    st.warning(
                        f"Preview for {item['model_format']} files: "
                        "wire up streamlit_extras.three_viewer here "
                        "(see README)."
                    )
