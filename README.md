# 3D Portfolio

A multi-page Streamlit site for showcasing 3D work: a Home page with a
featured interactive piece, a Portfolio gallery (multiple images and 3D
files per project, plus optional Spline/Sketchfab embeds), an About page,
and a password-protected Admin page for uploads.

## Run it locally

```bash
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# edit .streamlit/secrets.toml and set a real admin_password
streamlit run Home.py
```

Use the sidebar to navigate: **Home**, **Portfolio**, **About**, **Admin**.
Log into Admin and add your first piece — it appears on the Portfolio page
immediately.

## Structure

```
Home.py                 # landing page + featured embed
pages/1_Portfolio.py    # gallery - the main deliverable
pages/2_About.py        # placeholder copy, edit freely
pages/3_Admin.py        # password-gated upload form
utils/db.py             # SQLite: items, item_images, item_models
utils/storage.py        # local file storage (swap for cloud pre-deploy)
utils/theme.py          # shared fonts/colors/CSS
utils/embeds.py         # Spline/Sketchfab iframe rendering
utils/auth.py           # admin password gate
```

## Uploading multiple images/files

The admin form's file uploaders accept multiple files in one go — click
the uploader and select several, or drag a batch in. Each project can have
any number of images and any number of 3D files.

## Spline / Sketchfab embeds

Each project can optionally carry an embed URL instead of (or alongside)
an uploaded 3D file:

- **Spline**: open your scene → Export → Code Export → copy the *Public
  URL* (looks like `https://my.spline.design/xxxxxxxx/`).
- **Sketchfab**: open the model page → Share/Embed → copy the *embed* URL
  (looks like `https://sketchfab.com/models/xxxx/embed`).

Paste it into the admin form's embed field and pick the matching provider.

The Home page also has a featured embed slot — open `Home.py` and replace
`FEATURED_EMBED_URL` near the top with your own scene's public URL.

## Uploaded model file viewing

`.stl` files render immediately via `streamlit-stl`. For `.obj` / `.fbx` /
`.glb` / `.gltf` uploaded files (not embeds), wire in
`streamlit_extras.three_viewer` — in `pages/1_Portfolio.py`, replace the
`st.warning(...)` block with:

```python
from streamlit_extras.three_viewer import three_viewer
three_viewer(model["path"], height=380)
```

GLB is the best format for web viewing generally — smallest and fastest.

## Before deploying: switch to cloud storage

Streamlit Community Cloud's filesystem is **ephemeral** — local files
(your SQLite DB and uploaded files) are wiped on every redeploy/restart.
Before going live:

1. Create a free [Supabase](https://supabase.com) project (Postgres +
   file storage).
2. Rewrite the functions in `utils/db.py` to hit Postgres instead of
   `sqlite3` (same function signatures — nothing else needs to change).
3. Rewrite `save_image`/`save_model` in `utils/storage.py` to upload to a
   Supabase Storage bucket and return the bucket URL instead of a local
   path.
4. Add `supabase_url` / `supabase_key` to `secrets.toml`.

## Deploying

1. Push this repo to GitHub (`.streamlit/secrets.toml` is gitignored —
   never commit it).
2. Go to [share.streamlit.io](https://share.streamlit.io), connect GitHub,
   deploy this repo pointing at `Home.py` as the main file.
3. In the app's Settings → Secrets, paste your `secrets.toml` contents.
4. Every push to your GitHub repo auto-redeploys.

## A note on "view but not download"

Any 3D file rendered in-browser is technically retrievable via dev
tools/network tab — there's no way to make a file both interactively
viewable in WebGL and fully unextractable. What helps (without being
airtight): serving models via short-lived signed URLs instead of
permanent public links, disabling right-click/dev-tools shortcuts
(deters casual users only), or serving a decimated/low-poly preview
instead of your full-resolution source file.
