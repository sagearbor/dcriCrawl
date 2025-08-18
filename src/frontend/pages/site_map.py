"""Display a tree view of crawled sites."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import streamlit as st


def _load_site_map(file_path: str = "data/site_map.json") -> dict[str, Any]:
    """Load the site map from JSON."""
    path = Path(file_path)
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def _render_tree(tree: dict[str, Any]) -> None:
    """Recursively render the site map as expanders."""
    for url, children in tree.items():
        if isinstance(children, dict) and children:
            with st.expander(url):
                _render_tree(children)
        else:
            st.write(url)


def render() -> None:
    """Render the Site Map page."""
    st.title("Site Map")
    site_map = _load_site_map()
    if not site_map:
        st.info("No site map available.")
        return
    _render_tree(site_map)
