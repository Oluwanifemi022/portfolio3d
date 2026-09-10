"""
Renders one portfolio item as a uniform card: fixed-height cropped
thumbnail on top, title, meta line, optional short description. Used
on both Home (featured work) and Portfolio (full grid) so the two
pages look like one consistent design rather than two different ones.

Thumbnails are forced to the same height via CSS object-fit: cover,
regardless of the original image's aspect ratio - this is what keeps
every card the same size in the grid, the way Sketchfab/Behance-style
grids do. Streamlit's own st.image can't crop like this, so the
thumbnail is rendered as raw HTML instead.
"""

import streamlit as st
from utils.storage import get_display_url


def render_card_thumbnail(item, height: int = 190):
    if not item["image_paths"]:
        st.markdown(
            f'<div class="thumb thumb-empty" style="height:{height}px;"></div>',
            unsafe_allow_html=True,
        )
        return

    url = get_display_url(item["image_paths"][0])
    st.markdown(
        f'<div class="thumb" style="height:{height}px;">'
        f'<img src="{url}" alt="{item["title"]}" /></div>',
        unsafe_allow_html=True,
    )


def render_card_meta(item, max_description_chars: int = 90):
    st.markdown(f'<div class="card-title">{item["title"]}</div>', unsafe_allow_html=True)

    meta_bits = []
    if item.get("category_name"):
        meta_bits.append(item["category_name"])
    if item.get("price") is not None:
        meta_bits.append(f'${item["price"]:,.2f}')
    if meta_bits:
        st.markdown(
            f'<div class="card-meta">{" &middot; ".join(meta_bits)}</div>',
            unsafe_allow_html=True,
        )

    description = (item.get("description") or "").strip()
    if description:
        if len(description) > max_description_chars:
            description = description[:max_description_chars].rsplit(" ", 1)[0] + "…"
        st.markdown(f'<p class="card-desc">{description}</p>', unsafe_allow_html=True)
