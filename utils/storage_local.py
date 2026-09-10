"""
File storage layer.

Writes to the system temp directory rather than inside the app's own
folder - on Streamlit Community Cloud the cloned repo folder can be
read-only, so writing there fails. The OS temp dir is always
writable, on Streamlit Cloud and locally alike.

This is still local-disk storage, so it's still EPHEMERAL - files are
wiped on redeploy/restart. Before real deployment, replace the bodies
of save_image/save_model with calls to a cloud bucket (S3 / Supabase
Storage / Cloudflare R2) so uploads survive restarts. Keep the
function signatures the same and nothing else in the app changes.
"""

import os
import tempfile
import uuid
import base64
import mimetypes

BASE_DIR = os.path.join(tempfile.gettempdir(), "portfolio3d_uploads")
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


def get_display_url(path: str):
    """
    Returns something an <img src="..."> tag can use directly.

    Local files aren't reachable by the browser at all (they're on
    the server's disk, not served over HTTP), so this reads the file
    and encodes it as a data: URI. That keeps the interface identical
    to the Supabase backend, which returns a signed HTTPS URL instead -
    card-rendering code elsewhere doesn't need to know which one it's
    getting.
    """
    if not path or not os.path.exists(path):
        return None
    mime_type, _ = mimetypes.guess_type(path)
    mime_type = mime_type or "application/octet-stream"
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def get_local_model_path(path: str):
    """Already a local path - nothing to download."""
    return path
