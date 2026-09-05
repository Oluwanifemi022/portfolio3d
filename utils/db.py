"""
Database layer for portfolio items and categories.

Schema:
  categories   - id, name
  items        - one row per project, optional category_id
  item_images  - many per item
  item_models  - many per item

SQLite for local dev - see README for swapping to hosted Postgres
before deploy.
"""

import sqlite3
import os
from contextlib import contextmanager
from datetime import datetime, timezone

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "portfolio.db")
DB_PATH = os.path.abspath(DB_PATH)


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def _ensure_column(conn, table, column, coltype):
    """Add a column to an existing table if it isn't there yet. Lets
    the schema evolve without wiping data from an older deploy."""
    existing = {row["name"] for row in conn.execute(f"PRAGMA table_info({table})")}
    if column not in existing:
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {coltype}")


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                price REAL,
                embed_url TEXT,
                embed_provider TEXT,
                category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
                created_at TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS item_images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER NOT NULL REFERENCES items(id) ON DELETE CASCADE,
                path TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS item_models (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER NOT NULL REFERENCES items(id) ON DELETE CASCADE,
                path TEXT NOT NULL,
                format TEXT
            )
            """
        )
        # Migrate tables created by an older version of this app, so
        # upgrading in place doesn't crash on missing columns.
        _ensure_column(conn, "items", "embed_url", "TEXT")
        _ensure_column(conn, "items", "embed_provider", "TEXT")
        _ensure_column(conn, "items", "category_id", "INTEGER")


# ---------- Categories ----------

def add_category(name: str) -> int:
    name = name.strip()
    with get_conn() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO categories (name) VALUES (?)", (name,)
        )
        row = conn.execute(
            "SELECT id FROM categories WHERE name = ?", (name,)
        ).fetchone()
        return row["id"]


def get_categories():
    with get_conn() as conn:
        rows = conn.execute("SELECT id, name FROM categories ORDER BY name").fetchall()
        return [dict(r) for r in rows]


def delete_category(category_id: int):
    """Deletes the category only. Items keep existing (their
    category_id is set to NULL, they just become uncategorized)."""
    with get_conn() as conn:
        conn.execute("DELETE FROM categories WHERE id = ?", (category_id,))


# ---------- Items ----------

def add_item(title, description, price, embed_url, embed_provider,
             image_paths, model_entries, category_id=None):
    """model_entries: list of (path, format) tuples."""
    with get_conn() as conn:
        cur = conn.execute(
            """
            INSERT INTO items (title, description, price, embed_url,
                                embed_provider, category_id, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                title,
                description,
                price,
                embed_url or None,
                embed_provider or None,
                category_id,
                datetime.now(timezone.utc).isoformat(),
            ),
        )
        item_id = cur.lastrowid
        for path in image_paths:
            conn.execute(
                "INSERT INTO item_images (item_id, path) VALUES (?, ?)",
                (item_id, path),
            )
        for path, fmt in model_entries:
            conn.execute(
                "INSERT INTO item_models (item_id, path, format) VALUES (?, ?, ?)",
                (item_id, path, fmt),
            )
        return item_id


def _attach_related(conn, item):
    images = conn.execute(
        "SELECT path FROM item_images WHERE item_id = ?", (item["id"],)
    ).fetchall()
    models = conn.execute(
        "SELECT path, format FROM item_models WHERE item_id = ?", (item["id"],)
    ).fetchall()

    item = dict(item)
    item.setdefault("embed_url", None)
    item.setdefault("embed_provider", None)
    item.setdefault("category_id", None)
    item["image_paths"] = [r["path"] for r in images]
    item["models"] = [{"path": r["path"], "format": r["format"]} for r in models]

    item["category_name"] = None
    if item["category_id"] is not None:
        cat = conn.execute(
            "SELECT name FROM categories WHERE id = ?", (item["category_id"],)
        ).fetchone()
        item["category_name"] = cat["name"] if cat else None

    return item


def get_all_items(category_id=None):
    """category_id=None returns everything. Pass an id to filter."""
    with get_conn() as conn:
        if category_id is None:
            rows = conn.execute(
                "SELECT * FROM items ORDER BY created_at DESC"
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM items WHERE category_id = ? ORDER BY created_at DESC",
                (category_id,),
            ).fetchall()
        return [_attach_related(conn, row) for row in rows]


def get_item(item_id):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM items WHERE id = ?", (item_id,)
        ).fetchone()
        return _attach_related(conn, row) if row else None


def delete_item(item_id):
    """Returns the deleted item (with its file paths) so the caller
    can also remove the underlying files from storage."""
    item = get_item(item_id)
    if item:
        with get_conn() as conn:
            conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
    return item
