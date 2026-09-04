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
