"""
File storage backed by Supabase Storage.

Uploads go to a private bucket (not local disk), so files survive
app restarts/redeploys. Images/models are read back via short-lived
signed URLs rather than permanent public links - see README for why.

Requires supabase_url and supabase_key (the service_role key, not the
anon key - this code runs entirely server-side in Streamlit, so it's
safe to use the more privileged key here) in .streamlit/secrets.toml.
"""

import os
import uuid
import tempfile
import streamlit as st
from supabase import create_client

BUCKET = "portfolio-files"
SIGNED_URL_EXPIRY_SECONDS = 3600  # 1 hour

_client = None


def _get_client():
    global _client
    if _client is None:
        _client = create_client(st.secrets["supabase_url"], st.secrets["supabase_key"])
    return _client


def _unique_name(original_filename: str) -> str:
    ext = os.path.splitext(original_filename)[1]
    return f"{uuid.uuid4().hex}{ext}"


def save_image(uploaded_file) -> str:
    key = f"images/{_unique_name(uploaded_file.name)}"
    _get_client().storage.from_(BUCKET).upload(
        key,
        bytes(uploaded_file.getbuffer()),
        {"content-type": uploaded_file.type or "application/octet-stream"},
    )
    return key


def save_images(uploaded_files) -> list[str]:
    return [save_image(f) for f in uploaded_files]


def save_model(uploaded_file) -> tuple[str, str]:
    ext = os.path.splitext(uploaded_file.name)[1].lower()
    key = f"models/{_unique_name(uploaded_file.name)}"
    _get_client().storage.from_(BUCKET).upload(
        key, bytes(uploaded_file.getbuffer()), {"content-type": "application/octet-stream"}
    )
    return key, ext


def save_models(uploaded_files) -> list[tuple[str, str]]:
    return [save_model(f) for f in uploaded_files]


def delete_file(key: str):
    if key:
        _get_client().storage.from_(BUCKET).remove([key])


def get_display_url(key: str):
    """Signed URL for showing an image (st.image accepts URLs directly)."""
    if not key:
        return None
    result = _get_client().storage.from_(BUCKET).create_signed_url(
        key, SIGNED_URL_EXPIRY_SECONDS
    )
    return result.get("signedURL") or result.get("signed_url")


def get_local_model_path(key: str):
    """streamlit-stl reads from a local file path, not a URL - so
    download the model into a local temp cache the first time it's
    viewed, then reuse that cached copy."""
    if not key:
        return None
    cache_dir = os.path.join(tempfile.gettempdir(), "portfolio3d_model_cache")
    os.makedirs(cache_dir, exist_ok=True)
    local_path = os.path.join(cache_dir, key.replace("/", "_"))
    if not os.path.exists(local_path):
        data = _get_client().storage.from_(BUCKET).download(key)
        with open(local_path, "wb") as f:
            f.write(data)
    return local_path
