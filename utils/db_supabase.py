"""
Database backed by Supabase Postgres (via the Supabase client's table
API, over HTTPS - no raw Postgres connection needed).

Tables are created once via the Supabase SQL editor (see README for
the exact SQL) rather than in code, since there's no local file to
auto-migrate the way SQLite could.

Requires supabase_url and supabase_key (service_role key) in
.streamlit/secrets.toml.
"""

import streamlit as st
from supabase import create_client

_client = None


def _get_client():
    global _client
    if _client is None:
        _client = create_client(st.secrets["supabase_url"], st.secrets["supabase_key"])
    return _client


def init_db():
    # Tables live in Supabase already (created once via the SQL
    # editor - see README). Just confirm we can reach the project.
    _get_client()


# ---------- Categories ----------

def add_category(name: str) -> int:
    name = name.strip()
    client = _get_client()
    existing = client.table("categories").select("id").eq("name", name).execute()
    if existing.data:
        return existing.data[0]["id"]
    result = client.table("categories").insert({"name": name}).execute()
    return result.data[0]["id"]


def get_categories():
    client = _get_client()
    result = client.table("categories").select("id, name").order("name").execute()
    return result.data


def delete_category(category_id: int):
    """Deletes the category only. The items table's category_id
    column is ON DELETE SET NULL, so items survive as uncategorized."""
    _get_client().table("categories").delete().eq("id", category_id).execute()


# ---------- Items ----------

def add_item(title, description, price, embed_url, embed_provider,
             image_paths, model_entries, category_id=None):
    client = _get_client()
    result = client.table("items").insert({
        "title": title,
        "description": description,
        "price": price,
        "embed_url": embed_url or None,
        "embed_provider": embed_provider or None,
        "category_id": category_id,
    }).execute()
    item_id = result.data[0]["id"]

    if image_paths:
        client.table("item_images").insert(
            [{"item_id": item_id, "path": p} for p in image_paths]
        ).execute()
    if model_entries:
        client.table("item_models").insert(
            [{"item_id": item_id, "path": p, "format": fmt} for p, fmt in model_entries]
        ).execute()

    return item_id


def _attach_related(client, item):
    images = client.table("item_images").select("path").eq("item_id", item["id"]).execute().data
    models = client.table("item_models").select("path, format").eq("item_id", item["id"]).execute().data

    item = dict(item)
    item["image_paths"] = [r["path"] for r in images]
    item["models"] = [{"path": r["path"], "format": r["format"]} for r in models]

    item["category_name"] = None
    if item.get("category_id") is not None:
        cat = client.table("categories").select("name").eq("id", item["category_id"]).execute().data
        if cat:
            item["category_name"] = cat[0]["name"]

    return item


def get_all_items(category_id=None):
    client = _get_client()
    query = client.table("items").select("*").order("created_at", desc=True)
    if category_id is not None:
        query = query.eq("category_id", category_id)
    rows = query.execute().data
    return [_attach_related(client, row) for row in rows]


def get_item(item_id):
    client = _get_client()
    rows = client.table("items").select("*").eq("id", item_id).execute().data
    return _attach_related(client, rows[0]) if rows else None


def delete_item(item_id):
    """Returns the deleted item (with its file paths) so the caller
    can also remove the underlying files from storage."""
    item = get_item(item_id)
    if item:
        _get_client().table("items").delete().eq("id", item_id).execute()
    return item


# ---------- Gallery ----------

def add_gallery_image(path: str, caption: str = None) -> int:
    result = _get_client().table("gallery_images").insert(
        {"path": path, "caption": caption}
    ).execute()
    return result.data[0]["id"]


def get_gallery_images():
    result = (
        _get_client()
        .table("gallery_images")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )
    return result.data


def delete_gallery_image(image_id: int):
    client = _get_client()
    rows = client.table("gallery_images").select("*").eq("id", image_id).execute().data
    client.table("gallery_images").delete().eq("id", image_id).execute()
    return rows[0] if rows else None
