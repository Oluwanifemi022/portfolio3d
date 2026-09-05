"""
Shared visual theme. On every page:

    from utils.theme import theme_toggle, inject_theme
    dark = theme_toggle()
    inject_theme(dark)

theme_toggle() renders a small switch in the sidebar and returns the
current state (persisted in session_state, so it stays consistent as
you move between pages).
"""

import streamlit as st

LIGHT = {
    "bg": "#EEEFEC",
    "surface": "#FFFFFF",
    "border": "#DEDDD8",
    "text": "#1B1B18",
    "text-muted": "#6B6A64",
    "accent": "#2F5D50",
    "accent-hover": "#24473D",
    "price": "#B8863B",
}

DARK = {
    "bg": "#17181B",
    "surface": "#1F2124",
    "border": "#2C2F33",
    "text": "#ECEAE5",
    "text-muted": "#9A9FA6",
    "accent": "#6FA88F",
    "accent-hover": "#89C0A8",
    "price": "#E0B15C",
}


def _hex_to_rgba(hex_color: str, alpha: float) -> str:
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {alpha})"


def theme_toggle() -> bool:
    if "dark_mode" not in st.session_state:
        st.session_state["dark_mode"] = False
    st.sidebar.toggle("Dark mode", key="dark_mode")
    return st.session_state["dark_mode"]


def inject_theme(dark: bool = False, translucent: bool = False):
    c = DARK if dark else LIGHT
    bg_color = _hex_to_rgba(c["bg"], 0.86) if translucent else c["bg"]
    surface_color = _hex_to_rgba(c["surface"], 0.9) if translucent else c["surface"]

    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=IBM+Plex+Sans:wght@400;500;600&display=swap');

    :root {{
        --bg: {c['bg']};
        --surface: {c['surface']};
        --border: {c['border']};
        --text: {c['text']};
        --text-muted: {c['text-muted']};
        --accent: {c['accent']};
        --accent-hover: {c['accent-hover']};
        --price: {c['price']};
    }}

    .stApp {{
        background-color: {bg_color};
    }}

    html, body, [class*="css"] {{
        font-family: 'IBM Plex Sans', sans-serif;
        color: var(--text);
    }}

    h1, h2, h3 {{
        font-family: 'Fraunces', serif;
        font-weight: 500;
        letter-spacing: -0.01em;
        color: var(--text);
    }}

    h1 {{ font-size: 2.6rem; }}
    h2 {{ font-size: 1.7rem; }}

    p, li, .stMarkdown, label {{
        color: var(--text);
    }}

    [data-testid="stSidebar"] {{
        background-color: {surface_color};
        border-right: 1px solid var(--border);
    }}

    .stButton > button {{
        background-color: var(--accent);
        color: #FFFFFF;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1.3rem;
        font-family: 'IBM Plex Sans', sans-serif;
        font-weight: 500;
        transition: background-color 0.15s ease;
    }}

    .stButton > button:hover {{
        background-color: var(--accent-hover);
        color: #FFFFFF;
    }}

    [data-testid="stVerticalBlockBorderWrapper"] {{
        border-color: var(--border) !important;
        border-radius: 6px;
    }}

    .price-tag {{
        color: var(--price);
        font-weight: 600;
        font-size: 1.05rem;
    }}

    .muted {{
        color: var(--text-muted);
        font-size: 0.92rem;
    }}

    hr {{
        border-color: var(--border);
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
