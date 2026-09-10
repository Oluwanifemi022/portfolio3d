"""
Renders an interactive Spline or Sketchfab embed from a URL.

Spline: use the "Public URL" from Spline's Export > Embed dialog,
        looks like https://my.spline.design/xxxxxxxx/
Sketchfab: use the "Embed" URL from a model's Share/Embed dialog,
        looks like https://sketchfab.com/models/xxxx/embed
"""

import streamlit.components.v1 as components


def render_embed(url: str, provider: str, height: int = 450):
    provider = (provider or "").lower()

    if provider == "sketchfab":
        html = f"""
        <iframe title="3D model" width="100%" height="{height}"
            src="{url}" frameborder="0"
            allow="autoplay; fullscreen; xr-spatial-tracking"
            allowfullscreen
            style="border-radius: 6px;">
        </iframe>
        """
    else:  # default to spline
        html = f"""
        <iframe src="{url}" width="100%" height="{height}"
            frameborder="0" style="border-radius: 6px;">
        </iframe>
        """

    components.html(html, height=height)


def render_background_embed(url: str, provider: str = "spline", interactive: bool = False):
    """
    Pins the embed as a fixed, full-viewport layer behind the rest of
    the page - used for a hero/body background rather than a boxed
    viewer.

    This is a workaround, not an official Streamlit feature: Streamlit
    components normally render inside their own boxed iframe, so to
    make one act as a page background this reaches into the parent
    document via JavaScript and inserts a positioned iframe there
    instead. It relies on Streamlit's current DOM structure, so if a
    future Streamlit version changes that structure this may need a
    small update. Pair it with utils.theme.inject_theme(dark,
    translucent=True) so the app's own background is see-through
    enough for this to show through.

    interactive=False (default) lets clicks/scroll pass through to the
    page underneath, which is usually what you want for a background.
    Set True if you want visitors to be able to drag/rotate it.
    """
    pointer_events = "auto" if interactive else "none"

    html = f"""
    <script>
    (function() {{
        const doc = window.parent.document;
        let bg = doc.getElementById('app-bg-embed');
        if (!bg) {{
            bg = doc.createElement('iframe');
            bg.id = 'app-bg-embed';
            doc.body.appendChild(bg);
        }}
        bg.src = "{url}";
        bg.style.position = 'fixed';
        bg.style.top = '0';
        bg.style.left = '0';
        bg.style.width = '100vw';
        bg.style.height = '100vh';
        bg.style.border = '0';
        bg.style.zIndex = '-1';
        bg.style.pointerEvents = '{pointer_events}';
        bg.frameBorder = '0';
    }})();
    </script>
    """
    components.html(html, height=0)


def remove_background_embed():
    """Call on pages that should NOT show the pinned background (e.g.
    if you only want it on Home) - removes it if present."""
    html = """
    <script>
    (function() {
        const doc = window.parent.document;
        const bg = doc.getElementById('app-bg-embed');
        if (bg) bg.remove();
    })();
    </script>
    """
    components.html(html, height=0)
