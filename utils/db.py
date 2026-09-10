"""
Picks the database backend automatically:
  - Supabase Postgres, if supabase_url and supabase_key are set in
    .streamlit/secrets.toml
  - otherwise, local SQLite (data survives only until the app restarts)

The rest of the app imports from here (`from utils.db import ...`)
and never needs to know which backend is active.
"""

import streamlit as st


def _use_supabase() -> bool:
    try:
        return bool(st.secrets.get("supabase_url")) and bool(st.secrets.get("supabase_key"))
    except Exception:
        return False


if _use_supabase():
    from utils.db_supabase import (
        init_db, add_category, get_categories, delete_category,
        add_item, get_all_items, get_item, delete_item,
        add_gallery_image, get_gallery_images, delete_gallery_image,
    )
    DB_PATH = None  # not applicable - data lives in Supabase, not a local file
else:
    from utils.db_local import (
        init_db, add_category, get_categories, delete_category,
        add_item, get_all_items, get_item, delete_item, DB_PATH,
        add_gallery_image, get_gallery_images, delete_gallery_image,
    )
