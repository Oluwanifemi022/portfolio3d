# 3D Portfolio

A Streamlit app for showcasing a portfolio of 3D pieces: image, description,
price, and an interactive (view-only) 3D model per item, with a
password-protected admin page for uploads.

## Run it locally

```bash
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# edit .streamlit/secrets.toml and set a real admin_password
streamlit run app.py
```

Open the app, use the sidebar to go to **Admin**, log in, and add your first
piece. It'll immediately show up on the main gallery page.

## Current state (Stage 1: local dev)

- Metadata (title, description, price, file paths) is stored in a local
  SQLite file at `data/portfolio.db`.
- Uploaded images and 3D files are saved to `data/uploads/`.
- 3D viewing: `.stl` files render via `streamlit-stl`. For `.obj` / `.fbx` /
  `.glb` / `.gltf`, wire in `streamlit_extras.three_viewer` — swap the
  `st.warning(...)` block in `app.py` for:

  ```python
  from streamlit_extras.three_viewer import three_viewer
  three_viewer(item["model_path"], height=400)
  ```

  GLB is the recommended format for web viewing (smallest, fastest to load).
  If you're exporting from Spline, GLB/GLTF is the native export target.

## Before deploying: switch to cloud storage

Streamlit Community Cloud's filesystem is **ephemeral** — anything written
to local disk (your SQLite file and uploaded files) is wiped on every
redeploy or restart. Before going live:

1. Create a free [Supabase](https://supabase.com) project (Postgres +
   file storage in one).
2. Replace the body of the functions in `utils/db.py` with calls to
   Supabase's Postgres (or any Postgres) instead of `sqlite3`.
3. Replace the body of `save_image` / `save_model` in `utils/storage.py`
   with uploads to a Supabase Storage bucket, returning the bucket URL
   instead of a local path.
4. Add `supabase_url` and `supabase_key` to `secrets.toml`.

Nothing else in the app needs to change — `app.py` and the admin page only
call the functions in `utils/`, not the storage/DB implementation directly.

## Deploying

1. Push this repo to GitHub (`.streamlit/secrets.toml` is gitignored — never
   commit it).
2. Go to [share.streamlit.io](https://share.streamlit.io), connect your
   GitHub account, and deploy this repo, pointing at `app.py`.
3. In the app's settings on Streamlit Cloud, paste the contents of your
   `secrets.toml` into the **Secrets** section.
4. Every push to your GitHub repo auto-redeploys the app.

## A note on "view but not download"

Any 3D file rendered in-browser is technically retrievable via the
browser's dev tools/network tab — there's no way to make a file both
interactively viewable in WebGL and fully unextractable. What you *can* do:

- Serve models via short-lived signed URLs instead of permanent public
  links (Supabase Storage supports this).
- Disable right-click / dev-tools shortcuts (deters casual users, easily
  bypassed by anyone determined).
- Serve a decimated/low-poly preview version of the model instead of your
  full-resolution source file.

None of these are airtight. If true file protection is a hard requirement,
that needs a different architecture (server-side rendering to a video/image
stream) — worth a separate conversation if it matters to you.
