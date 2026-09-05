"""
File storage layer.

Local-disk implementation for development. Streamlit Community Cloud's
filesystem is EPHEMERAL - files here are wiped on redeploy/restart.
Before deploying, replace the bodies of save_image/save_model with
calls to a cloud bucket (S3 / Supabase Storage / Cloudflare R2). Keep
the function signatures the same and nothing else in the app changes.
"""

import os
import uuid

BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "uploads")
BASE_DIR = os.path.abspath(BASE_DIR)
IMAGES_DIR = os.path.join(BASE_DIR, "images")
MODELS_DIR = os.path.join(BASE_DIR, "models")

os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)


def _unique_name(original_filename: str) -> str:
    ext = os.path.splitext(original_filename)[1]
    return f"{uuid.uuid4().hex}{ext}"


def save_image(uploaded_file) -> str:
    filename = _unique_name(uploaded_file.name)
    path = os.path.join(IMAGES_DIR, filename)
    with open(path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return path


def save_images(uploaded_files) -> list[str]:
    return [save_image(f) for f in uploaded_files]


def save_model(uploaded_file) -> tuple[str, str]:
    filename = _unique_name(uploaded_file.name)
    ext = os.path.splitext(uploaded_file.name)[1].lower()
    path = os.path.join(MODELS_DIR, filename)
    with open(path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return path, ext


def save_models(uploaded_files) -> list[tuple[str, str]]:
    return [save_model(f) for f in uploaded_files]


def delete_file(path: str):
    if path and os.path.exists(path):
        os.remove(path)
