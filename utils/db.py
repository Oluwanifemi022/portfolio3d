"""
Database layer for portfolio items.

Uses SQLite for local development. Kept intentionally small and
isolated behind these functions so it can be swapped for a hosted
Postgres (e.g. Supabase) later without touching the rest of the app -
only this file changes.
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
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                price REAL,
                image_path TEXT,
                model_path TEXT,
                model_format TEXT,
                created_at TEXT
            )
            """
        )


def add_item(title, description, price, image_path, model_path, model_format):
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO items (title, description, price, image_path,
                                model_path, model_format, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                title,
                description,
                price,
                image_path,
                model_path,
                model_format,
                datetime.now(timezone.utc).isoformat(),
            ),
        )


def get_all_items():
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM items ORDER BY created_at DESC"
        ).fetchall()
        return [dict(row) for row in rows]


def get_item(item_id):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM items WHERE id = ?", (item_id,)
        ).fetchone()
        return dict(row) if row else None


def delete_item(item_id):
    item = get_item(item_id)
    with get_conn() as conn:
        conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
    return item  # caller can use this to also delete the associated files
