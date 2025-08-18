import json
from pathlib import Path
from unittest.mock import MagicMock

import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.crawler.spider import Spider
from src.crawler.state_manager import StateManager


def test_extract_links(tmp_path):
    html = (
        "<a href='/a'>A</a>"  # relative link
        "<a href='https://example.com/b'>B</a>"  # absolute link
        "<a href='/a'>Duplicate</a>"  # duplicate should be ignored
        "<a href='mailto:test@example.com'>Mail</a>"  # non-http should be ignored
        "<a href='#section'>Anchor</a>"  # anchor should be ignored
    )
    state = StateManager(
        state_file=str(tmp_path / "state.json"),
        site_map_file=str(tmp_path / "site_map.json"),
    )
    spider = Spider(state, output_file=str(tmp_path / "out.jsonl"))
    links = spider.extract_links(html, "https://example.com")
    assert links == ["https://example.com/a", "https://example.com/b"]


def test_incremental_and_site_map(tmp_path):
    state = StateManager(
        state_file=str(tmp_path / "state.json"),
        site_map_file=str(tmp_path / "site_map.json"),
    )
    out_file = tmp_path / "out.jsonl"
    spider = Spider(state, output_file=str(out_file))

    page = MagicMock()
    page.goto.return_value = None
    page.content.return_value = "<a href='/b'>B</a>"

    spider._crawl_page(page, "https://example.com", depth=0)
    # second run with same content should not duplicate
    spider._crawl_page(page, "https://example.com", depth=0)

    assert state.is_visited("https://example.com")
    data = [json.loads(line) for line in out_file.read_text().splitlines()]
    assert len(data) == 1
    site_map = json.loads((tmp_path / "site_map.json").read_text())
    assert "https://example.com/b" in site_map
