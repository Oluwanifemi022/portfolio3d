"""
Minimal password gate for the admin page.

Reads the password from Streamlit secrets (.streamlit/secrets.toml,
key: admin_password). Never hardcode the password in code.
"""

import streamlit as st


def require_admin():
    """Call at the top of the admin page. Halts the page until the
    correct password is entered."""

    if st.session_state.get("is_admin"):
        return

    st.title("Admin Login")
    password = st.text_input("Password", type="password")

    if st.button("Log in"):
        real_password = st.secrets.get("admin_password")
        if real_password is None:
            st.error(
                "No admin_password set in .streamlit/secrets.toml. "
                "Add one before using this page."
            )
            st.stop()
        if password == real_password:
            st.session_state["is_admin"] = True
            st.rerun()
        else:
            st.error("Incorrect password.")

    st.stop()
