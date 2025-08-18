"""AI Policy Dashboard page with URL-based filters."""
from __future__ import annotations

from pathlib import Path
from typing import List

import pandas as pd
import streamlit as st


def _load_data(file_path: str = "data/domain_summary.csv") -> pd.DataFrame:
    """Load aggregated domain data from CSV.

    Args:
        file_path: Path to the CSV file.

    Returns:
        DataFrame of aggregated data; empty if file missing.
    """
    path = Path(file_path)
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()


def render() -> None:
    """Render the AI Policy Dashboard page with URL-based filters."""
    st.title("AI Policy Dashboard")
    data = _load_data()
    if data.empty:
        st.info("No aggregated data available.")
        return

    params = st.experimental_get_query_params()
    domain_options: List[str] = sorted(data["domain"].unique())
    default_domains = params.get("domain", domain_options)
    selected_domains = st.multiselect(
        "Filter by domain", domain_options, default=default_domains
    )
    st.experimental_set_query_params(domain=selected_domains)

    filtered = data[data["domain"].isin(selected_domains)]
    st.dataframe(filtered)
