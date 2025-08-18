"""Streamlit entry point with multi-page navigation."""
from __future__ import annotations

import streamlit as st

from .pages import dashboard, ai_search, site_map

PAGES = {
    "AI Policy Dashboard": dashboard,
    "AI Search": ai_search,
    "Site Map": site_map,
}


def main() -> None:
    """Render the selected page with a sidebar for navigation."""
    st.set_page_config(page_title="AI Usage & Data Policy App")
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    page = PAGES[selection]
    page.render()


if __name__ == "__main__":  # pragma: no cover - manual execution
    main()
