import streamlit as st
from utils.auth import require_admin
from utils.db import init_db, add_item, get_all_items, delete_item
from utils.storage import save_image, save_model, delete_file

st.set_page_config(page_title="Admin", page_icon="🔒", layout="wide")

init_db()
require_admin()  # halts here until logged in

st.title("🔒 Admin")

if st.button("Log out"):
    st.session_state["is_admin"] = False
    st.rerun()

st.header("Add a new piece")

with st.form("add_item_form", clear_on_submit=True):
    title = st.text_input("Title")
    description = st.text_area("Description")
    price = st.number_input("Price ($)", min_value=0.0, step=1.0)
    image_file = st.file_uploader("Portfolio image", type=["png", "jpg", "jpeg", "webp"])
    model_file = st.file_uploader("3D file", type=["stl", "obj", "fbx", "glb", "gltf"])
    submitted = st.form_submit_button("Add to portfolio")

    if submitted:
        if not title or not image_file or not model_file:
            st.error("Title, image, and 3D file are all required.")
        else:
            image_path = save_image(image_file)
            model_path, model_format = save_model(model_file)
            add_item(title, description, price, image_path, model_path, model_format)
            st.success(f"Added '{title}'.")

st.divider()
st.header("Existing pieces")

items = get_all_items()
if not items:
    st.write("Nothing uploaded yet.")
else:
    for item in items:
        c1, c2, c3 = st.columns([1, 3, 1])
        with c1:
            if item["image_path"]:
                st.image(item["image_path"], width=100)
        with c2:
            st.write(f"**{item['title']}** — ${item['price']:,.2f}")
            st.caption(item["description"] or "")
            st.caption(f"Model: {item['model_format']}")
        with c3:
            if st.button("Delete", key=f"del_{item['id']}"):
                deleted = delete_item(item["id"])
                if deleted:
                    delete_file(deleted["image_path"])
                    delete_file(deleted["model_path"])
                st.rerun()
