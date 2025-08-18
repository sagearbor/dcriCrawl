"""AI Search page with generative AI integration."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import google.generativeai as genai
import streamlit as st


def _load_crawled_text(file_path: str = "data/crawled_data.jsonl") -> str:
    """Load crawled page text from a JSONL file.

    Args:
        file_path: Path to the crawled data file.

    Returns:
        Concatenated page contents or an empty string if the file is missing.
    """
    path = Path(file_path)
    if not path.exists():
        return ""
    texts: list[str] = []
    for line in path.read_text().splitlines():
        try:
            record: dict[str, Any] = json.loads(line)
            texts.append(record.get("content", ""))
        except json.JSONDecodeError:
            continue
    return "\n".join(texts)


def generate_response(query: str, data_file: str = "data/crawled_data.jsonl") -> str:
    """Generate an AI response for a query using crawled data as context.

    Args:
        query: User's search question.
        data_file: Path to crawled data for context.

    Returns:
        The generated response text.
    """
    context = _load_crawled_text(data_file)
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(f"{context}\n\nQuestion: {query}")
    return getattr(response, "text", "")


def render() -> None:
    """Render the AI Search page."""
    st.title("AI Search")
    query = st.text_input("Enter your question")
    if query:
        with st.spinner("Generating response..."):
            answer = generate_response(query)
        st.write(answer)
