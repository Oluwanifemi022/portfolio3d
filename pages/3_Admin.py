import streamlit as st
from utils.theme import theme_toggle, inject_theme
from utils.auth import require_admin
from utils.db import (
    init_db, add_item, get_all_items, delete_item,
    add_category, get_categories, delete_category,
)
from utils.storage import save_images, save_models, delete_file
from utils.embeds import remove_background_embed

st.set_page_config(page_title="Admin", page_icon="✳", layout="wide")
dark = theme_toggle()
inject_theme(dark)
remove_background_embed()

init_db()
require_admin()  # halts here until logged in

st.title("Admin")

if st.button("Log out"):
    st.session_state["is_admin"] = False
    st.rerun()

# ---------- Categories ----------

st.header("Categories")

categories = get_categories()

cat_col1, cat_col2 = st.columns([0.7, 0.3])
with cat_col1:
    new_category = st.text_input("New category name", key="new_category_input")
with cat_col2:
    st.write("")
    st.write("")
    if st.button("Add category"):
        if new_category.strip():
            try:
                add_category(new_category)
                st.toast(f"Added category '{new_category.strip()}'", icon="✅")
                st.rerun()
            except Exception as e:
                st.error(f"Couldn't add that category: {e}")
        else:
            st.error("Category name can't be empty.")

if categories:
    st.caption("Existing categories:")
    for cat in categories:
        c1, c2 = st.columns([0.85, 0.15])
        with c1:
            st.write(cat["name"])
        with c2:
            if st.button("Remove", key=f"del_cat_{cat['id']}"):
                delete_category(cat["id"])
                st.toast(f"Removed category '{cat['name']}'", icon="🗑️")
                st.rerun()
else:
    st.caption("No categories yet — add one above, or leave pieces uncategorized.")

st.divider()

# ---------- Add a piece ----------

st.header("Add a new piece")

category_options = {"Uncategorized": None}
category_options.update({c["name"]: c["id"] for c in categories})

with st.form("add_item_form", clear_on_submit=True):
    title = st.text_input("Title")
    description = st.text_area("Description")
    price = st.number_input("Price ($)", min_value=0.0, step=1.0)
    category_label = st.selectbox("Category", list(category_options.keys()))

    image_files = st.file_uploader(
        "Portfolio images (you can select several)",
        type=["png", "jpg", "jpeg", "webp"],
        accept_multiple_files=True,
    )
    model_files = st.file_uploader(
        "3D files (you can select several)",
        type=["stl", "obj", "fbx", "glb", "gltf"],
        accept_multiple_files=True,
    )

    st.caption(
        "Optional: instead of (or alongside) an uploaded 3D file, you can "
        "link a hosted Spline or Sketchfab scene."
    )
    embed_col1, embed_col2 = st.columns([0.7, 0.3])
    with embed_col1:
        embed_url = st.text_input("Spline / Sketchfab embed URL (optional)")
    with embed_col2:
        embed_provider = st.selectbox("Provider", ["spline", "sketchfab"])

    submitted = st.form_submit_button("Add to portfolio")

    if submitted:
        if not title or not image_files:
            st.error("Title and at least one image are required.")
        elif not model_files and not embed_url:
            st.error("Add at least one 3D file, or an embed URL.")
        else:
            try:
                image_paths = save_images(image_files)
                model_entries = save_models(model_files) if model_files else []
                category_id = category_options[category_label]
                add_item(
                    title, description, price,
                    embed_url, embed_provider if embed_url else None,
                    image_paths, model_entries,
                    category_id=category_id,
                )
                st.toast(f"Added '{title}' to the portfolio", icon="✅")
                st.rerun()
            except Exception as e:
                st.error(f"Something went wrong while saving this piece: {e}")

st.divider()
st.header("Existing pieces")

items = get_all_items()
if not items:
    st.write("Nothing uploaded yet.")
else:
    for item in items:
        c1, c2, c3 = st.columns([1, 3, 1])
        with c1:
            if item["image_paths"]:
                st.image(item["image_paths"][0], width=100)
        with c2:
            st.write(f"**{item['title']}** — ${item['price']:,.2f}")
            if item["category_name"]:
                st.caption(f"Category: {item['category_name']}")
            st.caption(item["description"] or "")
            details = f"{len(item['image_paths'])} image(s), {len(item['models'])} model(s)"
            if item["embed_url"]:
                details += f", {item['embed_provider']} embed"
            st.caption(details)
        with c3:
            if st.button("Delete", key=f"del_{item['id']}"):
                deleted = delete_item(item["id"])
                if deleted:
                    for path in deleted["image_paths"]:
                        delete_file(path)
                    for model in deleted["models"]:
                        delete_file(model["path"])
                st.rerun()
