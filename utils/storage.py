"""
Picks the file storage backend automatically:
  - Supabase Storage, if supabase_url and supabase_key are set in
    .streamlit/secrets.toml
  - otherwise, the local OS temp directory (files survive only until
    the app restarts)

The rest of the app imports from here (`from utils.storage import ...`)
and never needs to know which backend is active.
"""

import streamlit as st


def _use_supabase() -> bool:
    try:
        return bool(st.secrets.get("supabase_url")) and bool(st.secrets.get("supabase_key"))
    except Exception:
        return False


if _use_supabase():
    from utils.storage_supabase import (
        save_image, save_images, save_model, save_models,
        delete_file, get_display_url, get_local_model_path,
    )
else:
    from utils.storage_local import (
        save_image, save_images, save_model, save_models,
        delete_file, get_display_url, get_local_model_path,
    )
