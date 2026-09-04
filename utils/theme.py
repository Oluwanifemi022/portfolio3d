"""
Shared visual theme. Call inject_theme() at the top of every page,
right after st.set_page_config().

Palette (gallery / studio concept - neutral backdrop so the 3D pieces
carry the color, not the chrome around them):
  background   #EEEFEC  soft cool stone
  surface      #FFFFFF
  border       #DEDDD8  hairline
  text         #1B1B18
  text-muted   #6B6A64
  accent       #2F5D50  deep pine (interactive elements only)
  accent-hover #24473D
  price        #B8863B  muted ochre, used only for price tags
"""

import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=IBM+Plex+Sans:wght@400;500;600&display=swap');

:root {
    --bg: #EEEFEC;
    --surface: #FFFFFF;
    --border: #DEDDD8;
    --text: #1B1B18;
    --text-muted: #6B6A64;
    --accent: #2F5D50;
    --accent-hover: #24473D;
    --price: #B8863B;
}

.stApp {
    background-color: var(--bg);
}

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    color: var(--text);
}

h1, h2, h3 {
    font-family: 'Fraunces', serif;
    font-weight: 500;
    letter-spacing: -0.01em;
    color: var(--text);
}

h1 { font-size: 2.6rem; }
h2 { font-size: 1.7rem; }

p, li, .stMarkdown {
    color: var(--text);
}

[data-testid="stSidebar"] {
    background-color: var(--surface);
    border-right: 1px solid var(--border);
}

.stButton > button {
    background-color: var(--accent);
    color: #FFFFFF;
    border: none;
    border-radius: 4px;
    padding: 0.5rem 1.3rem;
    font-family: 'IBM Plex Sans', sans-serif;
    font-weight: 500;
    transition: background-color 0.15s ease;
}

.stButton > button:hover {
    background-color: var(--accent-hover);
    color: #FFFFFF;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: var(--border) !important;
    border-radius: 6px;
}

.price-tag {
    color: var(--price);
    font-weight: 600;
    font-size: 1.05rem;
}

.muted {
    color: var(--text-muted);
    font-size: 0.92rem;
}

hr {
    border-color: var(--border);
}
</style>
"""


def inject_theme():
    st.markdown(CSS, unsafe_allow_html=True)
